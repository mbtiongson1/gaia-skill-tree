"""Registry health summary for ``gaia stats``."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from gaia_cli.registry import named_skills_dir, registry_graph_path

TYPE_LABELS = {
    "basic": "Atomic",
    "extra": "Composite",
    "ultimate": "Legendary",
}

LEVEL_LABELS = {
    "0": "Basic",
    "I": "Awakened",
    "II": "Named",
    "III": "Evolved",
    "IV": "Hardened",
    "V": "Transcendent",
    "VI": "Transcendent★",
}

LEVEL_ORDER = ("0", "I", "II", "III", "IV", "V", "VI")
TYPE_ORDER = ("basic", "extra", "ultimate")
EVIDENCE_ORDER = ("A", "B", "C")
_EVIDENCE_RANK = {klass: rank for rank, klass in enumerate(reversed(EVIDENCE_ORDER), start=1)}


def _load_json(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _graph_path(registry_path: str | Path) -> Path:
    root = Path(registry_path)
    current = Path(registry_graph_path(root))
    if current.exists():
        return current
    return root / "graph" / "gaia.json"


def _named_dir(registry_path: str | Path) -> Path:
    root = Path(registry_path)
    current = Path(named_skills_dir(root))
    if current.is_dir():
        return current
    return root / "graph" / "named"


def _parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    frontmatter, sep, _body = text[4:].partition("\n---")
    if not sep:
        return {}
    data: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def _iter_named_skill_metadata(registry_path: str | Path) -> Iterable[dict[str, str]]:
    root = _named_dir(registry_path)
    if not root.is_dir():
        return []
    items = []
    for path in sorted(root.glob("*/*.md")):
        try:
            items.append(_parse_frontmatter(path.read_text(encoding="utf-8")))
        except OSError:
            continue
    return items


def _best_evidence_class(skill: dict) -> str | None:
    best: str | None = None
    for evidence in skill.get("evidence", []) or []:
        klass = str(evidence.get("class", "")).upper()
        if klass not in _EVIDENCE_RANK:
            continue
        if best is None or _EVIDENCE_RANK[klass] > _EVIDENCE_RANK[best]:
            best = klass
    return best


def collect_stats(registry_path: str | Path) -> dict:
    """Collect registry counts used by the stats command."""
    graph = _load_json(_graph_path(registry_path))
    skills = graph.get("skills", [])
    edges = graph.get("edges")
    if edges is None:
        edges = [
            {"source": prereq, "target": skill.get("id")}
            for skill in skills
            for prereq in (skill.get("prerequisites", []) or [])
        ]

    type_counts = Counter(skill.get("type", "unknown") for skill in skills)
    level_counts = Counter(skill.get("level", "?") for skill in skills)

    best_evidence_counts: Counter[str] = Counter()
    for skill in skills:
        best = _best_evidence_class(skill)
        if best:
            best_evidence_counts[best] += 1

    named_items = [
        item for item in _iter_named_skill_metadata(registry_path)
        if item.get("id") and item.get("genericSkillRef") and item.get("status", "named") == "named"
    ]
    named_slots = {item["genericSkillRef"] for item in named_items}
    eligible_slots = {
        skill["id"]
        for skill in skills
        if skill.get("id") and skill.get("level") != "0"
    }

    return {
        "total_skills": len(skills),
        "total_edges": len(edges),
        "type_counts": dict(type_counts),
        "level_counts": dict(level_counts),
        "evidence_counts": {klass: best_evidence_counts.get(klass, 0) for klass in EVIDENCE_ORDER},
        "skills_with_evidence": sum(best_evidence_counts.values()),
        "named_implemented": len(named_items),
        "named_slots": len(named_slots),
        "named_eligible": len(eligible_slots),
        "named_unclaimed": max(len(eligible_slots - named_slots), 0),
    }


def _bar(count: int, total: int, width: int = 25) -> str:
    if total <= 0:
        filled = 0
    else:
        filled = round((count / total) * width)
    filled = max(0, min(width, filled))
    return "█" * filled + "░" * (width - filled)


def _percent(count: int, total: int) -> int:
    return round((count / total) * 100) if total else 0


def render_stats(stats: dict) -> str:
    """Render a human-readable stats report."""
    total = stats["total_skills"]
    lines = [f"Gaia Registry — {total} skills  {stats['total_edges']} edges", ""]

    lines.append("Type breakdown")
    for skill_type in TYPE_ORDER:
        label = TYPE_LABELS[skill_type]
        count = stats["type_counts"].get(skill_type, 0)
        lines.append(f"  {label:<9} {count:>4}  {_bar(count, total)}  {_percent(count, total):>3}%")
    for skill_type, count in sorted(stats["type_counts"].items()):
        if skill_type not in TYPE_LABELS:
            lines.append(f"  {skill_type:<9} {count:>4}  {_bar(count, total)}  {_percent(count, total):>3}%")

    lines.extend(["", "Level breakdown"])
    for level in LEVEL_ORDER:
        label = LEVEL_LABELS[level]
        count = stats["level_counts"].get(level, 0)
        suffix = ""
        if level == "II" and stats.get("named_unclaimed", 0):
            suffix = f"  ({stats['named_unclaimed']} slots unclaimed)"
        lines.append(f"  {level:<3} {label:<14} {count:>4}{suffix}")
    for level, count in sorted(stats["level_counts"].items()):
        if level not in LEVEL_LABELS:
            lines.append(f"  {level:<3} {'Unknown':<14} {count:>4}")

    lines.extend(["", "Evidence coverage"])
    lines.append(f"  With evidence {stats['skills_with_evidence']:>4} / {total}")
    for klass in EVIDENCE_ORDER:
        lines.append(f"  Class {klass:<7} {stats['evidence_counts'].get(klass, 0):>4}")

    eligible = stats.get("named_eligible", 0)
    implemented = stats.get("named_implemented", 0)
    lines.extend(["", "Named skills"])
    lines.append(f"  Implemented  {implemented:>4} / {eligible} eligible ({_percent(implemented, eligible)}%)")
    return "\n".join(lines) + "\n"


def stats_command(args) -> None:
    print(render_stats(collect_stats(args.registry)), end="")
