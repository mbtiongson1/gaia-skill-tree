"""Tests for gaia_cli.interactive module.

Validates graceful degradation when questionary is not installed
or when running in a non-interactive context.
"""

import os
import sys
from unittest.mock import patch

import pytest

from gaia_cli.interactive import (
    _has_interactive,
    confirm,
    select_fusion_candidate,
    select_promotion_candidate,
    select_skill,
)


class TestHasInteractive:
    """Tests for _has_interactive() detection logic."""

    def test_returns_false_when_stdin_not_tty(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        monkeypatch.delenv("CI", raising=False)
        assert _has_interactive() is False

    def test_returns_false_when_ci_env_set(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setenv("CI", "true")
        assert _has_interactive() is False

    def test_returns_false_when_questionary_missing(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.delenv("CI", raising=False)
        with patch.dict(sys.modules, {"questionary": None}):
            # Simulate ImportError by removing the module
            import importlib
            with patch("builtins.__import__", side_effect=_make_import_raiser("questionary")):
                assert _has_interactive() is False

    def test_returns_true_when_all_conditions_met(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.delenv("CI", raising=False)
        # questionary may or may not be installed; mock it as available
        with patch("builtins.__import__", side_effect=_make_import_passer("questionary")):
            assert _has_interactive() is True


class TestSelectSkill:
    """Tests for select_skill() in non-interactive mode."""

    def test_returns_none_when_non_interactive(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        skills = [{"id": "python-basics", "type": "basic", "level": "1"}]
        assert select_skill(skills) is None

    def test_returns_none_with_empty_skills(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        assert select_skill([]) is None


class TestSelectFusionCandidate:
    """Tests for select_fusion_candidate() in non-interactive mode."""

    def test_returns_none_when_non_interactive(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        candidates = [
            {"candidateResult": "advanced-python", "detectedSkills": ["python-basics", "oop"]}
        ]
        assert select_fusion_candidate(candidates) is None

    def test_returns_none_with_empty_candidates(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        assert select_fusion_candidate([]) is None


class TestSelectPromotionCandidate:
    """Tests for select_promotion_candidate() in non-interactive mode."""

    def test_returns_none_when_non_interactive(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        candidates = [
            {"skillId": "python-basics", "currentLevel": "1", "suggestedLevel": "2"}
        ]
        assert select_promotion_candidate(candidates) is None


class TestConfirm:
    """Tests for confirm() in non-interactive mode."""

    def test_returns_default_true_when_non_interactive(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        assert confirm("Proceed?", default=True) is True

    def test_returns_default_false_when_non_interactive(self, monkeypatch):
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        assert confirm("Proceed?", default=False) is False


# -- Helpers --

def _make_import_raiser(blocked_module):
    """Create an __import__ side_effect that raises ImportError for a specific module."""
    real_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

    def _import(name, *args, **kwargs):
        if name == blocked_module:
            raise ImportError(f"No module named '{blocked_module}'")
        return real_import(name, *args, **kwargs)

    return _import


def _make_import_passer(allowed_module):
    """Create an __import__ side_effect that returns a mock for a specific module."""
    from unittest.mock import MagicMock
    real_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

    def _import(name, *args, **kwargs):
        if name == allowed_module:
            return MagicMock()
        return real_import(name, *args, **kwargs)

    return _import
