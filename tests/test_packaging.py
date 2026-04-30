import json
import os
import shutil
import subprocess
import sys
import tomllib
import venv
import zipfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_python(args, *, cwd=None, env=None):
    merged_env = os.environ.copy()
    merged_env["PYTHONPATH"] = os.pathsep.join([str(REPO_ROOT / "src"), str(REPO_ROOT)])
    merged_env["PYTHONIOENCODING"] = "utf-8"
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or REPO_ROOT,
        env=merged_env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def build_wheel(dist_dir):
    shutil.rmtree(REPO_ROOT / "build", ignore_errors=True)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(dist_dir),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_gaia_cli_package_imports():
    import gaia_cli

    assert gaia_cli.__name__ == "gaia_cli"


def test_python_module_help_runs_with_gaia_prog_name():
    result = run_python(["-m", "gaia_cli", "--help"])

    assert result.returncode == 0, result.stderr
    assert "usage: gaia" in result.stdout


def test_console_script_points_to_canonical_package():
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())

    assert data["project"]["scripts"]["gaia"] == "gaia_cli.main:main"


def test_plugin_cli_main_remains_importable():
    import plugin.cli.main as compat_main

    assert callable(compat_main.main)


def test_bundled_registry_is_used_for_read_only_doctor_without_registry(tmp_path):
    result = run_python(
        ["-m", "gaia_cli", "doctor"],
        cwd=tmp_path,
        env={"GAIA_HOME": str(tmp_path / "home")},
    )

    assert result.returncode == 0, result.stderr
    assert "Gaia CLI: OK" in result.stdout
    assert "Registry graph: found" in result.stdout


def test_scan_can_use_explicit_writable_registry(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / ".gaia").mkdir()
    (project / ".gaia" / "config.json").write_text(
        json.dumps({"gaiaUser": "juno", "scanPaths": ["."]})
    )
    (project / "notes.md").write_text("web-search\n")

    result = run_python(
        ["-m", "gaia_cli", "--registry", str(REPO_ROOT), "scan"],
        cwd=project,
        env={"GAIA_HOME": str(tmp_path / "home")},
    )

    assert result.returncode == 0, result.stderr
    assert "Matched 1 canonical skill(s)." in result.stdout


def test_write_commands_require_explicit_registry(tmp_path):
    (tmp_path / ".gaia").mkdir()
    (tmp_path / ".gaia" / "config.json").write_text(
        json.dumps({"gaiaUser": "juno", "scanPaths": ["."]})
    )
    (tmp_path / "notes.md").write_text("web-search\n")

    result = run_python(
        ["-m", "gaia_cli", "push", "--dry-run"],
        cwd=tmp_path,
        env={"GAIA_HOME": str(tmp_path / "home")},
    )

    assert result.returncode == 2
    assert "writable registry" in result.stderr
    assert "--registry PATH" in result.stderr


def test_install_cache_honors_gaia_home(tmp_path, monkeypatch):
    from gaia_cli.install import install_skill

    repo = tmp_path / "repo"
    repo.mkdir()
    registry = tmp_path / "registry"
    skill_dir = registry / "graph" / "named" / "alice"
    skill_dir.mkdir(parents=True)
    (skill_dir / "skill.md").write_text("content")
    gaia_home = tmp_path / "custom-home"

    monkeypatch.chdir(repo)
    monkeypatch.setenv("GAIA_HOME", str(gaia_home))

    assert install_skill("alice/skill", str(registry)) is True
    assert (gaia_home / "skills" / "alice" / "skill.md").exists()


@pytest.mark.packaging
def test_built_wheel_contains_only_python_package_data(tmp_path):
    dist_dir = tmp_path / "dist"
    result = build_wheel(dist_dir)
    assert result.returncode == 0, result.stderr

    wheels = list(dist_dir.glob("*.whl"))
    assert len(wheels) == 1
    with zipfile.ZipFile(wheels[0]) as wheel:
        names = set(wheel.namelist())

    assert "gaia_cli/data/graph/gaia.json" in names
    assert "gaia_cli/data/schema/skill.schema.json" in names
    assert any(name.startswith("gaia_cli/data/graph/named/") for name in names)
    forbidden_parts = (
        "node_modules/",
        "__pycache__/",
        ".pyc",
        "scratch/",
        "plugin/",
        "mcp-server/",
        "gaia_cli.egg-info/",
        "graph/gaia.gexf",
        "graph/render/",
        "skills/",
    )
    assert not any(part in name for name in names for part in forbidden_parts)


@pytest.mark.packaging
def test_wheel_install_smoke_tests_console_script(tmp_path):
    dist_dir = tmp_path / "dist"
    build_result = build_wheel(dist_dir)
    assert build_result.returncode == 0, build_result.stderr

    wheel = next(dist_dir.glob("*.whl"))
    venv_dir = tmp_path / "venv"
    venv.EnvBuilder(with_pip=True).create(venv_dir)
    python = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    gaia = venv_dir / ("Scripts/gaia.exe" if os.name == "nt" else "bin/gaia")
    install_result = subprocess.run(
        [str(python), "-m", "pip", "install", "--no-deps", str(wheel)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert install_result.returncode == 0, install_result.stderr

    help_result = subprocess.run(
        [str(gaia), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "GAIA_HOME": str(tmp_path / "home")},
    )
    assert help_result.returncode == 0, help_result.stderr
    assert "usage: gaia" in help_result.stdout
