#!/usr/bin/env python3
"""Batch 5: Add 5 scientific-domain skills sourced from GitHub /skills repos."""
import json

GRAPH_PATH = "registry/gaia.json"

NEW_SKILLS = [
    {
        "id": "statistical-analysis",
        "name": "Statistical Analysis",
        "type": "atomic",
        "level": "III",
        "rarity": "uncommon",
        "description": "Performs hypothesis testing, regression analysis, and Bayesian modelling with effect size calculation and APA-formatted statistical reporting using scipy, statsmodels, and PyMC.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2511.06701",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Sargsyan (2025) — Structural Enforcement of Statistical Rigor in AI-Driven Discovery; monadic architecture achieves 1.1% false discovery rate vs 41% for naive LLM approaches across automated hypothesis-testing pipelines."
            },
            {
                "class": "B",
                "source": "https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/statistical-analysis/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "K-Dense-AI scientific-agent-skills — reproducible statistical-analysis skill covering parametric, non-parametric, and Bayesian workflows with scipy/statsmodels/pingouin/PyMC and APA-formatted output."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "scientific-visualization",
        "name": "Scientific Visualization",
        "type": "atomic",
        "level": "II",
        "rarity": "uncommon",
        "description": "Creates publication-ready scientific figures with multi-panel layouts, statistical annotations, colorblind-safe palettes, and journal-specific formatting (Nature, Science, Cell) using matplotlib, seaborn, and plotly.",
        "prerequisites": [],
        "derivatives": [
            "scientific-writing"
        ],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scientific-visualization/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "K-Dense-AI scientific-agent-skills — reproducible scientific-visualization skill orchestrating matplotlib, seaborn, and plotly for journal-quality multi-panel figures with PDF/EPS/TIFF/PNG export and accessibility annotations."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "literature-review",
        "name": "Literature Review",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Conducts systematic multi-database academic literature searches following PRISMA/SWARM protocols, screens and synthesises findings, verifies all citations, and generates a structured review report.",
        "prerequisites": [
            "research",
            "cite-sources",
            "summarize"
        ],
        "derivatives": [],
        "conditions": "Requires access to academic databases (PubMed, bioRxiv, ChEMBL, or equivalent).",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2501.05468",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Rouzrokh et al. (2025) — LatteReview: multi-agent framework for systematic review automation; modular agents for title/abstract screening, relevance scoring, and structured data extraction with RAG and multimodal support."
            },
            {
                "class": "B",
                "source": "https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/literature-review/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "K-Dense-AI scientific-agent-skills — reproducible literature-review skill: seven-phase workflow from research-question planning through multi-database search, screening, extraction, synthesis, citation verification to final PDF output."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "scientific-writing",
        "name": "Scientific Writing",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": "Composes research manuscripts in IMRAD structure with reporting-guideline compliance (CONSORT, STROBE, PRISMA), citation management, publication-quality figures, and LaTeX/PDF formatting.",
        "prerequisites": [
            "write-report",
            "cite-sources",
            "scientific-visualization"
        ],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2405.20477",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Chamoun et al. (ACL 2024 Findings) — SWIFT: automated focused feedback for scientific writing; multi-component LLM system (planner, investigator, reviewer, controller) rated more specific and helpful than human reviewers on 300 peer-reviewed manuscripts."
            },
            {
                "class": "B",
                "source": "https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scientific-writing/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "K-Dense-AI scientific-agent-skills — reproducible scientific-writing skill: two-stage outline-to-prose pipeline with IMRAD structure, multi-style citation management, and reporting-guideline validation (CONSORT, STROBE, PRISMA, STARD, TRIPOD)."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    },
    {
        "id": "ml-pipeline",
        "name": "ML Pipeline",
        "type": "composite",
        "level": "IV",
        "rarity": "rare",
        "description": "Designs and implements production ML pipelines with experiment tracking (MLflow, W&B), feature stores (Feast), orchestration (Kubeflow, Airflow), and automated retraining workflows including model evaluation gates and A/B deployment.",
        "prerequisites": [
            "data-analysis",
            "automated-testing",
            "code-generation"
        ],
        "derivatives": [],
        "conditions": "Requires access to a container orchestration environment and model registry.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2502.18530",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Xue et al. (2025) — IMPROVE: Iterative Model Pipeline Refinement and Optimization Leveraging LLM Experts; iterative component-level refinement consistently outperforms single-step zero-shot LLM-based ML pipeline optimization with theoretical convergence guarantees."
            },
            {
                "class": "B",
                "source": "https://github.com/Jeffallan/claude-skills/blob/main/skills/ml-pipeline/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Jeffallan/claude-skills — reproducible ml-pipeline skill: full lifecycle from data validation and feature engineering through distributed training, experiment tracking, model evaluation gates, A/B testing, and automated retraining with DVC/Feast/MLflow/Kubeflow."
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": "2026-04-30",
        "updatedAt": "2026-04-30",
        "version": "0.1.0"
    }
]

# Existing skill IDs whose derivatives arrays need patching
DERIVATIVE_PATCHES = {
    "research":         ["literature-review"],
    "cite-sources":     ["literature-review", "scientific-writing"],
    "summarize":        ["literature-review"],
    "write-report":     ["scientific-writing"],
    "data-analysis":    ["ml-pipeline"],
    "automated-testing": ["ml-pipeline"],
    "code-generation":  ["ml-pipeline"],
}

NEW_EDGES = [
    # literature-review
    {"sourceSkillId": "research",      "targetSkillId": "literature-review", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["literature-review#evidence[0]"]},
    {"sourceSkillId": "cite-sources",  "targetSkillId": "literature-review", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["literature-review#evidence[0]"]},
    {"sourceSkillId": "summarize",     "targetSkillId": "literature-review", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["literature-review#evidence[0]"]},
    # scientific-writing
    {"sourceSkillId": "write-report",             "targetSkillId": "scientific-writing", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["scientific-writing#evidence[0]"]},
    {"sourceSkillId": "cite-sources",             "targetSkillId": "scientific-writing", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["scientific-writing#evidence[0]"]},
    {"sourceSkillId": "scientific-visualization", "targetSkillId": "scientific-writing", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["scientific-writing#evidence[0]"]},
    # ml-pipeline
    {"sourceSkillId": "data-analysis",    "targetSkillId": "ml-pipeline", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["ml-pipeline#evidence[0]"]},
    {"sourceSkillId": "automated-testing","targetSkillId": "ml-pipeline", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["ml-pipeline#evidence[0]"]},
    {"sourceSkillId": "code-generation",  "targetSkillId": "ml-pipeline", "edgeType": "prerequisite", "condition": "", "levelFloor": "II", "evidenceRefs": ["ml-pipeline#evidence[0]"]},
]


def main():
    with open(GRAPH_PATH, encoding='utf-8') as f:
        graph = json.load(f)

    existing_ids = {s["id"] for s in graph["skills"]}

    for skill in NEW_SKILLS:
        if skill["id"] in existing_ids:
            print(f"  SKIP (exists): {skill['id']}")
            continue
        graph["skills"].append(skill)
        print(f"  + skill: {skill['id']}")

    for skill_id, new_derivs in DERIVATIVE_PATCHES.items():
        for s in graph["skills"]:
            if s["id"] == skill_id:
                for d in new_derivs:
                    if d not in s.get("derivatives", []):
                        s.setdefault("derivatives", []).append(d)
                        print(f"  ~ {skill_id}.derivatives += {d}")
                s["updatedAt"] = "2026-04-30"
                break

    existing_edge_keys = {(e["sourceSkillId"], e["targetSkillId"]) for e in graph["edges"]}
    for edge in NEW_EDGES:
        key = (edge["sourceSkillId"], edge["targetSkillId"])
        if key in existing_edge_keys:
            print(f"  SKIP edge (exists): {key}")
            continue
        graph["edges"].append(edge)
        print(f"  + edge: {edge['sourceSkillId']} -> {edge['targetSkillId']} ({edge['edgeType']})")

    # Update registry-curation evidence to note this batch
    for s in graph["skills"]:
        if s["id"] == "registry-curation":
            s["evidence"].append({
                "class": "B",
                "source": "https://github.com/mbtiongson1/gaia-skill-tree",
                "evaluator": "mbtiongson1",
                "date": "2026-04-30",
                "notes": "Batch 5 curation: 5 skills added (2 atomic, 3 composite) -- statistical-analysis, scientific-visualization, literature-review, scientific-writing, ml-pipeline."
            })
            s["updatedAt"] = "2026-04-30"
            break

    graph["generatedAt"] = "2026-04-30"

    with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print("\nDone — registry/gaia.json updated.")


if __name__ == "__main__":
    main()
