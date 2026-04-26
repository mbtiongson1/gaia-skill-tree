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
| New atomic skill | `new_atomic_skill.md` | Adding a primitive capability to `gaia.json` |
| New composite skill | `new_composite_skill.md` | Adding a skill with 2+ prerequisites to `gaia.json` |
| New fusion recipe | `new_fusion.md` | Adding edge records to `gaia.json` |
| Reclassification | `reclassification.md` | Changing level or rarity of an existing skill |
| New user tree | `new_user_tree.md` | Registering your first skill tree in `users/` |

---

## Naming Conventions

- **Skill IDs** use `camelCase`: `webScrape`, `parseJson`, `autonomousDebug`.
- **Display names** use Title Case: "Web Scrape", "Parse JSON", "Autonomous Debug".
- **No vendor names** in skill IDs or definitions. Skills must be agent-agnostic.
- **No abbreviations** unless universally understood (`html`, `json`, `api` are fine; `nlp` should be `naturalLanguageProcessing`).
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

| Level | Name | Minimum Evidence |
|---|---|---|
| I | Latent | None |
| II | Emerging | 1× Class C |
| III | Competent | 1× Class B |
| IV | Proficient | 1× Class B or A |
| V | Mastered | 1× Class A |

### Legendary Requirements

Legendary-type skills have additional requirements:
- Minimum **3 Class A or B** evidence sources.
- **2 maintainer approvals** before merge.
- Status must be `validated` at merge (never `provisional`).

---

## How to Submit a PR

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
- `[atomic] Parse CSV — adds CSV parsing as a primitive skill`
- `[composite] Autonomous Debug — combines codeGen + bash + errorInterp`
- `[reclassify] webScrape — upgrade from Level II to Level III with new evidence`

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
| **Naming** | Does the ID follow camelCase conventions? Is it agent-agnostic? |

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
| **Legendary without approval** | Legendary skill submitted without meeting the 3-source / 2-approval bar. |

---

## Questions?

Open an issue with the `question` label or start a discussion in the Discussions tab.
