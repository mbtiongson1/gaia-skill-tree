# Contributing to Gaia

Thank you for helping map the frontier of AI agent capability. This guide covers everything you need to submit a high-quality contribution.

---

## Table of Contents

1. [Contribution Types](#contribution-types)
2. [Automated Workflow (Claude Code)](#automated-workflow-claude-code)
3. [Naming Conventions](#naming-conventions)
4. [Evidence Requirements](#evidence-requirements)
5. [How to Submit a PR](#how-to-submit-a-pr)
6. [Named Skills](#named-skills)
7. [Reviewer Rubric](#reviewer-rubric)
8. [Why a PR Gets Rejected](#why-a-pr-gets-rejected)

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

If you have [Claude Code](https://claude.ai/code) installed, this repository ships two slash commands that automate the full contribution and review cycle.

### `/gaia-curate` — add new skills to the registry

Runs the complete curation pipeline end-to-end:
1. Reads the current graph to avoid duplicates.
2. Researches candidate skills with Class A/B evidence. For each qualifying repo found on GitHub, checks common skill directory layouts (`skills/`, `.claude/skills/`, `codex/skills/`, etc.) to find individual SKILL.md files inside — each discovered skill is treated as a separate candidate with a specific file URL as evidence, not the repo root.
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

Every skill above Level I (Awakened) must include at least one evidence entry. Level 0 (Basic) and Level I (Awakened) require no evidence.

### Evidence Classes

| Class | Standard | Example |
|---|---|---|
| **A** | Peer-reviewed paper or rigorous public benchmark with reproducible methodology | arXiv paper with code and eval |
| **B** | Reproducible open-source demo with logs, inputs, and outputs archived | GitHub repo with demo script and output logs |
| **C** | Credible vendor or community demo with limited independent reproducibility | Blog post with screenshots |

### Evidence by Level

| Level | Rank | Minimum Evidence |
|---|---|---|
| 0 | **Basic** | None |
| I | **Awakened** | None |
| II | **Named** | 1× Class C |
| III | **Evolved** | 1× Class B |
| IV | **Hardened** | 1× Class B or A |
| V | **Transcendent** | 1× Class A |
| VI | **Transcendent ★** | Class A + peer review |

### Ultimate Skill Requirements

Ultimate Skill (`ultimate`) type skills have additional requirements:
- Minimum **3 Class A or B** evidence sources.
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
