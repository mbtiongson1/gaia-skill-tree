"""
Adds 5 new skills to registry/gaia.json:
  fine-tune, guardrails, agent-eval, semantic-cache, workflow-automation

Run from repo root:
    python scripts/add_skills.py
"""
import json
from datetime import date

GRAPH_PATH = "registry/gaia.json"
TODAY = str(date.today())

NEW_SKILLS = [
    {
        "id": "fine-tune",
        "name": "Fine-Tune",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": (
            "Adapts a pre-trained model to a new task or domain by updating model "
            "weights using parameter-efficient methods such as LoRA, QLoRA, or full "
            "supervised fine-tuning, without retraining from scratch."
        ),
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2604.22783",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "LARS (2026) -- Parameter Efficiency Is Not Memory Efficiency: "
                    "Rethinking Fine-Tuning on-Device LLM Adaptation; "
                    "reduces GPU memory footprint 33.54% vs LoRA."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/huggingface/peft",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "HuggingFace PEFT -- state-of-the-art LoRA/QLoRA/IA3 fine-tuning; "
                    "100k+ stars, CI, active maintenance."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/hiyouga/LlamaFactory",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "LlamaFactory (ACL 2024) -- unified efficient fine-tuning of 100+ "
                    "LLMs and VLMs; 50k+ stars, reproducible benchmarks."
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
        "id": "guardrails",
        "name": "Guardrails",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": (
            "Wraps LLM outputs with programmatic safety rules, content filters, and "
            "topical constraints that detect policy violations and enforce compliant, "
            "on-policy responses before they reach the user."
        ),
        "prerequisites": ["evaluate-output", "classify", "structured-output"],
        "derivatives": [],
        "conditions": "Requires a defined policy schema and an evaluation loop.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2603.25176",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Prompt Attack Detection with LLM-as-a-Judge (2026) -- guardrail "
                    "deployment framework for detecting jailbreaks and prompt injections "
                    "under production latency constraints."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/NVIDIA-NeMo/Guardrails",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "NeMo Guardrails -- open-source toolkit for adding programmable "
                    "safety rails to LLM-based conversational systems; actively maintained."
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
        "id": "agent-eval",
        "name": "Agent Evaluation",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": (
            "Holistically evaluates an AI agent's performance on multi-step tasks "
            "by running standardised benchmarks, scoring full interaction trajectories, "
            "and producing reproducible capability reports."
        ),
        "prerequisites": ["evaluate-output", "score-relevance"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2412.14470",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Agent-SafetyBench (2024) -- benchmark with 349 interaction "
                    "environments and 2,000 test cases covering safety risks in agent "
                    "deployments; establishes reproducible trajectory-level metrics."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/truera/trulens",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "TruLens -- open-source evaluation and tracking for LLM experiments "
                    "and AI agents; CI, active maintenance, 5k+ stars."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/Giskard-AI/giskard-oss",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Giskard OSS -- testing library for LLM agents with automated "
                    "vulnerability scanning and RAG evaluation; Apache-2 license."
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
        "id": "semantic-cache",
        "name": "Semantic Cache",
        "type": "atomic",
        "level": "IV",
        "rarity": "rare",
        "description": (
            "Stores LLM responses keyed by embedding similarity so that semantically "
            "equivalent queries are served from cache, reducing inference latency and "
            "token cost without sacrificing answer quality."
        ),
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2604.20021",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Continuous Semantic Caching for Low-Cost LLM Serving (2026) -- "
                    "first rigorous theoretical framework for semantic LLM caching in "
                    "continuous query space using kernel ridge regression."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/codefuse-ai/ModelCache",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "ModelCache -- LLM semantic caching system reducing response time "
                    "via cached query-result pairs; reproducible, MIT license."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/vcache-project/vCache",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "vCache -- reliable and efficient semantic prompt caching; "
                    "active research prototype with published benchmarks."
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
        "id": "workflow-automation",
        "name": "Workflow Automation",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": (
            "Designs, configures, and runs trigger-based multi-step automation pipelines "
            "that connect external services, schedule jobs, and orchestrate tool sequences "
            "without continuous human supervision."
        ),
        "prerequisites": ["plan-decompose", "tool-use", "api-call"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/n8n-io/n8n",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "n8n -- fair-code workflow automation with 400+ integrations and "
                    "native AI capabilities; 90k+ stars, Apache-2 + EE license."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/activepieces/activepieces",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Activepieces -- AI agents and workflow automation with 400 MCP "
                    "servers; MIT license, active community."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/FlowiseAI/Flowise",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": (
                    "Flowise -- visual AI agent and workflow builder; 40k+ stars, "
                    "Apache-2 license, reproducible demos."
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

# Existing skill IDs whose derivatives arrays need patching
DERIVATIVE_PATCHES = {
    "evaluate-output":   ["guardrails", "agent-eval"],
    "classify":          ["guardrails"],
    "structured-output": ["guardrails"],
    "score-relevance":   ["agent-eval"],
    "plan-decompose":    ["workflow-automation"],
    "tool-use":          ["workflow-automation"],
    "api-call":          ["workflow-automation"],
}

# New prerequisite edges to add (composite skills only)
NEW_EDGES = [
    # guardrails
    {"sourceSkillId": "evaluate-output",   "targetSkillId": "guardrails",          "edgeType": "prerequisite", "condition": "Requires a defined policy schema and an evaluation loop.", "levelFloor": "II", "evidenceRefs": ["guardrails#evidence[0]"]},
    {"sourceSkillId": "classify",          "targetSkillId": "guardrails",          "edgeType": "prerequisite", "condition": "Requires a defined policy schema and an evaluation loop.", "levelFloor": "II", "evidenceRefs": ["guardrails#evidence[0]"]},
    {"sourceSkillId": "structured-output", "targetSkillId": "guardrails",          "edgeType": "prerequisite", "condition": "Requires a defined policy schema and an evaluation loop.", "levelFloor": "II", "evidenceRefs": ["guardrails#evidence[0]"]},
    # agent-eval
    {"sourceSkillId": "evaluate-output",   "targetSkillId": "agent-eval",          "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["agent-eval#evidence[0]"]},
    {"sourceSkillId": "score-relevance",   "targetSkillId": "agent-eval",          "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["agent-eval#evidence[0]"]},
    # workflow-automation
    {"sourceSkillId": "plan-decompose",    "targetSkillId": "workflow-automation", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["workflow-automation#evidence[0]"]},
    {"sourceSkillId": "tool-use",          "targetSkillId": "workflow-automation", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["workflow-automation#evidence[0]"]},
    {"sourceSkillId": "api-call",          "targetSkillId": "workflow-automation", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["workflow-automation#evidence[0]"]},
]


def main():
    with open(GRAPH_PATH, encoding="utf-8") as f:
        graph = json.load(f)

    existing_ids = {s["id"] for s in graph["skills"]}
    added = []

    for skill in NEW_SKILLS:
        if skill["id"] in existing_ids:
            print(f"  SKIP (already exists): {skill['id']}")
            continue
        graph["skills"].append(skill)
        existing_ids.add(skill["id"])
        added.append(skill["id"])
        print(f"  + added skill: {skill['id']}")

    # Patch derivatives on existing skills
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

    # Add new edges (skip duplicates)
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
