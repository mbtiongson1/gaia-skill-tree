# Gaia Skill Batch Intake

`gaia push` writes reviewable skill batches to `intake/skill-batches/`.

Batch files are canonical intake records, not canonical DAG nodes. Maintainers
review proposed skills in batches, merge similar proposals, and promote accepted
skills into `graph/gaia.json`.

Validate intake records with:

```bash
python3 scripts/validate_intake.py
```
