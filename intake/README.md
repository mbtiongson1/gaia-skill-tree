# Gaia Skill Batch Intake

`gaia push` writes reviewable skill batches to `intake/skill-batches/`.
Use `gaia push --dry-run` to preview and `gaia push --no-pr` to write the batch
without opening a PR.

Batch files are canonical intake records, not canonical DAG nodes. Maintainers
review proposed skills in batches, merge similar proposals, and promote accepted
skills into `graph/gaia.json`.

Typical lifecycle:
1. Contributor runs `gaia push` (or `--no-pr`) to generate the intake batch.
2. Reviewers classify each proposed skill (`accept`, `rename`, `duplicate`, `needs-evidence`, `reject`).
3. Maintainers promote accepted skills via a separate canonical graph PR.

Validate intake records with:

```bash
python3 scripts/validate_intake.py
```
