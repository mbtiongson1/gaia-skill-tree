"""Graph rendering helpers for the Gaia CLI.

The registry source of truth is registry/gaia.json. This module deliberately uses
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

from gaia_cli.registry import named_skills_index_path, registry_graph_path

PALETTE = {
    "basic": {"fill": "#38bdf8", "stroke": "#7dd3fc", "label": "Basic"},
    "extra": {"fill": "#a78bfa", "stroke": "#c4b5fd", "label": "Extra"},
    "ultimate": {"fill": "#fbbf24", "stroke": "#fde68a", "label": "Ultimate"},
}
TYPE_ORDER = {"basic": 0, "extra": 1, "ultimate": 2}
RADIUS_BY_TYPE = {"basic": 285, "extra": 170, "ultimate": 54}
NODE_RADIUS = {"basic": 6, "extra": 10, "ultimate": 15}


def _registry_root(registry_path: str | os.PathLike[str]) -> Path:
    return Path(registry_path).expanduser().resolve()


def load_graph(registry_path: str | os.PathLike[str] = ".") -> dict[str, Any]:
    graph_path = Path(registry_graph_path(_registry_root(registry_path)))
    with graph_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_named_skills(registry_path: str | os.PathLike[str] = ".") -> dict[str, Any]:
    named_path = Path(named_skills_index_path(_registry_root(registry_path)))
    if not named_path.exists():
        return {"buckets": {}}
    with named_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _stable_angle(skill_id: str, index: int, total: int) -> float:
    # Deterministic jitter prevents same-type nodes from forming a perfectly
    # uniform ring while keeping output stable across machines.
    seed = sum((i + 1) * ord(ch) for i, ch in enumerate(skill_id))
    jitter = ((seed % 997) / 997.0 - 0.5) * (math.tau / max(total, 1)) * 0.35
    return math.tau * index / max(total, 1) + jitter - math.pi / 2


def build_render_graph(graph: dict[str, Any], width: int = 1280, height: int = 880) -> dict[str, Any]:
    skills = graph.get("skills", [])
    groups: dict[str, list[dict[str, Any]]] = {"basic": [], "extra": [], "ultimate": []}
    for skill in skills:
        groups.setdefault(skill.get("type", "basic"), []).append(skill)

    for bucket in groups.values():
        bucket.sort(key=lambda s: (str(s.get("level", "")), str(s.get("name", s.get("id", "")))))

    cx, cy = width / 2, height / 2
    nodes: list[dict[str, Any]] = []
    for skill_type in ("basic", "extra", "ultimate"):
        bucket = groups.get(skill_type, [])
        radius = RADIUS_BY_TYPE.get(skill_type, 220)
        for i, skill in enumerate(bucket):
            angle = _stable_angle(str(skill.get("id", "")), i, len(bucket))
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
                edges.append({"source": source, "target": target, "type": skill.get("type", "basic")})

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
        '<title id="title">Gaia AI Agent Skill Graph</title>',
        '<desc id="desc">Canonical Gaia skill graph rendered from registry/gaia.json, with basic skills on the outer ring, extra skills in the middle ring, and ultimate skills at the core.</desc>',
        "<defs>",
        '<radialGradient id="bg" cx="50%" cy="45%" r="70%"><stop offset="0%" stop-color="#172554"/><stop offset="55%" stop-color="#06111f"/><stop offset="100%" stop-color="#030712"/></radialGradient>',
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="url(#bg)"/>',
        '<g opacity="0.32" stroke="#334155" stroke-width="1" fill="none">',
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="{RADIUS_BY_TYPE["basic"]}"/>',
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="{RADIUS_BY_TYPE["extra"]}"/>',
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="{RADIUS_BY_TYPE["ultimate"]}"/>',
        "</g>",
        '<g class="edges" fill="none">',
    ]

    for edge in edges:
        source = node_by_id.get(edge.get("source"))
        target = node_by_id.get(edge.get("target"))
        if not source or not target:
            continue
        color = PALETTE.get(str(edge.get("type")), PALETTE["basic"])["fill"]
        lines.append(
            f'<line x1="{source["x"]}" y1="{source["y"]}" x2="{target["x"]}" y2="{target["y"]}" stroke="{color}" stroke-opacity="0.32" stroke-width="1.15"/>'
        )
    lines.append("</g>")

    lines.append('<g class="nodes" filter="url(#glow)">')
    for node in nodes:
        color = PALETTE.get(str(node.get("type")), PALETTE["basic"])
        lines.append(
            f'<circle cx="{node["x"]}" cy="{node["y"]}" r="{node["radius"]}" fill="{color["fill"]}" stroke="{color["stroke"]}" stroke-width="1.6"><title>{escape(str(node.get("label", "")))}</title></circle>'
        )
    lines.append("</g>")

    lines.append('<g class="labels" font-family="Inter, ui-sans-serif, system-ui, sans-serif" text-anchor="middle">')
    for node in nodes:
        typ = str(node.get("type"))
        if typ == "basic" and int(sum(ord(c) for c in str(node.get("id", ""))) % 4) != 0:
            continue
        color = PALETTE.get(typ, PALETTE["basic"])["fill"]
        size = 10 if typ == "basic" else 12 if typ == "extra" else 16
        weight = 600 if typ != "ultimate" else 800
        y = float(node["y"]) - float(node["radius"]) - 7
        lines.append(
            f'<text x="{node["x"]}" y="{y:.1f}" fill="{color}" font-size="{size}" font-weight="{weight}" opacity="0.92">{escape(str(node.get("label", "")))}</text>'
        )
    lines.append("</g>")

    legend_x = 44
    legend_y = height - 110
    lines.extend(
        [
            '<g font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="14" fill="#cbd5e1">',
            f'<text x="{legend_x}" y="{legend_y - 22}" font-size="20" font-weight="800" fill="#e2e8f0">Gaia Skill Graph</text>',
        ]
    )
    for i, skill_type in enumerate(("basic", "extra", "ultimate")):
        y = legend_y + i * 28
        color = PALETTE[skill_type]
        count = sum(1 for node in nodes if node.get("type") == skill_type)
        lines.append(f'<circle cx="{legend_x + 8}" cy="{y - 5}" r="6" fill="{color["fill"]}"/>')
        lines.append(f'<text x="{legend_x + 24}" y="{y}">{color["label"]}: {count}</text>')
    lines.append("</g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def _html_json(data: dict[str, Any]) -> str:
    return escape(json.dumps(data, indent=2, ensure_ascii=False), quote=False)


def render_html(graph: dict[str, Any], named_skills: dict[str, Any] | None = None) -> str:
    named_skills = named_skills or {"buckets": {}}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gaia Skill Graph</title>
<style>
  :root {{
    color-scheme: dark;
    --bg: #020617;
    --panel: rgba(15, 23, 42, .82);
    --panel-border: rgba(148, 163, 184, .22);
    --text: #e2e8f0;
    --muted: #94a3b8;
    --basic: #38bdf8;
    --extra: #c084fc;
    --ultimate: #f59e0b;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; min-height: 100%; background: var(--bg); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  body {{ overflow: hidden; }}
  .shell {{ position: fixed; inset: 0; background: radial-gradient(circle at 50% 45%, rgba(15, 23, 42, .88), #020617 72%); }}
  #gaiaGraphCanvas {{ display: block; width: 100%; height: 100%; }}
  .toolbar {{
    position: fixed; top: 16px; left: 16px; right: 16px; z-index: 2;
    display: flex; align-items: center; justify-content: space-between; gap: 12px; pointer-events: none;
  }}
  .panel {{
    pointer-events: auto; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
    background: var(--panel); border: 1px solid var(--panel-border); border-radius: 8px;
    box-shadow: 0 18px 50px rgba(0, 0, 0, .28); backdrop-filter: blur(16px); padding: 10px 12px;
  }}
  h1 {{ margin: 0; font-size: 15px; line-height: 1.15; letter-spacing: 0; }}
  .meta {{ color: var(--muted); font-size: 12px; }}
  .search {{
    width: min(320px, 46vw); height: 36px; border: 1px solid rgba(148, 163, 184, .28); border-radius: 7px;
    background: rgba(2, 6, 23, .7); color: var(--text); padding: 0 11px; outline: none;
  }}
  .search:focus {{ border-color: rgba(56, 189, 248, .7); box-shadow: 0 0 0 3px rgba(56, 189, 248, .12); }}
  .button {{
    height: 36px; border: 1px solid rgba(148, 163, 184, .28); border-radius: 7px; background: rgba(15, 23, 42, .72);
    color: var(--text); padding: 0 11px; cursor: pointer;
  }}
  .button.active {{ border-color: rgba(56, 189, 248, .7); color: #bae6fd; background: rgba(56, 189, 248, .12); }}
  .legend {{ position: fixed; right: 16px; bottom: 16px; z-index: 2; display: grid; gap: 7px; pointer-events: none; }}
  .legend-item {{ display: flex; align-items: center; gap: 8px; color: var(--muted); font-size: 12px; }}
  .swatch {{ width: 9px; height: 9px; border-radius: 50%; }}
  .tooltip {{
    position: fixed; z-index: 3; display: none; max-width: min(340px, calc(100vw - 32px));
    background: rgba(2, 6, 23, .92); border: 1px solid rgba(148, 163, 184, .28); border-radius: 8px;
    padding: 10px 12px; box-shadow: 0 18px 50px rgba(0, 0, 0, .35); pointer-events: none;
  }}
  .tooltip strong {{ display: block; margin-bottom: 4px; font-size: 13px; }}
  .tooltip span {{ color: var(--muted); font-size: 12px; line-height: 1.35; }}
  @media (max-width: 720px) {{
    .toolbar {{ align-items: stretch; flex-direction: column; }}
    .panel {{ align-items: stretch; }}
    .search {{ width: 100%; }}
  }}
</style>
</head>
<body>
<main class="shell" aria-label="Interactive Gaia skill graph">
  <canvas id="gaiaGraphCanvas"></canvas>
</main>
<div class="toolbar">
  <div class="panel">
    <div>
      <h1>Gaia Skill Graph</h1>
      <div class="meta" id="graphMeta">Loading graph</div>
    </div>
  </div>
  <div class="panel">
    <input class="search" id="graphSearch" type="search" placeholder="Search skills" aria-label="Search skills">
    <button class="button" id="namedToggle" type="button">Named Skills</button>
    <button class="button" id="resetView" type="button">Reset</button>
  </div>
</div>
<div class="panel legend" aria-hidden="true">
  <div class="legend-item"><span class="swatch" style="background: var(--basic)"></span>Basic</div>
  <div class="legend-item"><span class="swatch" style="background: var(--extra)"></span>Extra</div>
  <div class="legend-item"><span class="swatch" style="background: var(--ultimate)"></span>Ultimate</div>
</div>
<div class="tooltip" id="graphTooltip"></div>
<script type="application/json" id="gaia-graph-data">{_html_json(graph)}</script>
<script type="application/json" id="gaia-named-skills">{_html_json(named_skills)}</script>
<script>
(() => {{
  const graph = JSON.parse(document.getElementById('gaia-graph-data').textContent);
  const namedIndex = JSON.parse(document.getElementById('gaia-named-skills').textContent);
  const canvas = document.getElementById('gaiaGraphCanvas');
  const ctx = canvas.getContext('2d');
  const search = document.getElementById('graphSearch');
  const namedToggle = document.getElementById('namedToggle');
  const resetView = document.getElementById('resetView');
  const meta = document.getElementById('graphMeta');
  const tooltip = document.getElementById('graphTooltip');
  const palette = {{
    basic: '#38bdf8',
    extra: '#c084fc',
    ultimate: '#f59e0b'
  }};
  const typeRadius = {{ basic: 330, extra: 205, ultimate: 70 }};
  const typeSize = {{ basic: 4.5, extra: 7, ultimate: 11 }};
  const buckets = namedIndex.buckets || {{}};
  const namedMap = {{}};
  const titleMap = {{}};

  Object.entries(buckets).forEach(([skillId, entries]) => {{
    if (!Array.isArray(entries) || !entries.length) return;
    const origin = entries.find(entry => entry.origin) || entries[0];
    if (origin && origin.id) namedMap[skillId] = origin.id;
    if (origin && origin.title) titleMap[skillId] = origin.title;
  }});

  const skills = (graph.skills || []).filter(skill => skill.id).map(skill => ({{
    id: skill.id,
    name: skill.name || skill.id,
    type: skill.type || 'basic',
    level: skill.level || '',
    rarity: skill.rarity || '',
    description: skill.description || '',
    prerequisites: Array.isArray(skill.prerequisites) ? skill.prerequisites : [],
    named: namedMap[skill.id] || '',
    namedTitle: titleMap[skill.id] || ''
  }}));
  const nodeById = new Map(skills.map(skill => [skill.id, skill]));
  const edges = [];
  skills.forEach(target => {{
    target.prerequisites.forEach(sourceId => {{
      const source = nodeById.get(sourceId);
      if (source) edges.push({{ source, target }});
    }});
  }});

  let width = 0;
  let height = 0;
  let dpr = 1;
  let view = {{ x: 0, y: 0, scale: 1 }};
  let dragging = false;
  let dragStart = {{ x: 0, y: 0, viewX: 0, viewY: 0 }};
  let pointer = {{ x: 0, y: 0 }};
  let hovered = null;
  let query = '';
  let namedOnly = false;

  function stableHash(str) {{
    let hash = 2166136261;
    for (let i = 0; i < str.length; i += 1) {{
      hash ^= str.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }}
    return hash >>> 0;
  }}

  function placeNodes() {{
    const groups = {{ basic: [], extra: [], ultimate: [] }};
    skills.forEach(skill => (groups[skill.type] || groups.basic).push(skill));
    Object.entries(groups).forEach(([type, list]) => {{
      list.sort((a, b) => `${{a.level}} ${{a.name}}`.localeCompare(`${{b.level}} ${{b.name}}`));
      list.forEach((skill, index) => {{
        const seed = stableHash(skill.id);
        const angle = Math.PI * 2 * index / Math.max(list.length, 1) - Math.PI / 2 + ((seed % 997) / 997 - .5) * .18;
        const radius = typeRadius[type] || 250;
        skill.x = Math.cos(angle) * radius;
        skill.y = Math.sin(angle) * radius;
        skill.size = typeSize[type] || 5;
      }});
    }});
  }}

  function resize() {{
    dpr = window.devicePixelRatio || 1;
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = `${{width}}px`;
    canvas.style.height = `${{height}}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }}

  function screenPoint(node) {{
    return {{
      x: width / 2 + view.x + node.x * view.scale,
      y: height / 2 + view.y + node.y * view.scale
    }};
  }}

  function isVisible(node) {{
    const text = `${{node.id}} ${{node.name}} ${{node.named}} ${{node.namedTitle}}`.toLowerCase();
    if (query && !text.includes(query)) return false;
    if (namedOnly && !node.named) return false;
    return true;
  }}

  function draw() {{
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    const visible = new Set(skills.filter(isVisible));
    const dimmed = query || namedOnly;

    ctx.save();
    ctx.translate(width / 2 + view.x, height / 2 + view.y);
    ctx.scale(view.scale, view.scale);
    [typeRadius.basic, typeRadius.extra, typeRadius.ultimate].forEach(radius => {{
      ctx.beginPath();
      ctx.arc(0, 0, radius, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(148, 163, 184, .12)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }});
    ctx.restore();

    edges.forEach(edge => {{
      const sourceVisible = visible.has(edge.source);
      const targetVisible = visible.has(edge.target);
      if (dimmed && (!sourceVisible || !targetVisible)) return;
      const source = screenPoint(edge.source);
      const target = screenPoint(edge.target);
      ctx.beginPath();
      ctx.moveTo(source.x, source.y);
      ctx.lineTo(target.x, target.y);
      ctx.strokeStyle = `${{palette[edge.target.type] || palette.basic}}66`;
      ctx.lineWidth = 1;
      ctx.stroke();
    }});

    skills.forEach(node => {{
      const visibleNode = visible.has(node);
      const point = screenPoint(node);
      const color = palette[node.type] || palette.basic;
      ctx.globalAlpha = dimmed && !visibleNode ? .1 : 1;
      ctx.beginPath();
      ctx.arc(point.x, point.y, Math.max(3, node.size * view.scale), 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = visibleNode ? 14 : 0;
      ctx.fill();
      ctx.shadowBlur = 0;
      if (node === hovered) {{
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#f8fafc';
        ctx.stroke();
      }}
      if ((node.type !== 'basic' || node.named || node === hovered) && visibleNode) {{
        ctx.font = `${{node.type === 'ultimate' ? 700 : 600}} 12px Inter, system-ui, sans-serif`;
        ctx.textAlign = 'center';
        ctx.fillStyle = '#e2e8f0';
        ctx.fillText(node.named || node.name, point.x, point.y - node.size * view.scale - 9);
      }}
    }});
    ctx.globalAlpha = 1;
  }}

  function findNode(x, y) {{
    let best = null;
    let bestDistance = Infinity;
    skills.forEach(node => {{
      if (!isVisible(node)) return;
      const point = screenPoint(node);
      const distance = Math.hypot(point.x - x, point.y - y);
      if (distance < Math.max(11, node.size * view.scale + 6) && distance < bestDistance) {{
        best = node;
        bestDistance = distance;
      }}
    }});
    return best;
  }}

  function escapeHtml(value) {{
    return String(value || '').replace(/[&<>"']/g, char => ({{
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }}[char]));
  }}

  function updateTooltip(node, x, y) {{
    if (!node) {{
      tooltip.style.display = 'none';
      return;
    }}
    const title = node.namedTitle || node.name;
    const label = node.named ? `${{node.named}} | ${{node.level || node.type}}` : `${{node.id}} | ${{node.level || node.type}}`;
    tooltip.innerHTML = `<strong>${{escapeHtml(title)}}</strong><span>${{escapeHtml(label)}}</span><br><span>${{escapeHtml(node.description)}}</span>`;
    tooltip.style.left = `${{Math.min(x + 14, window.innerWidth - tooltip.offsetWidth - 16)}}px`;
    tooltip.style.top = `${{Math.min(y + 14, window.innerHeight - tooltip.offsetHeight - 16)}}px`;
    tooltip.style.display = 'block';
  }}

  function reset() {{
    view = {{ x: 0, y: 0, scale: 1 }};
    draw();
  }}

  canvas.addEventListener('pointerdown', event => {{
    dragging = true;
    pointer = {{ x: event.clientX, y: event.clientY }};
    dragStart = {{ x: event.clientX, y: event.clientY, viewX: view.x, viewY: view.y }};
    canvas.setPointerCapture(event.pointerId);
  }});
  canvas.addEventListener('pointermove', event => {{
    pointer = {{ x: event.clientX, y: event.clientY }};
    if (dragging) {{
      view.x = dragStart.viewX + event.clientX - dragStart.x;
      view.y = dragStart.viewY + event.clientY - dragStart.y;
      draw();
      return;
    }}
    hovered = findNode(event.clientX, event.clientY);
    updateTooltip(hovered, event.clientX, event.clientY);
    draw();
  }});
  canvas.addEventListener('pointerup', event => {{
    dragging = false;
    canvas.releasePointerCapture(event.pointerId);
  }});
  canvas.addEventListener('wheel', event => {{
    event.preventDefault();
    const nextScale = Math.max(.45, Math.min(2.7, view.scale * (event.deltaY > 0 ? .9 : 1.1)));
    view.scale = nextScale;
    hovered = findNode(pointer.x, pointer.y);
    updateTooltip(hovered, pointer.x, pointer.y);
    draw();
  }}, {{ passive: false }});
  search.addEventListener('input', () => {{
    query = search.value.trim().toLowerCase();
    hovered = null;
    updateTooltip(null);
    draw();
  }});
  namedToggle.addEventListener('click', () => {{
    namedOnly = !namedOnly;
    namedToggle.classList.toggle('active', namedOnly);
    hovered = null;
    updateTooltip(null);
    draw();
  }});
  resetView.addEventListener('click', reset);
  window.addEventListener('resize', resize);

  placeNodes();
  meta.textContent = `${{skills.length}} skills, ${{edges.length}} prerequisites, version ${{graph.version || 'unknown'}}`;
  resize();
}})();
</script>
</body>
</html>
"""


def write_graph_artifact(
    registry_path: str | os.PathLike[str] = ".",
    output: str | os.PathLike[str] | None = None,
    fmt: str = "html",
) -> Path:
    root = _registry_root(registry_path)
    graph = load_graph(root)
    render_graph = build_render_graph(graph)
    fmt = fmt.lower()
    if output is None:
        if fmt == "html":
            output = root / "registry" / "render" / "gaia.html"
        elif fmt == "svg":
            output = root / "registry" / "gaia.svg"
        else:
            output = root / "registry" / "render" / "latest.json"
    out_path = Path(output)
    if not out_path.is_absolute():
        out_path = root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "html":
        out_path.write_text(render_html(graph, load_named_skills(root)), encoding="utf-8")
    elif fmt == "svg":
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
    fmt = getattr(args, "format", "html") or "html"
    output = getattr(args, "output", None)
    out_path = write_graph_artifact(getattr(args, "registry", "."), output=output, fmt=fmt)
    print(f"Wrote Gaia graph {fmt.upper()}: {out_path}")
    if getattr(args, "open", True):
        open_path(out_path)
