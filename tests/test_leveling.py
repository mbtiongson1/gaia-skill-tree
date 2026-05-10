from gaia_cli.leveling import demerit_penalty, effective_level, level_summary


def test_effective_level_drops_one_rank_per_demerit():
    skill = {
        "id": "voice-agent",
<<<<<<< HEAD
        "level": "3⭐",
        "demerits": ["heavyweight-dependency"],
    }
    assert demerit_penalty(skill) == 1
    assert effective_level(skill) == "2⭐"
=======
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
>>>>>>> schema/star-tiers-split


def test_effective_level_floors_at_level_i():
    skill = {
        "id": "workflow-orchestration",
<<<<<<< HEAD
        "level": "2⭐",
        "demerits": ["niche-integration", "experimental-feature"],
    }
    assert demerit_penalty(skill) == 2
    assert effective_level(skill) == "1⭐"
=======
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
>>>>>>> schema/star-tiers-split


def test_level_summary_uses_base_and_effective_levels():
    skill = {
        "id": "mcp-integration",
<<<<<<< HEAD
        "level": "3⭐",
        "demerits": ["niche-integration"],
    }
    assert level_summary(skill) == {
        "baseLevel": "3⭐",
        "effectiveLevel": "2⭐",
=======
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
>>>>>>> schema/star-tiers-split
        "demerits": ["niche-integration"],
    }


def test_level_i_skips_demerit_reduction():
    skill = {
        "id": "tokenize",
<<<<<<< HEAD
        "level": "1⭐",
        "demerits": ["niche-integration"],
    }
    assert effective_level(skill) == "1⭐"
=======
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
>>>>>>> schema/star-tiers-split
