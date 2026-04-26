# Gaia User Skill Trees

This directory contains personal skill tree records, one per GitHub username.

## Structure

```
users/
├── mbtiongson1/
│   ├── skill-tree.json    ← Validated against skillTree.schema.json
│   └── skill-tree.md      ← Generated human-readable projection
└── [your-username]/
    ├── skill-tree.json
    └── skill-tree.md
```

## Identity Model

- Each user's directory is named after their GitHub username.
- Only the owner of a directory can modify its contents.
- Ownership is enforced via `CODEOWNERS` and GitHub Actions OAuth verification.
- You cannot write to another user's skill tree — PRs attempting this will be blocked.

## Getting Started

1. Install the Gaia plugin in your repo: `gaia init`
2. Scan for skills: `gaia scan`
3. When combinations are detected, confirm to create your skill tree.
4. Your first tree registration will open a PR to create `users/[you]/skill-tree.json`.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full details.
