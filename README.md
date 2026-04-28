# Gaia — AI Agent Skill Registry

> An open, graph-first registry of every AI agent skill in existence.

[![Validate](https://github.com/gaia-registry/gaia/actions/workflows/validate.yml/badge.svg)](https://github.com/gaia-registry/gaia/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is Gaia?

Gaia is both a **canonical dataset** and a **gamified progression system** for AI agent capabilities. Every skill is a node in a directed acyclic graph (DAG) — atomic primitives compose into higher-order composites, which compose into legendary-tier emergent capabilities.

Skills are evidence-backed, level up through validated demonstrations, and combine into new skills through a fusion system. Your personal **skill tree** follows your GitHub identity across every repository you own.

## Quickstart

```bash
# Clone the registry
git clone https://github.com/gaia-registry/gaia.git
cd gaia

# Validate the canonical graph
python3 scripts/validate.py

# Generate projections (skills/*.md, registry.md, combinations.md)
python3 scripts/generateProjections.py
```

## Install the Plugin (per-repo)

```bash
# Initialize Gaia in your project
gaia init

# Scan for skills
gaia scan

# Submit a batch of detected known/proposed skills for review
gaia push

# View your skill tree
gaia status
gaia tree --depth 3

# Fuse detected combinations
gaia fuse autonomousDebug
```

## Repository Structure

```
gaia/
├── graph/gaia.json          ← CANONICAL source of truth (the only file humans edit)
├── graph/similarity.json    ← Similarity/layout metadata, separate from DAG edges
├── intake/                  ← Batch skill proposals submitted by gaia push
├── schema/                  ← JSON Schema definitions
├── skills/                  ← GENERATED skill pages (atomic, composite, legendary)
├── users/                   ← Personal skill trees by GitHub username
├── scripts/                 ← Validation, projection, and analysis scripts
├── plugin/                  ← CLI + GitHub Action for per-repo integration
├── registry.md              ← GENERATED flat index of all skills
├── combinations.md          ← GENERATED fusion recipe matrix
├── CONTRIBUTING.md          ← How to contribute
└── docs/                    ← Governance, examples, frontier reports
```

## Key Concepts

| Concept | Description |
|---|---|
| **Atomic** | A primitive, indivisible AI agent capability (e.g., `tokenize`, `classify`) |
| **Composite** | Emerged from combining 2+ skills (e.g., `webScrape` = `webSearch` + `parseHtml` + `extractEntities`) |
| **Legendary** | High-complexity emergent skill with strict evidence bar and <1% agent prevalence |
| **Fusion** | Combining detected prerequisite skills to unlock a new composite or legendary |
| **Skill Tree** | Your personal record of unlocked skills, portable across all your repos |
| **Level (I–V)** | Proficiency from Latent → Mastered, determined by evidence quality |
| **Rarity** | Computed from real agent prevalence data, never self-declared |

## Evidence Policy

Skills level up through evidence, not declaration:

| Level | Name | Evidence Floor |
|---|---|---|
| I | Latent | None |
| II | Emerging | Class C (credible demo) |
| III | Competent | Class B (reproducible demo) |
| IV | Proficient | Class B or A |
| V | Mastered | Class A (peer-reviewed) |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines including:

- How to propose a new skill
- Evidence requirements and rubric
- PR templates and naming conventions
- Reviewer checklist

## License

MIT — see [LICENSE](LICENSE).

---

*Graph is canonical. Everything else is a shadow.*
