#!/usr/bin/env python3
"""
Dry-run report: parse a markdown table of agent slash commands,
classify real vs procedural entries, and show what would be proposed
for the Gaia skill tree. No files are written.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAIA_JSON = REPO_ROOT / "graph" / "gaia.json"
NAMED_INDEX = REPO_ROOT / "graph" / "named" / "index.json"

# Procedural URL pattern — auto-generated entries all share this shape
PROCEDURAL_URL = re.compile(
    r"https?://github\.com/[a-z]+/agent-skills/tree/main/skills/[^/]+/SKILL\.md"
)


def load_gaia_skills():
    with open(GAIA_JSON) as f:
        graph = json.load(f)
    return {s["id"] for s in graph["skills"]}


def load_named_index():
    if not NAMED_INDEX.exists():
        return {}
    with open(NAMED_INDEX) as f:
        data = json.load(f)
    return data.get("buckets", {})


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


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_best_match(cmd_id: str, gaia_ids: set[str]):
    """Return (best_id, score) for the closest existing skill, or (None, 0)."""
    best_id, best_score = None, 0.0
    for gid in gaia_ids:
        s = similarity(cmd_id, gid)
        if s > best_score:
            best_id, best_score = gid, s
    return best_id, best_score


def contributor_slug(owner: str) -> str:
    """Normalize owner name to a filesystem-safe slug."""
    slug = owner.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def skill_name(cmd: str) -> str:
    """Strip leading slash."""
    return cmd.lstrip("/")


def main():
    if len(sys.argv) < 2:
        print("Usage: python dry_run_agent_skills.py <path/to/10000_Agent_Slash_Skills.md>")
        sys.exit(1)

    md_path = sys.argv[1]
    gaia_ids = load_gaia_skills()
    named_buckets = load_named_index()

    rows = parse_rows(md_path)
    real = [r for r in rows if is_real(r["url"])]
    procedural_count = len(rows) - len(real)

    print("=" * 60)
    print("DRY RUN: Agent Skills Intake")
    print("=" * 60)
    print(f"Total rows parsed:      {len(rows):,}")
    print(f"Real entries found:     {len(real)}")
    print(f"Procedural (skipped):   {procedural_count:,}")
    print()

    seen_generics: dict[str, str] = {}  # skill_id → first cmd that proposed it
    new_generics: list[str] = []
    named_proposals: list[dict] = []
    MATCH_THRESHOLD = 0.55

    print("-" * 60)
    print("REAL SKILL PROPOSALS")
    print("-" * 60)

    for i, r in enumerate(real, 1):
        cmd_id = skill_name(r["cmd"])
        contrib = contributor_slug(r["owner"])
        named_path = f"graph/named/{contrib}/{cmd_id}.md"
        already_named = contrib in named_buckets and any(
            e.get("id") == f"{contrib}/{cmd_id}"
            for e in named_buckets.get(contrib, [])
        )

        # Check exact match first
        if cmd_id in gaia_ids:
            generic_id = cmd_id
            generic_status = "EXISTS (exact match)"
            is_new = False
        else:
            best_id, score = find_best_match(cmd_id, gaia_ids)
            if score >= MATCH_THRESHOLD:
                generic_id = best_id
                generic_status = "EXISTS -> maps to '{}' (score {:.2f})".format(best_id, score)
                is_new = False
            else:
                generic_id = cmd_id
                generic_status = "NEW -- not in gaia.json (closest: '{}' score {:.2f})".format(best_id, score)
                is_new = True

        if is_new and generic_id not in seen_generics:
            new_generics.append(generic_id)
        is_dup = generic_id in seen_generics
        if not is_dup:
            seen_generics[generic_id] = r["cmd"]

        named_status = "ALREADY EXISTS" if already_named else "WOULD CREATE"
        dup_suffix = "  ** DUPE: '{}' already maps here".format(seen_generics[generic_id]) if is_dup else ""

        print("\n{}. {}  ({})".format(i, r["cmd"], r["owner"]))
        print("   Source : {}".format(r["url"]))
        print("   Desc   : {}".format(r["desc"][:90]))
        print("   Generic: {}  [{}]".format(generic_id, generic_status))
        print("   Named  : {}  [{}]{}".format(named_path, named_status, dup_suffix))

        named_proposals.append({
            "cmd": r["cmd"],
            "cmd_id": cmd_id,
            "owner": r["owner"],
            "contrib": contrib,
            "url": r["url"],
            "desc": r["desc"],
            "generic_id": generic_id,
            "is_new_generic": is_new,
            "named_path": named_path,
            "already_named": already_named,
        })

    print()
    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"Named skill files to create : {sum(1 for p in named_proposals if not p['already_named'])}")
    print(f"Named skills already exist  : {sum(1 for p in named_proposals if p['already_named'])}")
    print(f"New generic skills needed   : {len(new_generics)}")
    if new_generics:
        for ng in new_generics:
            print(f"  + {ng}")
    print(f"Existing generics reused    : {len(named_proposals) - len(new_generics)}")
    dupes = [p for p in named_proposals if p["generic_id"] in seen_generics and
             seen_generics[p["generic_id"]] != p["cmd"]]
    if dupes:
        print(f"Duplicate generic mappings  : {len(dupes)}")
        for d in dupes:
            print("  {} -> same generic as another entry".format(d["cmd"]))
    print()
    print("No files were written. Approve the above to proceed.")


if __name__ == "__main__":
    main()
