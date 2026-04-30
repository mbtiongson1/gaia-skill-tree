"""Skill-tree level promotion logic.

Provides helpers to check promotion eligibility, advance a skill's level,
and inspect the current promotion state for a given skill.
"""

import json
import os
from datetime import date

from .treeManager import load_tree, save_tree

LEVEL_ORDER = ["0", "I", "II", "III", "IV", "V", "VI"]
LEVEL_NAMES = {
    "0": "Basic",
    "I": "Awakened",
    "II": "Named",
    "III": "Evolved",
    "IV": "Hardened",
    "V": "Transcendent",
    "VI": "Transcendent ★",
}

# Evidence class floors per level — None means no evidence required.
EVIDENCE_FLOOR = {
    "0": None,
    "I": None,
    "II": {"C", "B", "A"},
    "III": {"B", "A"},
    "IV": {"B", "A"},
    "V": {"B", "A"},
    "VI": {"A"},
}


def next_level(current: str) -> str | None:
    """Return the next level string, or None if already at max."""
    try:
        idx = LEVEL_ORDER.index(current)
    except ValueError:
        return None
    if idx >= len(LEVEL_ORDER) - 1:
        return None
    return LEVEL_ORDER[idx + 1]


def _get_skill_from_graph(graph_data: dict, skill_id: str) -> dict | None:
    """Look up a skill node by ID in the graph data."""
    for skill in graph_data.get("skills", []):
        if skill["id"] == skill_id:
            return skill
    return None


def _get_skill_from_tree(tree_data: dict, skill_id: str) -> dict | None:
    """Look up a skill entry by ID in the user's tree."""
    for entry in tree_data.get("unlockedSkills", []):
        if entry["skillId"] == skill_id:
            return entry
    return None


def _meets_evidence_floor(graph_skill: dict, target_level: str) -> bool:
    """Check whether the graph skill has evidence meeting the floor for target_level."""
    required_classes = EVIDENCE_FLOOR.get(target_level)
    if required_classes is None:
        return True
    evidence_list = graph_skill.get("evidence", [])
    for ev in evidence_list:
        if ev.get("class") in required_classes:
            return True
    return False


def check_promotion_eligibility(graph_data: dict, tree_data: dict) -> list[dict]:
    """Return a list of skills eligible for promotion.

    Each entry is a dict with keys:
        - skillId: the skill identifier
        - currentLevel: the level in the user's tree
        - nextLevel: the level it would be promoted to
        - name: display name from the graph
    """
    eligible = []
    for entry in tree_data.get("unlockedSkills", []):
        skill_id = entry["skillId"]
        current = entry["level"]
        target = next_level(current)
        if target is None:
            continue
        graph_skill = _get_skill_from_graph(graph_data, skill_id)
        if graph_skill is None:
            continue
        if _meets_evidence_floor(graph_skill, target):
            eligible.append({
                "skillId": skill_id,
                "currentLevel": current,
                "nextLevel": target,
                "name": graph_skill.get("name", skill_id),
            })
    return eligible


def promote_skill(
    username: str,
    skill_id: str,
    registry_path: str,
    new_display_name: str | None = None,
) -> dict:
    """Promote a skill to the next level in the user's tree.

    Args:
        username: GitHub username.
        skill_id: The skill ID to promote.
        registry_path: Path to the registry root (where users/ lives).
        new_display_name: Optional new display name (unused in tree storage
            but returned in the result dict for downstream consumers).

    Returns:
        A dict with keys: skillId, previousLevel, newLevel, displayName.

    Raises:
        ValueError: If the skill is not found in the tree or is already at max level.
    """
    tree_data = load_tree(username, registry_path)
    if tree_data is None:
        raise ValueError(f"No skill tree found for user '{username}'.")

    entry = _get_skill_from_tree(tree_data, skill_id)
    if entry is None:
        raise ValueError(f"Skill '{skill_id}' not found in {username}'s tree.")

    current = entry["level"]
    target = next_level(current)
    if target is None:
        raise ValueError(
            f"Skill '{skill_id}' is already at maximum level ({current})."
        )

    # Update the level in-place
    entry["level"] = target

    # Update the tree's updatedAt timestamp
    tree_data["updatedAt"] = date.today().isoformat()

    save_tree(username, tree_data, registry_path)

    # Load graph to get display name if not provided
    display_name = new_display_name
    if display_name is None:
        graph_path = os.path.join(registry_path, "graph", "gaia.json")
        if os.path.exists(graph_path):
            with open(graph_path, "r", encoding="utf-8") as f:
                graph_data = json.load(f)
            graph_skill = _get_skill_from_graph(graph_data, skill_id)
            if graph_skill:
                display_name = graph_skill.get("name", skill_id)
        if display_name is None:
            display_name = skill_id

    return {
        "skillId": skill_id,
        "previousLevel": current,
        "newLevel": target,
        "displayName": display_name,
    }


def promotion_state(skill_id: str, tree_data: dict, graph_data: dict) -> str:
    """Return the promotion state for a skill.

    Possible return values:
        - "not_unlocked" — skill is not in the user's tree
        - "max_level" — skill is already at max level (VI)
        - "eligible" — skill can be promoted (evidence requirement met)
        - "blocked" — next level requires evidence the graph skill lacks
    """
    entry = _get_skill_from_tree(tree_data, skill_id)
    if entry is None:
        return "not_unlocked"

    current = entry["level"]
    target = next_level(current)
    if target is None:
        return "max_level"

    graph_skill = _get_skill_from_graph(graph_data, skill_id)
    if graph_skill is None:
        return "blocked"

    if _meets_evidence_floor(graph_skill, target):
        return "eligible"

    return "blocked"
