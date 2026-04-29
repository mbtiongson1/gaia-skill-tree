#!/usr/bin/env python3
"""Batch 3 — inject 5 new skills into graph/gaia.json.

New skills added:
  Atomic  (2): self-consistency, few-shot-learning
  Composite (3): tree-of-thought, prompt-optimization, tool-creation

Run from repo root:
    python3 scripts/add_batch_3_skills.py
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_PATH = os.path.join(REPO_ROOT, "graph", "gaia.json")
TODAY = "2026-04-29"
VERSION = "0.2.0"
EVALUATOR = "mbtiongson1"


# ---------------------------------------------------------------------------
# New skills — Atomic
# ---------------------------------------------------------------------------

NEW_ATOMICS = [
    {
        "id": "self-consistency",
        "name": "Self-Consistency",
        "type": "atomic",
        "level": "IV",
        "rarity": "rare",
        "description": "Samples multiple independent reasoning paths for the same problem and selects the answer by majority vote, improving robustness without any additional training.",
        "prerequisites": [],
        "derivatives": ["tree-of-thought", "re-act-reasoning"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2203.11171",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Wang et al. (2022) — Self-Consistency Improves Chain of Thought Reasoning in Language Models; +17.9% on GSM8K and +11.0% on MATH over greedy CoT decoding.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "few-shot-learning",
        "name": "Few-Shot Learning",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Conditions a language model on a small number of input-output demonstrations within the prompt, enabling task adaptation without weight updates.",
        "prerequisites": [],
        "derivatives": ["chain-of-thought", "conversational-agent"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2005.14165",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Brown et al. (2020) — Language Models are Few-Shot Learners (GPT-3); in-context learning from 1-100 examples achieves near-SOTA on SuperGLUE, translation, and QA benchmarks.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
]

# ---------------------------------------------------------------------------
# New skills — Composite
# ---------------------------------------------------------------------------

NEW_COMPOSITES = [
    {
        "id": "tree-of-thought",
        "name": "Tree of Thought",
        "type": "composite",
        "level": "IV",
        "rarity": "rare",
        "description": "Frames problem solving as a search over a tree of partial solutions, using LLM-generated evaluations to prune unpromising branches and backtrack, dramatically improving success on complex reasoning tasks.",
        "prerequisites": ["chain-of-thought", "plan-decompose"],
        "derivatives": ["scientific-discovery"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2305.10601",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Yao et al. (2023) — Tree of Thoughts: Deliberate Problem Solving with LLMs; +74% on Game of 24 and +4% on Creative Writing vs chain-of-thought baseline.",
            },
            {
                "class": "B",
                "source": "https://github.com/princeton-nlp/tree-of-thought-llm",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Princeton-NLP ToT repo — reproducible breadth-first and depth-first tree search implementations with evaluation scripts for Game of 24 and Mini Crosswords.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "prompt-optimization",
        "name": "Prompt Optimization",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Automatically improves prompt instructions through iterative compilation, treating prompts as programs that can be optimized against a metric using LLM-driven feedback loops.",
        "prerequisites": ["evaluate-output", "generate-text"],
        "derivatives": ["registry-curation"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2310.03714",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Khattab et al. (2023) — DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines; automated prompt tuning matches or exceeds hand-crafted prompts on GSM8K, HotPotQA, and FEVER.",
            },
            {
                "class": "B",
                "source": "https://github.com/stanfordnlp/dspy",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "DSPy — Stanford NLP library for programmable LM pipelines; 18k+ GitHub stars, supports multiple optimizers (BootstrapFewShot, MIPRO, COPRO) across any LM.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "tool-creation",
        "name": "Tool Creation",
        "type": "composite",
        "level": "IV",
        "rarity": "rare",
        "description": "Dynamically generates reusable tool functions (code) at runtime to solve novel sub-tasks, then invokes those tools to complete the overall objective without human-written APIs.",
        "prerequisites": ["code-generation", "tool-use"],
        "derivatives": ["full-stack-developer", "autonomous-research-agent"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2305.17126",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Cai et al. (2023) — Large Language Models as Tool Makers (LATM); LLM-generated tools reused across problem instances achieve +8.7% on BigBench Hard vs per-instance CoT.",
            },
            {
                "class": "B",
                "source": "https://github.com/ctlllll/LLM-ToolMaker",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "LATM repo — reproducible tool-maker/tool-user pipeline with evaluation on BigBench Hard tasks and tool reuse across problem batches.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
]

# ---------------------------------------------------------------------------
# Derivative patches — existing skill IDs → new derivative IDs to append
# ---------------------------------------------------------------------------

DERIVATIVE_PATCHES = {
    "chain-of-thought": ["tree-of-thought", "self-consistency"],
    "plan-decompose":   ["tree-of-thought"],
    "evaluate-output":  ["prompt-optimization"],
    "generate-text":    ["prompt-optimization", "few-shot-learning"],
    "code-generation":  ["tool-creation"],
    "tool-use":         ["tool-creation"],
    "classify":         ["few-shot-learning"],
    "question-answer":  ["few-shot-learning"],
}

# ---------------------------------------------------------------------------
# Registry-curation self-evidence entry
# ---------------------------------------------------------------------------

CURATION_EVIDENCE = {
    "class": "B",
    "source": "https://github.com/mbtiongson1/gaia-skill-tree",
    "evaluator": EVALUATOR,
    "date": TODAY,
    "notes": "Batch 3 curation: 5 skills added (2 atomic, 3 composite) — self-consistency, few-shot-learning, tree-of-thought, prompt-optimization, tool-creation.",
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    skills_list = graph["skills"]
    skill_index = {s["id"]: s for s in skills_list}
    existing_ids = set(skill_index.keys())

    new_skills = NEW_ATOMICS + NEW_COMPOSITES

    # Deduplicate — skip any IDs already present
    added = []
    skipped = []
    for skill in new_skills:
        if skill["id"] in existing_ids:
            skipped.append(skill["id"])
            continue
        skills_list.append(skill)
        existing_ids.add(skill["id"])
        skill_index[skill["id"]] = skill
        added.append(skill["id"])

    # Apply derivative patches to existing skills
    patched = []
    for skill_id, new_derivatives in DERIVATIVE_PATCHES.items():
        if skill_id not in skill_index:
            print(f"  WARN: {skill_id} not found for derivative patch, skipping.")
            continue
        target = skill_index[skill_id]
        current = set(target.get("derivatives", []))
        to_add = [d for d in new_derivatives if d not in current and d in existing_ids]
        if to_add:
            target["derivatives"] = sorted(current | set(to_add))
            target["updatedAt"] = TODAY
            patched.append(f"{skill_id} += {to_add}")

    # Add prerequisite edges for new skills
    edge_set = {(e["sourceSkillId"], e["targetSkillId"]) for e in graph.get("edges", [])}
    new_edges_added = 0
    for skill in new_skills:
        if skill["id"] not in added:
            continue
        for prereq in skill.get("prerequisites", []):
            key = (prereq, skill["id"])
            if key not in edge_set:
                graph["edges"].append({
                    "sourceSkillId": prereq,
                    "targetSkillId": skill["id"],
                    "edgeType": "prerequisite",
                    "condition": "",
                    "levelFloor": "I",
                    "evidenceRefs": [],
                })
                edge_set.add(key)
                new_edges_added += 1
        for deriv in skill.get("derivatives", []):
            key = (skill["id"], deriv)
            if key not in edge_set and deriv in existing_ids:
                graph["edges"].append({
                    "sourceSkillId": skill["id"],
                    "targetSkillId": deriv,
                    "edgeType": "enhances",
                    "condition": "",
                    "levelFloor": "I",
                    "evidenceRefs": [],
                })
                edge_set.add(key)
                new_edges_added += 1

    # Append curation evidence to registry-curation skill
    if "registry-curation" in skill_index:
        skill_index["registry-curation"]["evidence"].append(CURATION_EVIDENCE)
        skill_index["registry-curation"]["updatedAt"] = TODAY

    graph["generatedAt"] = TODAY

    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Added {len(added)} skills: {added}")
    if skipped:
        print(f"Skipped {len(skipped)} (already exist): {skipped}")
    print(f"Patched derivatives on {len(patched)} existing skills:")
    for p in patched:
        print(f"   {p}")
    print(f"New edges added: {new_edges_added}")


if __name__ == "__main__":
    main()
