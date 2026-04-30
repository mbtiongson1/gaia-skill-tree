"""Add 4 new generic skills from the mattpocock/skills curation batch."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
GAIA = ROOT / "graph" / "gaia.json"

NEW_SKILLS = [
    {
        "id": "issue-triage",
        "name": "Issue Triage",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Classifies incoming issue reports through a structured state machine, assigns triage roles (bug/enhancement, needs-info/ready-for-agent/wontfix), reproduces bugs, requests missing detail, and produces structured resolution briefs for agent or human handoff.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Production triage skill with state-machine workflow, HITL/AFK routing, and structured agent-brief output."
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2501.18908",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "CASEY system: LLMs automate CWE identification (68% accuracy) and severity assessment (73.6%) for security bug triage."
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2504.18804",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "LLMs transform unstructured bug reports into high-quality structured formats; fine-tuned Qwen 2.5 achieves 77% CTQRS."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "prd-generation",
        "name": "PRD Generation",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Synthesizes conversation context and codebase knowledge into a structured Product Requirements Document containing a problem statement, extensive user stories, implementation decisions, module boundaries, testing decisions, and out-of-scope items.",
        "prerequisites": ["write-report", "plan-decompose"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Production skill that synthesises live conversation context into a fully-structured PRD and publishes it to the issue tracker."
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2507.19113",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Practical study: LLMs generate Functional Design Specifications and user stories from fragmented requirement sources in an IT consulting deployment."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "vertical-slice-planning",
        "name": "Vertical Slice Planning",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": "Decomposes a product plan into independently-demoable vertical slices that each cut through all integration layers end-to-end. Classifies each slice as HITL (human-in-the-loop) or AFK (autonomous), identifies dependency ordering, and publishes structured issues with acceptance criteria.",
        "prerequisites": ["plan-decompose", "route-intent"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Production skill implementing tracer-bullet vertical slicing with HITL/AFK classification and issue-tracker publication."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "design-review",
        "name": "Design Review",
        "type": "composite",
        "level": "III",
        "rarity": "rare",
        "description": "Stress-tests a plan or design through relentless targeted questioning, walking the decision tree branch-by-branch, resolving concept dependencies, surfacing contradictions against the existing codebase, and crystallising ubiquitous language — optionally persisting resolved decisions to CONTEXT.md and ADRs.",
        "prerequisites": ["evaluate-output", "plan-decompose"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Production interactive design-grilling skill; walks decision tree with recommended answers, one question at a time."
            },
            {
                "class": "B",
                "source": "https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Extended implementation with domain-model awareness: challenges language against CONTEXT.md, cross-references code, writes ADRs inline."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    }
]

NEW_EDGES = [
    # prd-generation prerequisites
    {"sourceSkillId": "write-report",    "targetSkillId": "prd-generation",          "edgeType": "prerequisite", "condition": "", "levelFloor": "III", "evidenceRefs": []},
    {"sourceSkillId": "plan-decompose",  "targetSkillId": "prd-generation",          "edgeType": "prerequisite", "condition": "", "levelFloor": "III", "evidenceRefs": []},
    # vertical-slice-planning prerequisites
    {"sourceSkillId": "plan-decompose",  "targetSkillId": "vertical-slice-planning", "edgeType": "prerequisite", "condition": "", "levelFloor": "II",  "evidenceRefs": []},
    {"sourceSkillId": "route-intent",    "targetSkillId": "vertical-slice-planning", "edgeType": "prerequisite", "condition": "", "levelFloor": "II",  "evidenceRefs": []},
    # design-review prerequisites
    {"sourceSkillId": "evaluate-output", "targetSkillId": "design-review",           "edgeType": "prerequisite", "condition": "", "levelFloor": "II",  "evidenceRefs": []},
    {"sourceSkillId": "plan-decompose",  "targetSkillId": "design-review",           "edgeType": "prerequisite", "condition": "", "levelFloor": "II",  "evidenceRefs": []},
    # issue-triage can enhance routing/classification
    {"sourceSkillId": "issue-triage",    "targetSkillId": "route-intent",            "edgeType": "enhances",     "condition": "", "levelFloor": "III", "evidenceRefs": []},
    # prd-generation can drive vertical-slice-planning
    {"sourceSkillId": "prd-generation",  "targetSkillId": "vertical-slice-planning", "edgeType": "enhances",     "condition": "", "levelFloor": "III", "evidenceRefs": []},
]


def main():
    data = json.loads(GAIA.read_text(encoding="utf-8"))

    existing_ids = {s["id"] for s in data["skills"]}
    existing_edges = {
        (e["sourceSkillId"], e["targetSkillId"], e["edgeType"])
        for e in data.get("edges", [])
    }

    added_skills = []
    for skill in NEW_SKILLS:
        if skill["id"] in existing_ids:
            print(f"SKIP (exists): {skill['id']}")
            continue
        data["skills"].append(skill)
        added_skills.append(skill["id"])
        print(f"ADDED skill: {skill['id']}")

    added_edges = []
    for edge in NEW_EDGES:
        key = (edge["sourceSkillId"], edge["targetSkillId"], edge["edgeType"])
        if key in existing_edges:
            print(f"SKIP (edge exists): {key}")
            continue
        # Validate both endpoints exist
        all_ids = {s["id"] for s in data["skills"]}
        if edge["sourceSkillId"] not in all_ids:
            print(f"ERROR: source {edge['sourceSkillId']} not found")
            continue
        if edge["targetSkillId"] not in all_ids:
            print(f"ERROR: target {edge['targetSkillId']} not found")
            continue
        data["edges"].append(edge)
        added_edges.append(key)
        print(f"ADDED edge: {edge['sourceSkillId']} --{edge['edgeType']}--> {edge['targetSkillId']}")

    # Update derivatives arrays on prereq skills
    derivative_map = {
        "write-report":    ["prd-generation"],
        "plan-decompose":  ["prd-generation", "vertical-slice-planning", "design-review"],
        "route-intent":    ["vertical-slice-planning"],
        "evaluate-output": ["design-review"],
    }
    for skill in data["skills"]:
        new_derivs = derivative_map.get(skill["id"], [])
        for d in new_derivs:
            if d not in skill.get("derivatives", []):
                skill.setdefault("derivatives", []).append(d)
                print(f"PATCHED derivatives: {skill['id']} += {d}")

    GAIA.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDone. Added {len(added_skills)} skills, {len(added_edges)} edges.")


if __name__ == "__main__":
    main()
