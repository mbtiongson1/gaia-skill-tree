"""
Adds 4 new AI-agent primitive skills to graph/gaia.json:
  context-compression, prompt-injection-defense, vision-qa, tool-chaining

Run from repo root:
    python scripts/add_agent_primitives.py
"""
import json
from datetime import date

GRAPH_PATH = "graph/gaia.json"
TODAY = str(date.today())

NEW_SKILLS = [
    {
        "id": "context-compression",
        "name": "Context Compression",
        "type": "atomic",
        "level": "III",
        "rarity": "common",
        "description": (
            "Reduces the length of prompts or retrieved context to fit token limits "
            "while preserving semantic content, using techniques such as selective "
            "token removal, summarization, or token-classification-based pruning "
            "(e.g. LLMLingua)."
        ),
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2403.12968",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "LLMLingua-2 (ACL 2024 Findings) — data-distillation for efficient "
                    "task-agnostic prompt compression; 3x-6x speed-up, BERT-base token "
                    "classifier; demonstrates measurable perplexity-based faithfulness."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/microsoft/LLMLingua",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Microsoft LLMLingua — reproducible open-source implementation of "
                    "LLMLingua-1/2/LongLLMLingua; CI, README, Apache-2.0 license."
                ),
            },
            {
                "class": "C",
                "source": "https://skillsmp.com/api/v1/skills/search?q=context-compression",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "SkillsMP top hit: sickn33/antigravity-awesome-skills "
                    "(35k+ stars), multiple community variants including "
                    "context-compression-v2."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.1.0",
    },
    {
        "id": "prompt-injection-defense",
        "name": "Prompt Injection Defense",
        "type": "atomic",
        "level": "III",
        "rarity": "uncommon",
        "description": (
            "Detects and neutralizes adversarial instructions injected into agent "
            "context from untrusted external sources (indirect prompt injection), "
            "using techniques such as context isolation, hierarchical intent "
            "verification, or semantic consistency checks."
        ),
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2604.10134",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "PlanGuard (2026) — training-free indirect prompt injection defense; "
                    "planning-based consistency verification reduces InjecAgent attack "
                    "success rate from 72.8% to 0%."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/tldrsec/prompt-injection-defenses",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "tldrsec/prompt-injection-defenses (682 stars) — curated, "
                    "reproducible catalog of defense techniques with "
                    "implementation references; actively maintained."
                ),
            },
            {
                "class": "C",
                "source": "https://skillsmp.com/api/v1/skills/search?q=prompt-injection-defense",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "SkillsMP top hit: openclaw/prompt-injection-defense (4,419 stars) "
                    "— 'Harden agent sessions against prompt injection from untrusted "
                    "content'; references CaMeL benchmark."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.1.0",
    },
    {
        "id": "vision-qa",
        "name": "Visual Question Answering",
        "type": "atomic",
        "level": "III",
        "rarity": "uncommon",
        "description": (
            "Answers natural-language questions grounded in a specific image or "
            "screenshot by combining visual perception with language reasoning, "
            "enabling visual debugging, UI analysis, and document-image Q&A."
        ),
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2604.17488",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "AutoVQA-G (ICASSP 2026) — self-improving agentic framework for "
                    "automated VQA and grounding annotation; uses Chain-of-Thought "
                    "verification + prompt optimization to generate high-quality "
                    "VQA-G datasets."
                ),
            },
            {
                "class": "C",
                "source": "https://skillsmp.com/api/v1/skills/search?q=vision-qa",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "SkillsMP: 6+ named entries including visual-qa, vision-qa-workflow, "
                    "claude-vision-qa, visual-qa-analysis from multiple contributors."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.1.0",
    },
    {
        "id": "tool-chaining",
        "name": "Tool Chaining",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": (
            "Sequences multiple tool invocations into a dependency graph where "
            "the output of each tool feeds as structured input to the next, "
            "handling state propagation, intermediate result validation, and "
            "error recovery across multi-step execution pipelines."
        ),
        "prerequisites": ["tool-use", "tool-select"],
        "derivatives": [],
        "conditions": (
            "Requires at least two distinct tools whose data schemas are "
            "compatible for chaining."
        ),
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2604.07223",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "TraceSafe (2026) — first benchmark with 1,000+ instances "
                    "explicitly evaluating sequential multi-step tool-calling "
                    "trajectories across 12 risk categories; establishes "
                    "tool-chaining as a distinct, measurable capability surface."
                ),
            },
            {
                "class": "C",
                "source": "https://skillsmp.com/api/v1/skills/search?q=tool-chaining",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "SkillsMP: dependency-aware-tool-chaining, "
                    "build-agentic-workflows-chaining-tool-calls; "
                    "emerging community consensus on the pattern."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.1.0",
    },
]

# Existing skill derivatives to patch
DERIVATIVE_PATCHES = {
    "tool-use":    ["tool-chaining"],
    "tool-select": ["tool-chaining"],
}

# New prerequisite edges (composite skills only)
NEW_EDGES = [
    {
        "sourceSkillId": "tool-use",
        "targetSkillId": "tool-chaining",
        "edgeType": "prerequisite",
        "condition": "Requires at least two distinct tools whose data schemas are compatible for chaining.",
        "levelFloor": "II",
        "evidenceRefs": ["tool-chaining#evidence[0]"],
    },
    {
        "sourceSkillId": "tool-select",
        "targetSkillId": "tool-chaining",
        "edgeType": "prerequisite",
        "condition": "Requires at least two distinct tools whose data schemas are compatible for chaining.",
        "levelFloor": "II",
        "evidenceRefs": ["tool-chaining#evidence[0]"],
    },
]


def main():
    with open(GRAPH_PATH, encoding="utf-8") as f:
        graph = json.load(f)

    existing_ids = {s["id"] for s in graph["skills"]}
    added = []

    for skill in NEW_SKILLS:
        if skill["id"] in existing_ids:
            print(f"  SKIP: '{skill['id']}' already exists")
            continue
        graph["skills"].append(skill)
        existing_ids.add(skill["id"])
        added.append(skill["id"])
        print(f"  + {skill['id']}")

    skill_map = {s["id"]: s for s in graph["skills"]}
    for skill_id, new_derivs in DERIVATIVE_PATCHES.items():
        skill = skill_map.get(skill_id)
        if skill is None:
            print(f"  WARN: skill '{skill_id}' not found for derivative patch")
            continue
        current = skill.setdefault("derivatives", [])
        for d in new_derivs:
            if d not in current:
                current.append(d)
                print(f"  ~ patched {skill_id}.derivatives += {d}")

    existing_pairs = {(e["sourceSkillId"], e["targetSkillId"]) for e in graph["edges"]}
    for edge in NEW_EDGES:
        pair = (edge["sourceSkillId"], edge["targetSkillId"])
        if pair not in existing_pairs:
            graph["edges"].append(edge)
            existing_pairs.add(pair)
            print(f"  + edge: {edge['sourceSkillId']} -> {edge['targetSkillId']}")

    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nDone. Added {len(added)} skill(s): {added}")


if __name__ == "__main__":
    main()
