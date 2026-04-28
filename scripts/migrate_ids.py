#!/usr/bin/env python3
"""One-time migration: convert all skill IDs from camelCase to lowercase-dash.

Transforms every ID reference across:
  - graph/gaia.json (skill.id, prerequisites, derivatives, edges)
  - users/*/skill-tree.json (skillId, combinedFrom, detectedSkills, candidateResult)

Usage:
    python3 scripts/migrate_ids.py [--dry-run]
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_PATH = os.path.join(REPO_ROOT, "graph", "gaia.json")
USERS_DIR = os.path.join(REPO_ROOT, "users")


def camel_to_dash(name: str) -> str:
    """Convert camelCase to lowercase-dash.

    Examples:
        chainOfThought -> chain-of-thought
        ragPipeline -> rag-pipeline
        multiAgentOrchestrationV -> multi-agent-orchestration-v
        textToSqlPipeline -> text-to-sql-pipeline
        parseJson -> parse-json
    """
    # Insert dash before uppercase letters (handles sequences like 'SQL' → 's-q-l'
    # but our IDs don't have consecutive caps by convention)
    result = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    return result.lower()


def migrate_graph(graph: dict, id_map: dict) -> None:
    """Migrate all ID references in the graph structure in-place."""
    for skill in graph["skills"]:
        skill["id"] = id_map.get(skill["id"], skill["id"])
        skill["prerequisites"] = [id_map.get(p, p) for p in skill.get("prerequisites", [])]
        skill["derivatives"] = [id_map.get(d, d) for d in skill.get("derivatives", [])]

    for edge in graph.get("edges", []):
        edge["sourceSkillId"] = id_map.get(edge["sourceSkillId"], edge["sourceSkillId"])
        edge["targetSkillId"] = id_map.get(edge["targetSkillId"], edge["targetSkillId"])


def migrate_user_tree(tree: dict, id_map: dict) -> None:
    """Migrate all ID references in a user skill-tree in-place."""
    for unlock in tree.get("unlockedSkills", []):
        unlock["skillId"] = id_map.get(unlock["skillId"], unlock["skillId"])
        unlock["combinedFrom"] = [id_map.get(s, s) for s in unlock.get("combinedFrom", [])]

    for combo in tree.get("pendingCombinations", []):
        combo["detectedSkills"] = [id_map.get(s, s) for s in combo.get("detectedSkills", [])]
        combo["candidateResult"] = id_map.get(combo.get("candidateResult", ""), combo.get("candidateResult", ""))


def main():
    dry_run = "--dry-run" in sys.argv

    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    # Build mapping: old camelCase ID → new lowercase-dash ID
    id_map = {}
    for skill in graph["skills"]:
        old_id = skill["id"]
        new_id = camel_to_dash(old_id)
        if old_id != new_id:
            id_map[old_id] = new_id

    print(f"📋 ID mapping: {len(id_map)} IDs to rename")
    if dry_run:
        for old, new in sorted(id_map.items()):
            print(f"   {old} → {new}")
        print("\n(dry run — no files modified)")
        return

    # Migrate graph
    migrate_graph(graph, id_map)

    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✅ Migrated graph/gaia.json ({len(graph['skills'])} skills, {len(graph['edges'])} edges)")

    # Migrate user skill trees
    if os.path.isdir(USERS_DIR):
        for username in sorted(os.listdir(USERS_DIR)):
            tree_path = os.path.join(USERS_DIR, username, "skill-tree.json")
            if not os.path.isfile(tree_path):
                continue
            with open(tree_path, "r", encoding="utf-8") as f:
                tree = json.load(f)
            migrate_user_tree(tree, id_map)
            with open(tree_path, "w", encoding="utf-8") as f:
                json.dump(tree, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print(f"✅ Migrated {tree_path}")

    print(f"\n🏁 Migration complete. Run validate.py to confirm.")


if __name__ == "__main__":
    main()
