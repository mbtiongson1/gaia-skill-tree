import json
import os
import datetime
import sys
import importlib.util


def _run_generate_named_index():
    """Invoke generateNamedIndex as a module to produce graph/named/index.json."""
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
        named_dir = os.path.join(repo_root, "graph", "named")
        graph_path = os.path.join(repo_root, "graph", "gaia.json")
        output_path = os.path.join(named_dir, "index.json")
        if os.path.isdir(named_dir) and os.path.isfile(graph_path):
            with open(graph_path, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
            ts = gdata.get("generatedAt", "")
            today = (ts.split("T")[0] if "T" in ts else ts) if ts else datetime.date.today().isoformat()
            named_skills = mod.load_named_skills(named_dir)
            valid_ids = {s["id"] for s in gdata.get("skills", [])}
            errors, buckets = mod.validate_and_group(named_skills, valid_ids)
            if errors:
                print(f"Warning: named skill validation errors ({len(errors)}):")
                for err in errors:
                    print(f"  {err}")
            else:
                mod.write_index(buckets, output_path, today)
                total = sum(len(v) for v in buckets.values())
                print(f"Generated named index: {total} skill(s) across "
                      f"{len(buckets)} bucket(s).")
    except Exception as exc:
        print(f"Warning: could not generate named index — {exc}")



def get_type_label(meta, skill_type):
    return meta.get("typeLabels", {}).get(skill_type, skill_type.capitalize())


def get_level_label(meta, level):
    name = meta.get("levelLabels", {}).get(level, level)
    return f"{level} · {name}"


def get_rarity_label(meta, rarity):
    return meta.get("rarityLabels", {}).get(rarity, rarity.capitalize())


def get_tier_symbol(skill_type):
    return {"atomic": "○", "composite": "◇", "legendary": "◆"}.get(skill_type, "·")


def _sorted_legendaries(skills):
    order = {"VI": 0, "V": 1, "IV": 2, "III": 3, "II": 4, "I": 5, "0": 6}
    return sorted(
        [s for s in skills if s.get("type") == "legendary"],
        key=lambda s: (order.get(s.get("level"), 9), s.get("name", ""))
    )


def _prereq_inline(skill, skill_map):
    prereq_ids = skill.get("prerequisites", [])
    if not prereq_ids or skill.get("type") not in ("composite", "legendary"):
        return ""
    names = [skill_map.get(pid, {}).get("name", pid) for pid in prereq_ids]
    short = [n.split(":")[-1].strip() if ":" in n else n for n in names]
    return "  ← " + " · ".join(short)


def _render_subtree(root_id, skill_map, meta, prefix, is_last, seen,
                    unlocked_ids=None, user_id=None):
    skill = skill_map.get(root_id)
    if not skill:
        return []

    connector = "└─" if is_last else "├─"
    symbol = get_tier_symbol(skill.get("type"))
    name = skill.get("name")
    level = skill.get("level")
    level_label = get_level_label(meta, level)

    if level == "VI" and user_id and unlocked_ids is not None and root_id in unlocked_ids:
        level_label = f"VI · {user_id} · Transcendent"

    inline = _prereq_inline(skill, skill_map)
    already_seen = root_id in seen
    back_ref = "  (↑ see above)" if already_seen else ""

    check = ""
    if unlocked_ids is not None:
        check = "✓ " if root_id in unlocked_ids else "· "

    line = f"{prefix}{connector} {check}{symbol} {name}  [{level_label}]{inline}{back_ref}"
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
            unlocked_ids=unlocked_ids, user_id=user_id,
        ))

    return lines


def main():
    with open("graph/gaia.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    version = data.get("version", "0.1.0")
    timestamp = data.get("generatedAt", datetime.datetime.now().isoformat() + "Z")
    meta = data.get("meta", {})
    skills = data.get("skills", [])

    skills.sort(key=lambda x: x["id"])

    os.makedirs("skills/atomic", exist_ok=True)
    os.makedirs("skills/composite", exist_ok=True)
    os.makedirs("skills/legendary", exist_ok=True)

    skill_map = {s["id"]: s for s in skills}
    date_str = timestamp.split("T")[0] if "T" in timestamp else timestamp

    for skill in skills:
        skill_type = skill.get("type", "atomic")
        skill_id = skill.get("id")
        skill_name = skill.get("name")
        level = skill.get("level")
        rarity = skill.get("rarity")
        file_path = f"skills/{skill_type}/{skill_id}.md"

        type_label = get_type_label(meta, skill_type)
        level_label = get_level_label(meta, level)
        rarity_label = get_rarity_label(meta, rarity)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# [{level_label} · {type_label}] {skill_name}\n")
            f.write(f"**ID:** {skill_id}  \n")
            f.write(f"**Type:** {type_label}  \n")
            f.write(f"**Level:** {level_label}  \n")
            f.write(f"**Rarity:** {rarity_label}  \n")
            f.write(f"**Status:** {skill.get('status', '').capitalize()}\n\n")
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
                        prereq_type = prereq.get("type", "atomic")
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
                        unlock_type = unlock.get("type", "atomic")
                        f.write(f"- [{unlock.get('name')}](../{unlock_type}/{unlock_id}.md)\n")
                    else:
                        f.write(f"- {unlock_id}\n")
                f.write("\n")

            if skill_type in ["composite", "legendary"]:
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
            f.write(f"*Generated from gaia.json v{version} on {date_str}. Do not edit directly.*\n")

    # generate registry.md
    with open("registry.md", "w", encoding="utf-8") as f:
        f.write("# Gaia Skill Registry\n\n")
        f.write("| Name | Class | Rank | Rarity | Status |\n")
        f.write("|---|---|---|---|---|\n")
        for skill in skills:
            skill_type = skill.get("type", "atomic")
            symbol = get_tier_symbol(skill_type)
            type_label = get_type_label(meta, skill_type)
            level_label = get_level_label(meta, skill.get("level"))
            rarity_label = get_rarity_label(meta, skill.get("rarity"))
            name_display = f"{symbol} {skill.get('name')}"
            f.write(f"| {name_display} | {type_label} | {level_label} | {rarity_label} | {skill.get('status', '').capitalize()} |\n")
        f.write(f"\n*Generated from gaia.json v{version}.*\n")

    # generate combinations.md
    with open("combinations.md", "w", encoding="utf-8") as f:
        f.write("# Combinations\n\n")
        f.write("| Skill | Class | Prerequisites | Level Floor | Conditions |\n")
        f.write("|---|---|---|---|---|\n")
        for skill in skills:
            if skill.get("type") in ["composite", "legendary"]:
                skill_type = skill.get("type")
                symbol = get_tier_symbol(skill_type)
                type_label = get_type_label(meta, skill_type)
                level_label = get_level_label(meta, skill.get("level"))
                prereqs = [skill_map.get(pid, {}).get("name", pid) for pid in skill.get("prerequisites", [])]
                prereq_str = ", ".join(prereqs)
                name_display = f"{symbol} {skill.get('name')}"
                f.write(f"| {name_display} | {type_label} | {prereq_str} | {level_label} | {skill.get('conditions', '')} |\n")
        f.write(f"\n*Generated from gaia.json v{version}.*\n")

    # generate tree.md
    _generate_tree(skills, skill_map, meta, version, date_str)

    # generate user skill tree markdown projections
    users_dir = "users"
    legendaries = _sorted_legendaries(skills)
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
                f.write(f"**Highest Rarity:** {get_rarity_label(meta, stats.get('highestRarity', 'none'))}  \n")
                f.write(f"**Deepest Lineage:** {stats.get('deepestLineage', 0)}\n\n")
                f.write("---\n\n")

                f.write("## Unlocked Skills\n\n")
                unlocked = tree.get("unlockedSkills", [])
                if unlocked:
                    f.write("| Skill | Class | Rank | Rarity | Unlocked In | Date |\n")
                    f.write("|---|---|---|---|---|---|\n")
                    for us in unlocked:
                        sid = us.get("skillId", "")
                        sk = skill_map.get(sid, {})
                        sk_type = sk.get("type", "")
                        symbol = get_tier_symbol(sk_type)
                        type_label = get_type_label(meta, sk_type)
                        level_label = get_level_label(meta, us.get("level", ""))
                        rarity_label = get_rarity_label(meta, sk.get("rarity", ""))
                        name_display = f"{symbol} {sk.get('name', sid)}"
                        f.write(f"| {name_display} | {type_label} | "
                                f"{level_label} | {rarity_label} | "
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

                    if llevel == "VI" and lid in unlocked_ids:
                        level_label = f"VI · {user_id} · Transcendent"
                    else:
                        level_label = get_level_label(meta, llevel)

                    inline = ""
                    if prereq_ids:
                        names = [skill_map.get(pid, {}).get("name", pid) for pid in prereq_ids]
                        short = [n.split(":")[-1].strip() if ":" in n else n for n in names]
                        inline = "  ← " + " · ".join(short)

                    check = "✓ " if lid in unlocked_ids else "· "
                    f.write(f"{check}◆ {lname}  [{level_label}]{inline}\n")

                    seen = {lid}
                    for i, prereq_id in enumerate(prereq_ids):
                        is_last = (i == len(prereq_ids) - 1)
                        for sl in _render_subtree(
                            prereq_id, skill_map, meta, "  ", is_last, seen,
                            unlocked_ids=unlocked_ids, user_id=user_id,
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

    # Generate named skill index
    _run_generate_named_index()


def _generate_tree(skills, skill_map, meta, version, date_str):
    legendaries = _sorted_legendaries(skills)

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

        inline = ""
        if prereq_ids:
            names = [skill_map.get(pid, {}).get("name", pid) for pid in prereq_ids]
            short = [n.split(":")[-1].strip() if ":" in n else n for n in names]
            inline = "  ← " + " · ".join(short)

        lines.append(f"◆ {lname}  [{level_label}]{inline}")
        lines.append("─" * 65)

        seen = {lid}
        for i, prereq_id in enumerate(prereq_ids):
            is_last = (i == len(prereq_ids) - 1)
            lines.extend(_render_subtree(prereq_id, skill_map, meta, "  ", is_last, seen))

        lines.append("")

    lines.append("```")
    lines.append("")
    lines.append(f"*Generated from gaia.json v{version} on {date_str}. Do not edit directly.*")

    with open("tree.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
