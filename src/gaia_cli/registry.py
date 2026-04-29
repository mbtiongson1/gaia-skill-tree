"""Registry path resolution for the Gaia CLI."""

import os
from importlib import resources
from pathlib import Path


WRITE_COMMANDS = {"push", "name", "fuse", "embed", "sync"}


def bundled_registry_path():
    """Return the bundled read-only registry data path."""
    return resources.files("gaia_cli").joinpath("data")


def resolve_registry_path(explicit_registry=None):
    """Resolve the registry path, honoring explicit paths before package data."""
    if explicit_registry:
        return os.path.abspath(os.path.expanduser(explicit_registry))
    return str(bundled_registry_path())


def registry_graph_path(registry_path):
    return os.path.join(str(registry_path), "graph", "gaia.json")


def require_explicit_writable_registry(parser, args):
    """Reject mutating commands unless --registry points at a writable checkout."""
    if args.command not in WRITE_COMMANDS:
        return
    if getattr(args, "registry_explicit", False):
        registry_path = Path(args.registry)
        if registry_path.is_dir() and os.access(registry_path, os.W_OK):
            return
        parser.error(
            f"{args.command} requires --registry PATH to point at a writable registry directory."
        )
    parser.error(
        f"{args.command} requires an explicit writable registry. "
        "Pass --registry PATH pointing at a local Gaia registry checkout."
    )
