from gaia_cli.leveling import demerit_penalty, effective_level, level_summary


def test_effective_level_drops_one_rank_per_demerit():
    skill = {
        "id": "voice-agent",
<<<<<<< Updated upstream
        "level": "III",
        "demerits": ["heavyweight-dependency"],
    }
    assert demerit_penalty(skill) == 1
    assert effective_level(skill) == "II"
=======
        "level": "3★",
        "demerits": ["heavyweight-dependency"],
    }
    assert demerit_penalty(skill) == 1
    assert effective_level(skill) == "2★"
>>>>>>> Stashed changes


def test_effective_level_floors_at_level_i():
    skill = {
        "id": "workflow-orchestration",
<<<<<<< Updated upstream
        "level": "II",
        "demerits": ["niche-integration", "experimental-feature"],
    }
    assert demerit_penalty(skill) == 2
    assert effective_level(skill) == "I"
=======
        "level": "2★",
        "demerits": ["niche-integration", "experimental-feature"],
    }
    assert demerit_penalty(skill) == 2
    assert effective_level(skill) == "1★"
>>>>>>> Stashed changes


def test_level_summary_uses_base_and_effective_levels():
    skill = {
        "id": "mcp-integration",
<<<<<<< Updated upstream
        "level": "III",
        "demerits": ["niche-integration"],
    }
    assert level_summary(skill) == {
        "baseLevel": "III",
        "effectiveLevel": "II",
=======
        "level": "3★",
        "demerits": ["niche-integration"],
    }
    assert level_summary(skill) == {
        "baseLevel": "3★",
        "effectiveLevel": "2★",
>>>>>>> Stashed changes
        "demerits": ["niche-integration"],
    }


def test_level_i_skips_demerit_reduction():
    skill = {
        "id": "tokenize",
<<<<<<< Updated upstream
        "level": "I",
        "demerits": ["niche-integration"],
    }
    assert effective_level(skill) == "I"
=======
        "level": "1★",
        "demerits": ["niche-integration"],
    }
    assert effective_level(skill) == "1★"
>>>>>>> Stashed changes
