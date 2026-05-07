---
name: gaia-audit
description: Review one Gaia skill, named skill, or real-skill catalog item for outdated, superseded, overpromoted, weakly sourced, or incorrectly mapped evidence. Use when the user asks to audit a specific skill or says a listed skill may not deserve its current rank.
version: 1.0.0
---

# gaia-audit

Audit exactly one Gaia skill, named skill, or real-skill catalog item and submit the smallest source-level correction.

## Workflow

1. Identify the target:
   - Canonical skill: `registry/gaia.json`
   - Named skill: `registry/named/<contributor>/<skill>.md`
   - Real-skill catalog item: `registry/real-skills.json`
2. Search the repo for every occurrence of the target with `rg`.
3. Re-check current source evidence. Prefer direct `SKILL.md`, paper, benchmark, release note, or reproducible repo URLs over directory listings or homepages.
4. Separate these questions:
   - Does the skill exist?
   - Does it map to the claimed Gaia capability?
   - Does it justify its level, rarity, named status, or `promotedNamedSkillId`?
   - Is it outdated, superseded, overpromoted, duplicate, or under-sourced?
5. Present findings first. If a correction is warranted, edit only source-of-truth files:
   - `registry/gaia.json`
   - `registry/named/**`
   - `registry/real-skills.json`
   - reviewer policy docs when criteria are missing
6. Regenerate outputs:
   ```bash
   python3 scripts/generateProjections.py
   python3 scripts/syncDocsGraphAssets.py
   PYTHONPATH=src python3 scripts/build_docs.py
   ```
7. Verify:
   ```bash
   ./.venv/bin/python scripts/validate.py
   ./.venv/bin/python scripts/validate_intake.py
   PYTHONPATH=src ./.venv/bin/python -m unittest tests.test_real_skill_catalog tests.test_named_skills tests.test_validate
   git diff --check
   ```

## Demotion Rules

- Keep real skills in `registry/real-skills.json` when the source is valid but remove unsupported promotion fields.
- Remove `promotedNamedSkillId` when the item does not justify the named claim.
- Remove or downgrade `status: named`, `title`, or `catalogRef` when reviewer classification is unsupported.
- Remap broad `mapsToGaia` links to narrower accurate IDs when evidence supports only a smaller capability.
- Do not claim Ultimate or Legendary rank from installability or source-directory presence alone.

## Output

Report:
- Evidence checked
- Correction made or reason no change was warranted
- Generated files updated
- Verification commands and results
