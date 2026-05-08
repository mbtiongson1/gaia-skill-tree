"""Render skill data as ASCII collectible cards for terminal display.

Supports 24-bit truecolor ANSI with 256-color fallback.
Respects NO_COLOR env var and non-TTY pipe detection.
"""

from __future__ import annotations

import json
import os
import sys

from gaia_cli.registry import registry_graph_path
import textwrap
from typing import Optional

# Enable VT100 processing on Windows
if sys.platform == "win32":
    os.system("")


# ─── ANSI color support ────────────────────────────────────────────────────

def _use_color() -> bool:
    """Return False if NO_COLOR is set or stdout is not a TTY."""
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty()


def _use_truecolor() -> bool:
    """Return True if terminal supports 24-bit color."""
    colorterm = os.environ.get("COLORTERM", "")
    return colorterm in ("truecolor", "24bit")


def fg(r: int, g: int, b: int) -> str:
    """Foreground color escape."""
    if not _use_color():
        return ""
    if _use_truecolor():
        return f"\033[38;2;{r};{g};{b}m"
    index = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
    return f"\033[38;5;{index}m"


def bg(r: int, g: int, b: int) -> str:
    """Background color escape."""
    if not _use_color():
        return ""
    if _use_truecolor():
        return f"\033[48;2;{r};{g};{b}m"
    index = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
    return f"\033[48;5;{index}m"


def reset() -> str:
    """Reset all attributes."""
    return "\033[0m" if _use_color() else ""


def bold() -> str:
    """Bold text."""
    return "\033[1m" if _use_color() else ""


def dim() -> str:
    """Dim text."""
    return "\033[2m" if _use_color() else ""


# ─── Color palette ─────────────────────────────────────────────────────────

TIER_COLORS = {
    "basic": (56, 189, 248),
    "extra": (192, 132, 252),
    "ultimate": (245, 158, 11),
}
RANK_COLORS = {
    "0":  (148, 163, 184),   # Slate
    "I":  (56, 189, 248),    # Sky
    "II": (99, 202, 183),    # Teal
    "III": (167, 139, 250),  # Violet
    "IV": (232, 121, 249),   # Fuchsia
    "V":  (251, 191, 36),    # Amber
    "VI": (251, 191, 36),    # Amber bright
}
COLOR_SUCCESS = (134, 239, 172)
COLOR_MISSING = (100, 116, 139)
COLOR_TEXT = (226, 232, 240)
COLOR_MUTED = (148, 163, 184)
COLOR_GOLD = (251, 191, 36)
COLOR_CONTRIBUTOR = (239, 68, 68)    # Red for named skill contributors
COLOR_LOCAL_USER = (134, 239, 172)   # Bright green for local/user skills


# ─── Style constants ────────────────────────────────────────────────────────

CARD_WIDTH = 48

# Box-drawing characters (rounded for appraise cards)
TL = "╭"
TR = "╮"
BL = "╰"
BR = "╯"
H = "─"
V = "│"
LT = "├"
RT = "┤"

# Tier glyphs
TIER_GLYPHS = {
    "basic": "○",      # ○
    "extra": "◇",      # ◇
    "ultimate": "◆",   # ◆
}

# Rarity decorators (shown in card header)
RARITY_LABELS = {
    "common": "Common",
    "uncommon": "Uncommon",
    "rare": "Rare",
    "epic": "Epic",
    "legendary": "Legendary",
}

# Level display
LEVEL_LABELS = {
    "0": "Lv.0 Basic",
    "I": "Lv.I Awakened",
    "II": "Lv.II Named",
    "III": "Lv.III Evolved",
    "IV": "Lv.IV Hardened",
    "V": "Lv.V Transcendent",
    "VI": "Lv.VI Transcendent ★",
}


# ─── Helper functions ───────────────────────────────────────────────────────


def _pad(text: str, width: int, align: str = "left") -> str:
    """Pad text to a fixed width with given alignment."""
    if len(text) > width:
        return text[: width - 1] + "…"
    if align == "center":
        return text.center(width)
    if align == "right":
        return text.rjust(width)
    return text.ljust(width)


def _wrap_lines(text: str, width: int) -> list[str]:
    """Word-wrap text to fit within width."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _fit_list(items: list[str], max_width: int, prefix: str = "") -> str:
    """
    Join items with commas, fitting within max_width.

    Shows as many items as will fit; appends '+N more' for omitted items.
    The prefix (e.g. 'Prereqs: ') is included in width calculation.
    """
    if not items:
        return prefix + "(none)"
    remaining_width = max_width - len(prefix)
    shown: list[str] = []
    used = 0
    for i, item in enumerate(items):
        # Calculate width needed for this item (including ", " separator)
        sep = ", " if shown else ""
        # Reserve space for the "+N more" suffix if there are remaining items
        remaining_items = len(items) - i - 1
        suffix = f" +{remaining_items} more" if remaining_items > 0 else ""
        needed = len(sep) + len(item)
        # Check if adding this item still leaves room for the suffix if we stop here
        if shown and used + needed + (len(suffix) if remaining_items > 0 else 0) > remaining_width:
            break
        shown.append(item)
        used += needed

    omitted = len(items) - len(shown)
    result = ", ".join(shown)
    if omitted > 0:
        result += f" +{omitted} more"
    return prefix + result


def _name_from_slug(slug: str) -> str:
    """Convert a kebab-case skill slug into a human display name."""
    small_words = {"and", "or", "of", "the", "to", "for", "in", "on", "with"}
    words = []
    for index, part in enumerate(piece for piece in slug.split("-") if piece):
        word = part.lower()
        if index > 0 and word in small_words:
            words.append(word)
        else:
            words.append(word.capitalize())
    return " ".join(words)


def _separator(width: int = CARD_WIDTH) -> str:
    """Return a horizontal separator line."""
    inner = width - 2
    return f"{LT}{H * inner}{RT}"


def _line(content: str, width: int = CARD_WIDTH) -> str:
    """Wrap content in card border characters."""
    inner = width - 4  # V + space + content + space + V
    return f"{V} {_pad(content, inner)} {V}"


def _top_border(width: int = CARD_WIDTH) -> str:
    inner = width - 2
    return f"{TL}{H * inner}{TR}"


def _bottom_border(width: int = CARD_WIDTH) -> str:
    inner = width - 2
    return f"{BL}{H * inner}{BR}"


# ─── Main rendering ─────────────────────────────────────────────────────────


def render_card(skill: dict, *, width: int = CARD_WIDTH) -> str:
    """
    Render a single skill as an ASCII card.

    Args:
        skill: A skill dict (from gaia.json skills array).
        width: Card width in characters (default 48).

    Returns:
        Multi-line string representing the card.
    """
    inner = width - 4  # usable content width

    tier = skill.get("type", "basic")
    glyph = TIER_GLYPHS.get(tier, "○")
    skill_id = skill.get("id", "unknown")
    name = f"/{skill_id}"
    rarity = skill.get("rarity", "common")
    rarity_label = RARITY_LABELS.get(rarity, rarity.capitalize())
    level = skill.get("level", "0")
    level_label = LEVEL_LABELS.get(level, f"Lv.{level}")
    description = skill.get("description", "")
    prereqs = skill.get("prerequisites", [])
    derivatives = skill.get("derivatives", [])
    status = skill.get("status", "provisional")
    evidence_count = len(skill.get("evidence", []))

    lines: list[str] = []

    # Top border
    lines.append(_top_border(width))

    # Header: glyph + name + rarity
    header_left = f"{glyph} {name}"
    header_right = f"[{rarity_label}]"
    available = inner - len(header_right) - 1
    if len(header_left) > available:
        header_left = header_left[: available - 1] + "…"
    header = f"{header_left}{' ' * (inner - len(header_left) - len(header_right))}{header_right}"
    lines.append(f"{V} {header} {V}")

    # Sub-header: level + tier label
    sub_left = level_label
    sub_right = f"{tier.capitalize()} Skill"
    sub_line = f"{sub_left}{' ' * (inner - len(sub_left) - len(sub_right))}{sub_right}"
    lines.append(f"{V} {sub_line} {V}")

    # Separator
    lines.append(_separator(width))

    # Description (wrapped)
    desc_lines = _wrap_lines(description, inner) if description else ["(no description)"]
    for dl in desc_lines[:4]:  # cap at 4 lines
        lines.append(_line(dl, width))
    if len(desc_lines) > 4:
        lines.append(_line("...", width))

    # Separator
    lines.append(_separator(width))

    # Prerequisites (slash-named)
    if prereqs:
        prereq_list = [f"/{p}" for p in prereqs]
        prereq_str = _fit_list(prereq_list, inner, prefix="Prereqs: ")
        lines.append(_line(prereq_str, width))
    else:
        lines.append(_line("Prereqs: (none)", width))

    # Derivatives (slash-named)
    if derivatives:
        deriv_list = [f"/{d}" for d in derivatives]
        deriv_str = _fit_list(deriv_list, inner, prefix="Unlocks: ")
        lines.append(_line(deriv_str, width))
    else:
        lines.append(_line("Unlocks: (none)", width))

    # Separator
    lines.append(_separator(width))

    # Footer: ID + status + evidence
    footer_left = skill_id
    footer_right = f"{status} | ev:{evidence_count}"
    footer_line = f"{footer_left}{' ' * (inner - len(footer_left) - len(footer_right))}{footer_right}"
    lines.append(f"{V} {footer_line} {V}")

    # Bottom border
    lines.append(_bottom_border(width))

    return "\n".join(lines)


def render_card_compact(skill: dict) -> str:
    """
    Render a compact single-line card summary.

    Format: [glyph] /skill-id (level) [rarity] — first 60 chars of description
    """
    tier = skill.get("type", "basic")
    glyph = TIER_GLYPHS.get(tier, "○")
    skill_id = skill.get("id", skill.get("name", "unknown"))
    name = f"/{skill_id}"
    level = skill.get("level", "0")
    rarity = skill.get("rarity", "common")
    desc = skill.get("description", "")
    short_desc = desc[:60] + "…" if len(desc) > 60 else desc
    return f"{glyph} {name} (Lv.{level}) [{rarity}] — {short_desc}"


def render_cards(skills: list[dict], *, width: int = CARD_WIDTH, compact: bool = False) -> str:
    """
    Render multiple skills as cards.

    Args:
        skills: List of skill dicts.
        width: Card width (ignored in compact mode).
        compact: If True, render one-line summaries instead of full cards.

    Returns:
        Multi-line string with all cards.
    """
    if compact:
        return "\n".join(render_card_compact(s) for s in skills)
    return "\n\n".join(render_card(s, width=width) for s in skills)


def load_and_render(
    skill_id: str,
    registry_path: str = ".",
    *,
    compact: bool = False,
    width: int = CARD_WIDTH,
) -> Optional[str]:
    """
    Load a skill by ID from the registry and render its card.

    Args:
        skill_id: The kebab-case skill ID.
        registry_path: Path to the registry root.
        compact: Use compact rendering.
        width: Card width.

    Returns:
        Rendered card string, or None if skill not found.
    """
    graph_path = registry_graph_path(registry_path)
    if not os.path.exists(graph_path):
        return None

    with open(graph_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    skill_map = {s["id"]: s for s in graph_data.get("skills", [])}
    skill = skill_map.get(skill_id)
    if skill is None:
        return None

    if compact:
        return render_card_compact(skill)
    return render_card(skill, width=width)


# ─── Appraise card (colored, with prereq status + actions) ─────────────────


def render_appraise_card(
    skill_data: dict,
    prereq_status: dict,
    derivatives: list,
    actions: list[str],
    owned: bool = False,
) -> str:
    """
    Rich appraise card with ANSI color.

    Args:
        skill_data: skill dict from gaia.json
        prereq_status: {prereq_id: True/False} — True = user has it
        derivatives: list of derivative skill dicts [{id, name, type}]
        actions: list of action labels (e.g. ["[F] Fuse", "[P] Promote"])
        owned: whether user owns this skill
    """
    width = CARD_WIDTH
    inner = width - 4

    tier = skill_data.get("type", "basic")
    tc = TIER_COLORS.get(tier, (56, 189, 248))
    rc = RANK_COLORS.get(skill_data.get("level", "0"), (148, 163, 184))
    glyph = TIER_GLYPHS.get(tier, "○")
    skill_id = skill_data.get("id", "?")
    name = f"/{skill_id}"
    level = skill_data.get("level", "0")
    rarity = skill_data.get("rarity", "common")
    desc = skill_data.get("description", "")

    bc = fg(*tc)  # border color
    r = reset()

    lines = []

    # Top border
    lines.append(f"{bc}{TL}{H * (width - 2)}{TR}{r}")

    # Header line: glyph + name + level (rank-colored)
    level_str = f"Level {level}"
    header_left = f"{glyph} {name}"
    space = inner - len(header_left) - len(level_str)
    if space < 1:
        header_left = header_left[: inner - len(level_str) - 2] + "…"
        space = 1
    lines.append(f"{bc}{V}{r} {bold()}{fg(*tc)}{header_left}{r}{' ' * space}{fg(*rc)}{level_str}{r} {bc}{V}{r}")

    # Thin divider
    lines.append(f"{bc}{V}{r} {fg(*COLOR_MUTED)}{H * inner}{r} {bc}{V}{r}")

    # Type + rarity (using proper type labels)
    type_labels = {"basic": "Basic Skill", "extra": "Extra Skill", "ultimate": "Ultimate Skill"}
    type_str = f"Type: {type_labels.get(tier, tier.capitalize())}"
    rarity_str = f"Rarity: {rarity}"
    meta = f"{type_str}    {rarity_str}"
    lines.append(f"{bc}{V}{r} {fg(*COLOR_MUTED)}{_pad(meta, inner)}{r} {bc}{V}{r}")

    # Blank
    lines.append(f"{bc}{V}{r} {' ' * inner} {bc}{V}{r}")

    # Description
    for dl in textwrap.wrap(desc, inner)[:3]:
        lines.append(f"{bc}{V}{r} {fg(*COLOR_TEXT)}{_pad(dl, inner)}{r} {bc}{V}{r}")

    # Blank
    lines.append(f"{bc}{V}{r} {' ' * inner} {bc}{V}{r}")

    # Prerequisites with check/circle
    lines.append(f"{bc}{V}{r} {bold()}Prerequisites:{r}{' ' * (inner - 14)} {bc}{V}{r}")
    if prereq_status:
        prereq_items = []
        for pid, has in prereq_status.items():
            icon = f"{fg(*COLOR_SUCCESS)}✓{r}" if has else f"{fg(*COLOR_MISSING)}○{r}"
            prereq_items.append(f"  {icon} /{pid}")
        # Two-column layout
        col_w = inner // 2
        for i in range(0, len(prereq_items), 2):
            left = prereq_items[i] if i < len(prereq_items) else ""
            right = prereq_items[i + 1] if i + 1 < len(prereq_items) else ""
            # Rough padding (ANSI codes make len unreliable, but good enough)
            raw_left = left.replace(fg(*COLOR_SUCCESS), "").replace(fg(*COLOR_MISSING), "").replace(r, "")
            pad_l = col_w - len(raw_left)
            if pad_l < 0:
                pad_l = 0
            combined = left + " " * pad_l + right
            lines.append(f"{bc}{V}{r} {combined}{' ' * max(0, inner - len(raw_left) - pad_l - len(right.replace(fg(*COLOR_SUCCESS), '').replace(fg(*COLOR_MISSING), '').replace(r, '')))} {bc}{V}{r}")
    else:
        lines.append(f"{bc}{V}{r}   {fg(*COLOR_MUTED)}(none){r}{' ' * (inner - 8)} {bc}{V}{r}")

    # Blank
    lines.append(f"{bc}{V}{r} {' ' * inner} {bc}{V}{r}")

    # Derivatives (unlocks) — slash-named
    if derivatives:
        deriv_line = "Unlocks: " + ", ".join("/" + (d.get("id", d) if isinstance(d, dict) else d) for d in derivatives[:4])
        if len(derivatives) > 4:
            deriv_line += f" +{len(derivatives) - 4} more"
        lines.append(f"{bc}{V}{r} {fg(*COLOR_MUTED)}{_pad(deriv_line, inner)}{r} {bc}{V}{r}")
    else:
        lines.append(f"{bc}{V}{r} {fg(*COLOR_MUTED)}{_pad('Unlocks: (terminal skill)', inner)}{r} {bc}{V}{r}")

    # Blank
    lines.append(f"{bc}{V}{r} {' ' * inner} {bc}{V}{r}")

    # Actions divider + actions
    lines.append(f"{bc}{V}{r} {fg(*COLOR_MUTED)}{H * inner}{r} {bc}{V}{r}")
    if actions:
        actions_str = "  ".join(actions)
        lines.append(f"{bc}{V}{r} {bold()}{_pad(actions_str, inner)}{r} {bc}{V}{r}")

    # Owned badge
    if owned:
        badge = f"{fg(*COLOR_GOLD)}★ OWNED{r}"
        lines.append(f"{bc}{V}{r} {badge}{' ' * (inner - 7)} {bc}{V}{r}")

    # Bottom border
    lines.append(f"{bc}{BL}{H * (width - 2)}{BR}{r}")

    return "\n".join(lines)


# ─── Unlock celebration ────────────────────────────────────────────────────


def render_unlock_card(skill_data: dict, new_paths: list) -> str:
    """Celebratory unlock card with ASCII art."""
    tier = skill_data.get("type", "basic")
    tc = TIER_COLORS.get(tier, (56, 189, 248))
    skill_id = skill_data.get("id", "?")
    name = f"/{skill_id}"
    glyph = TIER_GLYPHS.get(tier, "○")
    level = skill_data.get("level", "0")
    rarity = skill_data.get("rarity", "common")

    gc = fg(*COLOR_GOLD)
    tc_fg = fg(*tc)
    r = reset()
    b = bold()

    art = [
        f"{gc}        ✦  ·  ✦        {r}",
        f"{gc}     ·  ╱────╲  ·     {r}",
        f"{gc}    ✦  │ {tc_fg}{glyph}{glyph}{glyph}{glyph}{gc} │  ✦    {r}",
        f"{gc}     ·  ╲────╱  ·     {r}",
        f"{gc}        ✦  ·  ✦        {r}",
        f"",
        f"    {b}{gc}═══ SKILL UNLOCKED ═══{r}",
        f"",
        f"    {tc_fg}{b}{glyph} {name}{r}",
        f"    {fg(*COLOR_MUTED)}Level {level} • {tier.capitalize()} • {rarity}{r}",
    ]

    if new_paths:
        art.append(f"")
        art.append(f"    {fg(*COLOR_TEXT)}New paths opened:{r}")
        for p in new_paths[:4]:
            pname = p.get("name", p.get("skillId", "?")) if isinstance(p, dict) else p
            dist = p.get("distance", "?") if isinstance(p, dict) else "?"
            art.append(f"      {fg(*COLOR_MUTED)}→{r} {pname} ({dist} away)")

    return "\n".join(art)


# ─── Path summary ─────────────────────────────────────────────────────────


def render_path_summary(paths: dict) -> str:
    """Compact summary of progression state."""
    near = len(paths.get("nearUnlocks", []))
    one = len(paths.get("oneAway", []))
    avail = len(paths.get("availablePaths", []))

    gc = fg(*COLOR_GOLD)
    mc = fg(*COLOR_MUTED)
    r = reset()
    b = bold()

    parts = []
    if near:
        parts.append(f"{gc}{b}{near}{r} ready to fuse")
    if one:
        parts.append(f"{b}{one}{r} one away")
    if avail:
        parts.append(f"{mc}{avail}{r} reachable")

    if not parts:
        return f"{mc}No progression paths from current state.{r}"

    return f"⚡ {' │ '.join(parts)}"


# ─── Promotion prompt ──────────────────────────────────────────────────────


def render_promotion_prompt(skill_data: dict, proposed_level: str) -> str:
    """Prompt shown when a skill is eligible for promotion."""
    skill_id = skill_data.get("id", "?")
    skill_type = skill_data.get("type", "extra")
    prereqs = skill_data.get("prerequisites", [])
    gc = fg(*COLOR_GOLD)
    tc = fg(*TIER_COLORS.get(skill_type, COLOR_GOLD))
    r = reset()
    b = bold()

    from gaia_cli.promotion import LEVEL_NAMES
    level_name = LEVEL_NAMES.get(proposed_level, proposed_level)

    lines = [""]
    # Show fusion diagram if skill has prerequisites
    if prereqs:
        lines.append(render_fusion_diagram(prereqs, skill_id, skill_type))
    lines.extend([
        f"  {gc}┌─ Fusion ──────────────────────────────┐{r}",
        f"  {gc}│{r}  {tc}{b}/{skill_id}{r} can advance to {b}Level {proposed_level}{r} ({level_name})",
        f"  {gc}│{r}  Run: {b}gaia fuse {skill_id}{r}",
        f"  {gc}└───────────────────────────────────────────┘{r}",
        "",
    ])
    return "\n".join(lines)


# ─── Fusion diagram ───────────────────────────────────────────────────────


def render_fusion_diagram(prereqs: list[str], result: str, result_type: str = "extra") -> str:
    """Render a Unicode fusion flow diagram showing skill combination."""
    tier_color = TIER_COLORS.get(result_type, TIER_COLORS["extra"])
    glyph = TIER_GLYPHS.get(result_type, "◇")

    mc = fg(*COLOR_MUTED)
    tc = fg(*tier_color)
    tb = bold() + fg(*tier_color)
    r = reset()

    # Format skill names with slash prefix
    prereq_names = [f"/{p}" for p in prereqs]
    result_name = f"/{result}"

    # Single prereq: simple arrow
    if len(prereqs) == 1:
        return f"  {mc}{prereq_names[0]} ────▶{r} {tb}{result_name} {glyph}{r}"

    # Pad prereq names to equal width
    max_len = max(len(n) for n in prereq_names)
    padded = [n.ljust(max_len) for n in prereq_names]

    n = len(padded)
    lines = []

    if n == 2:
        # Two prereqs: bracket rows with a connector row in between
        padding = " " * max_len
        lines.append(f"  {mc}{padded[0]} ─┐{r}")
        lines.append(f"  {mc}{padding}  {r}{tc}├──▶{r} {tb}{result_name} {glyph}{r}")
        lines.append(f"  {mc}{padded[1]} ─┘{r}")
    else:
        # 3+ prereqs: arrow on the vertical midpoint row
        mid = n // 2
        for i, name in enumerate(padded):
            if i == 0:
                bracket = "─┐"
            elif i == n - 1:
                bracket = "─┘"
            elif i == mid:
                bracket = "─┼──▶"
            else:
                bracket = "─┤"

            if i == mid:
                line = f"  {mc}{name} {r}{tc}─┼──▶{r} {tb}{result_name} {glyph}{r}"
            else:
                line = f"  {mc}{name} {bracket}{r}"
            lines.append(line)

    return "\n".join(lines)
