# Contributing to Gaia

Thank you for helping map the frontier of AI agent capability. This guide covers everything you need to submit a high-quality contribution.

---

## Table of Contents

1. [Branch Naming Convention](#branch-naming-convention)
2. [Contribution Types](#contribution-types)
3. [Automated Workflow (Claude Code)](#automated-workflow-claude-code)
4. [Naming Conventions](#naming-conventions)
5. [Evidence Requirements](#evidence-requirements)
6. [How to Submit a PR](#how-to-submit-a-pr)
7. [Named Skills](#named-skills)
8. [Demotion and Reclassification Criteria](#demotion-and-reclassification-criteria)
9. [Reviewer Rubric](#reviewer-rubric)
10. [Why a PR Gets Rejected](#why-a-pr-gets-rejected)

---

## Branch Naming Convention

This repository uses prefix-based branch naming to enforce modularity. CI automatically validates that file changes match the branch prefix.

| Prefix | Purpose | Allowed File Scope |
|---|---|---|
| `schema/...` | Nomenclature, terminology, rank definitions | `registry/schema/` only |
| `cli/...` | CLI feature development | `src/gaia_cli/`, `packages/`, `tests/` |
| `docs/...` | User-facing documentation | `docs/`, `*.md` |
| `design/...` | Website/UI design | `docs/` (HTML/CSS/JS assets) |
| `review/gaia-push/...` | Intake PRs from `gaia push` | `registry-for-review/` |
| `review/meta/...` | Registry curation and promotion | `registry/` (excluding `registry/schema/`) |
| `dev/...` | Experimental features | Unrestricted (escape hatch) |
| `infra/...` | CI, tooling, repo infrastructure | `.github/`, `scripts/`, config files |
| `feat/...`, `fix/...` | General features and bugfixes | No forward restriction (reverse checks apply) |

### Key rules

- **Schema changes are strictly gated:** Any change to `registry/schema/` MUST come from a `schema/` branch. CI will hard-fail otherwise.
- **`dev/` is unrestricted:** Use this prefix for prototyping when you need to touch multiple areas without scope enforcement.
- **Emergency bypass:** Add the label `skip-scope-check` to a PR to bypass scope enforcement. Use sparingly.
- **Reverse checks always apply:** Even on `feat/` or `fix/` branches, touching schema files triggers the schema-branch requirement.

### Why this exists

Schema changes (level names, evidence tiers, type definitions) automatically propagate to documentation and the website via the build pipeline. Isolating these changes to dedicated branches ensures consistency and enables automated doc regeneration without cross-contaminating unrelated work.

---

## Contribution Types

| PR Type | Template | What You're Changing |
|---|---|---|
| New Basic Skill (`basic`) | `new_basic_skill.md` | Adding a primitive capability to `registry/gaia.json` |
| New Extra Skill (`extra`) | `new_extra_skill.md` | Adding a skill with 2+ prerequisites to `registry/gaia.json` |
| New fusion recipe | `new_fusion.md` | Adding edge records to `registry/gaia.json` |
| Reclassification | `reclassification.md` | Changing level or rarity of an existing skill |
| New user tree | `new_user_tree.md` | Registering your first skill tree in `skill-trees/` |
| Batch skill intake | `gaia push` / `/gaia-draft-curate` | Submitting known and proposed skills detected from agent usage |
| New named skill | `new_named_skill.md` | Adding a real-world implementation to `registry/named/` |
| Named skill classification | `named_skill_classification.md` | Reviewer-only: promoting an `awakened` named skill to `named` status |

---

## Automated Workflow (Claude Code)

If you have [Claude Code](https://claude.ai/code) installed, this repository ships slash commands that automate contribution, review, and audit workflows.

### `/gaia-curate` — add new skills to the registry

Runs the complete curation pipeline end-to-end:
1. Reads the current graph to avoid duplicates.
2. Researches candidate skills with Evidence Tier A/B evidence. For each qualifying repo found on GitHub, checks common skill directory layouts (`skills/`, `.claude/skills/`, `codex/skills/`, etc.) to find individual SKILL.md files inside — each discovered skill is treated as a separate candidate with a specific file URL as evidence, not the repo root.
3. Presents a draft review table — you classify each candidate as `accept`, `rename`, `duplicate`, `needs-evidence`, or `reject` before any file is touched.
4. Writes and runs the generation script, validates the DAG, regenerates derived files, and opens a PR.

```
/gaia-curate
```

### `/gaia-draft-curate` — triage pending intake batches

A lighter, read-only triage command for reviewing skill batches submitted via `gaia push`:
1. Pulls latest and scans `registry-for-review/skill-batches/*.json`.
2. Checks GitHub for open `draft-skills` PRs.
3. For each proposed skill, searches GitHub for evidence and inspects qualifying repos for individual SKILL.md files inside common skill directories — resolves any repo-root evidence URLs to specific file paths before accepting.
4. Presents each proposed skill for classification: `accept`, `rename`, `duplicate`, `needs-evidence`, or `reject`.
5. Optionally hands off to `/gaia-curate` to promote accepted skills into `registry/gaia.json`.

```
/gaia-draft-curate
```

Run `/gaia-draft-curate` first when contributors have pushed new intake batches. Use `/gaia-curate` when you are adding skills from your own research.

### `/gaia-audit` — review one skill or catalog item

Audits a single Gaia skill ID, named skill ID, or real-skill catalog item:
1. Reads the relevant source-of-truth files (`registry/gaia.json`, `registry/named/`, `registry/real-skills.json`, and generated projections as needed).
2. Checks current public source URLs without assuming prior classifications are still correct.
3. Compares the item against evidence, taxonomy mapping, promotion, demotion, and named-skill criteria.
4. Presents findings and, when warranted, makes the smallest source-level correction plus regenerated outputs.

```
/gaia-audit openai/chatgpt-apps
```

Use `/gaia-audit` when a specific skill may be outdated, superseded, overpromoted, weakly sourced, or mapped to the wrong Gaia node.

Reviewer expectation: Reviewers should use `/gaia-audit` before approving any PR that demotes, declassifies, remaps, disputes, or re-promotes a specific skill, named skill, or real-skill catalog item.

### `/gaia-meta-audit` — find skills needing review

Scans for review candidates before running focused audits:
1. Searches named skills and real-skill catalog entries for stale URLs, repo-root evidence, missing SKILL.md links, unsupported `promotedNamedSkillId` claims, and outdated mappings.
2. Flags likely superseded or duplicate entries where a newer official skill, source path, or canonical Gaia node appears to cover the same behavior better.
3. Prioritizes candidates by blast radius: Ultimate claims first, then named origins, then high-level mappings and stale catalog links.
4. Produces a review queue; each accepted candidate should then be handled with `/gaia-audit`.

```
/gaia-meta-audit
```

Reviewer expectation: Reviewers should use `/gaia-meta-audit` to build review queues when auditing stale source links, unsupported named-skill promotions, possible duplicates, superseded implementations, or broad high-level mappings across the registry.

> **Note:** These skills live in `.claude/skills/` at the root of this repo. Claude Code loads them automatically when you open the repo.

---

## Naming Conventions

- **Skill IDs** use `kebab-case` in `registry/gaia.json`: `web-scrape`, `parse-json`, `autonomous-debug`.
- **Display names** use Title Case: "Web Scrape", "Parse JSON", "Autonomous Debug".
- **Skill types** have display labels used in generated files — use the machine ID in `registry/gaia.json`:
  - `basic` → **Basic Skill**
  - `extra` → **Extra Skill**
  - `ultimate` → **Ultimate Skill**
- **No vendor names** in skill IDs or definitions. Skills must be agent-agnostic.
- **No abbreviations** unless universally understood (`html`, `json`, `api` are fine; `nlp` should be `natural-language-processing`).
- **No duplicates.** Before submitting, search `registry/gaia.json` for existing skills that may already cover your concept. If overlap exists, consider a reclassification PR instead.

---

## Evidence Requirements

Every skill above Level I (Awakened) must include at least one evidence entry. Level 0 (Unawakened) and Level I (Awakened) require no evidence.

### Evidence Tiers

| Evidence Tier | Standard | Example |
|---|---|---|
| **A** | Peer-reviewed paper or rigorous public benchmark with reproducible methodology | arXiv paper with code and eval |
| **B** | Reproducible open-source demo with logs, inputs, and outputs archived | GitHub repo with demo script and output logs |
| **C** | Credible vendor or community demo with limited independent reproducibility | Blog post with screenshots |

### Evidence by Level

| Level | Class | Rank | Minimum Evidence |
|---|---|---|---|
| 0 | F | **Unawakened** | None |
| I | D | **Awakened** | None |
| II | C | **Named** | 1× Evidence Tier C |
| III | B | **Evolved** | 1× Evidence Tier B |
| IV | A | **Hardened** | 1× Evidence Tier B or A |
| V | S | **Transcendent** | 1× Evidence Tier A |
| VI | SS | **Transcendent ★** | Evidence Tier A + peer review |

### Ultimate Skill Requirements

Ultimate Skill (`ultimate`) type skills have additional requirements:
- Minimum **3 Evidence Tier A or B** evidence sources.
- **2 maintainer approvals** before merge.
- Status must be `validated` at merge (never `provisional`).

---

## How to Submit a PR

### Batch Skill Intake

For most new skill discovery, use Gaia from the repository where your agent
demonstrates the skills:

```bash
gaia push
```

This creates a reviewable batch under `registry-for-review/skill-batches/` with detected
canonical skills, proposed new skills, and similarity hints. These batch records
are canonical intake records, but they are not DAG nodes until maintainers
promote accepted skills into `registry/gaia.json`.

To preview the batch without writing files:

```bash
gaia push --dry-run
```

Write the intake file without opening a PR:

```bash
gaia push --no-pr
```

Validate intake records locally:

```bash
python3 scripts/validate_intake.py
```

Review flow for intake PRs:
1. Contributor opens a draft intake PR containing `registry-for-review/skill-batches/<batchId>.json`.
2. Reviewers mark each proposed skill as `accept`, `rename`, `duplicate`, `needs-evidence`, or `reject`.
3. Maintainers promote accepted draft skills into `registry/gaia.json` in a separate canonical graph PR.

### Personal Skill Tree Progression

`gaia scan` is the source of promotion recommendations. It writes `generated-output/promotion-candidates.json` and renders `generated-output/tree.html` plus `generated-output/tree.md`.

Promotion is gated by that scan artifact:

```bash
gaia promote web-search
gaia promote --all
```

If the candidate file is missing, stale, or does not contain the skill, Gaia refuses the promotion. The target level comes from the scan recommendation, not from user input. This keeps the user's skill tree tied to observed evidence instead of manual level edits.

### Canonical Graph Changes

1. **Fork** this repository.
2. **Edit `registry/gaia.json`** directly — this is the only source of truth.
   - Add your skill node to the `skills` array.
   - Add any edge records to the `edges` array.
3. **Do NOT** edit files in `registry/skills/`, `registry/registry.md`, or `registry/combinations.md` — these are generated.
4. **Run validation locally:**
   ```bash
   python3 scripts/validate.py
   ```
5. **Open a PR** using the appropriate template from `.github/PULL_REQUEST_TEMPLATE/`.
6. Wait for CI to pass and a maintainer to review.

### PR Title Format

```
[type] Skill Name — brief description
```

Examples:
- `[basic] parse-csv — adds CSV parsing as a primitive Basic Skill`
- `[extra] autonomous-debug — combines code-generation + execute-bash + error-interpretation`
- `[reclassify] web-scrape — upgrade from Awakened (II) to Named (III) with new evidence`

---

## Named Skills

Named skills are real-world implementations of abstract Gaia skills, attributed to a specific contributor. They live at `registry/named/{contributor}/{skill-name}.md`.

### Contributor: submitting a named skill

Always submit with `status: awakened`. Never set `title`, `catalogRef`, or `status: named` — these fields are reviewer-only. CI will fail if you attempt to set them.

Use the `new_named_skill.md` PR template, which contains the full contributor and reviewer checklists.

```bash
# Example named skill frontmatter (contributor submits this)
id: karpathy/autoresearch
name: AutoResearch
contributor: karpathy
genericSkillRef: autonomous-research-agent
status: awakened          # <-- always awakened at submission
level: II
origin: true
description: "..."
```

### Reviewer: classifying a named skill

After a named skill is merged as `awakened`, a reviewer checks whether it matches a real-world published implementation (a SKILL.md, open-source repo, or documented tool). If yes:

1. Open a classification PR using the `named_skill_classification.md` template.
2. Add `title` (reviewer-assigned RPG epithet) and optionally `catalogRef` (back-link to `registry/real-skills.json`).
3. Change `status: awakened` → `status: named`.
4. Set `links.github` to the **specific SKILL.md file URL** inside the source repo (e.g., `https://github.com/owner/repo/blob/main/.claude/skills/skill-name/SKILL.md`), not the repo root or a directory listing. If no SKILL.md exists, a repo URL is acceptable but flag it as `needs-specific-url` in the classification PR.
5. If no catalog entry exists yet, add one to `registry/real-skills.json` with `promotedNamedSkillId` pointing back.

Only `status: named` skills surface as `realVariants` on abstract skill nodes and in the real-skills catalog. `awakened` skills remain in `registry/named-skills.json` under `awaitingClassification` until classified.

**Key rule:** Contributors declare skills. Reviewers classify identity.

---

## Demotion and Reclassification Criteria

Demotion is a source-of-truth correction, not a penalty. Use it when current evidence no longer supports a skill's level, rarity, named identity, or catalog promotion.

### When to demote or declassify

| Trigger | Correction |
|---|---|
| **Outdated evidence** | Lower the level or mark the skill `disputed`/`deprecated` if the cited source is stale, unreachable, contradicted by newer evidence, or no longer describes the current implementation. |
| **Superseded implementation** | Move origin or catalog emphasis to the newer maintained skill when an official, maintained, or more specific implementation replaces the older one. Preserve the old item only if it still has independent value. |
| **Overpromoted named skill** | Remove `status: named`, `title`, `catalogRef`, or `promotedNamedSkillId` when the source proves the skill exists but does not justify claiming that Gaia node. Keep the item in `registry/real-skills.json` if it remains a real source-backed skill. |
| **Insufficient usage evidence** | Do not use installability, directory presence, marketing copy, or a single source listing as proof of high-level adoption. Downgrade Legendary/Ultimate claims unless there are enough independent Class A/B sources or maintainer approvals. |
| **Wrong taxonomy mapping** | Replace broad mappings with the narrowest accurate Gaia IDs when the source supports a smaller capability than the current node suggests. |
| **Duplicate or merged concept** | Reclassify to the existing canonical skill and remove duplicate graph nodes or named-origin claims. |

### Demotion workflow

1. Start from the source of truth: `registry/gaia.json`, `registry/named/`, or `registry/real-skills.json`.
2. Re-check current external evidence and cite direct URLs. Prefer a specific `SKILL.md`, paper, benchmark, release note, or reproducible repo path over a directory or homepage.
3. Separate existence from rank: a skill may be real and useful while still not being Evolved, Hardened, Ultimate, or the named implementation of a broader Gaia node.
4. Make the smallest correction: adjust `mapsToGaia`, remove `promotedNamedSkillId`, declassify a named skill, lower level/status, or mark `deprecated` only when the evidence warrants it.
5. Use `/gaia-audit` for the focused correction. Use `/gaia-meta-audit` first when the review starts from a broad stale/superseded-skill scan rather than one named target.
6. Regenerate projections and docs, then run validation.

Demotion PRs should explain what changed in the evidence, why the previous classification is no longer supported, and what remains valid after the correction.

---

## Reviewer Rubric

Maintainers evaluate every PR against these criteria:

| Criterion | Question |
|---|---|
| **Correctness** | Is the definition precise, clear, and non-overlapping with existing skills? |
| **Compositional validity** | Do the listed prerequisites plausibly produce the claimed emergent behavior? |
| **Evidence quality** | Are sources reproducible, relevant, and correctly classified? |
| **Classification quality** | Are the level and rarity justified with rationale? |
| **Graph integrity** | Does the change introduce cycles, missing references, or orphaned nodes? |
| **Naming** | Does the ID follow kebab-case conventions? Is it agent-agnostic? |

---

## Why a PR Gets Rejected

| Reason | Explanation |
|---|---|
| **Duplicate** | A skill with substantially the same definition already exists. |
| **Vendor-specific** | The definition references a specific model or vendor as a requirement. |
| **Insufficient evidence** | Level claim exceeds available evidence quality. |
| **Invalid graph** | PR introduces a cycle, missing parent reference, or orphaned extra. |
| **Inflated rarity** | Rarity is declared rather than computed from prevalence data. |
| **Ambiguous definition** | The skill description is vague, overlapping, or not falsifiable. |
| **Hand-edited generated files** | Changes were made to `registry/skills/`, `registry/registry.md`, or `registry/combinations.md` instead of `registry/gaia.json`. |
| **Legendary without approval** | Ultimate Skill submitted without meeting the 3-source / 2-approval bar. |

---


## Community Skill Source Research

For contributors researching candidate skills from the broader SKILL.md ecosystem, see `docs/skill_source_contributions.md` for a curated list of commonly used repositories and extraction notes.

## Questions?

Open an issue with the `question` label or start a discussion in the Discussions tab.
