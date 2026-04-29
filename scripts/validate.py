#!/usr/bin/env python3
"""Gaia Skill Registry — Canonical Graph Validator.

Validates graph/gaia.json against:
1. JSON Schema validation for all skill nodes and edges.
2. DAG cycle detection (DFS from all root nodes).
3. Reference integrity (every parent ID resolves to an existing node).
4. Evidence threshold by level.
5. Legendary approval count check (placeholder).
6. Summary statistics output.

Usage:
    python scripts/validate.py [--graph PATH]

Exit codes:
    0 — All checks passed.
    1 — One or more validation errors.
"""

import json
import sys
import os
import argparse
from collections import defaultdict

# Optional: jsonschema for full schema validation
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


EVIDENCE_FLOOR = {
    "I": None,       # No evidence required (foundation tier)
    "II": {"C", "B", "A"},
    "III": {"B", "A"},
    "IV": {"B", "A"},
    "V": {"B", "A"},
    "VI": {"A"},
}

MIN_PREREQS = {
    "atomic": 0,
    "composite": 2,
    "legendary": 3,
}


def load_graph(path):
    """Load and parse the canonical graph JSON."""
    with open(path, "r") as f:
        return json.load(f)


def load_schema(schema_path):
    """Load a JSON Schema file."""
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_schema(graph, schema_dir):
    """Validate all skill nodes against skill.schema.json."""
    errors = []
    if not HAS_JSONSCHEMA:
        print("⚠  jsonschema not installed — skipping schema validation.")
        print("   Install with: pip install jsonschema")
        return errors

    skill_schema = load_schema(os.path.join(schema_dir, "skill.schema.json"))
    combo_schema = load_schema(os.path.join(schema_dir, "combination.schema.json"))

    for skill in graph.get("skills", []):
        try:
            jsonschema.validate(instance=skill, schema=skill_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema error in skill '{skill.get('id', '?')}': {e.message}")

    for edge in graph.get("edges", []):
        try:
            jsonschema.validate(instance=edge, schema=combo_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema error in edge '{edge.get('sourceSkillId', '?')}->{edge.get('targetSkillId', '?')}': {e.message}")

    return errors


def validate_dag(graph):
    """Check for cycles using DFS. Returns list of errors."""
    errors = []
    skill_ids = {s["id"] for s in graph.get("skills", [])}

    # Build adjacency list (parent -> children)
    children = defaultdict(list)
    for edge in graph.get("edges", []):
        children[edge["sourceSkillId"]].append(edge["targetSkillId"])

    # DFS cycle detection
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {sid: WHITE for sid in skill_ids}

    def dfs(node, path):
        color[node] = GRAY
        for child in children.get(node, []):
            if child not in color:
                continue  # reference integrity catches this
            if color[child] == GRAY:
                cycle_path = path + [node, child]
                errors.append(f"Cycle detected: {' -> '.join(cycle_path)}")
                return
            if color[child] == WHITE:
                dfs(child, path + [node])
        color[node] = BLACK

    for sid in skill_ids:
        if color[sid] == WHITE:
            dfs(sid, [])

    return errors


def validate_references(graph):
    """Check that all prerequisite and derivative IDs resolve to existing nodes."""
    errors = []
    skill_ids = {s["id"] for s in graph.get("skills", [])}

    for skill in graph.get("skills", []):
        for prereq in skill.get("prerequisites", []):
            if prereq not in skill_ids:
                errors.append(f"Skill '{skill['id']}' references missing prerequisite '{prereq}'.")
        for deriv in skill.get("derivatives", []):
            if deriv not in skill_ids:
                errors.append(f"Skill '{skill['id']}' references missing derivative '{deriv}'.")

    for edge in graph.get("edges", []):
        if edge["sourceSkillId"] not in skill_ids:
            errors.append(f"Edge references missing source skill '{edge['sourceSkillId']}'.")
        if edge["targetSkillId"] not in skill_ids:
            errors.append(f"Edge references missing target skill '{edge['targetSkillId']}'.")

    return errors


def validate_prerequisites_count(graph):
    """Check that each skill type has the minimum required number of prerequisites."""
    errors = []
    for skill in graph.get("skills", []):
        min_req = MIN_PREREQS.get(skill["type"], 0)
        actual = len(skill.get("prerequisites", []))
        if skill["type"] == "atomic" and actual > 0:
            errors.append(f"Atomic skill '{skill['id']}' must have 0 prerequisites (has {actual}).")
        elif actual < min_req:
            errors.append(f"{skill['type'].title()} skill '{skill['id']}' needs ≥{min_req} prerequisites (has {actual}).")
    return errors


def validate_evidence(graph):
    """Check that evidence meets the minimum threshold for each skill's level."""
    errors = []
    for skill in graph.get("skills", []):
        level = skill.get("level", "I")
        required_classes = EVIDENCE_FLOOR.get(level)

        if required_classes is None:
            continue  # Level I needs no evidence

        evidence = skill.get("evidence", [])
        if not evidence:
            errors.append(f"Skill '{skill['id']}' at Level {level} requires evidence but has none.")
            continue

        has_qualifying = any(e.get("class") in required_classes for e in evidence)
        if not has_qualifying:
            errors.append(
                f"Skill '{skill['id']}' at Level {level} needs evidence class "
                f"{required_classes} but only has: {[e.get('class') for e in evidence]}."
            )
    return errors


def validate_legendary(graph):
    """Check legendary-specific constraints."""
    errors = []
    for skill in graph.get("skills", []):
        if skill["type"] != "legendary":
            continue

        # Legendary stubs at Level I are allowed without evidence
        if skill["level"] == "I" and skill["status"] == "provisional":
            continue

        # Validated legendaries need 3+ Class A/B evidence
        if skill["status"] == "validated":
            ab_evidence = [e for e in skill.get("evidence", []) if e.get("class") in ("A", "B")]
            if len(ab_evidence) < 3:
                errors.append(
                    f"Validated legendary '{skill['id']}' needs ≥3 Class A/B evidence "
                    f"sources (has {len(ab_evidence)})."
                )
    return errors


def compute_stats(graph):
    """Compute and print summary statistics."""
    skills = graph.get("skills", [])
    by_type = defaultdict(int)
    by_level = defaultdict(int)
    by_rarity = defaultdict(int)
    by_status = defaultdict(int)

    for s in skills:
        by_type[s["type"]] += 1
        by_level[s["level"]] += 1
        by_rarity[s["rarity"]] += 1
        by_status[s["status"]] += 1

    # Compute max lineage depth
    children = defaultdict(list)
    parents = defaultdict(list)
    for edge in graph.get("edges", []):
        children[edge["sourceSkillId"]].append(edge["targetSkillId"])
        parents[edge["targetSkillId"]].append(edge["sourceSkillId"])

    skill_ids = {s["id"] for s in skills}
    roots = [sid for sid in skill_ids if not parents.get(sid)]

    max_depth = 0
    def depth_dfs(node, d):
        nonlocal max_depth
        max_depth = max(max_depth, d)
        for child in children.get(node, []):
            depth_dfs(child, d + 1)

    for root in roots:
        depth_dfs(root, 0)

    # Find orphaned composites
    orphaned = []
    for s in skills:
        if s["type"] in ("composite", "legendary") and len(s.get("prerequisites", [])) < 2:
            orphaned.append(s["id"])

    print("\n📊 Graph Statistics")
    print(f"   Total skills: {len(skills)}")
    print(f"   By type: {dict(by_type)}")
    print(f"   By level: {dict(by_level)}")
    print(f"   By rarity: {dict(by_rarity)}")
    print(f"   By status: {dict(by_status)}")
    print(f"   Total edges: {len(graph.get('edges', []))}")
    print(f"   Max lineage depth: {max_depth}")
    print(f"   Root nodes (atomics): {len(roots)}")
    if orphaned:
        print(f"   ⚠ Orphaned composites: {orphaned}")


def main():
    parser = argparse.ArgumentParser(description="Validate the Gaia canonical graph.")
    parser.add_argument("--graph", default=None, help="Path to gaia.json")
    parser.add_argument("--schema-dir", default=None, help="Path to schema directory")
    args = parser.parse_args()

    # Resolve paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graph_path = args.graph or os.path.join(repo_root, "graph", "gaia.json")
    schema_dir = args.schema_dir or os.path.join(repo_root, "schema")

    if not os.path.exists(graph_path):
        print(f"❌ Graph file not found: {graph_path}")
        sys.exit(1)

    print(f"🔍 Validating: {graph_path}")
    graph = load_graph(graph_path)

    all_errors = []

    # 1. Schema validation
    print("   [1/6] Schema validation...")
    all_errors.extend(validate_schema(graph, schema_dir))

    # 2. DAG cycle detection
    print("   [2/6] DAG cycle detection...")
    all_errors.extend(validate_dag(graph))

    # 3. Reference integrity
    print("   [3/6] Reference integrity...")
    all_errors.extend(validate_references(graph))

    # 4. Prerequisite count
    print("   [4/6] Prerequisite count...")
    all_errors.extend(validate_prerequisites_count(graph))

    # 5. Evidence threshold
    print("   [5/6] Evidence thresholds...")
    all_errors.extend(validate_evidence(graph))

    # 6. Legendary constraints
    print("   [6/6] Legendary constraints...")
    all_errors.extend(validate_legendary(graph))

    # Stats
    compute_stats(graph)

    if all_errors:
        print(f"\n❌ {len(all_errors)} validation error(s):")
        for i, err in enumerate(all_errors, 1):
            print(f"   {i}. {err}")
        sys.exit(1)
    else:
        print("\n✅ All validation checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
