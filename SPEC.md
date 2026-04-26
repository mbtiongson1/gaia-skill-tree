# SPEC.md — Gaia Skill Registry
**Version:** 0.1.0-draft  
**Status:** In Review  
**Last Updated:** 2026-04-26

---

## 1. Purpose

Gaia is an open, graph-first registry of every AI agent skill in existence. It is both a global dataset and a gamified progression system. Skills are atomic or composite, level up through evidence, combine into new skills, and are tracked per user across every repository they own.

This document defines what Gaia is, what it must do, and what constraints govern it.

---

## 2. Problem Statement

AI agent capabilities are fragmented across papers, benchmarks, vendor docs, and community repos with no shared taxonomy, no lineage model, and no way to know what skills a given agent has or what it would take to unlock the next tier. Gaia solves this by being the canonical, open, evidence-backed source of truth for AI agent skills — and by making skill progression something you earn, not declare.

---

## 3. Users

| User Type | Description |
|---|---|
| **Individual contributor** | Developer who installs the Gaia plugin into their repo and builds a personal skill tree. |
| **Taxonomy maintainer** | Reviewer who validates skill definitions, evidence, and fusion proposals. |
| **Researcher** | Reads the graph and registry to understand the frontier of agent capability. |
| **Agent framework author** | Integrates Gaia skill IDs into their framework's capability declarations. |

---

## 4. Functional Requirements

### 4.1 Registry (Global)
- FR-01: The registry SHALL store every known AI agent skill as a node in a directed acyclic graph (DAG).
- FR-02: Each skill node SHALL include: `id`, `name`, `type`, `level`, `rarity`, `description`, `prerequisites`, `derivatives`, `conditions`, `evidence`, `knownAgents`, `status`, `createdAt`, `updatedAt`, `version`.
- FR-03: The registry SHALL support three skill types: `atomic`, `composite`, `legendary`.
- FR-04: Each skill SHALL have a level between `I` and `V`.
- FR-05: Each skill SHALL have a rarity of `common`, `uncommon`, `rare`, `epic`, or `legendary`.
- FR-06: The registry SHALL enforce that all composite and legendary skills reference at least two valid parent skill IDs.
- FR-07: The registry SHALL enforce DAG integrity — no cycles are permitted at any depth.
- FR-08: Every non-`latent` (Level I) skill SHALL reference at least one evidence source.
- FR-09: Legendary skills SHALL require a minimum of three Class A or B evidence sources and explicit maintainer approval before status can be set to `validated`.
- FR-10: The registry SHALL export the canonical graph in both JSON (D3/Cytoscape-compatible) and GEXF (Gephi-compatible) formats.
- FR-11: All human-readable files (`skills/`, `registry.md`, `combinations.md`) SHALL be generated outputs — never hand-maintained as source of truth.

### 4.2 User Skill Trees
- FR-12: Each GitHub user SHALL have at most one canonical skill tree stored at `users/[username]/skill-tree.json`.
- FR-13: A skill tree SHALL record: which skills are unlocked, at what level, when they were unlocked, and in which repository they were detected.
- FR-14: A skill tree SHALL record pending combinations — detected prerequisite clusters that have not yet been confirmed by the user.
- FR-15: A user's skill tree SHALL be loadable and queryable from any repository they own via the Gaia plugin.
- FR-16: Writing to a user's skill tree SHALL require GitHub identity verification — no user may write to another user's tree.

### 4.3 Plugin (Per-Repo)
- FR-17: The Gaia plugin SHALL be installable into any repository via a single command (`gaia init`) or GitHub Action.
- FR-18: The plugin SHALL scan the repository for skill references across declared scan paths (`.gaia/`, `skills/`, `agents/`, MCP tool declarations).
- FR-19: The plugin SHALL resolve detected skills against the Gaia registry.
- FR-20: The plugin SHALL detect combination candidates: sets of prerequisite skills that together unlock a composite or legendary skill the user does not yet own.
- FR-21: When a combination is detected, the plugin SHALL prompt the user to confirm the fusion before writing it to their skill tree.
- FR-22: On user confirmation, the plugin SHALL update the skill tree in `users/[username]/skill-tree.json` via an automated PR to the Gaia registry.
- FR-23: The plugin SHALL expose `gaia status`, `gaia tree`, and `gaia load [username]` commands.

### 4.4 Contribution Workflow
- FR-24: Contributors SHALL be able to propose a new atomic skill, a new composite skill, a new fusion recipe, or a reclassification (level or rarity) via pull request.
- FR-25: All PRs SHALL be validated against JSON schema before merge.
- FR-26: All PRs SHALL pass DAG integrity checks before merge.
- FR-27: Legendary skill additions SHALL require at least two maintainer approvals.
- FR-28: CI SHALL fail if generated output files are stale relative to `gaia.json`.

---

## 5. Non-Functional Requirements

- NFR-01: Graph export (`generateProjections.py`) SHALL be deterministic and idempotent.
- NFR-02: Schema validation SHALL complete in under 5 seconds for a graph of up to 10,000 nodes.
- NFR-03: The plugin scan SHALL complete in under 30 seconds on a repository with up to 500 files.
- NFR-04: All schemas, scripts, and plugin code SHALL be open-source under MIT license.
- NFR-05: The registry SHALL be agent-agnostic — no skill definition SHALL reference a specific model or vendor as a requirement.
- NFR-06: All user identity operations SHALL use GitHub OAuth — no separate account system.

---

## 6. Skill Data Model

### 6.1 Skill Node Schema
```json
{
  "id": "webScrape",
  "name": "Web Scrape",
  "type": "composite",
  "level": "III",
  "rarity": "uncommon",
  "description": "Retrieves and structures data from web pages into usable entities.",
  "prerequisites": ["webSearch", "parseHtml", "extractEntities"],
  "derivatives": ["knowledgeHarvest"],
  "conditions": "Structured output mode required.",
  "evidence": [
    {
      "class": "B",
      "source": "https://example.com/demo",
      "evaluator": "mbtiongson1",
      "date": "2025-04-01",
      "notes": "Reproduced on GPT-4o with Playwright tool."
    }
  ],
  "knownAgents": [],
  "status": "validated",
  "createdAt": "2025-04-01",
  "updatedAt": "2026-04-26",
  "version": "1.0.0"
}
```

### 6.2 Edge Schema
```json
{
  "sourceSkillId": "webSearch",
  "targetSkillId": "webScrape",
  "edgeType": "prerequisite",
  "condition": "structured output mode enabled",
  "levelFloor": "II",
  "evidenceRefs": ["webScrape#evidence[0]"]
}
```

### 6.3 User Skill Tree Schema
```json
{
  "userId": "mbtiongson1",
  "updatedAt": "2026-04-26",
  "unlockedSkills": [
    {
      "skillId": "webScrape",
      "level": "III",
      "unlockedAt": "2026-03-10",
      "unlockedIn": "mbtiongson1/tracker-automation",
      "combinedFrom": ["webSearch", "parseHtml", "extractEntities"]
    }
  ],
  "pendingCombinations": [
    {
      "detectedSkills": ["codeGeneration", "executeBash"],
      "candidateResult": "autonomousDebug",
      "levelFloor": "III",
      "promptedAt": "2026-04-26"
    }
  ],
  "stats": {
    "totalUnlocked": 14,
    "highestRarity": "rare",
    "deepestLineage": 5
  }
}
```

### 6.4 Plugin Config Schema (per repo)
```json
{
  "gaiaUser": "mbtiongson1",
  "gaiaRegistryRef": "https://github.com/gaia-registry/gaia",
  "scanPaths": ["skills/", ".claude/", "agents/"],
  "autoPromptCombinations": true,
  "lastScan": "2026-04-26T00:00:00Z"
}
```

---

## 7. Skill Taxonomy

### 7.1 Types

| Type | Description | Min Parents |
|---|---|---|
| `atomic` | Primitive, indivisible capability | 0 |
| `composite` | Emerged from two or more skills | 2 |
| `legendary` | High-complexity, rare, evidence-heavy emergent skill | 3+ |

### 7.2 Levels

| Level | Name | Description | Evidence Floor |
|---|---|---|---|
| I | Latent | Conceptual only, no verified run | None |
| II | Emerging | Constrained demo success | Class C |
| III | Competent | Repeatable across standard tasks | Class B |
| IV | Proficient | Handles edge cases and failures | Class B or A |
| V | Mastered | Self-improving, teachable, composable | Class A |

### 7.3 Rarity

| Rarity | Prevalence (tracked agents) |
|---|---|
| Common | >40% |
| Uncommon | 20–40% |
| Rare | 5–20% |
| Epic | 1–5% |
| Legendary | <1% |

Rarity is computed from observed agent prevalence data — it is never declared by the contributor.

### 7.4 Status

| Status | Meaning |
|---|---|
| `provisional` | Default on submission. Accepted as plausible, not yet independently confirmed. |
| `validated` | Independently confirmed. Evidence checked by a maintainer. |
| `disputed` | Conflicting evidence exists. Both arguments preserved with references. |
| `deprecated` | Superseded by a more precise or accurate skill. Kept for lineage integrity. |

---

## 8. Evidence Policy

### 8.1 Evidence Classes

| Class | Standard |
|---|---|
| A | Peer-reviewed paper or rigorous public benchmark with reproducible methodology |
| B | Reproducible open-source demo with logs, inputs, and outputs archived |
| C | Credible vendor or community demo with limited independent reproducibility |

### 8.2 Evidence Requirements by Level

- **Level I:** No evidence required.
- **Level II:** At least one Class C source.
- **Level III:** At least one Class B source.
- **Level IV:** At least one Class B or A source, with documented failure modes.
- **Level V:** At least one Class A source with composability or self-improvement evidence.
- **Legendary type:** Minimum three Class A or B sources, two maintainer approvals, no `provisional` status permitted at merge.

---

## 9. Seed Taxonomy (MVP)

### 9.1 Atomic (target: 50–80)
Examples: `tokenize`, `classify`, `retrieve`, `rank`, `parseJson`, `parseHtml`, `executeBash`, `generateText`, `summarize`, `citeSources`, `extractEntities`, `routeIntent`, `evaluateOutput`, `embedText`, `chunkDocument`

### 9.2 Composite (target: 80–150)
Examples:
- `webScrape` = `webSearch` + `parseHtml` + `extractEntities`
- `research` = `webSearch` + `summarize` + `citeSources`
- `ghostwrite` = `research` + `writeReport` + `audienceModel`
- `autonomousDebug` = `codeGeneration` + `executeBash` + `errorInterpretation`
- `planAndExecute` = `routeIntent` + `taskDecompose` + `toolSelect`

### 9.3 Legendary (target: 5–20, provisional stubs at launch)
Examples: `recursiveSelfImprovement`, `multiAgentOrchestrationV`, `autonomousResearchAgent`

---

## 10. Constraints and Out-of-Scope

### In Scope
- Skill graph data model, schema, and validation.
- User skill trees and portability.
- Plugin scan, detection, and combination prompt flow.
- Generated projections (`skills/`, `registry.md`, `combinations.md`).
- Community contribution workflow.

### Out of Scope (v1)
- Real-time benchmark crawling or automatic skill detection from public repos.
- Automatic trust scoring without human review.
- Monetization, paywalls, or closed skill tiers.
- Vendor-specific metadata requirements.
- Native mobile application.

---

## 11. Glossary

| Term | Definition |
|---|---|
| **Atomic skill** | A primitive, indivisible AI agent capability. |
| **Composite skill** | A skill that emerges from combining two or more parent skills. |
| **Legendary skill** | A high-complexity emergent skill with strict evidence requirements and rarity <1%. |
| **Fusion** | The act of combining detected prerequisite skills into a new composite or legendary skill. |
| **Skill tree** | The personal record of all skills unlocked by a given user. |
| **Lineage** | The full DAG ancestry of a skill, tracing back to atomic roots. |
| **Projection** | A generated human-readable file derived from `gaia.json`. |
| **Plugin** | The Gaia tool installed per-repo that scans, detects, and syncs a user's skill tree. |
| **Pending combination** | A detected prerequisite cluster awaiting user confirmation before fusion. |