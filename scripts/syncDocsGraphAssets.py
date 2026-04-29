#!/usr/bin/env python3
"""Copy generated graph artifacts into docs/ for GitHub Pages.

GitHub Pages commonly serves the docs/ directory as the site root. Keep the
canonical graph files in graph/, then mirror only the public artifacts that the
static page needs to fetch or download.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sync_docs_graph_assets(root: Path = ROOT) -> None:
    docs_graph = root / "docs" / "graph"
    docs_graph.mkdir(parents=True, exist_ok=True)

    required = ("graph/gaia.json", "graph/gaia.gexf", "graph/gaia.svg")
    missing = [rel for rel in required if not (root / rel).exists()]
    if missing:
        raise FileNotFoundError(
            "Missing generated graph artifact(s): " + ", ".join(missing) +
            ". Run scripts/exportGexf.py and scripts/renderGraphSvg.py first."
        )

    for rel in required:
        src = root / rel
        dst = docs_graph / src.name
        shutil.copyfile(src, dst)
        print(f"Synced {src.relative_to(root)} -> {dst.relative_to(root)}")

    tree_src = root / "tree.md"
    if not tree_src.exists():
        raise FileNotFoundError("Missing tree.md. Run scripts/generateProjections.py first.")
    tree_dst = root / "docs" / "tree.md"
    shutil.copyfile(tree_src, tree_dst)
    print(f"Synced tree.md -> {tree_dst.relative_to(root)}")


def main() -> None:
    sync_docs_graph_assets()


if __name__ == "__main__":
    main()
