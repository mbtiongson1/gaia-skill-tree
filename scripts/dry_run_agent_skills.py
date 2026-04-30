#!/usr/bin/env python3
"""
Dry-run report: parse a markdown table of agent slash commands,
classify real vs procedural entries, and show what would be proposed
for the Gaia skill tree. No files are written.
"""
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from gaia_cli.resolver import load_canonical_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
NAMED_INDEX = REPO_ROOT / "graph" / "named" / "index.json"

# Procedural URL pattern — auto-generated entries all share this shape
PROCEDURAL_URL = re.compile(
    r"https?://github\.com/[a-z]+/agent-skills/tree/main/skills/[^/]+/SKILL\.md"
)
MATCH_THRESHOLD = 0.55


def load_named_ids() -> set[str]:
    """Return the set of all known named skill IDs (contributor/skill-name)."""
    import json
    if not NAMED_INDEX.exists():
        return set()
    with open(NAMED_INDEX) as f:
        data = json.load(f)
    return {
        e["id"]
        for entries in data.get("buckets", {}).values()
        for e in entries
    }


def parse_rows(md_path: str):
    rows = []
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith("| **"):
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 4:
                continue
            owner = parts[0].strip("*").strip()
            cmd = parts[1].strip("`").strip()
            desc = parts[2].strip()
            url_match = re.search(r"https?://\S+\)", parts[3])
            url = url_match.group(0).rstrip(")") if url_match else ""
            rows.append({"owner": owner, "cmd": cmd, "desc": desc, "url": url})
    return rows


def is_real(url: str) -> bool:
    return bool(url) and not PROCEDURAL_URL.match(url)


def find_best_match(cmd_id: str, gaia_ids: set[str]) -> tuple[str | None, float]:
    best_id, best_score = None, 0.0
    for gid in gaia_ids:
        s = SequenceMatcher(None, cmd_id, gid).ratio()
        if s > best_score:
            best_id, best_score = gid, s
    return best_id, best_score


def contributor_slug(owner: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", owner.lower()).strip("-")


def skill_name(cmd: str) -> str:
    return cmd.lstrip("/")


def main():
    if len(sys.argv) < 2:
        print("Usage: python dry_run_agent_skills.py <path/to/skills.md>")
        sys.exit(1)

    md_path = sys.argv[1]
    gaia_ids = load_canonical_skills(str(REPO_ROOT / "graph" / "gaia.json"))
    named_ids = load_named_ids()

    rows = parse_rows(md_path)
    real = [r for r in rows if is_real(r["url"])]

    print("=" * 60)
    print("DRY RUN: Agent Skills Intake")
    print("=" * 60)
    print(f"Total rows parsed:      {len(rows):,}")
    print(f"Real entries found:     {len(real)}")
    print(f"Procedural (skipped):   {len(rows) - len(real):,}")
    print()

    first_cmd_for_generic: dict[str, str] = {}  # generic_id -> first cmd that claimed it
    new_generics: list[str] = []
    named_proposals: list[dict] = []

    print("-" * 60)
    print("REAL SKILL PROPOSALS")
    print("-" * 60)

    for i, r in enumerate(real, 1):
        cmd_id = skill_name(r["cmd"])
        contrib = contributor_slug(r["owner"])
        named_path = f"graph/named/{contrib}/{cmd_id}.md"
        already_named = f"{contrib}/{cmd_id}" in named_ids

        if cmd_id in gaia_ids:
            generic_id = cmd_id
            generic_status = "EXISTS (exact match)"
            is_new = False
        else:
            best_id, score = find_best_match(cmd_id, gaia_ids)
            if score >= MATCH_THRESHOLD:
                generic_id = best_id
                generic_status = f"EXISTS -> maps to '{best_id}' (score {score:.2f})"
                is_new = False
            else:
                generic_id = cmd_id
                generic_status = f"NEW -- not in gaia.json (closest: '{best_id}' score {score:.2f})"
                is_new = True

        is_dup = generic_id in first_cmd_for_generic
        if not is_dup:
            first_cmd_for_generic[generic_id] = r["cmd"]
            if is_new:
                new_generics.append(generic_id)

        named_status = "ALREADY EXISTS" if already_named else "WOULD CREATE"
        dup_suffix = f"  ** DUPE of {first_cmd_for_generic[generic_id]}" if is_dup else ""

        print(f"\n{i}. {r['cmd']}  ({r['owner']})")
        print(f"   Source : {r['url']}")
        print(f"   Desc   : {r['desc'][:90]}")
        print(f"   Generic: {generic_id}  [{generic_status}]")
        print(f"   Named  : {named_path}  [{named_status}]{dup_suffix}")

        named_proposals.append({
            "cmd": r["cmd"],
            "owner": r["owner"],
            "url": r["url"],
            "desc": r["desc"],
            "generic_id": generic_id,
            "is_new_generic": is_new,
            "named_path": named_path,
            "already_named": already_named,
        })

    generic_counts = Counter(p["generic_id"] for p in named_proposals)

    print()
    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"Named skill files to create : {sum(1 for p in named_proposals if not p['already_named'])}")
    print(f"Named skills already exist  : {sum(1 for p in named_proposals if p['already_named'])}")
    print(f"New generic skills needed   : {len(new_generics)}")
    for ng in new_generics:
        print(f"  + {ng}")
    print(f"Existing generics reused    : {len(named_proposals) - len(new_generics)}")
    dupes = [p for p in named_proposals if generic_counts[p["generic_id"]] > 1]
    if dupes:
        print(f"Duplicate generic mappings  : {len(dupes)}")
        for d in dupes:
            print(f"  {d['cmd']} -> generic '{d['generic_id']}' claimed by multiple entries")
    print()
    print("No files were written. Approve the above to proceed.")


if __name__ == "__main__":
    main()
