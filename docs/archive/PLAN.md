# PLAN.md — Gaia Skill Registry
**Version:** 0.1.0-draft
**Status:** In Review
**Last Updated:** 2026-04-26

---

## 1. Objective

Ship Gaia v1 — a validated, graph-first AI agent skill registry with a working plugin, portable user skill trees, and a community contribution workflow — in 90 days from kickoff.

---

## 2. Guiding Constraints

- All development is open-source from day one.
- No custom infrastructure. Everything runs on GitHub (Actions, PRs, Pages, CODEOWNERS).
- The canonical graph must validate before any other work continues — it is the blocker for all downstream deliverables.
- Plugin is built after the registry and schemas are stable. Not before.
- Legendary skills are stubs at launch. No legendary reaches `validated` status in v1 without three Evidence Tier A/B sources and two maintainer approvals.

---

## 3. Milestones Overview

| Milestone | Name | Target |
|---|---|---|
| M0 | Foundation | Day 3 |
| M1 | Canonical Graph + Validation | Day 7 |
| M2 | Projection Pipeline | Day 10 |
| M3 | User Skill Trees | Day 17 |
| M4 | Plugin v1 | Day 24 |
| M5 | Contribution Workflow | Day 28 |
| M6 | Community Open | Day 45 |
| M7 | Frontier v1 | Day 90 |

---

## 4. Phase 0 — Foundation
**Days 1–3 | Milestone: M0**

### Goal
Stand up a usable, validated repo skeleton with schemas and seed data that passes all integrity checks.

### Deliverables
- [ ] Initialize repository structure exactly matching the target layout in DESIGN.md.
- [ ] Write `registry/schema/skill.schema.json` — validates skill nodes including type, level, rarity enums, evidence array shape.
- [ ] Write `registry/schema/combination.schema.json` — validates edge records.
- [ ] Write `registry/schema/skillTree.schema.json` — validates user skill tree records.
- [ ] Write `registry/schema/pluginConfig.schema.json` — validates `.gaia/config.json`.
- [ ] Seed `registry/gaia.json` with:
  - 25–30 atomic skills (primitives: tokenize, classify, retrieve, rank, parseJson, parseHtml, executeBash, generateText, summarize, citeSources, extractEntities, routeIntent, evaluateOutput, embedText, chunkDocument, planDecompose, writeReport, audienceModel, toolSelect, errorInterpretation, codeGeneration, webSearch, scoreRelevance, formatOutput, diffContent).
  - 10–15 composite skills with full prerequisite chains traceable to atomics.
  - 2–3 legendary stubs (clearly `provisional`, 1★ only).
- [ ] Write `CONTRIBUTING.md` with evidence requirements, PR types, naming conventions, and reviewer rubric.
- [ ] Write `README.md` with project overview, quickstart, and link to CONTRIBUTING.

### Exit Criteria
- [ ] All seed skill nodes pass schema validation.
- [ ] No cycles in seed graph (DAG check passes).
- [ ] Every seed composite traces to atomic roots with no missing references.
- [ ] Legendary stubs are clearly marked `provisional` with no false level claims.

---

## 5. Phase 1 — Canonical Graph + Validation Pipeline
**Days 4–7 | Milestone: M1**

### Goal
`gaia.json` is the live, validated canonical dataset. CI enforces correctness on every PR.

### Deliverables
- [ ] Implement `scripts/validate.py`:
  - JSON Schema validation for all nodes and edges.
  - DAG cycle detection (DFS from all root nodes).
  - Reference integrity (every parent ID resolves to an existing node).
  - Evidence threshold by level (2★ needs Evidence Tier C+, 3★ needs Evidence Tier B+, etc.).
  - Legendary approval count check (placeholder for Phase 5 enforcement).
- [ ] Set up `.github/workflows/validate.yml`:
  - Triggers on all PRs touching `registry/`.
  - Runs `validate.py` and fails with descriptive output on any violation.
- [ ] Write DAG utility in `scripts/validate.py` that outputs:
  - Total nodes by type.
  - Max lineage depth.
  - Any orphaned composite nodes (composites with fewer than 2 valid parents).
- [ ] Tag `v0.1.0-foundation`.

### Exit Criteria
- [ ] CI passes on the seed graph with zero warnings.
- [ ] CI correctly catches: a cycle, a missing parent reference, a 3★ skill with no Evidence Tier B source.
- [ ] `python scripts/validate.py` runs in under 5 seconds on the seed graph.

---

## 6. Phase 2 — Projection Pipeline
**Days 8–10 | Milestone: M2**

### Goal
All human-readable files are generated from `gaia.json`. No manual file editing beyond the canonical graph.

### Deliverables
- [ ] Implement `scripts/generateProjections.py`:
  - Generates `skills/atomic/[id].md` for all atomic skills.
  - Generates `skills/composite/[id].md` for all composite skills.
  - Generates `skills/legendary/[id].md` for all legendary skills.
  - Generates `registry.md` — flat sorted index of all skills with type, level, rarity, status.
  - Generates `combinations.md` — matrix of all fusion recipes with prerequisite lists, conditions, level floors.
  - Includes provenance footer on every generated file (timestamp + graph version).
- [ ] Implement `scripts/exportGexf.py`:
  - Exports `registry/gaia.gexf` in GEXF 1.2 with custom attribute namespaces for `level`, `rarity`, `status`, `type`.
- [ ] Extend CI with `generate.yml`:
  - Runs `generateProjections.py` after validation.
  - Fails if committed generated files differ from freshly generated output (drift detection).
- [ ] Create first static snapshot: `registry/render/v0.1.0.json`.

### Exit Criteria
- [ ] `python scripts/generateProjections.py` is deterministic — identical input produces identical output on any machine.
- [ ] CI detects and blocks a PR where a generated file was hand-edited.
- [ ] All 30+ seed skills have a rendered `.md` page that matches DESIGN.md §5 structure.

---

## 7. Phase 3 — User Skill Trees
**Days 11–17 | Milestone: M3**

### Goal
User skill trees exist, validate, and are portable across repositories by username.

### Deliverables
- [ ] Create `skill-trees/` directory with `README.md` explaining the identity model and CODEOWNERS protection.
- [ ] Set up `CODEOWNERS` so `skill-trees/[username]/` can only be modified by PRs opened under that username's verified GitHub Actions context.
- [ ] Seed 2–3 example user skill trees (`skill-trees/mbtiongson1/`, etc.) that validate against `skillTree.schema.json`.
- [ ] Implement `scripts/generateProjections.py` extension for user trees:
  - Generates `skill-trees/[username]/skill-tree.md` matching DESIGN.md §6 structure.
- [ ] Write `scripts/detectCombinations.py`:
  - Accepts a set of detected skill IDs + a user's current skill tree.
  - Returns a list of combination candidates (each with candidate skill ID, prerequisites met, level floor).
  - Shared module — used by both the plugin (Phase 4) and CI checks.
- [ ] Add `computeRarity.py`:
  - Reads all user skill trees in `skill-trees/`.
  - Computes prevalence percentages per skill.
  - Outputs a rarity override table — used to auto-update rarity fields in `gaia.json` if prevalence data moves a skill across thresholds.

### Exit Criteria
- [ ] Seed user trees validate against schema.
- [ ] CODEOWNERS correctly blocks a PR where user A attempts to modify user B's tree.
- [ ] `detectCombinations.py` correctly identifies a combination candidate from a given skill set.
- [ ] `computeRarity.py` produces correct prevalence counts from seed user trees.

---

## 8. Phase 4 — Plugin v1
**Days 18–24 | Milestone: M4**

### Goal
A developer can install the Gaia plugin into any repo, scan it, and receive combination prompts that update their skill tree via PR.

### Deliverables
- [ ] Implement `packages/cli-npm/cli/scanner.py`:
  - Reads `.gaia/config.json` for `scanPaths`.
  - Scans declared paths for skill ID references (skill `.md` files, MCP tool declarations, agent configs).
  - Returns a set of resolved Gaia skill IDs.
- [ ] Implement `packages/cli-npm/cli/resolver.py`:
  - Fetches or reads `gaia.json` from the configured `gaiaRegistryRef`.
  - Resolves raw detected tokens to canonical skill IDs.
- [ ] Implement `packages/cli-npm/cli/combinator.py`:
  - Wraps `scripts/detectCombinations.py` as a callable module.
  - Returns ranked combination candidates (prioritize higher rarity unlocks).
- [ ] Implement `packages/cli-npm/cli/treeManager.py`:
  - Load: fetches `skill-trees/[username]/skill-tree.json` from registry, caches locally.
  - Save: diffs current tree against incoming changes, prepares patch.
  - Status: renders summary to stdout.
  - Tree: renders lineage-aware tree view with optional depth and type filters.
- [ ] Implement `packages/cli-npm/cli/prWriter.py`:
  - Uses GitHub API to open a PR against `gaia` repo with updated `skill-tree.json`.
  - PR body includes: detected skills, combination confirmed, repo where detected, timestamp.
- [ ] Implement `packages/cli-npm/cli/main.py` — CLI entrypoint with commands: `init`, `scan`, `status`, `tree`, `load`, `fuse`, `diff`.
- [ ] Implement `packages/cli-npm/github-action/action.yml`:
  - Runs `gaia scan` on push.
  - Posts combination candidates as a PR comment if any are found.
- [ ] Write `packages/cli-npm/README.md` with installation instructions, command reference, and config options.

### Exit Criteria
- [ ] `gaia init` creates a valid `.gaia/config.json`.
- [ ] `gaia scan` on a test repo with known skills detects the correct skill IDs.
- [ ] `gaia fuse [skillId]` opens a valid PR to the Gaia registry with a correctly structured `skill-tree.json` diff.
- [ ] `gaia status` displays the user's skill tree summary correctly.
- [ ] GitHub Action runs cleanly on push and posts a comment when combinations are detected.

---

## 9. Phase 5 — Contribution Workflow
**Days 25–28 | Milestone: M5**

### Goal
External contributors can submit new skills, fusions, and reclassifications through a documented, enforceable, PR-based process.

### Deliverables
- [ ] Write PR templates in `.github/PULL_REQUEST_TEMPLATE/`:
  - `new_atomic_skill.md`
  - `new_composite_skill.md`
  - `new_fusion.md`
  - `reclassification.md` (level or rarity change)
  - `new_user_tree.md`
- [ ] Add reviewer checklist to each template:
  - Correctness: definition is precise and non-overlapping.
  - Compositional validity: parents plausibly produce emergent behavior.
  - Evidence quality: sources are reproducible and relevant.
  - Classification quality: level and rarity justified with rationale.
  - Graph integrity: no invalid references or cycles.
- [ ] Add "why rejected" taxonomy to `CONTRIBUTING.md`.
- [ ] Add example submissions for each PR type under `docs/examples/`.
- [ ] Update CI to enforce legendary two-approval requirement via `CODEOWNERS` + branch protection rules.
- [ ] Write governance doc `docs/GOVERNANCE.md`:
  - Maintainer roles and responsibilities.
  - Dispute resolution process.
  - Quarterly re-audit schedule for legendary and disputed skills.
  - Release cadence (monthly frontier releases post-MVP).

### Exit Criteria
- [ ] A first-time external contributor can open a new composite skill PR using only the template and CONTRIBUTING.md — no external guidance required.
- [ ] A PR adding a legendary skill without two maintainer approvals is blocked by branch protection.
- [ ] A PR with a DAG cycle is caught and blocked by CI.

---

## 10. Phase 6 — Community Open
**Days 29–45 | Milestone: M6**

### Goal
The first wave of external contributions is live and the community contribution flywheel is turning.

### Deliverables
- [ ] Open public "Call for Skills" GitHub Issue with contribution guidelines and skill wishlist.
- [ ] Publish initial frontier page (`docs/FRONTIER.md`) listing top-priority skill gaps and controversial legendary candidates.
- [ ] Target: 20 external PRs reviewed, 10+ merged.
- [ ] Add discovery UX to docs:
  - "How to find prerequisites for a skill you want to unlock."
  - "How to propose a fusion that doesn't exist yet."
- [ ] Publish `v0.2.0` with first community-contributed skills.
- [ ] Compute first real rarity scores from accumulated user tree data and update `gaia.json`.

### Exit Criteria
- [ ] 10+ external contributions merged cleanly.
- [ ] Median PR review time under 7 days.
- [ ] At least 3 distinct GitHub usernames with validated skill trees.

---

## 11. Phase 7 — Frontier v1
**Days 46–90 | Milestone: M7**

### Goal
Gaia v1 is a living system with real analytics, quarterly reporting, and a defensible legendary tier.

### Deliverables
- [ ] Implement `scripts/graphAnalytics.py`:
  - Most central prerequisite skills (betweenness centrality).
  - Underexplored fusion opportunities (prerequisites owned by many skill-trees but composite not yet defined).
  - Lineage depth distribution across all composite/legendary skills.
- [ ] Publish `docs/frontier-v1.md` — first frontier report using graph analytics output.
- [ ] Reclassify provisional legendary candidates using evidence accumulated since launch.
- [ ] Publish `v1.0.0` with changelog.
- [ ] Publish quarterly roadmap for v2 ambitions.
- [ ] Optional: add static graph explorer UI using D3.js deployed via GitHub Pages.

### Exit Criteria
- [ ] Canonical graph validates and exports cleanly with 100+ skills.
- [ ] Every non-trivial skill level has at least one citation.
- [ ] At least one external contributor has successfully added a skill end-to-end.
- [ ] Frontier v1 report published with at least 3 insight findings from graph analytics.

---

## 12. Seed Taxonomy — Build Order

Build atomics first. Composites depend on atomics. Legendaries depend on composites. Do not attempt to add composites before their full prerequisite atomic set exists and validates.

### Atomic Layer (build first)
```
tokenize          classify          retrieve
rank              parseJson         parseHtml
executeBash       generateText      summarize
citeSources       extractEntities   routeIntent
evaluateOutput    embedText         chunkDocument
planDecompose     writeReport       audienceModel
toolSelect        errorInterpretation codeGeneration
webSearch         scoreRelevance    formatOutput
diffContent
```

### Composite Layer (build second)
```
webScrape         = webSearch + parseHtml + extractEntities
research          = webSearch + summarize + citeSources
ghostwrite        = research + writeReport + audienceModel
autonomousDebug   = codeGeneration + executeBash + errorInterpretation
planAndExecute    = routeIntent + planDecompose + toolSelect
knowledgeHarvest  = webScrape + extractEntities + embedText
ragPipeline       = retrieve + chunkDocument + embedText + scoreRelevance
documentAnalyst   = parseJson + extractEntities + summarize + formatOutput
```

### Legendary Stubs (stubs only at launch, 1★, provisional)
```
recursiveSelfImprovement
multiAgentOrchestrationV
autonomousResearchAgent
```

---

## 13. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Taxonomy fragmentation from inconsistent naming | Medium | High | Strict slug policy + alias map + duplicate check in CI |
| R-02 | Subjective level inflation from contributors | High | High | Mandatory evidence rubric + reviewer voting + `provisional` default |
| R-03 | DAG cycle introduced via PR | Low | High | Automated cycle detection blocks all PRs with cycles |
| R-04 | Vendor bias in skill definitions | Medium | Medium | Agent-agnostic definitions required; vendor-specific evidence flagged |
| R-05 | Legendary inflation devaluing the tier | Medium | High | Higher merge bar, minimum 3 Evidence Tier A/B sources, 2 maintainer approvals |
| R-06 | Username squatting or tree impersonation | Low | High | CODEOWNERS + GitHub Actions OAuth verification |
| R-07 | Plugin false-positive skill detection | Medium | Medium | Conservative scanner — only match explicit skill ID references, not guesses |
| R-08 | Stale registry (skills not updated as AI evolves) | High | Medium | Scheduled quarterly re-audit; stale-skill flag if not updated in 180 days |
| R-09 | Plugin creates unwanted PRs | Low | Low | `autoPromptCombinations: false` default; user must opt in |
| R-10 | Generated files committed out of sync | Medium | Low | CI drift detection fails PR until files are regenerated |

---

## 14. Success Metrics

### Data Quality
- % of skills with all required fields populated.
- % of 3★+ skills with at least one Evidence Tier B source.
- Number of disputed claims resolved per month.
- Zero `validated` legendary skills with fewer than 3 evidence sources.

### Community Health
- External PR count and merge rate by month.
- Median time-to-review (target: <7 days).
- Repeat contributor rate (target: >30% of contributors return).
- Number of distinct GitHub usernames with active skill trees.

### Graph Value
- Total skill count and lineage depth growth over time.
- Number of new validated fusions discovered per quarter.
- Graph export download count.
- Number of external repos with Gaia plugin installed.

---

## 15. 30/60/90-Day Summary

### Day 0–30
- Repository scaffold live.
- Seed graph published and validated (~40 skills).
- CI pipeline (validate + generate + drift check) live.
- Generated projections (`skills/`, `registry.md`, `combinations.md`) live.
- Plugin v1 scan + detect + fuse + PR flow working.
- PR templates and governance docs live.
- Tag `v0.1.0-foundation`.

### Day 31–60
- First 10+ community contributions merged.
- At least 3 user skill trees registered and validated.
- Rarity computed from real user tree prevalence.
- Frontier gaps identified and published.
- Tag `v0.2.0-community`.

### Day 61–90
- Graph analytics live.
- Frontier v1 report published.
- Provisional legendary candidates reclassified or substantiated.
- Quarterly v2 roadmap published.
- Tag `v1.0.0`.

---

## 16. Immediate Next Actions (This Week)

| # | Action | Owner | Day |
|---|---|---|---|
| 1 | Initialize folder structure with all placeholder files | mbtiongson1 | 1 |
| 2 | Write all four JSON schemas | mbtiongson1 | 1 |
| 3 | Seed `gaia.json` with atomic layer (25 skills) | mbtiongson1 | 2 |
| 4 | Seed composites and legendary stubs | mbtiongson1 | 2 |
| 5 | Implement `validate.py` with DAG check | mbtiongson1 | 3 |
| 6 | Set up CI validation workflow | mbtiongson1 | 3 |
| 7 | Implement `generateProjections.py` | mbtiongson1 | 4–5 |
| 8 | Implement CI drift detection | mbtiongson1 | 5 |
| 9 | Seed 2 example user trees | mbtiongson1 | 6 |
| 10 | Implement `detectCombinations.py` | mbtiongson1 | 6–7 |
| 11 | Open first public "Call for Skills" issue | mbtiongson1 | 7 |
| 12 | Tag and release `v0.1.0-foundation` | mbtiongson1 | 7 |
