#!/usr/bin/env python3
"""Render registry/gaia.svg from the canonical Gaia skill graph."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gaia_cli.graph import write_graph_artifact  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Gaia skill graph artifacts")
    parser.add_argument("--registry", default=str(ROOT), help="Path to Gaia registry root")
    parser.add_argument("--format", choices=("svg", "json"), default="svg")
    parser.add_argument("-o", "--output", default=None, help="Output path (default: registry/gaia.svg)")
    args = parser.parse_args()
    path = write_graph_artifact(args.registry, output=args.output, fmt=args.format)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
