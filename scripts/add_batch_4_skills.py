#!/usr/bin/env python3
"""Batch 4 -- inject 6 new skills into graph/gaia.json.

New skills added:
  Atomic    (4): ocr, object-detection, code-explain, reward-modeling
  Composite (2): grounding, multi-agent-debate

Run from repo root:
    python3 scripts/add_batch_4_skills.py
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_PATH = os.path.join(REPO_ROOT, "graph", "gaia.json")
TODAY = "2026-04-30"
VERSION = "0.2.0"
EVALUATOR = "mbtiongson1"


# ---------------------------------------------------------------------------
# New skills -- Atomic
# ---------------------------------------------------------------------------

NEW_ATOMICS = [
    {
        "id": "ocr",
        "name": "OCR",
        "type": "atomic",
        "level": "II",
        "rarity": "uncommon",
        "description": (
            "Extracts machine-readable text from raster images, scanned pages, and "
            "photo documents using optical character recognition, preserving layout "
            "and handling skew, noise, and varied fonts."
        ),
        "prerequisites": [],
        "derivatives": ["document-digitization"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2109.10282",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "TrOCR (Li et al., 2021) -- transformer-based OCR model achieving "
                    "SOTA on IIIT-5K (97.9%), SVT (97.0%), and CUTE80 (97.9%) scene-text "
                    "benchmarks, outperforming CNN+attention baselines across all datasets."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/JaidedAI/EasyOCR",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "EasyOCR -- production-grade OCR library supporting 80+ languages; "
                    "24k+ GitHub stars, reproducible benchmarks, and documented "
                    "performance across diverse real-world document types."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "object-detection",
        "name": "Object Detection",
        "type": "atomic",
        "level": "II",
        "rarity": "uncommon",
        "description": (
            "Locates and classifies multiple objects within images by producing "
            "bounding boxes, confidence scores, and category labels in a single "
            "forward pass."
        ),
        "prerequisites": [],
        "derivatives": ["multimodal-reasoning", "browser-automation"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2005.12872",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "DETR (Carion et al., 2020) -- end-to-end object detection with "
                    "transformers; eliminates hand-crafted anchor design and achieves "
                    "COCO AP 42.0 with ResNet-50, matching Faster R-CNN with simplified "
                    "pipeline."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/ultralytics/ultralytics",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "Ultralytics YOLOv8 -- production real-time detection library; "
                    "COCO AP 50.2 at 8ms inference, 25k+ GitHub stars, reproducible "
                    "training and evaluation scripts for detection and segmentation."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "code-explain",
        "name": "Code Explain",
        "type": "atomic",
        "level": "II",
        "rarity": "common",
        "description": (
            "Generates accurate natural-language explanations of source code, "
            "describing intent, logic flow, and key decisions at function or "
            "module level."
        ),
        "prerequisites": [],
        "derivatives": ["code-review-pipeline", "autonomous-debug"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2109.00859",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "CodeT5 (Wang et al., 2021) -- unified pre-trained model for code "
                    "understanding and generation; 73.7 BLEU on CodeSearchNet code "
                    "summarization (Python), SOTA across 4 programming languages on the "
                    "NL4Code benchmark."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/salesforce/CodeT5",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "Salesforce CodeT5/CodeT5+ open-source repository -- reproducible "
                    "fine-tuning and evaluation scripts for code summarization, "
                    "generation, and translation across 8 programming languages."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "reward-modeling",
        "name": "Reward Modeling",
        "type": "atomic",
        "level": "II",
        "rarity": "rare",
        "description": (
            "Learns a scalar reward signal from human preference comparisons between "
            "model outputs, enabling reinforcement learning from human feedback (RLHF) "
            "to align model behavior with human values."
        ),
        "prerequisites": [],
        "derivatives": ["recursive-self-improvement", "prompt-optimization"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2203.02155",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "InstructGPT (Ouyang et al., 2022) -- RLHF with reward model "
                    "trained on 33K human comparisons; 1.3B InstructGPT preferred over "
                    "175B GPT-3 by 85% of labelers, demonstrating reward modeling as the "
                    "key alignment primitive."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/huggingface/trl",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "TRL (HuggingFace) -- production RLHF library with reward model "
                    "training, PPO, DPO, and GRPO support; 10k+ GitHub stars, "
                    "reproducible training scripts and documented evaluation pipelines."
                ),
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
# New skills -- Composite
# ---------------------------------------------------------------------------

NEW_COMPOSITES = [
    {
        "id": "grounding",
        "name": "Grounding",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": (
            "Verifies generated claims against retrieved evidence, identifies "
            "unsupported or contradicted assertions, and anchors outputs in "
            "traceable, cited sources."
        ),
        "prerequisites": ["retrieve", "cite-sources", "evaluate-output"],
        "derivatives": ["research"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2210.08726",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "RARR (Gao et al., 2022) -- retrieval and attribution for LLM "
                    "outputs; +32 points on the AIS attribution benchmark by revising "
                    "ungrounded claims using retrieved web evidence."
                ),
            },
            {
                "class": "B",
                "source": "https://github.com/shmsw25/FActScoring",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "FActScore (Min et al., EMNLP 2023) -- atomic factuality scoring "
                    "pipeline decomposing generation into claims and verifying each "
                    "against a retrieval corpus; open-source with reproducible "
                    "evaluation on biography generation."
                ),
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "multi-agent-debate",
        "name": "Multi-Agent Debate",
        "type": "composite",
        "level": "IV",
        "rarity": "rare",
        "description": (
            "Runs multiple LLM agents that propose, critique, and iteratively "
            "refine answers across structured debate rounds, converging on more "
            "accurate and well-reasoned responses than any single agent achieves."
        ),
        "prerequisites": ["self-critique", "evaluate-output", "chain-of-thought"],
        "derivatives": ["recursive-self-improvement"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2305.14325",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "Du et al. (2023) -- Improving Factuality and Reasoning through "
                    "Multi-Agent Debate; +14% truthfulness on TruthfulQA and +6% on "
                    "MMLU Reasoning over single-model greedy decoding baselines."
                ),
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2308.07201",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": (
                    "ChatEval (Chan et al., 2023) -- role-play multi-agent debate "
                    "framework for open-ended text quality evaluation; outperforms "
                    "single LLM judges on correlation with human ratings across "
                    "MT-Bench and Vicuna benchmarks."
                ),
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
# Derivative patches -- existing skill IDs -> new derivative IDs to append
# ---------------------------------------------------------------------------

DERIVATIVE_PATCHES = {
    # grounding prerequisites
    "retrieve":      ["grounding"],
    "cite-sources":  ["grounding"],
    "evaluate-output": ["grounding", "multi-agent-debate"],
    # multi-agent-debate prerequisites
    "self-critique": ["multi-agent-debate"],
    "chain-of-thought": ["multi-agent-debate"],
    # atomic new skills enhance existing composites
    "image-caption": ["object-detection"],
}


# ---------------------------------------------------------------------------
# Registry-curation self-evidence entry
# ---------------------------------------------------------------------------

CURATION_EVIDENCE = {
    "class": "B",
    "source": "https://github.com/mbtiongson1/gaia-skill-tree",
    "evaluator": EVALUATOR,
    "date": TODAY,
    "notes": (
        "Batch 4 curation: 6 skills added (4 atomic, 2 composite) -- "
        "ocr, object-detection, code-explain, reward-modeling, "
        "grounding, multi-agent-debate."
    ),
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

    # Deduplicate -- skip any IDs already present
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

    # Add prerequisite edges for composite new skills
    # and enhances edges for atomic new skills pointing to derivatives
    edge_set = {(e["sourceSkillId"], e["targetSkillId"]) for e in graph.get("edges", [])}
    new_edges_added = 0

    for skill in new_skills:
        if skill["id"] not in added:
            continue
        # prerequisite edges (composite skills only have prerequisites)
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
        # enhances edges from new atomics toward their derivative targets
        if skill["type"] == "atomic":
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
