import json
import os
import datetime
import sys
import importlib.util


def _run_generate_named_index():
    """Invoke generateNamedIndex as a module to produce registry/named-skills.json."""
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    module_path = os.path.join(scripts_dir, "generateNamedIndex.py")
    if not os.path.isfile(module_path):
        print("Warning: generateNamedIndex.py not found — skipping named index.")
        return
    spec = importlib.util.spec_from_file_location("generateNamedIndex", module_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        repo_root = os.path.dirname(scripts_dir)
        named_dir = os.path.join(repo_root, "registry", "named")
        graph_path = os.path.join(repo_root, "registry", "gaia.json")
        output_path = os.path.join(repo_root, "registry", "named-skills.json")
        if os.path.isdir(named_dir) and os.path.isfile(graph_path):
            with open(graph_path, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
            ts = gdata.get("generatedAt", "")
            today = (ts.split("T")[0] if "T" in ts else ts) if ts else datetime.date.today().isoformat()
            named_skills = mod.load_named_skills(named_dir)
            valid_ids = {s["id"] for s in gdata.get("skills", [])}
            errors, buckets, awaiting_classification, by_contributor = mod.validate_and_group(named_skills, valid_ids)
            if errors:
                print(f"Warning: named skill validation errors ({len(errors)}):")
                for err in errors:
                    print(f"  {err}")
            else:
                mod.write_index(buckets, awaiting_classification, by_contributor, output_path, today)
                total = sum(len(v) for v in buckets.values())
                print(f"Generated named index: {total} skill(s) across "
                      f"{len(buckets)} bucket(s).")
    except Exception as exc:
        print(f"Warning: could not generate named index — {exc}")


try:
    from generateRealSkills import generate_catalog_pages
except ModuleNotFoundError:
    from scripts.generateRealSkills import generate_catalog_pages


def get_type_label(meta, skill_type):
    return meta.get("typeLabels", {}).get(skill_type, skill_type.capitalize())


def get_level_label(meta, level):
    return str(level)


def get_rarity_label(meta, rarity):
    return meta.get("rarityLabels", {}).get(rarity, rarity.capitalize())


def get_tier_label(meta, level):
    return meta.get("levelLabels", {}).get(str(level), str(level))


def get_tier_symbol(skill_type):
    return {"basic": "○", "extra": "◇", "ultimate": "◆"}.get(skill_type, "·")


def _build_skill_display(skill_id, skill_type, named_map=None):
    """Return canonical display string for a skill.

    Basic  -> /slug (no tier prefix)
    Extra  -> Extra Skill: /slug  (or Extra Skill: contributor/name)
    Ultimate (claimed)   -> Ultimate Skill: contributor/name
    Ultimate (unclaimed) -> Ultimate Skill: /slug [Unclaimed ✦]
    """
    named_id = (named_map or {}).get(skill_id)
    if skill_type == "ultimate":
        if named_id:
            return f"Ultimate Skill: {named_id}"
        return f"Ultimate Skill: /{skill_id} [Unclaimed ✦]"
    if skill_type == "extra":
        if named_id:
            return f"Extra Skill: {named_id}"
        return f"Extra Skill: /{skill_id}"
    return named_id if named_id else f"/{skill_id}"

def _sorted_ultimates(skills):
    order = {"VI": 0, "V": 1, "IV": 2, "III": 3, "II": 4, "I": 5, "0": 6}
    return sorted(
        [s for s in skills if s.get("type") == "ultimate"],
        key=lambda s: (order.get(s.get("level"), 9), s.get("name", ""))
    )


def _render_subtree(root_id, skill_map, meta, prefix, is_last, seen,
                    unlocked_ids=None, user_id=None, named_map=None):
    skill = skill_map.get(root_id)
    if not skill:
        return []

    connector = "└─" if is_last else "├─"
    symbol = get_tier_symbol(skill.get("type"))
    name = skill.get("name")
    level = skill.get("level")
    level_label = get_level_label(meta, level)

    skill_type = skill.get("type", "basic")
    display = _build_skill_display(root_id, skill_type, named_map)

    already_seen = root_id in seen
    back_ref = "  (↑ see above)" if already_seen else ""

    check = ""
    if unlocked_ids is not None:
        check = "✓ " if root_id in unlocked_ids else "· "

    line = f"{prefix}{connector} {check}{symbol} {display}  [{level_label}]{back_ref}"
    lines = [line]

    if already_seen:
        return lines

    seen.add(root_id)

    if not skill.get("prerequisites"):
        return lines
    child_prefix = prefix + ("   " if is_last else "│  ")
    prereq_ids = skill.get("prerequisites", [])
    for i, prereq_id in enumerate(prereq_ids):
        is_last_child = (i == len(prereq_ids) - 1)
        lines.extend(_render_subtree(
            prereq_id, skill_map, meta, child_prefix, is_last_child, seen,
            unlocked_ids=unlocked_ids, user_id=user_id, named_map=named_map,
        ))

    return lines


def main():
    with open("registry/gaia.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    version = data.get("version", "0.1.0")
    timestamp = data.get("generatedAt", datetime.datetime.now().isoformat() + "Z")
    meta = data.get("meta", {})
    skills = data.get("skills", [])

    skills.sort(key=lambda x: x["id"])

    # Build named_map early so skill pages and registry can use it
    _run_generate_named_index()
    named_map = {}
    named_index_path = os.path.join("registry", "named-skills.json")
    if os.path.isfile(named_index_path):
        with open(named_index_path, "r", encoding="utf-8") as nf:
            nidx = json.load(nf)
        for _sid, entries in nidx.get("buckets", {}).items():
            if entries:
                origin = next((e for e in entries if e.get("origin")), entries[0])
                named_map[_sid] = origin.get("id", "")

    os.makedirs("registry/skills/basic", exist_ok=True)
    os.makedirs("registry/skills/extra", exist_ok=True)
    os.makedirs("registry/skills/ultimate", exist_ok=True)

    skill_map = {s["id"]: s for s in skills}
    date_str = timestamp.split("T")[0] if "T" in timestamp else timestamp

    for skill in skills:
        skill_type = skill.get("type", "basic")
        skill_id = skill.get("id")
        skill_name = skill.get("name")
        level = skill.get("level")
        rarity = skill.get("rarity")
        file_path = f"registry/skills/{skill_type}/{skill_id}.md"

        type_label = get_type_label(meta, skill_type)
        level_label = get_level_label(meta, level)
        tier_label = get_tier_label(meta, level)

        with open(file_path, "w", encoding="utf-8") as f:
            page_display = _build_skill_display(skill_id, skill_type, named_map)
            f.write(f"# {page_display}  [{level_label} · {tier_label}]\n")
            f.write(f"**ID:** {skill_id}  \n")
            f.write(f"**Type:** {type_label or 'Basic Skill'}  \n")
            f.write(f"**Level:** {level_label}  \n")
            f.write(f"**Tier:** {tier_label}  \n")
            f.write(f"**Skill Call:** `/{skill_id}`\n\n")
            f.write("---\n\n")

            f.write("## Description\n")
            f.write(f"{skill.get('description', '')}\n\n")

            f.write("## Prerequisites\n")
            prereqs = skill.get("prerequisites", [])
            if not prereqs:
                f.write("_None._\n\n")
            else:
                for prereq_id in prereqs:
                    prereq = skill_map.get(prereq_id)
                    if prereq:
                        prereq_type = prereq.get("type", "basic")
                        f.write(f"- [{prereq.get('name')}](../{prereq_type}/{prereq_id}.md)\n")
                    else:
                        f.write(f"- {prereq_id}\n")
                f.write("\n")

            f.write("## Unlocks\n")
            unlocks = skill.get("derivatives", [])
            if not unlocks:
                f.write("_None._\n\n")
            else:
                for unlock_id in unlocks:
                    unlock = skill_map.get(unlock_id)
                    if unlock:
                        unlock_type = unlock.get("type", "basic")
                        f.write(f"- [{unlock.get('name')}](../{unlock_type}/{unlock_id}.md)\n")
                    else:
                        f.write(f"- {unlock_id}\n")
                f.write("\n")

            if skill_type in ["extra", "ultimate"]:
                f.write("## Fusion Condition\n")
                conditions = skill.get("conditions", "")
                if not conditions:
                    f.write("_None specified._\n\n")
                else:
                    f.write(f"{conditions}\n\n")

            f.write("## Evidence\n")
            evidence = skill.get("evidence", [])
            if not evidence:
                f.write("_None._\n\n")
            else:
                f.write("| Class | Source | Evaluator | Date |\n")
                f.write("|---|---|---|---|\n")
                for ev in evidence:
                    f.write(f"| {ev.get('class', '')} | {ev.get('source', '')} | {ev.get('evaluator', '')} | {ev.get('date', '')} |\n")
                f.write("\n")

            f.write("## Known Agents\n")
            agents = skill.get("knownAgents", [])
            if not agents:
                f.write("_None verified yet._\n\n")
            else:
                for agent in agents:
                    f.write(f"- {agent}\n")
                f.write("\n")

            f.write("---\n")
            # f.write(f"*Generated from gaia.json v{version} on {date_str}. Do not edit directly.*\n")

    # generate registry.md
    with open("registry/registry.md", "w", encoding="utf-8") as f:
        f.write("# Gaia Skill Registry\n\n")
        f.write("| Name | Class | Rank | Tier | Skill Call |\n")
        f.write("|---|---|---|---|---|\n")

        # collect orphaned basic IDs for the pure section
        all_prereq_ids = set()
        for skill in skills:
            for pid in skill.get("prerequisites", []):
                all_prereq_ids.add(pid)
        orphan_ids = {
            s["id"] for s in skills
            if s.get("type") == "basic"
            and s["id"] not in all_prereq_ids
            and not s.get("prerequisites")
        }

        for skill in skills:
            if skill["id"] in orphan_ids:
                continue
            skill_type = skill.get("type", "basic")
            symbol = get_tier_symbol(skill_type)
            type_label = get_type_label(meta, skill_type)
            level = skill.get("level")
            level_label = get_level_label(meta, level)
            tier_label = get_tier_label(meta, level)
            reg_display = _build_skill_display(skill.get('id'), skill_type, named_map)
            name_display = f"{symbol} {reg_display}"
            skill_call = f"`/{skill.get('id')}`"
            f.write(f"| {name_display} | {type_label or 'Basic Skill'} | {level_label} | {tier_label} | {skill_call} |\n")

        f.write("\n")
        f.write("## Pure / Undeveloped\n\n")
        f.write("*Atomic skills with no connections to the upgrade graph — no prerequisites and not referenced as a component of any other skill.*\n\n")
        f.write("| Name | Class | Rank | Tier | Skill Call |\n")
        f.write("|---|---|---|---|---|\n")
        for skill in skills:
            if skill["id"] not in orphan_ids:
                continue
            level = skill.get("level")
            level_label = get_level_label(meta, level)
            tier_label = get_tier_label(meta, level)
            name_display = f"○ {skill.get('name')}"
            skill_call = f"`/{skill.get('id')}`"
            f.write(f"| {name_display} | Intrinsic Skill | {level_label} | {tier_label} | {skill_call} |\n")

        f.write("\n")

        # Unclaimed Ultimates section
        unclaimed = [s for s in skills if s.get("type") == "ultimate" and s["id"] not in named_map]
        if unclaimed:
            f.write("## Ultimate Skills Awaiting Name\n\n")
            f.write(
                "*These Ultimate skills have no named implementation yet. "
                "The first contributor to submit a valid named implementation "
                "claims the title slot.  Submit with `gaia push` and open a PR.*\n\n"
            )
            f.write("| Skill Call | Level | Prerequisites |\n")
            f.write("|---|---|---|\n")
            for s in unclaimed:
                prereq_names = ", ".join(f"`/{p}`" for p in s.get("prerequisites", []))
                level_lbl = get_tier_label(meta, s.get("level"))
                f.write(f"| `/{s['id']}` | {level_lbl} | {prereq_names} |\n")
            f.write("\n")

        # f.write(f"*Generated from gaia.json v{version}.*\n")

    # generate combinations.md
    with open("registry/combinations.md", "w", encoding="utf-8") as f:
        f.write("# Combinations\n\n")
        f.write("| Skill | Class | Prerequisites | Level Floor | Conditions |\n")
        f.write("|---|---|---|---|---|\n")
        for skill in skills:
            if skill.get("type") in ["extra", "ultimate"]:
                skill_type = skill.get("type")
                symbol = get_tier_symbol(skill_type)
                type_label = get_type_label(meta, skill_type)
                level_label = get_level_label(meta, skill.get("level"))
                prereqs = [skill_map.get(pid, {}).get("name", pid) for pid in skill.get("prerequisites", [])]
                prereq_str = ", ".join(prereqs)
                combo_display = _build_skill_display(skill.get('id'), skill_type, named_map)
                name_display = f"{symbol} {combo_display}"
                f.write(f"| {name_display} | {type_label} | {prereq_str} | {level_label} | {skill.get('conditions', '')} |\n")
        # f.write(f"\n*Generated from gaia.json v{version}.*\n")

    # generate tree.md
    _generate_tree(skills, skill_map, meta, version, date_str, named_map)

    catalog_path = 'registry/real-skills.json'
    if os.path.isfile(catalog_path):
        with open(catalog_path, 'r', encoding='utf-8') as cf:
            generate_catalog_pages(json.load(cf))

    # generate user skill tree markdown projections
    users_dir = "skill-trees"
    legendaries = _sorted_ultimates(skills)
    if os.path.isdir(users_dir):
        for username in sorted(os.listdir(users_dir)):
            user_dir = os.path.join(users_dir, username)
            tree_path = os.path.join(user_dir, "skill-tree.json")
            if not os.path.isfile(tree_path):
                continue
            with open(tree_path, "r", encoding="utf-8") as tf:
                tree = json.load(tf)

            md_path = os.path.join(user_dir, "skill-tree.md")
            with open(md_path, "w", encoding="utf-8") as f:
                user_id = tree.get("userId", username)
                f.write(f"# Skill Tree — {user_id}\n")
                f.write(f"**Last Updated:** {tree.get('updatedAt', 'unknown')}  \n")
                stats = tree.get("stats", {})
                f.write(f"**Total Skills Unlocked:** {stats.get('totalUnlocked', 0)}  \n")
                highest_level = stats.get('highestLevel', stats.get('highestRarity', ''))
                f.write(f"**Highest Tier:** {get_tier_label(meta, highest_level)}  \n")
                f.write(f"**Deepest Lineage:** {stats.get('deepestLineage', 0)}\n\n")
                f.write("---\n\n")

                f.write("## Unlocked Skills\n\n")
                unlocked = tree.get("unlockedSkills", [])
                if unlocked:
                    f.write("| Skill | Class | Rank | Tier | Unlocked In | Date |\n")
                    f.write("|---|---|---|---|---|---|\n")
                    for us in unlocked:
                        sid = us.get("skillId", "")
                        sk = skill_map.get(sid, {})
                        sk_type = sk.get("type", "basic")
                        symbol = get_tier_symbol(sk_type)
                        type_label = get_type_label(meta, sk_type)
                        level = us.get("level", sk.get("level", ""))
                        level_label = get_level_label(meta, level)
                        tier_label = get_tier_label(meta, level)
                        name_display = f"{symbol} {sk.get('name', sid)}"
                        f.write(f"| {name_display} | {type_label} | "
                                f"{level_label} | {tier_label} | "
                                f"{us.get('unlockedIn', '')} | {us.get('unlockedAt', '')} |\n")
                else:
                    f.write("_No skills unlocked yet._\n")
                f.write("\n---\n\n")

                # Upgrade path tree with unlock markers
                f.write("## Upgrade Path\n\n")
                f.write("```\n")
                unlocked_ids = {us.get("skillId") for us in unlocked}
                for legendary in legendaries:
                    lid = legendary.get("id")
                    lname = legendary.get("name")
                    llevel = legendary.get("level")
                    prereq_ids = legendary.get("prerequisites", [])

                    level_label = get_level_label(meta, llevel)
                    display = _build_skill_display(lid, "ultimate", named_map)

                    check = "✓ " if lid in unlocked_ids else "· "
                    f.write(f"{check}◆ {display}  [{level_label}]\n")

                    seen = {lid}
                    for i, prereq_id in enumerate(prereq_ids):
                        is_last = (i == len(prereq_ids) - 1)
                        for sl in _render_subtree(
                            prereq_id, skill_map, meta, "  ", is_last, seen,
                            unlocked_ids=unlocked_ids, user_id=user_id,
                            named_map=named_map,
                        ):
                            f.write(sl + "\n")
                    f.write("\n")
                f.write("```\n\n")

                f.write("## Pending Combinations\n\n")
                pending = tree.get("pendingCombinations", [])
                if pending:
                    for pc in pending:
                        candidate = pc.get("candidateResult", "")
                        prereqs_list = ", ".join(f"`{s}`" for s in pc.get("detectedSkills", []))
                        level_floor = get_level_label(meta, pc.get("levelFloor", ""))
                        f.write(f"> **{candidate}** — combine {prereqs_list}  \n")
                        f.write(f"> Level floor: {level_floor}  \n")
                        f.write(f"> Run `gaia fuse {candidate}` to confirm.\n\n")
                else:
                    f.write("_No pending combinations._\n\n")

                f.write("---\n")
                f.write("*Generated from skill-tree.json. Do not edit directly.*\n")

    print(f"Generated projections for {len(skills)} skills.")


def _generate_tree(skills, skill_map, meta, version, date_str, named_map=None):
    legendaries = _sorted_ultimates(skills)

    # compute orphaned atomics
    all_prereq_ids = set()
    for s in skills:
        for pid in s.get("prerequisites", []):
            all_prereq_ids.add(pid)
    pure_skills = sorted(
        [s for s in skills
         if s.get("type") == "basic"
         and s["id"] not in all_prereq_ids
         and not s.get("prerequisites")],
        key=lambda s: s.get("id", "")
    )

    lines = []
    lines.append("# Gaia Skill Tree")
    lines.append("")
    lines.append("```")
    lines.append(f"GAIA SKILL TREE  v{version}  ·  generated {date_str}")
    lines.append("═" * 70)
    lines.append("Upgrade paths — each legendary shows its full prerequisite chain.")
    lines.append("Shared prerequisites marked (↑ see above) on second occurrence.")
    lines.append("═" * 70)
    lines.append("")

    for legendary in legendaries:
        lid = legendary.get("id")
        lname = legendary.get("name")
        llevel = legendary.get("level")
        level_label = get_level_label(meta, llevel)
        prereq_ids = legendary.get("prerequisites", [])

        display = _build_skill_display(lid, "ultimate", named_map)

        lines.append(f"◆ {display}  [{level_label}]")
        lines.append("─" * 65)

        seen = {lid}
        for i, prereq_id in enumerate(prereq_ids):
            is_last = (i == len(prereq_ids) - 1)
            lines.extend(_render_subtree(prereq_id, skill_map, meta, "  ", is_last, seen,
                                         named_map=named_map))

        lines.append("")

    if pure_skills:
        lines.append("═" * 70)
        lines.append("Pure / Undeveloped — basic skills not yet wired into any upgrade path.")
        lines.append("═" * 70)
        lines.append("")
        for ps in pure_skills:
            pid = ps.get("id")
            level_label = get_level_label(meta, ps.get("level"))
            tier_label = get_tier_label(meta, ps.get("level"))
            named_id = (named_map or {}).get(pid)
            display = f"{named_id} - {ps.get('name')}" if named_id else f"/{pid}"
            lines.append(f"  ○ {display}  [{level_label} · {tier_label}]")
        lines.append("")

    lines.append("```")
    lines.append("")
    lines.append(f"*Generated from gaia.json on {date_str}. Do not edit directly.*")

    os.makedirs("generated-output", exist_ok=True)
    with open("generated-output/tree.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
