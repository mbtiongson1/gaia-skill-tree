"""Registry path resolution for the Gaia CLI."""

import json
import os
from importlib import resources
from pathlib import Path


WRITE_COMMANDS = {"push", "name", "fuse", "embed", "sync", "promote"}


def _gaia_home_dir() -> Path:
    """Return the gaia data home: $GAIA_HOME if set, else ~/.gaia."""
    gaia_home = os.environ.get("GAIA_HOME")
    if gaia_home:
        return Path(gaia_home)
    return Path.home() / ".gaia"


def _global_config_path() -> Path:
    """Return the global gaia config path, honouring GAIA_HOME if set."""
    return _gaia_home_dir() / "config.json"


def bundled_registry_path():
    """Return the bundled read-only registry data path."""
    return resources.files("gaia_cli").joinpath("data")


def read_global_registry():
    """Return the globally-registered registry path, or None if not set."""
    try:
        with open(_global_config_path(), encoding="utf-8") as f:
            data = json.load(f)
        path = data.get("defaultRegistry")
        if path and Path(path).is_dir():
            return path
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    return None


def read_local_registry() -> str | None:
    """Return registry path from .gaia/config.json in CWD, or None if not found."""
    local_cfg = Path(".gaia") / "config.json"
    if not local_cfg.exists():
        return None
    try:
        data = json.loads(local_cfg.read_text(encoding="utf-8"))
        registry_path = data.get("localRegistryPath") or os.path.abspath(".")
        p = Path(registry_path)
        if p.is_dir() and (p / "graph" / "gaia.json").exists():
            return str(p)
    except (OSError, json.JSONDecodeError):
        pass
    return None


def write_global_registry(path: str) -> None:
    """Persist the registry path to the global ~/.gaia/config.json."""
    cfg = _global_config_path()
    cfg.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if cfg.exists():
        try:
            with open(cfg, encoding="utf-8") as f:
                existing = json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
    existing["defaultRegistry"] = str(Path(path).resolve())
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)


def resolve_registry_path(explicit_registry=None, global_flag=False):
    """Resolve the registry path: explicit → --global → local .gaia → global config → bundled."""
    if explicit_registry:
        return os.path.abspath(os.path.expanduser(explicit_registry))
    if global_flag:
        global_reg = read_global_registry()
        return global_reg if global_reg else str(bundled_registry_path())
    local_reg = read_local_registry()
    if local_reg:
        return local_reg
    global_reg = read_global_registry()
    if global_reg:
        return global_reg
    return str(bundled_registry_path())


def registry_graph_path(registry_path):
    return os.path.join(str(registry_path), "graph", "gaia.json")


def require_explicit_writable_registry(parser, args):
    """Reject mutating commands unless the registry resolves to a writable checkout."""
    if args.command not in WRITE_COMMANDS:
        return
    registry_path = Path(args.registry)
    bundled = Path(str(bundled_registry_path()))
    if registry_path != bundled and registry_path.is_dir() and os.access(registry_path, os.W_OK):
        return
    if registry_path == bundled:
        parser.error(
            f"`gaia {args.command}` needs a writable registry. Either:\n"
            "  • Run `gaia init` from your gaia-skill-tree clone (sets localRegistryPath automatically), or\n"
            "  • Pass --registry PATH explicitly."
        )
    parser.error(
        f"`gaia {args.command}` requires --registry PATH to point at a writable registry directory."
    )
