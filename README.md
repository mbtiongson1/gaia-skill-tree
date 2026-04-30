# Gaia — AI Agent Skill Registry

> The open, evidence-backed skill graph for AI agents — collect, evolve, and fuse capabilities into something legendary.

[![Validate](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml/badge.svg)](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tutorial](https://img.shields.io/badge/Tutorial-gaia.tiongson.co-38bdf8)](https://gaia.tiongson.co/)

---

## The Tree

Every AI agent capability exists somewhere on this graph. Skills start at the foundation tier, awaken through evidence, evolve through use, and fuse into things greater than the sum of their parts.

The snapshot below shows two example upgrade paths from the full graph.

```
GAIA SKILL TREE  v2.1.3
═══════════════════════════════════════════════════════

◆ karpathy/autoresearch - Wisdom King  [VI]
  ├─ ◇ /research  [III]
  │  ├─ ○ /web-search  [I]
  │  ├─ ○ /summarize  [0]
  │  └─ ○ /cite-sources  [I]
  ├─ ◇ /knowledge-harvest  [IV]
  │  ├─ ◇ /web-scrape  [III] ...
  │  └─ ○ /embed-text  [I]
  └─ ◇ /ghostwrite  [IV] ...

◆ /recursive-self-improvement  [V]
  ├─ ◇ /autonomous-debug  [IV]
  │  ├─ ○ /code-generation  [I]
  │  ├─ ○ /execute-bash  [I]
  │  └─ ○ /error-interpretation  [I]
  ├─ ○ /evaluate-output  [I]
  └─ ◇ /plan-and-execute  [IV] ...

→ Full graph: tree.md
```

---

## What This Means for You

- **Track your agent's capabilities** — every skill your agent demonstrates gets logged to your personal skill tree, tied to your GitHub identity, portable across every repo you own.
- **Unlock combinations** — when your agent has the prerequisites, a new extra or ultimate skill becomes available to fuse. The CLI detects it automatically.
- **Name and share skills** — contribute named implementations of generic skills (e.g., `karpathy/autoresearch`), attributed to your GitHub identity and installable by anyone via `gaia install`. Submit with `status: awakened`; a reviewer promotes to `status: named` after confirming the real-world identity. Browse all named skills at [`docs/index.html`](docs/index.html) or the live tutorial site.
- **Contribute to the canon** — review draft skills, submit evidence, or create new skills from strong reviews. The graph grows with the field.

---

## Tutorial

> [!TIP]
> **New here?** The interactive tutorial at **[gaia.tiongson.co](https://gaia.tiongson.co/)** covers everything visually — skill tiers, the rank system, and the full get-started workflow with copy-paste commands.

---

## The Hierarchy

| Tier | Symbol | Display Name | What it means |
|---|---|---|---|
| basic | ○ | **Basic Skill** | Primitive, indivisible capability — the genome of every agent |
| extra | ◇ | **Extra Skill** | Emerges from combining 2+ basic skills — transcends its parts |
| ultimate | ◆ | **Ultimate Skill** | High-complexity emergent capability — strict evidence bar, <1% agent prevalence |

## Rank System — The Transcendent Line

Skills level up through evidence, not declaration:

| Level | Rank | Evidence Floor | What it means |
|---|---|---|---|
| `0` | **Basic** | None | Universal LLM primitive — any capable model does this by default |
| `I` | **Awakened** | None | Foundation tier — catalogued agent capability |
| `II` | **Named** | Class C | First confirmed demonstration |
| `III` | **Evolved** | Class B | Reproducible, fully documented |
| `IV` | **Hardened** | Class B or A | Failure modes known; battle-tested |
| `V` | **Transcendent** | Class B or A | Composable and self-improving |
| `VI` | **Transcendent ★** | Class A | Apex — peer-reviewed, named to the agent who unlocked it |

---

## Quickstart

```bash
# ── Works on Windows, macOS, and Linux — copy-paste the whole block ──────

git clone https://github.com/mbtiongson1/gaia-skill-tree.git
cd gaia-skill-tree

pip install -e ".[embeddings]"  # install CLI + semantic search support

# ── Windows only: if `gaia` is not recognized after install ──────────────
# Run this in PowerShell to add the user Scripts folder to your PATH:
#   $env:PATH += ";" + (python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))")
# To persist across sessions, add that path via System → Environment Variables → Path.
# ─────────────────────────────────────────────────────────────────────────

gaia init                        # auto-detects your GitHub username and
                                 # skill files (AGENTS.md, SKILLS.md,
                                 # .gemini/, .claude/skills/, etc.)

gaia embed                       # build vector index (~30 s, run once)

gaia --registry . scan           # detect skills in your repo and show
                                 # available fusions

gaia --registry . appraise       # inspect your most recent skill card
```

## Named Skills Browser

The registry ships an interactive Named Skills browser at [`docs/index.html`](docs/index.html):

- **Level-filtered tabs** — browse by Named (II), Evolved (III), Hardened (IV), or all levels.
- **Expandable cards** — each card shows the contributor, title, description, `genericSkillRef`, tags, and a direct link to the upstream SKILL.md.
- **Graph canvas** — node labels show `contributor/skill-name` for named implementations (e.g. `karpathy/autoresearch`) and `/slug` for anonymous skills by default. The **Named Skills** button dims all non-named nodes and adds a coloured ring glow to highlight named implementations.

Serve locally with `python -m http.server 8080` from the repo root, then open `http://localhost:8080/docs/`.

## Real Skill Catalog

Gaia also keeps a curated catalog of real-world named `SKILL.md` entries before they are promoted into the canonical graph:

- Source data: [`graph/real_skill_catalog.json`](graph/real_skill_catalog.json)
- Generated HTML: [`real-skills.html`](real-skills.html)
- Generated Markdown: [`real-skills.md`](real-skills.md)

Use this catalog to bucket popular named skills from sources such as VoltAgent's Awesome Agent Skills, AgentSkills.me, official skill pages, and Superpowers. The canonical DAG still lives in `graph/gaia.json`; the real skill catalog is a review surface for source-backed names and Gaia mappings.

## CLI Usage

Install once from the repo root:

```bash
pip install -e .
```

Then `gaia` works from any directory — no path prefix needed.

### Project setup

```bash
gaia init                        # auto-detects GitHub username and skill files
gaia init --user your-username   # override the detected username
```

### Commands

| Command | What it does |
|---|---|
| `gaia init` | Creates `.gaia/config.json`. Auto-detects GitHub username from git remote and skill files (AGENTS.md, SKILLS.md, .claude/skills/, .gemini/, etc.). Supports `--user`, `--registry-ref`, and `--scan` overrides. |
| `gaia doctor` | Checks CLI/config/registry health and reports missing setup pieces. |
| `gaia scan` | Scans configured paths and reports detected canonical skills and possible fusions. |
| `gaia push --dry-run` | Prints the batch intake JSON without writing files. |
| `gaia push` | Writes a batch intake record under `intake/skill-batches/` in the registry checkout. |
| `gaia push --no-pr` | Writes a batch intake record without trying to open a PR. |
| `gaia name <batch> <index> <contributor/skill>` | Promotes an awakened skill from intake to a named skill in `graph/named/`. |
| `gaia install <contributor/skill>` | Downloads a named skill into the repo (global cache + repo reference). |
| `gaia install --list` | Lists all installed named skills. |
| `gaia sync` | Updates installed named skills from their registry origin. |
| `gaia uninstall <contributor/skill>` | Removes an installed named skill. |
| `gaia embed` | Pre-computes embeddings for all skills. Run once after `pip install -e ".[embeddings]"`, re-run when the graph changes. |
| `gaia search <query>` | Semantic search across generic and named skills (requires embeddings). |
| `gaia graph` | Generates `graph/gaia.svg` from the canonical registry and opens it in your browser. |
| `gaia graph -o graph/gaia.svg --no-open` | Writes a graph image to a custom path without opening it. |
| `gaia status` | Shows the configured user's registered skill-tree summary. |
| `gaia tree` | Lists unlocked skills for the configured user. |
| `gaia fuse <skillId>` | Adds a pending fusion candidate to the user's skill tree. |
| `gaia appraise [skillId]` | Renders a skill card with prereq status, derivatives, and contextual actions. Defaults to the most recently unlocked skill. |
| `gaia promote [skillId] [--name "Display Name"]` | Advances an eligible skill to the next level. Optionally renames your named variant. |
| `gaia paths` | Shows a progression summary: skills ready to fuse, one prerequisite away, and all reachable paths. |

### View the skill graph

```bash
gaia graph                                              # generate and open SVG
gaia graph -o graph/gaia.svg --no-open                 # write to specific path
gaia graph --format json -o graph/render/latest.json   # browser-friendly JSON
python scripts/exportGexf.py                           # Gephi/Cytoscape GEXF
```

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
├── graph/gaia.json               ← CANONICAL source (the only file humans edit)
├── graph/named/                  ← Named skill implementations ({contributor}/{skill-name}.md)
├── graph/named/index.json        ← GENERATED bucket index (named + awaitingClassification + byContributor)
├── graph/real_skill_catalog.json ← Upstream catalog of real-world named skills
├── graph/embeddings.json         ← GENERATED skill embeddings (sentence-transformers)
├── graph/similarity.json         ← GENERATED pairwise similarity scores
├── intake/                       ← Batch skill proposals submitted by gaia push
├── mcp-server/                   ← TypeScript MCP server (agent-native integration)
├── schema/                       ← JSON Schema definitions
├── schema/realSkillCatalog.schema.json ← Schema for graph/real_skill_catalog.json
├── skills/                       ← GENERATED skill pages (basic, extra, ultimate)
├── users/                        ← Personal skill trees by GitHub username
├── scripts/                      ← Validation, projection, and analysis scripts
├── scripts/crawlers/             ← Bot crawlers (MCP registries, npm, VS Code, HuggingFace)
├── src/gaia_cli/                 ← Python package source for the gaia CLI (pip-installable)
├── plugin/                       ← TypeScript CLI wrapper + GitHub Action for per-repo integration
├── pyproject.toml                ← Package metadata and optional dependencies (e.g. [embeddings])
├── registry.md                   ← GENERATED flat index — connected skills + Pure/Undeveloped section
├── combinations.md               ← GENERATED fusion recipe matrix
├── tree.md                       ← GENERATED full ASCII skill graph
├── real-skills.html              ← GENERATED linked catalog of real named skills
├── CONTRIBUTING.md               ← How to contribute
└── docs/                         ← Governance, design spec, examples
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


## Contributors

Thank you to everyone who has expanded the Gaia registry.

| Contributor | Contribution |
|---|---|
| [@mbtiongson1](https://github.com/mbtiongson1) | Creator & maintainer — graph design, CLI, MCP server, curation pipeline |
| [@rico-tiongson](https://github.com/rico-tiongson) | Early contributor |
| [@karpathy](https://github.com/karpathy) | Origin named skill: `karpathy/autoresearch` (AutoResearch — The Scholar's Compass) |
| [@mattpocock](https://github.com/mattpocock) | Named skills: diagnose, tdd, to-prd, triage, zoom-out, and 6 others |
| [@intelligentcode-ai](https://github.com/intelligentcode-ai) | Named skills: database-engineer, devops-engineer, mcp-client, security-engineer, and 5 others |
| [@ruvnet](https://github.com/ruvnet) | Named skill: `ruvnet/flow-nexus-swarm` (Grand Conductor: Multi-Agent Orchestration) |
| [@GLINCKER](https://github.com/GLINCKER) | Named skill: `glincker/readme-generator` (Write Report) |
| [@spring-ai-alibaba](https://github.com/spring-ai-alibaba) | Named skill: `spring-ai/readme-generate` |
| [@balukosuri](https://github.com/balukosuri) | Evidence: community reproduction of Karpathy's autoresearch as a universal skill |

---

## License

MIT — see [LICENSE](LICENSE).

---

*Graph is canonical. Everything else is a shadow.*
