"""Registry path resolution for the Gaia CLI."""

import json
import os
from importlib import resources
from pathlib import Path


WRITE_COMMANDS = {"push", "name", "fuse", "embed", "sync", "promote"}

_GLOBAL_CONFIG_PATH = Path.home() / ".gaia" / "config.json"


def bundled_registry_path():
    """Return the bundled read-only registry data path."""
    return resources.files("gaia_cli").joinpath("data")


def read_global_registry():
    """Return the globally-registered registry path, or None if not set."""
    try:
        with open(_GLOBAL_CONFIG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        path = data.get("defaultRegistry")
        if path and Path(path).is_dir():
            return path
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    return None


def write_global_registry(path: str) -> None:
    """Persist the registry path to the global ~/.gaia/config.json."""
    _GLOBAL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if _GLOBAL_CONFIG_PATH.exists():
        try:
            with open(_GLOBAL_CONFIG_PATH, encoding="utf-8") as f:
                existing = json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
    existing["defaultRegistry"] = str(Path(path).resolve())
    with open(_GLOBAL_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)


def resolve_registry_path(explicit_registry=None):
    """Resolve the registry path: explicit → global config → bundled data."""
    if explicit_registry:
        return os.path.abspath(os.path.expanduser(explicit_registry))
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
            f"`gaia {args.command}` needs a writable registry checkout. "
            "Run `gaia init` once from your gaia-skill-tree clone to register it globally, "
            "or pass --registry PATH explicitly."
        )
    parser.error(
        f"`gaia {args.command}` requires --registry PATH to point at a writable registry directory."
    )
