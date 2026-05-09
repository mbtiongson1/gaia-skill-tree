from gaia_cli.leveling import demerit_penalty, effective_level, level_summary


def test_effective_level_drops_one_rank_per_demerit():
    skill = {
        "id": "voice-agent",
        "level": "III",
        "demerits": ["heavyweight-dependency"],
    }
    assert demerit_penalty(skill) == 1
    assert effective_level(skill) == "II"


def test_effective_level_floors_at_level_i():
    skill = {
        "id": "workflow-orchestration",
        "level": "II",
        "demerits": ["niche-integration", "experimental-feature"],
    }
    assert demerit_penalty(skill) == 2
    assert effective_level(skill) == "I"


def test_level_summary_uses_base_and_effective_levels():
    skill = {
        "id": "mcp-integration",
        "level": "III",
        "demerits": ["niche-integration"],
    }
    assert level_summary(skill) == {
        "baseLevel": "III",
        "effectiveLevel": "II",
        "demerits": ["niche-integration"],
    }


def test_level_i_skips_demerit_reduction():
    skill = {
        "id": "tokenize",
        "level": "I",
        "demerits": ["niche-integration"],
    }
    assert effective_level(skill) == "I"
