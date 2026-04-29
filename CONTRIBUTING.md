# Contributing to Gaia

Thank you for helping map the frontier of AI agent capability. This guide covers everything you need to submit a high-quality contribution.

---

## Table of Contents

1. [Contribution Types](#contribution-types)
2. [Naming Conventions](#naming-conventions)
3. [Evidence Requirements](#evidence-requirements)
4. [How to Submit a PR](#how-to-submit-a-pr)
5. [Reviewer Rubric](#reviewer-rubric)
6. [Why a PR Gets Rejected](#why-a-pr-gets-rejected)

---

## Contribution Types

| PR Type | Template | What You're Changing |
|---|---|---|
| New Intrinsic Skill (`atomic`) | `new_atomic_skill.md` | Adding a primitive capability to `gaia.json` |
| New Extra Skill (`composite`) | `new_composite_skill.md` | Adding a skill with 2+ prerequisites to `gaia.json` |
| New fusion recipe | `new_fusion.md` | Adding edge records to `gaia.json` |
| Reclassification | `reclassification.md` | Changing level or rarity of an existing skill |
| New user tree | `new_user_tree.md` | Registering your first skill tree in `users/` |
| Batch skill intake | `gaia push` | Submitting known and proposed skills detected from agent usage |

---

## Naming Conventions

- **Skill IDs** use `kebab-case` in `gaia.json`: `web-scrape`, `parse-json`, `autonomous-debug`.
- **Display names** use Title Case: "Web Scrape", "Parse JSON", "Autonomous Debug".
- **Skill types** have display labels used in generated files — use the machine ID in `gaia.json`:
  - `atomic` → **Intrinsic Skill**
  - `composite` → **Extra Skill**
  - `legendary` → **Ultimate Skill**
- **No vendor names** in skill IDs or definitions. Skills must be agent-agnostic.
- **No abbreviations** unless universally understood (`html`, `json`, `api` are fine; `nlp` should be `natural-language-processing`).
- **No duplicates.** Before submitting, search `gaia.json` for existing skills that may already cover your concept. If overlap exists, consider a reclassification PR instead.

---

## Evidence Requirements

Every skill above Level I must include at least one evidence entry.

### Evidence Classes

| Class | Standard | Example |
|---|---|---|
| **A** | Peer-reviewed paper or rigorous public benchmark with reproducible methodology | arXiv paper with code and eval |
| **B** | Reproducible open-source demo with logs, inputs, and outputs archived | GitHub repo with demo script and output logs |
| **C** | Credible vendor or community demo with limited independent reproducibility | Blog post with screenshots |

### Evidence by Level

| Level | Rank | Minimum Evidence |
|---|---|---|
| I | Dormant | None |
| II | Awakened | 1× Class C |
| III | Named | 1× Class B |
| IV | Evolved | 1× Class B or A |
| V | Transcendent | 1× Class A |

### Ultimate Skill Requirements

Ultimate Skill (`legendary`) type skills have additional requirements:
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

This creates a reviewable batch under `intake/skill-batches/` with detected
canonical skills, proposed new skills, and similarity hints. These batch records
are canonical intake records, but they are not DAG nodes until maintainers
promote accepted skills into `graph/gaia.json`.

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
1. Contributor opens a draft intake PR containing `intake/skill-batches/<batchId>.json`.
2. Reviewers mark each proposed skill as `accept`, `rename`, `duplicate`, `needs-evidence`, or `reject`.
3. Maintainers promote accepted draft skills into `graph/gaia.json` in a separate canonical graph PR.

### Canonical Graph Changes

1. **Fork** this repository.
2. **Edit `graph/gaia.json`** directly — this is the only source of truth.
   - Add your skill node to the `skills` array.
   - Add any edge records to the `edges` array.
3. **Do NOT** edit files in `skills/`, `registry.md`, or `combinations.md` — these are generated.
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
- `[atomic] parse-csv — adds CSV parsing as a primitive Intrinsic Skill`
- `[composite] autonomous-debug — combines code-generation + execute-bash + error-interpretation`
- `[reclassify] web-scrape — upgrade from Awakened (II) to Named (III) with new evidence`

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
| **Invalid graph** | PR introduces a cycle, missing parent reference, or orphaned composite. |
| **Inflated rarity** | Rarity is declared rather than computed from prevalence data. |
| **Ambiguous definition** | The skill description is vague, overlapping, or not falsifiable. |
| **Hand-edited generated files** | Changes were made to `skills/`, `registry.md`, or `combinations.md` instead of `gaia.json`. |
| **Legendary without approval** | Ultimate Skill submitted without meeting the 3-source / 2-approval bar. |

---


## Community Skill Source Research

For contributors researching candidate skills from the broader SKILL.md ecosystem, see `docs/skill_source_contributions.md` for a curated list of commonly used repositories and extraction notes.

## Questions?

Open an issue with the `question` label or start a discussion in the Discussions tab.
