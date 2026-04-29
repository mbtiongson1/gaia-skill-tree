import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from plugin.cli.main import main
from plugin.cli.scanner import scan_repo, scan_repo_detailed


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

    config = json.loads((tmp_path / ".gaia" / "config.json").read_text())
    assert config["gaiaUser"] == "juno"
    assert config["gaiaRegistryRef"] == "https://github.com/mbtiongson1/gaia-skill-tree"
    assert config["scanPaths"] == ["AGENTS.md", "scripts"]
    assert config["autoPromptCombinations"] is False


def test_init_yes_mode_preserves_non_interactive_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init", "--yes"])

    config = json.loads((tmp_path / ".gaia" / "config.json").read_text())
    assert config["gaiaUser"] == "gaiabot"
    assert config["gaiaRegistryRef"] == "https://github.com/mbtiongson1/gaia-skill-tree"
    assert config["scanPaths"] == ["scripts", "plugin"]


def test_scan_repo_skips_generated_and_vendor_directories(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gaia").mkdir()
    (tmp_path / ".gaia" / "config.json").write_text(
        json.dumps({"scanPaths": ["."], "gaiaUser": "juno"})
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
        json.dumps({"scanPaths": ["docs"], "gaiaUser": "juno"})
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "one.md").write_text("web-search and code-generation")
    (tmp_path / "docs" / "image.png").write_bytes(b"not scanned")

    detailed = scan_repo_detailed()

    assert detailed["files_scanned"] == 1
    assert detailed["paths_found"] == ["docs"]
    assert "web-search" in detailed["tokens"]
    assert detailed["candidate_count"] >= 2


def test_status_missing_tree_prints_next_steps(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gaia").mkdir()
    (tmp_path / ".gaia" / "config.json").write_text(
        json.dumps({"scanPaths": ["."], "gaiaUser": "juno"})
    )
    registry = tmp_path / "registry"
    registry.mkdir()

    run_cli(monkeypatch, ["--registry", str(registry), "status"])

    out = capsys.readouterr().out
    assert 'No skill tree found for user "juno".' in out
    assert "gaia scan" in out
    assert "gaia push --dry-run" in out


def test_doctor_reports_installation_state(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gaia").mkdir()
    (tmp_path / ".gaia" / "config.json").write_text(
        json.dumps({"scanPaths": ["AGENTS.md"], "gaiaUser": "juno"})
    )
    (tmp_path / "AGENTS.md").write_text("tool-use")
    registry = tmp_path / "registry"
    (registry / "graph").mkdir(parents=True)
    (registry / "graph" / "gaia.json").write_text(json.dumps({"skills": []}))

    run_cli(monkeypatch, ["--registry", str(registry), "doctor"])

    out = capsys.readouterr().out
    assert "Gaia CLI: OK" in out
    assert f"Registry path: {registry}" in out
    assert "Config: .gaia/config.json" in out
    assert "User: juno" in out
    assert "Skill tree: missing" in out
    assert "AGENTS.md exists" in out
