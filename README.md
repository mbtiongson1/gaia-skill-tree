# Gaia — AI Agent Skill Registry

> The open, evidence-backed skill graph for AI agents — collect, evolve, and fuse capabilities into something legendary.

[![Validate](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml/badge.svg)](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tutorial](https://img.shields.io/badge/Tutorial-gaia.tiongson.co-38bdf8)](https://gaia.tiongson.co/)

---

## The Tree

Every AI agent capability exists somewhere on this graph. Skills start at the foundation tier, awaken through evidence, evolve through use, and fuse into things greater than the sum of their parts.

The snapshot below shows the upgrade-path structure. Each legendary traces
back through its full prerequisite chain.

```
GAIA SKILL TREE  v1.0.0
═════════════════════════════════════════════════════════════════

◆ Wisdom King: Autonomous Research Agent  [VI · Transcendent ★]
  ├─ ◇ Research  [III · Evolved]  ← Web Search · Summarize · Cite Sources
  │  ├─ ○ Web Search  [I · Awakened]
  │  ├─ ○ Summarize  [I · Awakened]
  │  └─ ○ Cite Sources  [I · Awakened]
  ├─ ◇ Knowledge Harvest  [IV · Transcendent]  ← Web Scrape · Extract Entities · Embed Text
  │  ├─ ◇ Web Scrape  [III · Evolved]  ← Web Search · Parse HTML · Extract Entities
  │  │  ├─ ○ Web Search  [I · Awakened]  (↑ see above)
  │  │  ├─ ○ Parse HTML  [I · Awakened]
  │  │  └─ ○ Extract Entities  [I · Awakened]
  │  ├─ ○ Extract Entities  [I · Awakened]  (↑ see above)
  │  └─ ○ Embed Text  [I · Awakened]
  └─ ◇ Ghostwrite  [IV · Transcendent]  ← Research · Write Report · Audience Model
     ├─ ◇ Research  [III · Evolved]  (↑ see above)
     ├─ ○ Write Report  [I · Awakened]
     └─ ○ Audience Model  [I · Awakened]

→ Full graph: tree.md
```

---

## What This Means for You

- **Track your agent's capabilities** — every skill your agent demonstrates gets logged to your personal skill tree, tied to your GitHub identity, portable across every repo you own.
- **Unlock combinations** — when your agent has the prerequisites, a new composite or ultimate skill becomes available to fuse. The CLI detects it automatically.
- **Name and share skills** — contribute named implementations of generic skills (e.g., `karpathy/autoresearch`), attributed to your GitHub identity and installable by anyone via `gaia install`.
- **Contribute to the canon** — review draft skills, submit evidence, or create new skills from strong reviews. The graph grows with the field.

---

## The Hierarchy

| Tier | Symbol | Display Name | What it means |
|---|---|---|---|
| `atomic` | ○ | **Intrinsic Skill** | Primitive, indivisible capability — the genome of every agent |
| `composite` | ◇ | **Extra Skill** | Emerges from combining 2+ intrinsic skills — transcends its parts |
| `legendary` | ◆ | **Ultimate Skill** | High-complexity emergent capability — strict evidence bar, <1% agent prevalence |

## Rank System

Skills level up through evidence, not declaration:

| Level | Rank | Evidence Floor | What it means |
|---|---|---|---|
| 0 | **Basic** | None | Universal LLM primitive — any capable model does this by default |
| I | **Awakened** | None | Foundation tier — catalogued agent capability |
| II | **Named** | Class C | First confirmed demonstration |
| III | **Evolved** | Class B | Reproducible, fully documented |
| IV | **Hardened** | Class B or A | Failure modes known; battle-tested |
| V | **Transcendent** | Class B or A | Composable and self-improving |
| VI | **Transcendent ★** | Class A | Apex — peer-reviewed, named to the agent who unlocked it |

---

## Tutorial

**New here?** The interactive tutorial at **[gaia.tiongson.co](https://gaia.tiongson.co/)** covers everything visually — skill tiers, the rank system, and the full get-started workflow with copy-paste commands.

---

## Quickstart

```bash
git clone https://github.com/mbtiongson1/gaia-skill-tree.git
cd gaia-skill-tree

# 1. Install the gaia CLI
pip install -e .

# 2. Enable semantic search (strongly recommended)
pip install -e ".[embeddings]"
gaia embed                      # ~30 seconds — run once, re-run when the graph changes

# 3. Validate the canonical graph
gaia --registry . scan

# 4. Regenerate all skill pages, registry, tree, and user trees
python3 scripts/generateProjections.py
```

## Real Skill Catalog

Gaia also keeps a curated catalog of real-world named `SKILL.md` entries before they are promoted into the canonical graph:

- Source data: [`graph/real_skill_catalog.json`](graph/real_skill_catalog.json)
- Generated HTML: [`real-skills.html`](real-skills.html)
- Generated Markdown: [`real-skills.md`](real-skills.md)

Use this catalog to bucket popular named skills from sources such as VoltAgent's Awesome Agent Skills, AgentSkills.me, official skill pages, and Superpowers. The canonical DAG still lives in `graph/gaia.json`; the real skill catalog is a review surface for source-backed names and Gaia mappings.

## Install the Plugin (per-repo)

Write the SVG somewhere specific:

```bash
gaia graph -o graph/gaia.svg --no-open
```

Generate browser-friendly layout JSON instead of SVG:

```bash
gaia graph --format json -o graph/render/latest.json --no-open
```

For graph tools such as Gephi or Cytoscape, regenerate the GEXF export:

```bash
python3 scripts/exportGexf.py
```

The public Pages experience also mirrors downloadable graph artifacts under `docs/graph/` so the site can offer JSON, GEXF, and SVG downloads.

### Typical workflow

```bash
# In the project repo you want to scan
gaia init

# Preview detected skills and proposed intake
gaia scan
gaia push --dry-run

# Submit the batch intake record for review
gaia push
```

Intake PRs are draft review artifacts. Accepted candidates are promoted later
into canonical `graph/gaia.json` updates.

### Maintainer hooks

Contributors who edit the canonical graph can install the repo-local hook once:

```bash
bash scripts/install-git-hooks.sh
```

The pre-commit hook runs validation, regenerates Markdown projections, exports GEXF, renders `graph/gaia.svg`, mirrors public graph assets into `docs/graph/`, and stages the known generated files whenever staged graph source files change.

## MCP Server (Agent-Native Integration)

> **Status: In Development** — `@gaia-registry/mcp-server` is not yet published to npm. See [mcp-server/](mcp-server/) to run it locally or contribute.

The fastest way to use Gaia — connect it directly to your agent (Claude Code, Cursor, VS Code, etc.) via MCP:

```json
{
  "mcpServers": {
    "gaia": {
      "command": "npx",
      "args": ["@gaia-registry/mcp-server"],
      "env": { "GAIA_USER": "your-github-username" }
    }
  }
}
```

Once connected, your agent gets these tools:

| Tool | What it does |
|------|-------------|
| `gaia_lookup` | Search skills by ID or fuzzy name |
| `gaia_suggest` | Get fusion recommendations from your current context |
| `gaia_scan_context` | Detect skills from connected tools and project signals |
| `gaia_my_tree` | View your skill tree and stats |
| `gaia_propose` | Claim a fusion or propose a novel skill (opens PR) |

The MCP server also exposes resources at `gaia://registry` and `gaia://tree/{username}`.

See [`mcp-server/`](mcp-server/) for full documentation.

---

## Repository Structure

```
gaia-skill-tree/
├── graph/gaia.json          ← CANONICAL source (the only file humans edit)
├── graph/real_skill_catalog.json ← Curated real-world named skills
├── mcp-server/              ← TypeScript MCP server (agent-native integration)
├── schema/                  ← JSON Schema definitions
├── skills/                  ← GENERATED skill pages (atomic, composite, legendary)
├── users/                   ← Personal skill trees by GitHub username
├── scripts/                 ← Validation, projection, and analysis scripts
├── scripts/crawlers/        ← Bot crawlers (MCP registries, npm, VS Code, HuggingFace)
├── src/gaia_cli/            ← Python package source for the gaia CLI (pip-installable)
├── plugin/                  ← TypeScript CLI wrapper + GitHub Action for per-repo integration
├── pyproject.toml           ← Package metadata and optional dependencies (e.g. [embeddings])
├── registry.md              ← GENERATED flat index of all skills
├── combinations.md          ← GENERATED fusion recipe matrix
├── tree.md                  ← GENERATED full ASCII skill graph
├── real-skills.html         ← GENERATED linked catalog of real named skills
├── CONTRIBUTING.md          ← How to contribute
└── docs/                    ← Governance, design spec, examples
```

---

## Contributing

Gaia is meant to be a shared map of agent capabilities, and there are a few
good ways to help even if you are not ready to edit the graph directly.

You can contribute by **reviewing skill drafts**: read a proposed skill, check
whether the definition is clear, compare it against existing skills, evaluate
the cited evidence, and submit peer review analysis that helps maintainers
decide whether the skill should be accepted, renamed, merged, or reclassified.

You can also contribute by **creating skills directly from reviews**: turn a
well-supported review into a concrete Intrinsic Skill, Extra Skill, Ultimate
Skill, fusion recipe, or reclassification PR with evidence and rationale.

For full instructions, including evidence requirements, PR templates, naming
rules, and reviewer criteria, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

---

*Graph is canonical. Everything else is a shadow.*
