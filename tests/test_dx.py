import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gaia_cli.main import main
from gaia_cli.scanner import scan_repo, scan_repo_detailed


def run_cli(monkeypatch, argv):
    monkeypatch.setattr(sys, "argv", ["gaia", *argv])
    main()


def test_init_accepts_flags_and_uses_current_registry_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    run_cli(
        monkeypatch,
        [
            "init",
            "--user",
            "juno",
            "--scan",
            "AGENTS.md",
            "--scan",
            "scripts",
        ],
    )

    config = parse_config(tmp_path / ".gaia" / "config.toml")
    assert config["username"] == "juno"
    assert config["gaiaRegistryRef"] == "https://github.com/mbtiongson1/gaia-skill-tree"
    assert config["scanPaths"] == ["AGENTS.md", "scripts"]
    assert config["autoPromptCombinations"] is False


def test_init_yes_mode_preserves_non_interactive_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Prevent auto-detection from picking up the parent repo's username
    import gaia_cli.main as gaia_main
    monkeypatch.setattr(gaia_main, "_detect_github_username", lambda: None)

    run_cli(monkeypatch, ["init", "--yes"])

    config = parse_config(tmp_path / ".gaia" / "config.toml")
    assert config["username"] == "gaiabot"
    assert config["gaiaRegistryRef"] == "https://github.com/mbtiongson1/gaia-skill-tree"
    assert config["scanPaths"] == ["scripts", "packages/cli-npm"]


def test_scan_repo_skips_generated_and_vendor_directories(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gaia").mkdir()
    (tmp_path / ".gaia" / "config.json").write_text(
        '{"scanPaths": ["."], "gaiaUser": "juno"}'
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("web-search\n")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "noise.js").write_text("voice-agent\n")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "packed-refs").write_text("autonomous-debug\n")

    tokens = scan_repo()

    assert "web-search" in tokens
    assert "voice-agent" not in tokens
    assert "autonomous-debug" not in tokens


def test_scan_repo_detailed_reports_file_and_candidate_counts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gaia").mkdir()
    (tmp_path / ".gaia" / "config.json").write_text(
        '{"scanPaths": ["docs"], "gaiaUser": "juno"}'
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "one.md").write_text("web-search and code-generation")
    (tmp_path / "docs" / "image.png").write_bytes(b"not scanned")

    detailed = scan_repo_detailed()

    assert detailed["files_scanned"] == 1
    assert detailed["paths_found"] == ["docs"]
    assert "web-search" in detailed["tokens"]
    assert detailed["candidate_count"] >= 2


def test_flat_skill_verbs_are_removed(monkeypatch):
    with pytest.raises(SystemExit) as exc:
        run_cli(monkeypatch, ["install", "--help"])
    assert exc.value.code == 2


def test_version_flags_print_cli_version(monkeypatch, capsys):
    run_cli(monkeypatch, ["--version"])
    assert capsys.readouterr().out.strip() == "2.2.1"

    run_cli(monkeypatch, ["-v"])
    assert capsys.readouterr().out.strip() == "2.2.1"


def test_promote_label_override_is_not_available(monkeypatch):
    with pytest.raises(SystemExit) as exc:
        run_cli(monkeypatch, ["promote", "web-search", "--label", "III"])
    assert exc.value.code == 2


def parse_config(path):
    data = {}
    for line in path.read_text().splitlines():
        if "=" not in line:
            continue
        key, _, raw = line.partition("=")
        value = raw.strip()
        if value.startswith("["):
            data[key.strip()] = [item.strip().strip('"') for item in value[1:-1].split(",") if item.strip()]
        elif value in ("true", "false"):
            data[key.strip()] = value == "true"
        else:
            data[key.strip()] = value.strip('"')
    return data
