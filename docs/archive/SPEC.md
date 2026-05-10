# SPEC.md — Gaia Skill Registry
**Version:** 0.1.0-draft  
**Status:** In Review  
**Last Updated:** 2026-04-26

---

## 1. Purpose

Gaia is an open, graph-first registry of every AI agent skill in existence. It is both a global dataset and a gamified progression system. Skills are basic, extra, or ultimate, level up through evidence, combine into new skills, and are tracked per user across every repository they own.

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
- FR-03: The registry SHALL support three skill types: `basic`, `extra`, `ultimate`.
- FR-04: Each skill SHALL have a level between `0` and `VI`.
- FR-05: Each skill SHALL have a rarity of `common`, `uncommon`, `rare`, `epic`, or `legendary`.
- FR-06: The registry SHALL enforce that all extra and ultimate skills reference at least two valid parent skill IDs.
- FR-07: The registry SHALL enforce DAG integrity — no cycles are permitted at any depth.
<<<<<<< HEAD
- FR-08: Every non-Unawakened (0★) and non-Awakened (1★) skill SHALL reference at least one evidence source.
=======
<<<<<<< Updated upstream
- FR-08: Every non-Unawakened (Level 0) and non-Awakened (Level I) skill SHALL reference at least one evidence source.
=======
- FR-08: Every non-Unawakened (0★) and non-Awakened (1★) skill SHALL reference at least one evidence source.
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
- FR-09: Ultimate skills SHALL require a minimum of three Evidence Tier A or B sources and explicit maintainer approval before status can be set to `validated`.
- FR-10: The registry SHALL export the canonical graph in both JSON (D3/Cytoscape-compatible) and GEXF (Gephi-compatible) formats.
- FR-11: All human-readable files (`skills/`, `registry.md`, `combinations.md`) SHALL be generated outputs — never hand-maintained as source of truth.

### 4.2 User Skill Trees
- FR-12: Each GitHub user SHALL have at most one canonical skill tree stored at `skill-trees/[username]/skill-tree.json`.
- FR-13: A skill tree SHALL record: which skills are unlocked, at what level, when they were unlocked, and in which repository they were detected.
- FR-14: A skill tree SHALL record pending combinations — detected prerequisite clusters that have not yet been confirmed by the user.
- FR-15: A user's skill tree SHALL be loadable and queryable from any repository they own via the Gaia plugin.
- FR-16: Writing to a user's skill tree SHALL require GitHub identity verification — no user may write to another user's tree.

### 4.3 Plugin (Per-Repo)
- FR-17: The Gaia plugin SHALL be installable into any repository via a single command (`gaia init`) or GitHub Action.
- FR-18: The plugin SHALL scan the repository for skill references across declared scan paths (`.gaia/`, `skills/`, `agents/`, MCP tool declarations).
- FR-19: The plugin SHALL resolve detected skills against the Gaia registry.
- FR-20: The plugin SHALL detect combination candidates: sets of prerequisite skills that together unlock an extra or ultimate skill the user does not yet own.
- FR-21: When a combination is detected, the plugin SHALL prompt the user to confirm the fusion before writing it to their skill tree.
- FR-22: On user confirmation, the plugin SHALL update the skill tree in `skill-trees/[username]/skill-tree.json` via an automated PR to the Gaia registry.
- FR-23: The plugin SHALL expose `gaia status`, `gaia tree`, and `gaia load [username]` commands.

### 4.4 Contribution Workflow
- FR-24: Contributors SHALL be able to propose a new basic skill, a new extra skill, a new fusion recipe, or a reclassification (level or rarity) via pull request.
- FR-25: All PRs SHALL be validated against JSON schema before merge.
- FR-26: All PRs SHALL pass DAG integrity checks before merge.
- FR-27: Ultimate skill additions SHALL require at least two maintainer approvals.
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
  "type": "extra",
<<<<<<< HEAD
  "level": "3★",
=======
<<<<<<< Updated upstream
  "level": "III",
=======
  "level": "3★",
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
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
<<<<<<< HEAD
  "levelFloor": "2★",
=======
<<<<<<< Updated upstream
  "levelFloor": "II",
=======
  "levelFloor": "2★",
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
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
<<<<<<< HEAD
      "level": "3★",
=======
<<<<<<< Updated upstream
      "level": "III",
=======
      "level": "3★",
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
      "unlockedAt": "2026-03-10",
      "unlockedIn": "mbtiongson1/tracker-automation",
      "combinedFrom": ["webSearch", "parseHtml", "extractEntities"]
    }
  ],
  "pendingCombinations": [
    {
      "detectedSkills": ["codeGeneration", "executeBash"],
      "candidateResult": "autonomousDebug",
<<<<<<< HEAD
      "levelFloor": "3★",
=======
<<<<<<< Updated upstream
      "levelFloor": "III",
=======
      "levelFloor": "3★",
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
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
| `basic` | Primitive, indivisible capability | 0 |
| `extra` | Emerged from two or more skills | 2 |
| `ultimate` | High-complexity, rare, evidence-heavy emergent skill | 3+ |

### 7.2 Levels

| Level | Class | Name | Description | Evidence Floor |
|---|---|---|---|---|
| 0 | F | Unawakened | Universal LLM primitive: any capable model does this by default | None |
| I | D | Awakened | Foundation tier: catalogued agent capability | None |
| II | C | Named | First confirmed demonstration | Evidence Tier C |
| III | B | Evolved | Reproducible and fully documented | Evidence Tier B |
| IV | A | Hardened | Failure modes known; battle-tested | Evidence Tier B or A |
| V | S | Transcendent | Composable and self-improving | Evidence Tier A |
| VI | SS | Transcendent ★ | Apex: peer-reviewed, named to the agent who unlocked it | Evidence Tier A + peer review |

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

### 8.1 Evidence Tiers

| Evidence Tier | Standard |
|---|---|
| A | Peer-reviewed paper or rigorous public benchmark with reproducible methodology |
| B | Reproducible open-source demo with logs, inputs, and outputs archived |
| C | Credible vendor or community demo with limited independent reproducibility |

### 8.2 Evidence Requirements by Level

<<<<<<< HEAD
- **0★ (Unawakened):** No evidence required.
- **1★ (Awakened):** No evidence required.
- **2★ (Named):** At least one Evidence Tier C source.
- **3★ (Evolved):** At least one Evidence Tier B source.
- **4★ (Hardened):** At least one Evidence Tier B or A source, with documented failure modes.
- **5★ (Transcendent):** At least one Evidence Tier A source with composability or self-improvement evidence.
=======
<<<<<<< Updated upstream
- **Level 0 (Unawakened):** No evidence required.
- **Level I (Awakened):** No evidence required.
- **Level II (Named):** At least one Evidence Tier C source.
- **Level III (Evolved):** At least one Evidence Tier B source.
- **Level IV (Hardened):** At least one Evidence Tier B or A source, with documented failure modes.
- **Level V (Transcendent):** At least one Evidence Tier A source with composability or self-improvement evidence.
=======
- **0★ (Unawakened):** No evidence required.
- **1★ (Awakened):** No evidence required.
- **2★ (Named):** At least one Evidence Tier C source.
- **3★ (Evolved):** At least one Evidence Tier B source.
- **4★ (Hardened):** At least one Evidence Tier B or A source, with documented failure modes.
- **5★ (Transcendent):** At least one Evidence Tier A source with composability or self-improvement evidence.
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
- **Ultimate type:** Minimum three Evidence Tier A or B sources, two maintainer approvals, no `provisional` status permitted at merge.

---

## 9. Seed Taxonomy (MVP)

### 9.1 Basic (target: 50–80)
Examples: `tokenize`, `classify`, `retrieve`, `rank`, `parseJson`, `parseHtml`, `executeBash`, `generateText`, `summarize`, `citeSources`, `extractEntities`, `routeIntent`, `evaluateOutput`, `embedText`, `chunkDocument`

### 9.2 Extra (target: 80–150)
Examples:
- `webScrape` = `webSearch` + `parseHtml` + `extractEntities`
- `research` = `webSearch` + `summarize` + `citeSources`
- `ghostwrite` = `research` + `writeReport` + `audienceModel`
- `autonomousDebug` = `codeGeneration` + `executeBash` + `errorInterpretation`
- `planAndExecute` = `routeIntent` + `taskDecompose` + `toolSelect`

### 9.3 Ultimate (target: 5–20, provisional stubs at launch)
Examples: `recursiveSelfImprovement`, `multiAgentOrchestrationV`, `autonomousResearchAgent`

### 9.4 Unclaimed Ultimate Skills

Five Ultimate skills ship with a hidden seed `title` in `gaia.json` but no contributor implementation. They appear in `registry.md` and projections as:

```
◆ /skill-id  [Unclaimed ✦]
```

The seed title is suppressed until the skill is claimed. The first contributor to push a named implementation via `gaia name` whose `genericSkillRef` points to one of these skills claims the title slot, becomes the origin contributor, and the display changes to `Ultimate Skill: contributor/skill-name`.

| Skill ID | Seed Title |
|---|---|
| `recursive-self-improvement` | Unbound Sage |
| `full-stack-developer` | Sovereign Craftsman |
| `autonomous-data-scientist` | Primordial Oracle |
| `real-time-voice-assistant` | Eternal Herald |
| `autonomous-scientific-discovery` | The Doctor |

Claiming requirements are the same as any named skill (intake review → awakened lifecycle → `gaia name` promotion). Claiming priority follows standard named skill origin rules: earlier `createdAt` wins if two contributors submit simultaneously.

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
| **Basic skill** | A primitive, indivisible AI agent capability. |
| **Extra skill** | A skill that emerges from combining two or more parent skills. |
| **Ultimate skill** | A high-complexity emergent skill with strict evidence requirements and rarity <1%. |
| **Fusion** | The act of combining detected prerequisite skills into a new extra or ultimate skill. |
| **Skill tree** | The personal record of all skills unlocked by a given user. |
| **Lineage** | The full DAG ancestry of a skill, tracing back to basic roots. |
| **Projection** | A generated human-readable file derived from `gaia.json`. |
| **Plugin** | The Gaia tool installed per-repo that scans, detects, and syncs a user's skill tree. |
| **Pending combination** | A detected prerequisite cluster awaiting user confirmation before fusion. |
| **Unclaimed Ultimate** | An Ultimate skill in `gaia.json` with a seed title but no named contributor implementation yet. |