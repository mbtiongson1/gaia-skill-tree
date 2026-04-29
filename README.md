# Gaia — AI Agent Skill Registry

> The open, evidence-backed skill graph for AI agents — collect, evolve, and fuse capabilities into something legendary.

[![Validate](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml/badge.svg)](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The Tree

Every AI agent capability exists somewhere on this graph. Skills start **Dormant**, awaken through evidence, evolve through use, and fuse into things greater than the sum of their parts.

```
GAIA SKILL GRAPH  v0.2.0
═════════════════════════════════════════════════════════════════

◆ ULTIMATE SKILLS  (7)  — Evidence-locked. One agent per era.
│
├─ ◆ True Dragon: Autonomous Scientific Discovery     [IV · Evolved]
├─ ◆ True Oracle: Autonomous Data Scientist           [IV · Evolved]
├─ ◆ True Herald: Real-Time Voice Assistant           [IV · Evolved]
├─ ◆ True Craftsman: Full-Stack Developer             [IV · Evolved]
├─ ◆ Grand Conductor: Multi-Agent Orchestration       [I · Dormant]
├─ ◆ True Sage: Recursive Self-Improvement            [I · Dormant]
└─ ◆ Wisdom King: Autonomous Research Agent           [I · Dormant]

◇ EXTRA SKILLS  (22)  — Emerged from combination. Transcend their parts.
│
├─ ◇ Research              [III · Named]    ← Web Search + Summarize + Cite Sources
├─ ◇ RAG Pipeline          [III · Named]    ← Retrieve + Chunk Document + Embed Text + Score Relevance
├─ ◇ Autonomous Debug      [III · Named]    ← Code Generation + Execute Bash + Error Interpretation
└─ ◇ ...and 19 more

○ INTRINSIC SKILLS  (49)  — Atomic. The genome of every agent.
│
├─ ○ Code Generation       [II · Awakened]
├─ ○ Web Search            [II · Awakened]
└─ ○ ...and 47 more

→ Full graph: tree.md
```

---

## What This Means for You

- **Track your agent's capabilities** — every skill your agent demonstrates gets logged to your personal skill tree, tied to your GitHub identity, portable across every repo you own.
- **Unlock combinations** — when your agent has the prerequisites, a new composite or ultimate skill becomes available to fuse. The CLI detects it automatically.
- **Contribute to the canon** — submit evidence for new skills or level-ups via PR. The graph grows with the field.

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
| I | **Dormant** | None | Catalogued but not yet demonstrated |
| II | **Awakened** | Class C | First confirmed demonstration |
| III | **Named** | Class B | Reproducible, fully documented |
| IV | **Evolved** | Class B or A | Failure modes known; battle-tested |
| V | **Transcendent** | Class A | Composable and self-improving; peer-reviewed |

---

## Quickstart

```bash
git clone https://github.com/mbtiongson1/gaia-skill-tree.git
cd gaia-skill-tree

# Validate the canonical graph
python3 scripts/validate.py

# Regenerate all skill pages, registry, tree, and user trees
python3 scripts/generateProjections.py
```

## Real Skill Catalog

Gaia also keeps a curated catalog of real-world named `SKILL.md` entries before they are promoted into the canonical graph:

- Source data: [`graph/real_skill_catalog.json`](graph/real_skill_catalog.json)
- Generated HTML: [`real-skills.html`](real-skills.html)
- Generated Markdown: [`real-skills.md`](real-skills.md)

Use this catalog to bucket popular named skills from sources such as VoltAgent's Awesome Agent Skills, AgentSkills.me, official skill pages, and Superpowers. The canonical DAG still lives in `graph/gaia.json`; the real skill catalog is a review surface for source-backed names and Gaia mappings.

## Install the Plugin (per-repo)

> **Status: In Development** — The `gaia` CLI is not yet published to npm. Track progress or contribute in [plugin/](plugin/).

```bash
# Initialize Gaia in your project
gaia init

# Scan for skills your agent demonstrates
gaia scan

# Submit a batch of detected known/proposed skills for review
gaia push

# View your skill tree
gaia status
gaia tree --depth 3

# Fuse a detected combination
gaia fuse autonomous-debug
```

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
├── plugin/                  ← CLI + GitHub Action for per-repo integration
├── registry.md              ← GENERATED flat index of all skills
├── combinations.md          ← GENERATED fusion recipe matrix
├── tree.md                  ← GENERATED full ASCII skill graph
├── real-skills.html         ← GENERATED linked catalog of real named skills
├── CONTRIBUTING.md          ← How to contribute
└── docs/                    ← Governance, design spec, examples
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines including evidence requirements, PR templates, and naming conventions.

## License

MIT — see [LICENSE](LICENSE).

---

*Graph is canonical. Everything else is a shadow.*
