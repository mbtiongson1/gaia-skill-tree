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

def show_tree(tree_data):
    if not tree_data:
        print("No skill tree found.")
        return
    print("Unlocked Skills:")
    for skill in tree_data.get('unlockedSkills', []):
        sid = skill.get('skillId')
        lvl = skill.get('level')
        print(f"  - {sid} (Level {lvl})")
