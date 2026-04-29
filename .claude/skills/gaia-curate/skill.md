---
name: gaia-curate
description: Expand the Gaia skill registry with new popular AI agent skills, fully evidenced and validated, then push a PR. Use this skill when the user asks to "update the tree", "add new skills to Gaia", "curate the registry", "expand the skill graph", or explicitly types /gaia-curate.
version: 1.3.0
---

# gaia-curate

Expand the Gaia skill registry (`graph/gaia.json`) with new popular AI agent skills, fully evidenced and validated, then push a PR.

## What this skill does

1. **Read the current graph** — load `graph/gaia.json` to see every existing skill ID so nothing is duplicated.
2. **Research** — identify the most impactful AI agent capabilities not yet in the registry. Prioritise skills with strong public evidence (arXiv papers, reproducible GitHub repos).
3. **Design the batch** — for each candidate skill determine:
   - Type: `atomic` (no prerequisites) / `composite` (≥2 prereqs) / `legendary` (≥3 prereqs + 3 Class A/B sources)
   - Level: target **IV** (Proficient) minimum — requires at least 1× Class B or A evidence
   - Rarity: `common` / `uncommon` / `rare` / `epic` / `legendary`
   - Prerequisites and derivatives (must reference existing IDs)
4. **Present draft for review** — before writing any code or committing, display the full proposed skills table:

   | ID | Name | Type | Rarity | Prereqs | Similarity hints |
   |---|---|---|---|---|---|
   | … | … | … | … | … | … |

   Similarity hints are lexical matches from the existing registry (≥0.45 score). For each proposed skill, ask the user to mark one of:
   - `accept` — proceed as designed
   - `rename <new-id>` — change the ID before generating
   - `duplicate` — already covered by an existing skill; drop it
   - `needs-evidence` — hold until a Class A/B source is supplied
   - `reject` — remove from the batch entirely

   **Do not proceed to step 5 until the user has reviewed and the batch contains at least one `accept`.** Incorporate all `rename` decisions before writing the script. Drop everything that is not `accept`/`rename`.

5. **Write a generation script** (`scripts/add_skills.py` or equivalent) that patches `gaia.json` in place — only for the accepted skills from step 4.
6. **Run validation** — `PYTHONIOENCODING=utf-8 python3 scripts/validate.py` must exit 0 before any commit.
7. **Regenerate derived files** — run `python3 scripts/generateProjections.py` and `python3 scripts/exportGexf.py` so that `registry.md`, `combinations.md`, `skills/**/*.md`, `graph/gaia.gexf`, and `users/*/skill-tree.md` stay in sync. Commit these alongside `gaia.json` to pass CI drift detection.
8. **Commit on a feature branch** — branch name `feat/add-<slug>-skills`, commit message follows `[type] Title — brief description`.
9. **Push and open a PR** via the GitHub API using stored git credentials. The auto-triage CI classifies the PR:
   - PRs touching `graph/` from a bot with evidence score ≥ 60 are auto-merged.
   - PRs flagged `draft-skills` or `needs-review` are routed to the `route-review` job — a human must approve before merge.
   - Legendary skill proposals always require maintainer approval.
10. **Register the batch itself** as a `registryCuration` evidence entry if new demonstrations were produced.

## Two-phase intake workflow (gaia push)

For contributors who use the `gaia push` CLI, a separate **draft intake** path exists that does NOT directly modify `graph/gaia.json`:

1. **`gaia push`** — scans the source repo for skill-shaped tokens, builds `intake/skill-batches/<batchId>.json`, and opens a draft PR with labels `draft-skills` and `needs-review`.
2. **Reviewer classification** — maintainers review the draft PR and mark each proposed skill: `accept` / `rename` / `duplicate` / `needs-evidence` / `reject`.
3. **Promotion PR** — accepted skills are promoted into `graph/gaia.json` in a separate follow-up PR. That PR must run `python3 scripts/validate.py` and `python3 scripts/validate_intake.py` and must link back to the intake PR.

Use `/gaia-draft-curate` to triage pending intake batches before running this skill.

To validate intake batch files locally:
```bash
python3 scripts/validate_intake.py
```

## Constraints

- Only edit `graph/gaia.json` — never touch `skills/`, `registry.md`, or `combinations.md` (those are generated).
- All evidence `source` values must be real, resolvable URLs (arXiv abs pages or GitHub repos).
- Legendary skills at `status: validated` require ≥3 Class A/B entries; new legendaries should be `provisional` until the maintainer merges.
- No cycles in the DAG. No orphaned composite nodes.
- Skill IDs: `lowercase-dash` format (e.g., `chain-of-thought`, `web-search`). No camelCase, no vendor names, no abbreviations unless universally understood. Pattern: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`.
- **Edge schema**: edges use `sourceSkillId`/`targetSkillId` keys (not `from`/`to`). Valid `edgeType` values are `prerequisite`, `corequisite`, `enhances` only — there is NO `derivative` edge type. Use `enhances` for skill→derivative edges.
- **Encoding**: all Python `open()` calls must use `encoding='utf-8'` to avoid CP-1252 drift on Windows (em-dash `—` becomes `0x97` without it, failing CI on Linux).

## Evidence standards (quick reference)

| Class | Standard |
|---|---|
| A | Peer-reviewed paper — use `https://arxiv.org/abs/<id>` |
| B | Reproducible open-source demo — use the GitHub repo URL |
| C | Credible vendor/community demo (only sufficient for Level II) |

## Repo location

Run from the root of your local clone of this repository. If you have not cloned it yet:
```
git clone https://github.com/mbtiongson1/gaia-skill-tree.git
cd gaia-skill-tree
```

## Output

At the end, report:
- PR URL
- Skills added (count by type)
- Validation result summary
- Any existing skills whose `derivatives` arrays were patched
- Review decisions applied (accepted / renamed / dropped)
