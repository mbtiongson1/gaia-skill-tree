#!/usr/bin/env python3
"""Gaia Skill Registry — Canonical Graph Validator.

Validates graph/gaia.json against:
1. JSON Schema validation for all skill nodes and edges.
2. DAG cycle detection (DFS from all root nodes).
3. Reference integrity (every parent ID resolves to an existing node).
4. Evidence threshold by level.
5. Ultimate approval count check (placeholder).
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
import glob
import argparse
from collections import defaultdict

# Optional: jsonschema for full schema validation
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


EVIDENCE_FLOOR = {
    "0": None,       # No evidence required (Basic tier — universal LLM primitives)
    "I": None,       # No evidence required (foundation tier)
    "II": {"C", "B", "A"},
    "III": {"B", "A"},
    "IV": {"B", "A"},
    "V": {"B", "A"},
    "VI": {"A"},
}

MIN_PREREQS = {
    "basic": 0,
    "extra": 2,
    "ultimate": 3,
}


def load_graph(path):
    """Load and parse the canonical graph JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_schema(schema_path):
    """Load a JSON Schema file."""
    with open(schema_path, "r", encoding="utf-8") as f:
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
        if skill["type"] == "basic" and actual > 0:
            errors.append(f"Basic skill '{skill['id']}' must have 0 prerequisites (has {actual}).")
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


def validate_ultimate(graph):
    """Check ultimate-specific constraints."""
    errors = []
    for skill in graph.get("skills", []):
        if skill["type"] != "ultimate":
            continue

        # Ultimate stubs at Level I are allowed without evidence
        if skill["level"] == "I" and skill["status"] == "provisional":
            continue

        # Validated ultimates need 3+ Class A/B evidence
        if skill["status"] == "validated":
            ab_evidence = [e for e in skill.get("evidence", []) if e.get("class") in ("A", "B")]
            if len(ab_evidence) < 3:
                errors.append(
                    f"Validated ultimate '{skill['id']}' needs ≥3 Class A/B evidence "
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
        if s["type"] in ("extra", "ultimate") and len(s.get("prerequisites", [])) < 2:
            orphaned.append(s["id"])

    print("\n📊 Graph Statistics")
    print(f"   Total skills: {len(skills)}")
    print(f"   By type: {dict(by_type)}")
    print(f"   By level: {dict(by_level)}")
    print(f"   By rarity: {dict(by_rarity)}")
    print(f"   By status: {dict(by_status)}")
    print(f"   Total edges: {len(graph.get('edges', []))}")
    print(f"   Max lineage depth: {max_depth}")
    print(f"   Root nodes (basics): {len(roots)}")
    if orphaned:
        print(f"   ⚠ Orphaned extras: {orphaned}")


_NAMED_REQUIRED_FIELDS = [
    "id",
    "name",
    "contributor",
    "origin",
    "genericSkillRef",
    "status",
    "level",
    "description",
]

_NAMED_VALID_LEVELS = {"II", "III", "IV", "V", "VI"}


def _parse_named_frontmatter(text):
    """Parse simple YAML frontmatter from a named skill markdown file.

    Returns a dict of the frontmatter fields, or raises ValueError on malformed
    input. Supports scalars, quoted strings, booleans, block sequences, and one
    level of nested mappings (e.g. links:).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("File does not begin with '---' frontmatter delimiter.")

    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("Frontmatter closing '---' not found.")

    fm_lines = lines[1:end]
    data = {}
    i = 0

    def _coerce(raw):
        stripped = raw.strip().strip('"').strip("'")
        if raw.strip().lower() == "true":
            return True
        if raw.strip().lower() == "false":
            return False
        return stripped

    while i < len(fm_lines):
        line = fm_lines[i]
        if not line.strip():
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue

        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()

        if rest == "":
            # Nested mapping or block sequence follows
            nested_dict = {}
            nested_list = []
            j = i + 1
            while j < len(fm_lines):
                nline = fm_lines[j]
                if not nline.strip():
                    j += 1
                    continue
                if not nline.startswith(" "):
                    break
                stripped = nline.strip()
                if stripped.startswith("- "):
                    nested_list.append(stripped[2:].strip().strip('"').strip("'"))
                    j += 1
                elif ":" in stripped:
                    sk, _, sv = stripped.partition(":")
                    nested_dict[sk.strip()] = _coerce(sv.strip())
                    j += 1
                else:
                    j += 1
            if nested_list:
                data[key] = nested_list
                i = j
            elif nested_dict:
                data[key] = nested_dict
                i = j
            else:
                data[key] = {}
                i += 1
        elif rest.startswith("["):
            inner = rest[1:-1] if rest.endswith("]") else rest[1:]
            if not inner.strip():
                data[key] = []
            else:
                data[key] = [item.strip().strip('"').strip("'") for item in inner.split(",")]
            i += 1
        else:
            data[key] = _coerce(rest)
            i += 1

    return data


def validate_named_skills(graph, named_dir=None, catalog_path=None):
    """Validate all named skill .md files in graph/named/.

    Checks:
      - All required fields are present.
      - level is II or above.
      - genericSkillRef resolves to a skill ID in graph (gaia.json).
      - At most one origin: true per genericSkillRef bucket.
      - status 'named' requires title OR catalogRef (reviewer gate).
      - title/catalogRef requires status 'named' (prevents contributor bypassing).
      - catalogRef (if set) resolves to an item id in real_skill_catalog.json.

    Returns a list of error strings.
    """
    errors = []

    if named_dir is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        named_dir = os.path.join(repo_root, "graph", "named")

    if catalog_path is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        catalog_path = os.path.join(repo_root, "graph", "real_skill_catalog.json")

    if not os.path.isdir(named_dir):
        # Not an error — directory simply doesn't exist yet.
        return errors

    # Load catalog item IDs for catalogRef resolution check
    catalog_ids = set()
    if os.path.isfile(catalog_path):
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog_data = json.load(f)
            catalog_ids = {item["id"] for item in catalog_data.get("items", []) if "id" in item}
        except (OSError, json.JSONDecodeError):
            pass  # Catalog missing or malformed — skip resolution checks

    valid_ids = {s["id"] for s in graph.get("skills", [])}

    pattern = os.path.join(named_dir, "**", "*.md")
    md_files = sorted(glob.glob(pattern, recursive=True))
    # Exclude any generated index file that might be .md (unlikely but safe)
    md_files = [f for f in md_files if not f.endswith("index.json")]

    buckets = defaultdict(list)  # genericSkillRef -> list of parsed fm dicts

    for fp in md_files:
        rel = os.path.relpath(fp)
        try:
            with open(fp, "r", encoding="utf-8") as f:
                text = f.read()
            fm = _parse_named_frontmatter(text)
        except (OSError, ValueError) as exc:
            errors.append(f"Named skill {rel}: cannot parse — {exc}")
            continue

        # Required fields
        missing = [field for field in _NAMED_REQUIRED_FIELDS
                   if field not in fm or fm[field] is None or fm[field] == ""]
        if missing:
            errors.append(
                f"Named skill {rel}: missing required field(s): {', '.join(missing)}"
            )

        # Level >= II
        level = fm.get("level", "")
        if level not in _NAMED_VALID_LEVELS:
            errors.append(
                f"Named skill {rel}: 'level' must be II or above (got '{level}')."
            )

        # genericSkillRef resolves
        ref = fm.get("genericSkillRef", "")
        if ref and ref not in valid_ids:
            errors.append(
                f"Named skill {rel}: 'genericSkillRef' value '{ref}' "
                f"does not match any skill ID in gaia.json."
            )

        # Reviewer gate: status 'named' requires title OR catalogRef
        status = fm.get("status", "")
        has_title = bool(fm.get("title", "").strip() if isinstance(fm.get("title"), str) else fm.get("title"))
        has_catalog_ref = bool(fm.get("catalogRef", "").strip() if isinstance(fm.get("catalogRef"), str) else fm.get("catalogRef"))
        if status == "named" and not has_title and not has_catalog_ref:
            errors.append(
                f"Named skill {rel}: status 'named' requires a reviewer-assigned "
                f"'title' or 'catalogRef'. Submit with status: awakened first."
            )
        # Inverse: title/catalogRef are only valid on named status
        if (has_title or has_catalog_ref) and status != "named":
            errors.append(
                f"Named skill {rel}: 'title' and 'catalogRef' are only valid on "
                f"status: named skills (got '{status}'). These fields are reviewer-only."
            )
        # catalogRef must resolve to a known catalog item
        catalog_ref = fm.get("catalogRef", "")
        if catalog_ref and catalog_ids and catalog_ref not in catalog_ids:
            errors.append(
                f"Named skill {rel}: 'catalogRef' value '{catalog_ref}' does not "
                f"match any item id in real_skill_catalog.json."
            )

        if not missing and level in _NAMED_VALID_LEVELS:
            buckets[ref].append(fm)

    # Origin uniqueness per bucket
    for ref, entries in buckets.items():
        origins = [e for e in entries if e.get("origin") is True]
        if len(origins) > 1:
            ids = [e.get("id", "?") for e in origins]
            errors.append(
                f"Named skills: genericSkillRef '{ref}' has more than one "
                f"origin:true — {ids}"
            )

    return errors


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
    print("   [1/7] Schema validation...")
    all_errors.extend(validate_schema(graph, schema_dir))

    # 2. DAG cycle detection
    print("   [2/7] DAG cycle detection...")
    all_errors.extend(validate_dag(graph))

    # 3. Reference integrity
    print("   [3/7] Reference integrity...")
    all_errors.extend(validate_references(graph))

    # 4. Prerequisite count
    print("   [4/7] Prerequisite count...")
    all_errors.extend(validate_prerequisites_count(graph))

    # 5. Evidence threshold
    print("   [5/7] Evidence thresholds...")
    all_errors.extend(validate_evidence(graph))

    # 6. Ultimate constraints
    print("   [6/7] Ultimate constraints...")
    all_errors.extend(validate_ultimate(graph))

    # 7. Named skills validation (includes reviewer gate + catalog cross-refs)
    print("   [7/7] Named skills validation...")
    all_errors.extend(validate_named_skills(graph))

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
