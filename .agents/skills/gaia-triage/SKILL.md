---
name: gaia-triage
description: Triage and audit GitHub issues for the Gaia Skill Tree project. Helps identify stale issues, gather evidence from the codebase, and manage issue lifecycle via GitHub CLI.
---

# Gaia Triage Skill

This skill provides a standardized workflow for auditing and pruning issues in the `gaia-skill-tree` repository.

## Workflow

1.  **Identify Issues**: List open issues using `gh issue list --repo mbtiongson1/gaia-skill-tree`.
2.  **Audit State**: For each issue, verify if the requested feature or bug fix is already present in the codebase.
    - Check `src/gaia_cli/commands/` for CLI features.
    - Check `tests/` for existing coverage.
    - Check `docs/` or `README.md` for documented behavior.
3.  **Gather Evidence**: Document specific files or test runs that prove the issue is resolved or outdated.
4.  **Execute Action**: Use the `gh` CLI to post a "Triage update" comment and optionally close the issue.

## Evidence Checkpoints

Refer to `references/evidence-check.md` for common file paths and verification commands specific to Gaia.

## Commands

### Post Triage Comment
Use this to update an issue with findings without closing it.
```bash
gh issue comment <issue-number> --repo mbtiongson1/gaia-skill-tree --body "Triage update: <your-findings>"
```

### Close Resolved Issue
Use this when the issue is clearly addressed in the current main branch.
```bash
gh issue close <issue-number> --repo mbtiongson1/gaia-skill-tree --reason completed --comment "Closing as implemented/resolved. Evidence: <summary>"
```

## Tips
- Always check `uv.lock` and `pyproject.toml` for dependency-related issues (#181).
- For documentation drift (#182), run `python scripts/build_docs.py --check`.
- For skill registry issues (#119), check `registry/gaia.json`.
