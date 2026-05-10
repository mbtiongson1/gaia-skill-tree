"""Tests for the centralized skill display formatter."""

from __future__ import annotations

import pytest

import gaia_cli.formatting as fmt_mod
from gaia_cli.formatting import (
    COLOR_CONTRIBUTOR,
    COLOR_LOCAL_USER,
    RANK_COLORS,
    TIER_COLORS,
    TYPE_SYMBOLS,
    format_level_colored,
    format_skill_colored,
    format_skill_plain,
    format_type_colored,
    format_type_label,
    fusion_equation,
)


# ---------------------------------------------------------------------------
# format_skill_plain
# ---------------------------------------------------------------------------


class TestFormatSkillPlain:
    def test_canon_unnamed(self):
        assert format_skill_plain("python-basics") == "/python-basics"

    def test_named_contributor(self):
        result = format_skill_plain("web-scraping", named_contributor="alice")
        assert result == "alice/web-scraping"

    def test_local_user(self):
        result = format_skill_plain("my-tool", is_local=True, local_user="bob")
        assert result == "bob/my-tool"

    def test_local_without_user_falls_to_canon(self):
        # is_local=True but no local_user -> fallback to canon display
        result = format_skill_plain("orphan-skill", is_local=True)
        assert result == "/orphan-skill"

    def test_named_takes_precedence_over_local(self):
        # If both named_contributor and is_local are given, named wins
        result = format_skill_plain(
            "dual", named_contributor="alice", is_local=True, local_user="bob"
        )
        assert result == "alice/dual"


# ---------------------------------------------------------------------------
# format_skill_colored — with NO_COLOR
# ---------------------------------------------------------------------------


class TestFormatSkillColoredNoColor:
    """When NO_COLOR is set, output should be identical to plain."""

    def test_canon_no_color(self, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")
        result = format_skill_colored("python-basics", "1⭐")
        assert result == "/python-basics"
        assert "\033" not in result

    def test_named_no_color(self, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")
        result = format_skill_colored("web-scraping", "2⭐", named_contributor="alice")
        assert result == "alice/web-scraping"
        assert "\033" not in result

    def test_local_no_color(self, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")
        result = format_skill_colored("my-tool", "3⭐", is_local=True, local_user="bob")
        assert result == "bob/my-tool"
        assert "\033" not in result


# ---------------------------------------------------------------------------
# format_skill_colored — with color enabled (truecolor)
# ---------------------------------------------------------------------------


class TestFormatSkillColoredTruecolor:
    """Force truecolor output and verify ANSI sequences."""

    @pytest.fixture(autouse=True)
    def _enable_color(self, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("COLORTERM", "truecolor")
        # Patch _use_color to always return True (avoids pytest stdout capture issues)
        monkeypatch.setattr(fmt_mod, "_use_color", lambda: True)

    def test_canon_has_rank_color(self):
        result = format_skill_colored("python-basics", "1⭐")
        r, g, b = RANK_COLORS["1⭐"]
        assert f"\033[38;2;{r};{g};{b}m" in result
        assert "/python-basics" in result
        assert "\033[0m" in result

    def test_named_has_red_contributor(self):
        result = format_skill_colored("web-scraping", "2⭐", named_contributor="alice")
        r, g, b = COLOR_CONTRIBUTOR
        assert f"\033[38;2;{r};{g};{b}m" in result
        assert "alice" in result
        # Skill name has rank color
        sr, sg, sb = RANK_COLORS["2⭐"]
        assert f"\033[38;2;{sr};{sg};{sb}m" in result
        assert "web-scraping" in result

    def test_local_has_green_user(self):
        result = format_skill_colored("my-tool", "3⭐", is_local=True, local_user="bob")
        r, g, b = COLOR_LOCAL_USER
        assert f"\033[38;2;{r};{g};{b}m" in result
        assert "bob" in result
        sr, sg, sb = RANK_COLORS["3⭐"]
        assert f"\033[38;2;{sr};{sg};{sb}m" in result
        assert "my-tool" in result

    def test_unknown_level_falls_to_zero(self):
        result = format_skill_colored("foo", "IX")
        r, g, b = RANK_COLORS["0⭐"]
        assert f"\033[38;2;{r};{g};{b}m" in result

    def test_default_level_is_zero(self):
        result = format_skill_colored("bar")
        r, g, b = RANK_COLORS["0⭐"]
        assert f"\033[38;2;{r};{g};{b}m" in result


# ---------------------------------------------------------------------------
# format_skill_colored — 256-color fallback
# ---------------------------------------------------------------------------


class TestFormatSkillColored256:
    """When COLORTERM is not truecolor, should emit 256-color sequences."""

    @pytest.fixture(autouse=True)
    def _enable_256(self, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("COLORTERM", "")
        # Patch _use_color to always return True (avoids pytest stdout capture issues)
        monkeypatch.setattr(fmt_mod, "_use_color", lambda: True)

    def test_256_color_format(self):
        result = format_skill_colored("test-skill", "1⭐")
        assert "\033[38;5;" in result
        assert "\033[38;2;" not in result


# ---------------------------------------------------------------------------
# format_type_label
# ---------------------------------------------------------------------------


class TestFormatTypeLabel:
    def test_basic(self):
        assert format_type_label("basic") == "○ Basic Skill"

    def test_extra(self):
        assert format_type_label("extra") == "◇ Extra Skill"

    def test_ultimate(self):
        assert format_type_label("ultimate") == "◆ Ultimate Skill"

    def test_unknown_type(self):
        result = format_type_label("legendary")
        assert result == "? legendary"


# ---------------------------------------------------------------------------
# format_type_colored
# ---------------------------------------------------------------------------


class TestFormatTypeColored:
    def test_no_color_matches_plain(self, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")
        assert format_type_colored("basic") == format_type_label("basic")

    def test_with_color(self, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("COLORTERM", "truecolor")
        monkeypatch.setattr(fmt_mod, "_use_color", lambda: True)

        result = format_type_colored("extra")
        r, g, b = TIER_COLORS["extra"]
        assert f"\033[38;2;{r};{g};{b}m" in result
        assert "◇ Extra Skill" in result
        assert "\033[0m" in result


# ---------------------------------------------------------------------------
# format_level_colored
# ---------------------------------------------------------------------------


class TestFormatLevelColored:
    def test_no_color(self, monkeypatch):
        monkeypatch.setenv("NO_COLOR", "1")
        assert format_level_colored("3⭐") == "3⭐"

    def test_with_color(self, monkeypatch):
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("COLORTERM", "truecolor")
        monkeypatch.setattr(fmt_mod, "_use_color", lambda: True)

        result = format_level_colored("5⭐")
        r, g, b = RANK_COLORS["5⭐"]
        assert f"\033[38;2;{r};{g};{b}m" in result
        assert "5⭐" in result
        assert "\033[0m" in result


# ---------------------------------------------------------------------------
# fusion_equation
# ---------------------------------------------------------------------------


class TestFusionEquation:
    def test_basic_fusion(self):
        result = fusion_equation(["a", "b"], "c")
        assert result == "/a + /b → /c ◇"

    def test_single_prereq(self):
        result = fusion_equation(["x"], "y")
        assert result == "/x → /y ◇"

    def test_custom_glyph(self):
        result = fusion_equation(["alpha", "beta"], "gamma", result_glyph="◆")
        assert result == "/alpha + /beta → /gamma ◆"

    def test_three_prereqs(self):
        result = fusion_equation(["a", "b", "c"], "d")
        assert result == "/a + /b + /c → /d ◇"

    def test_empty_prereqs(self):
        result = fusion_equation([], "lonely")
        assert result == " → /lonely ◇"


# ---------------------------------------------------------------------------
# Constants integrity
# ---------------------------------------------------------------------------


class TestConstants:
    def test_tier_colors_keys(self):
        assert set(TIER_COLORS.keys()) == {"basic", "extra", "ultimate"}

    def test_rank_colors_keys(self):
        assert set(RANK_COLORS.keys()) == {"0⭐", "1⭐", "2⭐", "3⭐", "4⭐", "5⭐", "6⭐"}

    def test_type_symbols_keys(self):
        assert set(TYPE_SYMBOLS.keys()) == {"basic", "extra", "ultimate"}

    def test_all_colors_are_rgb_tuples(self):
        for name, color in RANK_COLORS.items():
            assert len(color) == 3, f"RANK_COLORS[{name}] not a 3-tuple"
            assert all(0 <= c <= 255 for c in color)
        for name, color in TIER_COLORS.items():
            assert len(color) == 3, f"TIER_COLORS[{name}] not a 3-tuple"
            assert all(0 <= c <= 255 for c in color)
        assert len(COLOR_CONTRIBUTOR) == 3
        assert len(COLOR_LOCAL_USER) == 3
