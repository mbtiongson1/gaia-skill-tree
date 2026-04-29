# Gaia Skill Registry

Gaia maps AI agent capabilities as a composable skill tree: intrinsic skills, extra skills, and ultimate skills connected by prerequisite relationships.

This page is a lightweight, read-only entrypoint for browsing the registry from GitHub Pages.

## Browse the registry

- [Skill Registry](../registry.md) — canonical generated list of skills, levels, rarity, and evidence links.
- [Skill Tree](../tree.md) — hierarchy-oriented view of the graph.
- [Fusion Recipes](../combinations.md) — prerequisite combinations that produce composite skills.

## Contribute

- [Contributing Guide](../CONTRIBUTING.md) — contribution types, naming rules, evidence requirements, and PR workflow.
- [Skill Source Contributions](./skill_source_contributions.md) — source research notes for broader skill discovery.

## Source of truth

The canonical graph lives in [`graph/gaia.json`](../graph/gaia.json). Files such as `registry.md`, `tree.md`, `combinations.md`, and generated skill pages are projections from that graph.

For graph changes, edit `graph/gaia.json` and run:

```bash
python3 scripts/validate.py
python3 scripts/generateProjections.py
```
