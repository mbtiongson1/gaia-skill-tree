# Gaia User Skill Trees

This directory contains personal skill tree records, one per Gaia username.

## Structure

```text
skill-trees/
├── mbtiongson1/
│   ├── skill-tree.json    ← Validated against registry/schema/skillTree.schema.json
│   └── skill-tree.md      ← Generated human-readable projection
└── <your-username>/
    ├── skill-tree.json
    └── skill-tree.md
```

`skill-tree.json` is the durable user-owned record. `skill-tree.md` is a generated projection for humans. New local renders from `gaia scan` and `gaia tree` are written to `generated-output/tree.md` and `generated-output/tree.html`.

## Identity Model

- Each directory is named after the configured Gaia username.
- A user's tree records unlocked skills, evidence, pending combinations, and summary stats.
- Ownership is enforced through repository review rules and CODEOWNERS.
- You should not write to another user's skill tree without explicit review.

## How Skill Trees Grow

1. Run `gaia init --user <you>` in a project.
2. Run `gaia scan` to detect skills and render your local tree.
3. Review `generated-output/promotion-candidates.json` for recommended level-ups.
4. Run `gaia promote <skill>` or `gaia promote --all` to apply only scan-approved promotions. Gaia uses the level suggested by the scan.
5. Run `gaia push` when you want to submit new skill intake for review.

The skill tree is the heart of Gaia: it is the map of what an agent can actually do, how those skills combine, and what evidence supports each level.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full details.
