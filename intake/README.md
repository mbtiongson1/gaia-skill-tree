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

## Skill Lifecycle

Each proposed skill in a batch has a `lifecycle` field:

1. **pending** — Initial state when `gaia push` creates the batch. Awaiting reviewer classification.
2. **awakened** — Reviewer has accepted the skill but it has no named attribution yet. The skill exists in the registry's awareness but isn't tied to a specific implementation.
3. **named** — A contributor has claimed the skill and promoted it to `graph/named/{contributor}/{skill-name}.md`. The skill is now a fully attributed, named implementation.

### Promoting a skill

To promote an awakened skill to named:

```bash
gaia name intake/skill-batches/batch-abc123.json 0 karpathy/autoresearch
```

This creates the named skill file and updates the batch record.
