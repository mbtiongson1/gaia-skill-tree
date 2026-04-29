# Gaia — AI Agent Skill Registry

> The open, evidence-backed skill graph for AI agents — collect, evolve, and fuse capabilities into something legendary.

[![Validate](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml/badge.svg)](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The Tree

Every AI agent capability exists somewhere on this graph. Skills start **Dormant**, awaken through evidence, evolve through use, and fuse into things greater than the sum of their parts.

The snapshot below is an example of how the graph is rendered. Counts and labels
will drift as the registry evolves.

```
GAIA SKILL GRAPH  example snapshot
═════════════════════════════════════════════════════════════════

◆ ULTIMATE SKILLS  (<1% prevalence)  — Evidence-locked. Exceptionally rare.
│
├─ ◆ True Dragon: Autonomous Scientific Discovery     [IV · Evolved]
├─ ◆ True Oracle: Autonomous Data Scientist           [IV · Evolved]
├─ ◆ True Herald: Real-Time Voice Assistant           [IV · Evolved]
├─ ◆ True Craftsman: Full-Stack Developer             [IV · Evolved]
├─ ◆ Grand Conductor: Multi-Agent Orchestration       [I · Dormant]
├─ ◆ True Sage: Recursive Self-Improvement            [I · Dormant]
└─ ◆ Wisdom King: Autonomous Research Agent           [I · Dormant]

◇ EXTRA SKILLS  (example set)  — Emerged from combination. Transcend their parts.
│
├─ ◇ Research              [III · Named]    ← Web Search + Summarize + Cite Sources
├─ ◇ RAG Pipeline          [III · Named]    ← Retrieve + Chunk Document + Embed Text + Score Relevance
├─ ◇ Autonomous Debug      [III · Named]    ← Code Generation + Execute Bash + Error Interpretation
└─ ◇ ...and more as the registry grows

○ INTRINSIC SKILLS  (example set)  — Atomic. The genome of every agent.
│
├─ ○ Code Generation       [II · Awakened]
├─ ○ Web Search            [II · Awakened]
└─ ○ ...and more as the registry grows

→ Full graph: tree.md
```

---

## What This Means for You

- **Track your agent's capabilities** — every skill your agent demonstrates gets logged to your personal skill tree, tied to your GitHub identity, portable across every repo you own.
- **Unlock combinations** — when your agent has the prerequisites, a new composite or ultimate skill becomes available to fuse. The CLI detects it automatically.
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

## CLI Usage

The Gaia CLI scans an agent/project repository, compares detected skill names
against the canonical Gaia registry, and can submit batch skill intake records
for review.

### Run from this checkout

From the Gaia registry checkout:

```bash
python3 plugin/cli/main.py --help
```

From another project, pass the local Gaia registry path with `--registry`:

```bash
python3 /path/to/gaia-skill-tree/plugin/cli/main.py \
  --registry /path/to/gaia-skill-tree \
  scan
```

If you have a shell wrapper named `gaia`, the same commands become:

```bash
gaia --registry /path/to/gaia-skill-tree scan
gaia --registry /path/to/gaia-skill-tree push --dry-run
gaia --registry /path/to/gaia-skill-tree push
```

### Project setup

Run this inside the project you want Gaia to scan:

```bash
gaia init
```

This creates `.gaia/config.json`:

```json
{
  "gaiaUser": "gaiabot",
  "gaiaRegistryRef": "https://github.com/gaia-registry/gaia",
  "scanPaths": ["scripts", "plugin"],
  "autoPromptCombinations": false
}
```

Update `gaiaUser` and `scanPaths` for your project before scanning.

### Commands

| Command | What it does |
|---|---|
| `gaia init` | Creates `.gaia/config.json` in the current project. |
| `gaia scan` | Scans configured paths and reports detected canonical skills and possible fusions. |
| `gaia push --dry-run` | Prints the batch intake JSON without writing files. |
| `gaia push` | Writes a batch intake record under `intake/skill-batches/` in the registry checkout. |
| `gaia push --no-pr` | Writes a batch intake record without trying to open a PR. |
| `gaia status` | Shows the configured user's registered skill-tree summary. |
| `gaia tree` | Lists unlocked skills for the configured user. |
| `gaia fuse <skillId>` | Adds a pending fusion candidate to the user's skill tree. |

### Typical workflow

```bash
# In the project repo you want to scan
gaia init

# Preview detected skills and proposed intake
gaia --registry /path/to/gaia-skill-tree scan
gaia --registry /path/to/gaia-skill-tree push --dry-run

# Submit the batch intake record for review
gaia --registry /path/to/gaia-skill-tree push
```

Intake PRs are draft review artifacts. Accepted candidates are promoted later
into canonical `graph/gaia.json` updates.

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
