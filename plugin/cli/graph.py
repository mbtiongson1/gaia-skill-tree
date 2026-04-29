"""Graph rendering helpers for the Gaia CLI.

The registry source of truth is graph/gaia.json. This module deliberately uses
only the Python standard library so graph viewing remains available in a fresh
clone without Graphviz, Matplotlib, or a browser automation dependency.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import webbrowser
from html import escape
from pathlib import Path
from typing import Any

PALETTE = {
    "atomic": {"fill": "#38bdf8", "stroke": "#7dd3fc", "label": "Atomic"},
    "composite": {"fill": "#a78bfa", "stroke": "#c4b5fd", "label": "Composite"},
    "legendary": {"fill": "#fbbf24", "stroke": "#fde68a", "label": "Legendary"},
}
TYPE_ORDER = {"atomic": 0, "composite": 1, "legendary": 2}
RADIUS_BY_TYPE = {"atomic": 285, "composite": 170, "legendary": 54}
NODE_RADIUS = {"atomic": 6, "composite": 10, "legendary": 15}


def _registry_root(registry_path: str | os.PathLike[str]) -> Path:
    return Path(registry_path).expanduser().resolve()


def load_graph(registry_path: str | os.PathLike[str] = ".") -> dict[str, Any]:
    graph_path = _registry_root(registry_path) / "graph" / "gaia.json"
    with graph_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _stable_angle(skill_id: str, index: int, total: int) -> float:
    # Deterministic jitter prevents same-type nodes from forming a perfectly
    # uniform, sterile ring while keeping output stable across machines.
    seed = sum((i + 1) * ord(ch) for i, ch in enumerate(skill_id))
    jitter = ((seed % 997) / 997.0 - 0.5) * (math.tau / max(total, 1)) * 0.35
    return math.tau * index / max(total, 1) + jitter - math.pi / 2


def build_render_graph(graph: dict[str, Any], width: int = 1280, height: int = 880) -> dict[str, Any]:
    skills = graph.get("skills", [])
    groups: dict[str, list[dict[str, Any]]] = {"atomic": [], "composite": [], "legendary": []}
    for skill in skills:
        groups.setdefault(skill.get("type", "atomic"), []).append(skill)

    for bucket in groups.values():
        bucket.sort(key=lambda s: (str(s.get("level", "")), str(s.get("name", s.get("id", "")))))

    cx, cy = width / 2, height / 2
    nodes: list[dict[str, Any]] = []
    for skill_type in ("atomic", "composite", "legendary"):
        bucket = groups.get(skill_type, [])
        radius = RADIUS_BY_TYPE.get(skill_type, 220)
        for i, skill in enumerate(bucket):
            angle = _stable_angle(str(skill.get("id", "")), i, len(bucket))
            # Make legendary nodes visible as a small crown rather than one pile.
            local_radius = radius if len(bucket) > 1 else 0
            x = cx + math.cos(angle) * local_radius
            y = cy + math.sin(angle) * local_radius
            nodes.append(
                {
                    "id": skill.get("id"),
                    "label": skill.get("name") or skill.get("id"),
                    "type": skill_type,
                    "level": skill.get("level"),
                    "rarity": skill.get("rarity"),
                    "description": skill.get("description", ""),
                    "x": round(x, 3),
                    "y": round(y, 3),
                    "radius": NODE_RADIUS.get(skill_type, 7),
                }
            )

    skill_ids = {node["id"] for node in nodes}
    edges: list[dict[str, Any]] = []
    for skill in skills:
        target = skill.get("id")
        if target not in skill_ids:
            continue
        for source in skill.get("prerequisites", []) or []:
            if source in skill_ids:
                edges.append({"source": source, "target": target, "type": skill.get("type", "atomic")})

    nodes.sort(key=lambda n: (TYPE_ORDER.get(str(n.get("type")), 9), str(n.get("label", ""))))
    return {
        "version": graph.get("version"),
        "generatedAt": graph.get("generatedAt"),
        "width": width,
        "height": height,
        "nodes": nodes,
        "edges": edges,
    }


def render_svg(render_graph: dict[str, Any]) -> str:
    width = int(render_graph.get("width", 1280))
    height = int(render_graph.get("height", 880))
    nodes = render_graph.get("nodes", [])
    edges = render_graph.get("edges", [])
    node_by_id = {node["id"]: node for node in nodes}

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">Gaia AI Agent Skill Graph</title>",
        "<desc id=\"desc\">Canonical Gaia skill graph rendered from graph/gaia.json, with atomic skills on the outer ring, composite skills in the middle ring, and legendary skills at the core.</desc>",
        "<defs>",
        "<radialGradient id=\"bg\" cx=\"50%\" cy=\"45%\" r=\"70%\"><stop offset=\"0%\" stop-color=\"#172554\"/><stop offset=\"55%\" stop-color=\"#06111f\"/><stop offset=\"100%\" stop-color=\"#030712\"/></radialGradient>",
        "<filter id=\"glow\" x=\"-50%\" y=\"-50%\" width=\"200%\" height=\"200%\"><feGaussianBlur stdDeviation=\"4\" result=\"blur\"/><feMerge><feMergeNode in=\"blur\"/><feMergeNode in=\"SourceGraphic\"/></feMerge></filter>",
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="url(#bg)"/>',
        '<g opacity="0.32" stroke="#334155" stroke-width="1" fill="none">',
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="{RADIUS_BY_TYPE["atomic"]}"/>',
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="{RADIUS_BY_TYPE["composite"]}"/>',
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="{RADIUS_BY_TYPE["legendary"]}"/>',
        "</g>",
        '<g class="edges" fill="none">',
    ]

    for edge in edges:
        source = node_by_id.get(edge.get("source"))
        target = node_by_id.get(edge.get("target"))
        if not source or not target:
            continue
        color = PALETTE.get(str(edge.get("type")), PALETTE["atomic"])["fill"]
        lines.append(
            f'<line x1="{source["x"]}" y1="{source["y"]}" x2="{target["x"]}" y2="{target["y"]}" stroke="{color}" stroke-opacity="0.32" stroke-width="1.15"/>'
        )
    lines.append("</g>")

    lines.append('<g class="nodes" filter="url(#glow)">')
    for node in nodes:
        color = PALETTE.get(str(node.get("type")), PALETTE["atomic"])
        lines.append(
            f'<circle cx="{node["x"]}" cy="{node["y"]}" r="{node["radius"]}" fill="{color["fill"]}" stroke="{color["stroke"]}" stroke-width="1.6"><title>{escape(str(node.get("label", "")))}</title></circle>'
        )
    lines.append("</g>")

    lines.append('<g class="labels" font-family="Inter, ui-sans-serif, system-ui, sans-serif" text-anchor="middle">')
    for node in nodes:
        typ = str(node.get("type"))
        # Label all composites/legendaries plus a readable sample of atomics.
        if typ == "atomic" and int(sum(ord(c) for c in str(node.get("id", ""))) % 4) != 0:
            continue
        color = PALETTE.get(typ, PALETTE["atomic"])["fill"]
        size = 10 if typ == "atomic" else 12 if typ == "composite" else 16
        weight = 600 if typ != "legendary" else 800
        y = float(node["y"]) - float(node["radius"]) - 7
        lines.append(
            f'<text x="{node["x"]}" y="{y:.1f}" fill="{color}" font-size="{size}" font-weight="{weight}" opacity="0.92">{escape(str(node.get("label", "")))}</text>'
        )
    lines.append("</g>")

    legend_x = 44
    legend_y = height - 110
    lines.extend([
        f'<g font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="14" fill="#cbd5e1">',
        f'<text x="{legend_x}" y="{legend_y - 22}" font-size="20" font-weight="800" fill="#e2e8f0">Gaia Skill Graph</text>',
    ])
    for i, skill_type in enumerate(("atomic", "composite", "legendary")):
        y = legend_y + i * 28
        color = PALETTE[skill_type]
        count = sum(1 for node in nodes if node.get("type") == skill_type)
        lines.append(f'<circle cx="{legend_x + 8}" cy="{y - 5}" r="6" fill="{color["fill"]}"/>')
        lines.append(f'<text x="{legend_x + 24}" y="{y}">{color["label"]}: {count}</text>')
    lines.append("</g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def write_graph_artifact(
    registry_path: str | os.PathLike[str] = ".",
    output: str | os.PathLike[str] | None = None,
    fmt: str = "svg",
) -> Path:
    root = _registry_root(registry_path)
    graph = load_graph(root)
    render_graph = build_render_graph(graph)
    fmt = fmt.lower()
    if output is None:
        if fmt == "svg":
            output = root / "graph" / "gaia.svg"
        else:
            output = root / "graph" / "render" / "latest.json"
    out_path = Path(output)
    if not out_path.is_absolute():
        out_path = root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "svg":
        out_path.write_text(render_svg(render_graph), encoding="utf-8")
    elif fmt == "json":
        out_path.write_text(json.dumps(render_graph, indent=2) + "\n", encoding="utf-8")
    else:
        raise ValueError(f"Unsupported graph format: {fmt}")
    return out_path


def open_path(path: Path) -> None:
    uri = path.resolve().as_uri()
    try:
        opened = webbrowser.open(uri)
    except Exception:
        opened = False
    if opened:
        return
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    elif os.name == "nt":
        os.startfile(str(path))  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def graph_command(args: Any) -> None:
    fmt = getattr(args, "format", "svg") or "svg"
    output = getattr(args, "output", None)
    out_path = write_graph_artifact(getattr(args, "registry", "."), output=output, fmt=fmt)
    print(f"Wrote Gaia graph {fmt.upper()}: {out_path}")
    if getattr(args, "open", True):
        open_path(out_path)
