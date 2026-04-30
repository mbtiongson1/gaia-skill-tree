"""Tests for src/gaia_cli/treeManager.py — path-traversal rejection."""

import json
import pytest

from gaia_cli.treeManager import load_tree, save_tree


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_tree(tmp_path, username, data):
    user_dir = tmp_path / "users" / username
    user_dir.mkdir(parents=True, exist_ok=True)
    (user_dir / "skill-tree.json").write_text(json.dumps(data))


_SAMPLE_TREE = {
    "userId": "alice",
    "updatedAt": "2026-01-01",
    "unlockedSkills": [],
    "pendingCombinations": [],
    "stats": {"totalUnlocked": 0, "highestRarity": "common", "deepestLineage": 0},
}


# ---------------------------------------------------------------------------
# load_tree — valid username
# ---------------------------------------------------------------------------


class TestLoadTreeValid:
    def test_returns_tree_for_valid_username(self, tmp_path):
        _write_tree(tmp_path, "alice", _SAMPLE_TREE)
        result = load_tree("alice", registry_path=str(tmp_path))
        assert result is not None
        assert result["userId"] == "alice"

    def test_returns_none_when_file_missing(self, tmp_path):
        result = load_tree("alice", registry_path=str(tmp_path))
        assert result is None

    def test_accepts_username_with_dots_and_hyphens(self, tmp_path):
        _write_tree(tmp_path, "alice.bob-99", _SAMPLE_TREE)
        result = load_tree("alice.bob-99", registry_path=str(tmp_path))
        assert result is not None


# ---------------------------------------------------------------------------
# load_tree — invalid username
# ---------------------------------------------------------------------------


class TestLoadTreeInvalid:
    @pytest.mark.parametrize("bad", [
        "../evil",
        "../../etc/passwd",
        "",
        "/root",
        "foo/bar",
        "foo bar",
        "foo\x00bar",
        ".hidden",
    ])
    def test_raises_for_path_traversal(self, tmp_path, bad):
        with pytest.raises(ValueError, match="Invalid username"):
            load_tree(bad, registry_path=str(tmp_path))


# ---------------------------------------------------------------------------
# save_tree — valid username
# ---------------------------------------------------------------------------


class TestSaveTreeValid:
    def test_writes_tree_to_correct_path(self, tmp_path):
        save_tree("alice", _SAMPLE_TREE, registry_path=str(tmp_path))
        expected = tmp_path / "users" / "alice" / "skill-tree.json"
        assert expected.exists()
        data = json.loads(expected.read_text())
        assert data["userId"] == "alice"

    def test_creates_parent_directories(self, tmp_path):
        save_tree("newuser", _SAMPLE_TREE, registry_path=str(tmp_path))
        assert (tmp_path / "users" / "newuser" / "skill-tree.json").exists()


# ---------------------------------------------------------------------------
# save_tree — invalid username
# ---------------------------------------------------------------------------


class TestSaveTreeInvalid:
    @pytest.mark.parametrize("bad", [
        "../evil",
        "../../etc/passwd",
        "",
        "/root",
        "foo/bar",
    ])
    def test_raises_for_path_traversal(self, tmp_path, bad):
        with pytest.raises(ValueError, match="Invalid username"):
            save_tree(bad, _SAMPLE_TREE, registry_path=str(tmp_path))
