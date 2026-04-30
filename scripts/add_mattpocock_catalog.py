"""Add 11 mattpocock catalog entries to real_skill_catalog.json."""
import json
from pathlib import Path

CATALOG = Path("graph/real_skill_catalog.json")

NEW_ITEMS = [
    {
        "id": "mattpocock-diagnose",
        "name": "mattpocock/diagnose",
        "contributor": "mattpocock",
        "title": "The Disciplined Diagnosis Loop",
        "description": "Enforces a five-phase debugging discipline prioritising the feedback loop above all else — refuses to proceed until a fast deterministic pass/fail signal exists.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnose/SKILL.md",
        "mapsToGaia": ["autonomous-debug"],
        "promotedNamedSkillId": "mattpocock/diagnose",
        "addedAt": "2026-04-30",
        "tags": ["debugging", "diagnosis", "feedback-loop", "regression", "root-cause-analysis"]
    },
    {
        "id": "mattpocock-tdd",
        "name": "mattpocock/tdd",
        "contributor": "mattpocock",
        "title": "Vertical-Slice TDD",
        "description": "Enforces strict vertical-slice TDD, blocking horizontal slicing (all tests first, then all code) and requiring tests against public interfaces only.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md",
        "mapsToGaia": ["test-driven-development"],
        "promotedNamedSkillId": "mattpocock/tdd",
        "addedAt": "2026-04-30",
        "tags": ["tdd", "red-green-refactor", "vertical-slicing", "tracer-bullet", "public-interface-testing"]
    },
    {
        "id": "mattpocock-zoom-out",
        "name": "mattpocock/zoom-out",
        "contributor": "mattpocock",
        "title": "The Abstraction Lift",
        "description": "Signals the agent to ascend one layer of abstraction and produce a map of all relevant modules, callers, and domain-glossary terms.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/zoom-out/SKILL.md",
        "mapsToGaia": ["code-explain"],
        "promotedNamedSkillId": "mattpocock/zoom-out",
        "addedAt": "2026-04-30",
        "tags": ["code-navigation", "abstraction", "module-map", "domain-glossary", "codebase-orientation"]
    },
    {
        "id": "mattpocock-edit-article",
        "name": "mattpocock/edit-article",
        "contributor": "mattpocock",
        "title": "The Section-by-Section Rewrite",
        "description": "Edits articles by modelling them as a DAG of information dependencies, confirming section order, then rewriting each section with a 240-character-per-paragraph constraint.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/personal/edit-article/SKILL.md",
        "mapsToGaia": ["document-editing"],
        "promotedNamedSkillId": "mattpocock/edit-article",
        "addedAt": "2026-04-30",
        "tags": ["article-editing", "prose-rewrite", "information-dag", "section-structure", "clarity"]
    },
    {
        "id": "mattpocock-write-a-skill",
        "name": "mattpocock/write-a-skill",
        "contributor": "mattpocock",
        "title": "The Skill Scaffolder",
        "description": "Guides creation of new agent skills via structured interview, producing a SKILL.md with trigger-aware description, progressive-disclosure layout, and optional bundled scripts.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/productivity/write-a-skill/SKILL.md",
        "mapsToGaia": ["tool-creation"],
        "promotedNamedSkillId": "mattpocock/write-a-skill",
        "addedAt": "2026-04-30",
        "tags": ["skill-authoring", "meta-agent", "claude-code", "skill-scaffolding", "progressive-disclosure"]
    },
    {
        "id": "mattpocock-triage",
        "name": "mattpocock/triage",
        "contributor": "mattpocock",
        "title": "The State-Machine Triager",
        "description": "Moves GitHub issues through a two-category x five-state machine with bug reproduction, agent-brief writing, and structured triage notes bearing an AI-generation disclaimer.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md",
        "mapsToGaia": ["issue-triage"],
        "promotedNamedSkillId": "mattpocock/triage",
        "addedAt": "2026-04-30",
        "tags": ["issue-triage", "state-machine", "bug-reproduction", "agent-brief", "github-issues"]
    },
    {
        "id": "mattpocock-to-prd",
        "name": "mattpocock/to-prd",
        "contributor": "mattpocock",
        "title": "The PRD Synthesiser",
        "description": "Synthesises conversation context and codebase knowledge into a fully-structured PRD with user stories, implementation decisions, and testing decisions, then publishes to the issue tracker.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md",
        "mapsToGaia": ["prd-generation"],
        "promotedNamedSkillId": "mattpocock/to-prd",
        "addedAt": "2026-04-30",
        "tags": ["prd", "requirements", "user-stories", "product-management", "issue-tracker"]
    },
    {
        "id": "mattpocock-to-issues",
        "name": "mattpocock/to-issues",
        "contributor": "mattpocock",
        "title": "The Vertical Slicer",
        "description": "Breaks a plan into independently-demoable vertical slices, classifies each HITL or AFK, maps dependency chains, and publishes structured GitHub issues with acceptance criteria in dependency order.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md",
        "mapsToGaia": ["vertical-slice-planning"],
        "promotedNamedSkillId": "mattpocock/to-issues",
        "addedAt": "2026-04-30",
        "tags": ["vertical-slicing", "issue-decomposition", "tracer-bullet", "hitl", "afk", "acceptance-criteria"]
    },
    {
        "id": "mattpocock-grill-with-docs",
        "name": "mattpocock/grill-with-docs",
        "contributor": "mattpocock",
        "title": "The Domain-Aware Interrogator",
        "description": "Stress-tests a plan against the project's domain model, challenging language against CONTEXT.md, cross-referencing code, and persisting resolved decisions as inline glossary updates and ADRs.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md",
        "mapsToGaia": ["design-review"],
        "promotedNamedSkillId": "mattpocock/grill-with-docs",
        "addedAt": "2026-04-30",
        "tags": ["design-review", "domain-model", "ubiquitous-language", "adr", "context-md", "socratic-method"]
    },
    {
        "id": "mattpocock-grill-me",
        "name": "mattpocock/grill-me",
        "contributor": "mattpocock",
        "title": "The Relentless Interviewer",
        "description": "Conducts a relentless one-question-at-a-time interview walking every branch of the decision tree with a recommended answer, substituting codebase exploration wherever empirically determinable.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md",
        "mapsToGaia": ["design-review"],
        "promotedNamedSkillId": "mattpocock/grill-me",
        "addedAt": "2026-04-30",
        "tags": ["design-review", "decision-tree", "socratic-method", "plan-stress-test", "one-question-at-a-time"]
    },
    {
        "id": "mattpocock-improve-codebase-architecture",
        "name": "mattpocock/improve-codebase-architecture",
        "contributor": "mattpocock",
        "title": "The Depth Seeker",
        "description": "Identifies shallow modules via the deletion test, presents deepening opportunities with locality/leverage analysis, then grills the developer on the chosen candidate to design a deep-module replacement.",
        "sourceRepo": "mattpocock/skills",
        "url": "https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md",
        "mapsToGaia": ["refactor-code"],
        "promotedNamedSkillId": "mattpocock/improve-codebase-architecture",
        "addedAt": "2026-04-30",
        "tags": ["architecture-review", "deep-modules", "refactoring", "locality", "testability", "deletion-test"]
    }
]


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing_ids = {item["id"] for item in data["items"]}
    added = 0
    for item in NEW_ITEMS:
        if item["id"] in existing_ids:
            print(f"SKIP (exists): {item['id']}")
            continue
        data["items"].append(item)
        print(f"ADDED: {item['id']}")
        added += 1
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDone. Added {added} catalog items.")


if __name__ == "__main__":
    main()
