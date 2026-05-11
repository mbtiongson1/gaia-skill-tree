"""Centralized display formatting for skill identifiers.

Implements the three-tier slash-naming hierarchy with ANSI coloring.
"""

from __future__ import annotations
import os
import sys


# --- ANSI helpers (minimal, reuses pattern from cardRenderer) ---

def _use_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty()


def _fg(r: int, g: int, b: int) -> str:
    if not _use_color():
        return ""
    colorterm = os.environ.get("COLORTERM", "")
    if colorterm in ("truecolor", "24bit"):
        return f"\033[38;2;{r};{g};{b}m"
    index = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
    return f"\033[38;5;{index}m"


def _reset() -> str:
    return "\033[0m" if _use_color() else ""


def _bold() -> str:
    return "\033[1m" if _use_color() else ""


# --- Color palettes ---

TIER_COLORS = {
    "basic": (56, 189, 248),
    "extra": (192, 132, 252),
    "unique": (124, 58, 237),
    "ultimate": (245, 158, 11),
}

RANK_COLORS = {
    "0★":   (148, 163, 184),   # Slate
    "1★":   (56, 189, 248),    # Sky
    "2★":  (99, 202, 183),    # Teal
    "3★": (167, 139, 250),   # Violet
    "4★":  (232, 121, 249),   # Fuchsia
    "5★":   (251, 191, 36),    # Amber
    "6★":  (251, 191, 36),    # Amber bright
}

TYPE_SYMBOLS = {"basic": "○", "extra": "◇", "unique": "◉", "ultimate": "◆"}

COLOR_CONTRIBUTOR = (239, 68, 68)    # #ef4444 -- red for named contributors
COLOR_LOCAL_USER  = (134, 239, 172)  # #86efac -- bright green for local/user skills


# --- Public formatting API ---

def format_skill_plain(skill_id: str, *, named_contributor: str | None = None,
                       is_local: bool = False, local_user: str | None = None) -> str:
    """Return plain display string without ANSI codes."""
    if named_contributor:
        return f"{named_contributor}/{skill_id}"
    if is_local and local_user:
        return f"{local_user}/{skill_id}"
    return f"/{skill_id}"


def format_skill_colored(skill_id: str, level: str = "0★", *,
                         named_contributor: str | None = None,
                         is_local: bool = False, local_user: str | None = None) -> str:
    """Return ANSI-colored display string.

    - Named: RED contributor + rank-colored skill name
    - Local: GREEN username + rank-colored skill name
    - Canon: rank-colored /skill-id
    """
    r = _reset()
    rank_color = RANK_COLORS.get(level, RANK_COLORS["0★"])
    skill_colored = f"{_fg(*rank_color)}{skill_id}{r}"

    if named_contributor:
        contrib_colored = f"{_fg(*COLOR_CONTRIBUTOR)}{named_contributor}{r}"
        return f"{contrib_colored}/{skill_colored}"
    if is_local and local_user:
        user_colored = f"{_fg(*COLOR_LOCAL_USER)}{local_user}{r}"
        return f"{user_colored}/{skill_colored}"
    return f"{_fg(*rank_color)}/{skill_id}{r}"


def format_type_label(skill_type: str) -> str:
    """Return type glyph + label like '○ Basic Skill'."""
    labels = {"basic": "Basic Skill", "extra": "Extra Skill", "unique": "Unique Skill", "ultimate": "Ultimate Skill"}
    symbol = TYPE_SYMBOLS.get(skill_type, "?")
    label = labels.get(skill_type, skill_type)
    return f"{symbol} {label}"


def format_type_colored(skill_type: str) -> str:
    """Return colored type glyph + label."""
    raw = format_type_label(skill_type)
    color = TIER_COLORS.get(skill_type, (148, 163, 184))
    return f"{_fg(*color)}{raw}{_reset()}"


def format_level_colored(level: str) -> str:
    """Return level badge colored by rank."""
    rank_color = RANK_COLORS.get(level, RANK_COLORS["0★"])
    return f"{_fg(*rank_color)}{level}{_reset()}"


def fusion_equation(prereqs: list[str], result: str, result_glyph: str = "◇") -> str:
    """Plain text fusion equation: /a + /b -> /result glyph"""
    parts = " + ".join(f"/{p}" for p in prereqs)
    return f"{parts} → /{result} {result_glyph}"
