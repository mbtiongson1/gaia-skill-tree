"""Builds valid Gaia skill node candidates from crawler output."""

from datetime import datetime


def build_candidate(
    id: str,
    name: str,
    description: str,
    skill_type: str = "atomic",
    source_url: str = "",
    source_type: str = "manual",
    evaluator: str = "gaiabot",
    evidence_class: str = "C",
    score: int = 0,
) -> dict:
    """Build a skill candidate matching schema/skill.schema.json."""
    return {
        "id": id,
        "name": name,
        "type": skill_type,
        "level": "I",
        "rarity": "common",
        "description": description,
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": evidence_class,
                "source": source_url,
                "evaluator": evaluator,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "notes": f"Auto-discovered from {source_type}. Evidence score: {score}/100.",
                "source_type": source_type,
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": datetime.now().strftime("%Y-%m-%d"),
        "updatedAt": datetime.now().strftime("%Y-%m-%d"),
        "version": "0.1.0",
    }


def normalize_id(name: str) -> str:
    """Convert a display name to a kebab-case skill ID."""
    import re
    cleaned = re.sub(r"[^a-z0-9\s-]", "", name.lower())
    cleaned = re.sub(r"\s+", "-", cleaned.strip())
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned[:64]
