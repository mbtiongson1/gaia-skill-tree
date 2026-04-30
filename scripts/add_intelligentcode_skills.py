"""
Add 8 skills sourced from intelligentcode-ai/skills to graph/gaia.json.

New skills:
  atomic  : mcp-integration, parallel-execution, requirements-analysis, schema-design
  composite: e2e-testing, security-audit, release-automation, deployment-automation
"""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_PATH = os.path.join(ROOT, "graph", "gaia.json")

TODAY = date.today().isoformat()
ICA_BASE = "https://github.com/intelligentcode-ai/skills/blob/main/skills"

NEW_SKILLS = [
    # ── atomics ──────────────────────────────────────────────────────────────
    {
        "id": "mcp-integration",
        "name": "MCP Integration",
        "type": "atomic",
        "level": "III",
        "rarity": "uncommon",
        "description": "Connect to and invoke tools exposed by Model Context Protocol (MCP) servers — enumerate available tools, execute calls, and handle responses across any MCP-compatible backend.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/modelcontextprotocol/go-sdk",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "Official Go SDK for MCP servers and clients (4.4k stars, maintained by Anthropic + Google). Demonstrates production-grade MCP client integration pattern.",
            },
            {
                "class": "B",
                "source": "https://github.com/nanbingxyz/5ire",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "Cross-platform AI assistant with full MCP client support (5.2k stars). Reproduces tool enumeration, execution, and multi-server routing.",
            },
            {
                "class": "C",
                "source": f"{ICA_BASE}/mcp-client/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills mcp-client — portable CLI MCP client with server enumeration, tool display, and on-demand execution.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    {
        "id": "parallel-execution",
        "name": "Parallel Execution",
        "type": "atomic",
        "level": "II",
        "rarity": "uncommon",
        "description": "Decompose a task into independent sub-tasks and execute them concurrently, merging results with configurable concurrency limits and queue-based state tracking.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "C",
                "source": f"{ICA_BASE}/parallel-execution/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills parallel-execution — concurrent work item execution with independence verification and configurable concurrency (default 5).",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    {
        "id": "requirements-analysis",
        "name": "Requirements Analysis",
        "type": "atomic",
        "level": "II",
        "rarity": "common",
        "description": "Elicit and structure requirements from stakeholder inputs into formal specifications — user stories, acceptance criteria, and traceability matrices.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "C",
                "source": f"{ICA_BASE}/requirements-engineer/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills requirements-engineer — business analysis specialist bridging stakeholders and technical teams for full requirements lifecycle.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    {
        "id": "schema-design",
        "name": "Schema Design",
        "type": "atomic",
        "level": "II",
        "rarity": "common",
        "description": "Design database schemas across relational, NoSQL, graph, and time-series stores — entity modelling, normalization, indexing strategies, and migration planning.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "C",
                "source": f"{ICA_BASE}/database-engineer/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills database-engineer — schema design and query optimization expert across relational, NoSQL, graph, time-series, and data warehouses.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    # ── composites ───────────────────────────────────────────────────────────
    {
        "id": "e2e-testing",
        "name": "End-to-End Testing",
        "type": "composite",
        "level": "III",
        "rarity": "uncommon",
        "description": "Execute full end-to-end user journey tests using browser automation frameworks (Playwright/Puppeteer), validating complete workflows from UI to backend across real environments.",
        "prerequisites": ["browser-automation", "automated-testing"],
        "derivatives": [],
        "conditions": "Requires a live or containerised target environment; browser automation must be available.",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/zachblume/autospec",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "autospec — AI agent that takes a web app URL and autonomously QAs it, saving passing specs as E2E test code (59 stars, active).",
            },
            {
                "class": "C",
                "source": f"{ICA_BASE}/user-tester/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills user-tester — E2E testing specialist with Puppeteer/Playwright automation and cross-browser user journey validation.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    {
        "id": "security-audit",
        "name": "Security Audit",
        "type": "composite",
        "level": "II",
        "rarity": "rare",
        "description": "Systematically identify security vulnerabilities, assess attack surface, and produce actionable remediation guidance across code, dependencies, and infrastructure.",
        "prerequisites": ["code-review-pipeline", "evaluate-output"],
        "derivatives": [],
        "conditions": "Requires access to the full codebase or diff; output must include severity classification and reproduction steps.",
        "evidence": [
            {
                "class": "C",
                "source": f"{ICA_BASE}/security-engineer/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills security-engineer — vulnerability assessment and security architecture with zero-trust principles and compliance management.",
            },
            {
                "class": "C",
                "source": "https://github.com/microsoft/PromptKit",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "microsoft/PromptKit (42 stars) — composable prompt components for security audits, code review, and bug investigation with any LLM.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    {
        "id": "release-automation",
        "name": "Release Automation",
        "type": "composite",
        "level": "II",
        "rarity": "uncommon",
        "description": "Automate the full software release cycle: determine semantic version bump, update CHANGELOG, commit, create a git tag, and publish a GitHub release with release notes.",
        "prerequisites": ["workflow-automation", "execute-bash", "generate-text"],
        "derivatives": [],
        "conditions": "Requires write access to the repository and a configured release token.",
        "evidence": [
            {
                "class": "C",
                "source": f"{ICA_BASE}/release/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills release — automates semantic versioning, CHANGELOG updates, PR merging, git tagging, and GitHub release creation with verification gates.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
    {
        "id": "deployment-automation",
        "name": "Deployment Automation",
        "type": "composite",
        "level": "II",
        "rarity": "uncommon",
        "description": "Automate CI/CD pipeline execution and deployment to target environments — build, test, artifact publishing, environment promotion, and rollback strategies.",
        "prerequisites": ["workflow-automation", "execute-bash"],
        "derivatives": [],
        "conditions": "Requires environment credentials and a configured pipeline definition.",
        "evidence": [
            {
                "class": "C",
                "source": f"{ICA_BASE}/devops-engineer/SKILL.md",
                "evaluator": "mbtiongson1",
                "date": TODAY,
                "notes": "intelligentcode-ai/skills devops-engineer — CI/CD pipeline design and deployment automation with build systems and release management.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": "0.2.0",
    },
]

# prerequisite edges to add: (source, target)
NEW_PREREQ_EDGES = [
    ("browser-automation",   "e2e-testing"),
    ("automated-testing",    "e2e-testing"),
    ("code-review-pipeline", "security-audit"),
    ("evaluate-output",      "security-audit"),
    ("workflow-automation",  "release-automation"),
    ("execute-bash",         "release-automation"),
    ("generate-text",        "release-automation"),
    ("workflow-automation",  "deployment-automation"),
    ("execute-bash",         "deployment-automation"),
]

# derivatives to append on existing skills: {existing_id: [new_derivative_id, ...]}
DERIVATIVES_PATCH = {
    "browser-automation":   ["e2e-testing"],
    "automated-testing":    ["e2e-testing"],
    "code-review-pipeline": ["security-audit"],
    "evaluate-output":      ["security-audit"],
    "workflow-automation":  ["release-automation", "deployment-automation"],
    "execute-bash":         ["release-automation", "deployment-automation"],
    "generate-text":        ["release-automation"],
}


def main():
    with open(GRAPH_PATH, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {s["id"] for s in data["skills"]}
    added = []

    for skill in NEW_SKILLS:
        if skill["id"] in existing_ids:
            print(f"  SKIP (already exists): {skill['id']}")
            continue
        data["skills"].append(skill)
        existing_ids.add(skill["id"])
        added.append(skill["id"])
        print(f"  ADD skill: {skill['id']}")

    # patch derivatives on existing skills
    skill_map = {s["id"]: s for s in data["skills"]}
    for parent_id, new_derivs in DERIVATIVES_PATCH.items():
        parent = skill_map.get(parent_id)
        if not parent:
            print(f"  WARN: parent {parent_id} not found")
            continue
        for d in new_derivs:
            if d not in parent.get("derivatives", []):
                parent.setdefault("derivatives", []).append(d)
                print(f"  PATCH derivatives: {parent_id} -> +{d}")

    # add prerequisite edges
    existing_edges = {
        (e["sourceSkillId"], e["targetSkillId"]) for e in data.get("edges", [])
    }
    for src, tgt in NEW_PREREQ_EDGES:
        if (src, tgt) in existing_edges:
            continue
        data.setdefault("edges", []).append({
            "sourceSkillId": src,
            "targetSkillId": tgt,
            "edgeType": "prerequisite",
            "condition": "",
            "levelFloor": "II",
            "evidenceRefs": [],
        })
        print(f"  ADD edge: {src} -> {tgt}")

    data["generatedAt"] = TODAY + "T00:00:00Z"

    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Added {len(added)} skill(s): {', '.join(added)}")


if __name__ == "__main__":
    main()
