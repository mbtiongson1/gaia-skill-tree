"""Tests for src/gaia_cli/treeManager.py — path-traversal rejection and show_tree modes."""

import json
import os
import pytest

from gaia_cli.treeManager import load_tree, save_tree, show_tree


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_tree(tmp_path, username, data):
    user_dir = tmp_path / "skill-trees" / username
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
        expected = tmp_path / "skill-trees" / "alice" / "skill-tree.json"
        assert expected.exists()
        data = json.loads(expected.read_text())
        assert data["userId"] == "alice"

    def test_creates_parent_directories(self, tmp_path):
        save_tree("newuser", _SAMPLE_TREE, registry_path=str(tmp_path))
        assert (tmp_path / "skill-trees" / "newuser" / "skill-tree.json").exists()


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


# ---------------------------------------------------------------------------
# show_tree — display modes
# ---------------------------------------------------------------------------

_GRAPH_DATA = {
    "skills": [
<<<<<<< HEAD
        {"id": "web-search", "name": "Web Search", "type": "basic", "level": "1⭐", "prerequisites": []},
        {"id": "summarize",  "name": "Summarize",  "type": "basic", "level": "0⭐", "prerequisites": []},
        {"id": "research",   "name": "Research",   "type": "extra", "level": "3⭐", "prerequisites": ["web-search", "summarize"]},
=======
<<<<<<< Updated upstream
        {"id": "web-search", "name": "Web Search", "type": "basic", "level": "I", "prerequisites": []},
        {"id": "summarize",  "name": "Summarize",  "type": "basic", "level": "0", "prerequisites": []},
        {"id": "research",   "name": "Research",   "type": "extra", "level": "III", "prerequisites": ["web-search", "summarize"]},
=======
        {"id": "web-search", "name": "Web Search", "type": "basic", "level": "1★", "prerequisites": []},
        {"id": "summarize",  "name": "Summarize",  "type": "basic", "level": "0★", "prerequisites": []},
        {"id": "research",   "name": "Research",   "type": "extra", "level": "3★", "prerequisites": ["web-search", "summarize"]},
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
    ]
}

_TREE_DATA = {
    "userId": "testuser",
    "updatedAt": "2026-01-01",
    "unlockedSkills": [
<<<<<<< HEAD
        {"skillId": "web-search", "level": "1⭐"},
        {"skillId": "summarize",  "level": "0⭐"},
        {"skillId": "research",   "level": "3⭐"},
=======
<<<<<<< Updated upstream
        {"skillId": "web-search", "level": "I"},
        {"skillId": "summarize",  "level": "0"},
        {"skillId": "research",   "level": "III"},
=======
        {"skillId": "web-search", "level": "1★"},
        {"skillId": "summarize",  "level": "0★"},
        {"skillId": "research",   "level": "3★"},
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
    ],
    "pendingCombinations": [],
    "stats": {},
}


def _make_named_index(tmp_path, buckets):
    named_dir = tmp_path / "registry"
    named_dir.mkdir(parents=True, exist_ok=True)
    (named_dir / "named-skills.json").write_text(json.dumps({"generatedAt": "2026-01-01", "buckets": buckets, "awaitingClassification": [], "byContributor": {}}))


class TestShowTreeModes:
    def test_default_shows_slash_slugs(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        show_tree(_TREE_DATA, graph_data=_GRAPH_DATA, registry_path=str(tmp_path), mode="default")
        out = capsys.readouterr().out
        assert "/research" in out
        assert "/web-search" in out
        assert "Research" not in out  # display name should not appear in default mode

    def test_title_shows_display_names(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        show_tree(_TREE_DATA, graph_data=_GRAPH_DATA, registry_path=str(tmp_path), mode="title")
        out = capsys.readouterr().out
        assert "Research" in out
        assert "Web Search" in out
        assert "/research" not in out

    def test_default_shows_named_contributor_id(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        _make_named_index(tmp_path, {
            "research": [{"id": "alice/deep-research", "name": "Deep Research", "contributor": "alice",
                          "origin": True, "genericSkillRef": "research", "status": "named",
<<<<<<< HEAD
                          "level": "3⭐", "description": ""}]
=======
<<<<<<< Updated upstream
                          "level": "III", "description": ""}]
=======
                          "level": "3★", "description": ""}]
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
        })
        show_tree(_TREE_DATA, graph_data=_GRAPH_DATA, registry_path=str(tmp_path), mode="default")
        out = capsys.readouterr().out
        assert "alice/deep-research" in out
        # Generic skills without a named impl still show slash form
        assert "/web-search" in out

    def test_named_mode_filters_to_named_only(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        _make_named_index(tmp_path, {
            "research": [{"id": "alice/deep-research", "name": "Deep Research", "contributor": "alice",
                          "origin": True, "genericSkillRef": "research", "status": "named",
<<<<<<< HEAD
                          "level": "3⭐", "description": ""}]
=======
<<<<<<< Updated upstream
                          "level": "III", "description": ""}]
=======
                          "level": "3★", "description": ""}]
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
        })
        show_tree(_TREE_DATA, graph_data=_GRAPH_DATA, registry_path=str(tmp_path), mode="named")
        out = capsys.readouterr().out
        assert "alice/deep-research" in out
        # Unnamed skills should not appear
        assert "/web-search" not in out
        assert "/summarize" not in out

    def test_named_mode_empty_when_no_named_skills(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        show_tree(_TREE_DATA, graph_data=_GRAPH_DATA, registry_path=str(tmp_path), mode="named")
        out = capsys.readouterr().out
        # Only username header, no skill lines
        assert "testuser" in out
        assert "├" not in out and "└" not in out

    def test_tree_connectors_present(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        show_tree(_TREE_DATA, graph_data=_GRAPH_DATA, registry_path=str(tmp_path), mode="title")
        out = capsys.readouterr().out
        assert "├" in out or "└" in out
