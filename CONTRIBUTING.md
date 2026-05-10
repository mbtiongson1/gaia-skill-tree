# Contributing to Gaia

Thanks for helping improve the Gaia skill graph.

This page is now a **contributor quickstart**. Detailed policy, reviewer playbooks, and deep troubleshooting now live in the GitHub Wiki repo.

---

---

## 1) Pick your workflow

### A) Submit discovered skills (recommended)

```bash
gaia push
```

Useful variants:

```bash
gaia push --dry-run
gaia push --no-pr
python3 scripts/validate_intake.py
```

Use this when proposing skills via `registry-for-review/skill-batches/*.json`.

### B) Update the canonical graph directly

1. Fork the repo.
2. Edit `registry/gaia.json` (`skills` and/or `edges`).
3. Validate:
   ```bash
   python3 scripts/validate.py
   ```
4. Open a PR using the right template in `.github/PULL_REQUEST_TEMPLATE/`.

---

## 2) What files are source-of-truth?

- ✅ `registry/gaia.json` (canonical graph)
- ✅ `registry-for-review/skill-batches/*.json` (intake batches)
- ❌ Do not hand-edit generated docs/graph projections produced by docs/build pipelines.

---

## 3) Branch naming (copy/paste)

| Prefix | Use for | Scope |
|---|---|---|
| `schema/...` | schema + terminology changes | `registry/schema/` only |
| `cli/...` | CLI / package code | `src/gaia_cli/`, `packages/`, `tests/` |
| `docs/...` | markdown/docs content | `docs/`, `*.md` |
| `design/...` | website UI assets | `docs/` HTML/CSS/JS |
| `review/gaia-push/...` | intake PRs | `registry-for-review/` |
| `review/meta/...` | registry curation | `registry/` (excluding schema) |
| `infra/...` | CI/tooling/config | `.github/`, `scripts/`, config |
| `dev/...` | experiments | unrestricted |
| `feat/...`, `fix/...` | general changes | unrestricted (schema rules still enforced) |

Hard rule: any schema file change must come from a `schema/...` branch.

---

## 4) Naming + evidence minimums

### Naming

- Skill IDs: `kebab-case` (`web-scrape`, `parse-json`)
- Display names: Title Case
- Skill types in graph: `basic`, `extra`, `ultimate`
- Keep skills vendor-agnostic

### Evidence by level

- Level 0–I: no evidence required
- Level II (Named): ≥ 1 Tier C
- Level III (Evolved): ≥ 1 Tier B
- Level IV (Hardened): ≥ 1 Tier B/A
- Level V (Transcendent): ≥ 1 Tier A
- Level VI (Transcendent ★): Tier A + peer review

### Ultimate (`ultimate`) requirements

- At least 3 Tier A/B evidence items
- 2 maintainer approvals
- Must be `validated` at merge

### Demerits and effective level

- Demerits are allowed only on claimed levels `II` and above.
- Allowed demerit IDs are canonical and schema-validated: `niche-integration`, `experimental-feature`, `heavyweight-dependency`.
- Each demerit lowers runtime potential by one level (effective level), floored at `I`.
- Named skill claims stay constrained by canonical level requirements; demerits do not bypass evidence floors.

---

## 5) PR checklist (copy/paste)

- [ ] Correct branch prefix
- [ ] Edited only source-of-truth files
- [ ] Validation command(s) passed
- [ ] Evidence meets level/type requirements
- [ ] PR template selected
- [ ] PR title format:
  ```
  [type] skill-name — short description
  ```

Examples:
- `[basic] parse-csv — add CSV parsing primitive`
- `[extra] autonomous-debug — compose debug workflow`
- `[reclassify] web-scrape — promote with new evidence`

---

## 6) FAQ

**Q: I ran `gaia push`. Are proposed skills already in the DAG?**  
No. Intake batches are review artifacts until accepted skills are promoted into `registry/gaia.json`.

**Q: Where should long-form guidance go?**  
In the [Wiki](https://github.com/mbtiongson1/gaia-skill-tree/wiki) (review standards, curation heuristics, edge cases, troubleshooting).

---

## 7) Helpful links

- [README quickstart](../README.md)
- [Docs site](docs/index.html)
- [Governance](docs/GOVERNANCE.md)
- [Wiki](https://github.com/mbtiongson1/gaia-skill-tree/wiki) · [Wiki git repo](https://github.com/mbtiongson1/gaia-skill-tree.wiki.git)


---

## 8) Demotion and Reclassification Criteria

Use this section for reviewer decisions when a skill should be demoted, remapped, or declassified.

A review is required when evidence shows a skill is:
- **outdated** (implementation or evidence no longer reflects current behavior),
- **superseded** (a better canonical mapping or replacement now exists),
- **overpromoted** (current level exceeds demonstrated evidence tier), or
- supported by **insufficient usage evidence** for its assigned rank.

Reviewer workflow:
- Reviewers should use `/gaia-audit` before approving PRs that demote, declassify, remap, dispute, or re-promote a specific skill.
- Reviewers should use `/gaia-meta-audit` to build queues for stale links, unsupported promotions, possible duplicates, and broad mapping quality checks.
