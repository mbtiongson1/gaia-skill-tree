import json
import os
import re

_USERNAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]*$")


def _check_username(username: str) -> None:
    if not username or not _USERNAME_RE.match(username):
        raise ValueError(f"Invalid username: {username!r}")


def load_tree(username, registry_path="."):
    _check_username(username)
    tree_path = os.path.join(registry_path, "users", username, "skill-tree.json")
    if not os.path.exists(tree_path):
        return None
    with open(tree_path, 'r') as f:
        return json.load(f)

def save_tree(username, tree_data, registry_path="."):
    _check_username(username)
    tree_path = os.path.join(registry_path, "users", username, "skill-tree.json")
    os.makedirs(os.path.dirname(tree_path), exist_ok=True)
    with open(tree_path, 'w') as f:
        json.dump(tree_data, f, indent=2)

def show_status(tree_data):
    if not tree_data:
        print("No skill tree found.")
        return
    print(f"User: {tree_data.get('userId')}")
    print(f"Last Updated: {tree_data.get('updatedAt')}")
    stats = tree_data.get('stats', {})
    print(f"Total Unlocked: {stats.get('totalUnlocked', 0)}")
    print(f"Highest Rarity: {stats.get('highestRarity', 'common').capitalize()}")
    pending = tree_data.get('pendingCombinations', [])
    if pending:
        print("\nPending Combinations:")
        for p in pending:
            print(f"- {p.get('candidateResult')} (Floor: {p.get('levelFloor')})")

_TYPE_SYMBOL = {"basic": "○", "extra": "◇", "ultimate": "◆"}


def _render_subtree(skill_id, skill_map, unlocked_ids, prefix, is_last, seen):
    symbol = _TYPE_SYMBOL.get(skill_map.get(skill_id, {}).get("type", "basic"), "○")
    name = skill_map.get(skill_id, {}).get("name", skill_id)
    level = skill_map.get(skill_id, {}).get("level", "?")
    connector = "└── " if is_last else "├── "
    lines = [f"{prefix}{connector}{symbol} {name}  [{level}]"]
    seen.add(skill_id)
    child_prefix = prefix + ("    " if is_last else "│   ")
    prereqs = [
        p for p in skill_map.get(skill_id, {}).get("prerequisites", [])
        if p in unlocked_ids
    ]
    for i, child_id in enumerate(prereqs):
        child_is_last = i == len(prereqs) - 1
        if child_id in seen:
            connector2 = "└── " if child_is_last else "├── "
            child_sym = _TYPE_SYMBOL.get(skill_map.get(child_id, {}).get("type", "basic"), "○")
            child_name = skill_map.get(child_id, {}).get("name", child_id)
            child_lvl = skill_map.get(child_id, {}).get("level", "?")
            lines.append(f"{child_prefix}{connector2}{child_sym} {child_name}  [{child_lvl}] ...")
        else:
            lines.extend(_render_subtree(child_id, skill_map, unlocked_ids, child_prefix, child_is_last, seen))
    return lines


def show_tree(tree_data, graph_data=None):
    if not tree_data:
        print("No skill tree found.")
        return

    unlocked = tree_data.get("unlockedSkills", [])
    username = tree_data.get("userId", "unknown")

    skill_map = {}
    if graph_data:
        skill_map = {s["id"]: s for s in graph_data.get("skills", [])}

    unlocked_ids = {s["skillId"] for s in unlocked}

    # Skills that appear as a prerequisite of another unlocked skill are not roots
    all_prereqs = set()
    for sid in unlocked_ids:
        for p in skill_map.get(sid, {}).get("prerequisites", []):
            if p in unlocked_ids:
                all_prereqs.add(p)
    roots = [s for s in unlocked if s["skillId"] not in all_prereqs]

    # Sort roots: ultimate first, then extra, then basic; alphabetical within tier
    tier_order = {"ultimate": 0, "extra": 1, "basic": 2}
    roots.sort(key=lambda s: (tier_order.get(skill_map.get(s["skillId"], {}).get("type", "basic"), 2), s["skillId"]))

    print(username)
    seen: set[str] = set()
    for i, entry in enumerate(roots):
        sid = entry["skillId"]
        is_last = i == len(roots) - 1
        for line in _render_subtree(sid, skill_map, unlocked_ids, "", is_last, seen):
            print(line)
