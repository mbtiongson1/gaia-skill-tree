# Gaia - AI Agent Skill Registry

> The open, evidence-backed skill graph for AI agents: collect, evolve, and fuse capabilities into something legendary.

[![Validate](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml/badge.svg)](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tutorial](https://img.shields.io/badge/Tutorial-gaia.tiongson.co-38bdf8)](https://gaia.tiongson.co/)

---

## The Tree

Every AI agent capability exists somewhere on this graph. Skills start at the foundation tier, awaken through evidence, evolve through use, and fuse into things greater than the sum of their parts.

The snapshot below shows two example upgrade paths from the full graph.

```text
GAIA SKILL TREE
=======================================================

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

Full graph: registry/registry.md
Personal renders: generated-output/tree.md and generated-output/tree.html
```

---

## What This Means for You

- **Track your agent's capabilities**: every skill your agent demonstrates gets logged to your personal skill tree, tied to your configured Gaia username, and portable across every repo you own.
- **Unlock combinations**: when your agent has the prerequisites, a new extra or ultimate skill becomes available to fuse. `gaia scan` detects recommendations and writes promotion candidates for you to review.
- **Name and share skills**: contribute named implementations of generic skills, such as `karpathy/autoresearch`, attributed to your identity and installable by anyone via `gaia skills install`. Pending intakes are overlaid in `gaia skills list/search/info` by default.
- **Contribute to the canon**: review draft skills, submit evidence, or create new skills from strong reviews. Curated registry changes live in `registry/`; draft intake lives in `registry-for-review/`.

---

## Tutorial

> [!TIP]
> **New here?** The interactive tutorial at **[gaia.tiongson.co](https://gaia.tiongson.co/)** covers everything visually: skill tiers, the rank system, the full get-started workflow, and copy-paste commands.

---

## The Hierarchy

| Symbol | Tier | What it means |
|---|---|---|
| ○ | **Basic Skill** | Primitive, indivisible capability: the genome of every agent |
| ◇ | **Extra Skill** | Emerges from combining 2+ basic skills and transcends its parts |
| ◆ | **Ultimate Skill** | High-complexity emergent capability with a strict evidence bar |

## Rank System: The Transcendent Line

Skills level up through evidence, not declaration:

| Level | Class | Rank | Evidence Floor | What it means |
|---|---|---|---|---|
| `0` | F | **Unawakened** | None | Universal LLM primitive: any capable model does this by default |
| `I` | D | **Awakened** | None | Foundation tier: catalogued agent capability |
| `II` | C | **Named** | C | First confirmed demonstration |
| `III` | B | **Evolved** | B | Reproducible and fully documented |
| `IV` | A | **Hardened** | B or A | Failure modes known; battle-tested |
| `V` | S | **Transcendent** | A | Composable and self-improving |
| `VI` | SS | **Transcendent ★** | A | Apex: peer-reviewed, named to the agent who unlocked it |

---

## Install

For registry development, use an editable install from the repo root:
```bash
git clone https://github.com/mbtiongson1/gaia-skill-tree.git
cd gaia-skill-tree
pip install -e ".[embeddings]"
pip install gaia-cli
```
If pip fails, run this:
```bash
brew install pipx
pipx install ".[embeddings]"
pipx install gaia-cli
```
Windows Only (one-time setup):
If `gaia` isn't recognized after install, run the command below in PowerShell.
```bash
$env:PATH += ";" + (python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))")
```

<!-- gaia:version-start -->
Current Gaia CLI version: `2.13.1`.

Python install:

```bash
pip install gaia-cli
```

npm wrapper alternative:

```bash
npm install -g @gaia-registry/cli
```
<!-- gaia:version-end -->

## Quickstart
In your terminal:
```bash
gaia init
```
pass `gaia init --user your-username` to override.

```bash
gaia pull
gaia scan
gaia tree
```
`gaia scan` detects skills, writes `generated-output/promotion-candidates.json`, and renders your local tree to `generated-output/tree.html` and `generated-output/tree.md`.
```bash
gaia appraise skill-name
```
Replace `skill-name` with the actual skill listed in the tree. Promotion is scan-gated. `gaia promote <skill>` uses the level recommended by the most recent `generated-output/promotion-candidates.json`, and the scan must be less than 24 hours old.

## Push
Go to your integrated terminal in your repo and run this command after scanning:
```bash
gaia push --dry-run
```
`--dry-run` will only list down your push-able skills. If you want to push it to the registry for review:
```bash
gaia push
```
Note: Make sure not to include sensitive information, otherwise it will be rejected! If found that your /skills are legit, it can be named after you!

### Github CLI issues
[!TIP] `push` command requires Github CLI authentication! Run this in your terminal:
MacOS:
```bash
brew install gh
```
Ubuntu/Debian:
```bash
sudo apt install gh
```
Windows:
```bash
winget install --id GitHub.cli
```
Once installed, run:
```bash
gh auth login
```
Then follow the instructions from the terminal to get yourself authenticated. (Use HTTPS + Browser for easy set up).
## Named Skills Browser

The registry ships an interactive Named Skills browser at [`docs/index.html`](docs/index.html):

- **Level-filtered tabs**: browse by Named (II), Evolved (III), Hardened (IV), or all levels.
- **Expandable cards**: each card shows the contributor, title, description, `genericSkillRef`, tags, and a direct link to the upstream `SKILL.md`.
- **Graph canvas**: node labels show `contributor/skill-name` for named implementations and `/slug` for anonymous skills by default. The **Named Skills** button dims all non-named nodes and highlights named implementations.

Serve locally with `python -m http.server 8080` from the repo root, then open `http://localhost:8080/docs/`.

`docs/graph/*` is a generated GitHub Pages mirror so the `docs/` site can run as a self-contained static site. The canonical files live in `registry/`.

## Real Skill Catalog

Gaia also keeps a curated catalog of real-world named `SKILL.md` entries before they are promoted into the canonical graph:

- Source data: [`registry/real-skills.json`](registry/real-skills.json)
- Generated HTML: [`registry/real-skills.html`](registry/real-skills.html)
- Generated Markdown: [`registry/real-skills.md`](registry/real-skills.md)

Use this catalog to bucket popular named skills from sources such as VoltAgent's Awesome Agent Skills, AgentSkills.me, official skill pages, and Superpowers. The canonical DAG lives in `registry/gaia.json`; the real skill catalog is a review surface for source-backed names and Gaia mappings.

## CLI Usage

### Command Reference

<!-- gaia:cli-start -->
```text
usage: gaia [-h] [--registry REGISTRY] [--global] [--version]
            {help,init,scan,pull,tree,push,propose,version,mcp,release,graph,appraise,promote,fuse,docs,skills}
            ...

Gaia Registry CLI

positional arguments:
  {help,init,scan,pull,tree,push,propose,version,mcp,release,graph,appraise,promote,fuse,docs,skills}
    help                Show command help
    init                Create or update local Gaia config
    scan                Scan configured paths for skill evidence
    pull                Refresh registry data from origin
    tree                Show your Gaia skill tree
    push                Prepare detected skills for review
    propose             Propose a single canonical skill as a named PR
    version             Print the Gaia CLI version
    mcp                 Run the bundled Gaia MCP server
    release             Bump release version files
    graph               Generate and open the Gaia skill graph
    appraise            Inspect a skill card with status and actions
    promote             Promote a skill eligible for level-up
    fuse                Confirm a skill combination or promotion candidate
    docs                Documentation maintenance commands
    skills              Browse and manage named skills

options:
  -h, --help            show this help message and exit
  --registry REGISTRY   Path to a local Gaia registry checkout. Defaults to auto-resolved local or
                        global registry.
  --global, -g          Use global GAIA_HOME registry, ignoring any local .gaia/ config.
  --version, -v         Print the Gaia CLI version and exit.

Quick usage:
  gaia init [--user <name>] [--scan <path>] [--yes]
  gaia scan [--quiet] [--auto-promote]
  gaia pull
  gaia tree [--named] [--title]
  gaia push [--dry-run] [--no-pr]
  gaia propose [<skillId>] [--ultimate] [--target <name>] [--no-pr]
  gaia version
  gaia mcp
  gaia release <patch|minor|major>
  gaia graph [--format html|svg|json] [-o <path>] [--no-open]
  gaia appraise [<skillId>]
  gaia promote [<skillId>] [--all] [--name <name>]
  gaia fuse <skillId> [--name <name>]
  gaia docs build [--check]
  gaia skills <list|search|info|install|uninstall>
  gaia skills list [--exclude-pending]
  gaia skills search <query> [--exclude-pending]
  gaia skills info <skill_id> [--exclude-pending]
  gaia skills install <skill> [--global | --local]
  gaia skills uninstall <skill_id>

```
<!-- gaia:cli-end -->

### Commands

| Command | What it does |
|---|---|
| `gaia init` | Creates `.gaia/config.toml`, asks for or accepts `--user`, and creates a stub user tree when run inside a registry clone. |
| `gaia scan` | Scans configured paths, writes `generated-output/promotion-candidates.json`, and renders `generated-output/tree.{html,md}`. |
| `gaia scan --auto-promote` | Runs scan, promotes every scan-approved candidate, and re-renders the tree. |
| `gaia pull` | Refreshes registry data from `origin`. |
| `gaia push` | Writes a batch intake record under `registry-for-review/skill-batches/` and opens a PR when possible. |
| `gaia appraise [skillId]` | Renders a skill card and shows what the last scan flagged as promotable. |
| `gaia promote <skill>` | Promotes only if the skill appeared in the last scan candidates; Gaia uses the scan-suggested level. |
| `gaia promote --all` | Promotes every valid candidate from the last scan. |
| `gaia tree` | Renders your personal tree to `generated-output/tree.html` and `generated-output/tree.md`. |
| `gaia graph` | Generates and opens `registry/render/gaia.html`; use `--format svg` for `registry/gaia.svg` or `--format json` for render JSON. |
| `gaia version`, `gaia --version`, `gaia -v` | Prints the CLI version. |
| `gaia mcp` | Runs the bundled MCP server from `packages/mcp`. |
| `gaia release {patch|minor|major}` | Maintainer release bump across Python, npm, MCP, and registry versions. |
| `gaia docs build` | Regenerates marker-owned docs sections and docs-site stats. |
| `gaia docs build --check` | Fails if generated docs have drifted. |
| `gaia skills list/search/info/install/uninstall` | Browses and manages named skills, overlaying your pending intake by default. |

### Typical Workflow

```bash
# In the project repo you want Gaia to scan
gaia init --user your-username

# Detect skills and render your tree
gaia scan
gaia appraise

# Promote only scan-approved candidates
gaia promote web-search

# Submit draft skill intake for maintainer review
gaia push --dry-run
gaia push
```

Intake PRs are draft review artifacts. Accepted candidates are promoted later into canonical `registry/gaia.json` updates.

## MCP Server (Agent-Native Integration)

`@gaia-registry/mcp-server` connects Gaia directly to MCP-compatible agents such as Claude Code, Cursor, VS Code, and others:

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
| `gaia_propose` | Claim a fusion or propose a novel skill |

The MCP server also exposes resources at `gaia://registry` and `gaia://tree/{username}`.

See [`packages/mcp/`](packages/mcp/) for full documentation.

---

## Repository Structure

<!-- gaia:layout-start -->
```text
registry/                 curated registry data and public generated catalogs
registry-for-review/      pending skill batch intake records
skill-trees/              per-user skill-tree.json files
generated-output/         ignored local scan and render output
docs/                     docs site
src/gaia_cli/             Python CLI package
packages/cli-npm/         npm wrapper package
packages/mcp/             MCP server package
scripts/                  validation, rendering, docs, and release helpers
tests/                    Python test suite
```
<!-- gaia:layout-end -->

Important files:

```text
registry/gaia.json               canonical source graph
registry/named/                  named skill implementations
registry/named-skills.json       generated named skill index
registry/real-skills.json        upstream catalog of real-world named skills
registry/skills/                 generated skill pages
registry/schema/                 JSON Schema definitions
registry-for-review/             draft batch proposals from gaia push
skill-trees/                     personal skill trees by username
generated-output/                local scan output and personal renders, gitignored
docs/graph/                     GitHub Pages mirror of registry graph assets
packages/cli-npm/                npm wrapper and GitHub Action package
packages/mcp/                    TypeScript MCP server
```

---

## Maintainer Hooks

Contributors who edit the canonical graph can install the repo-local hook once:

```bash
bash scripts/install-git-hooks.sh
```

The pre-commit hook checks version lockstep, applies a semantic bump from the commit message, regenerates registry artifacts, runs `gaia docs build`, and stages generated outputs.

## Contributing

Gaia is a shared map of agent capabilities.

Common ways to help:
- Review draft skills for clarity, overlap, and evidence quality.
- Turn accepted reviews into concrete PRs (new skill, fusion, or reclassification).

Quickstart contribution steps: [CONTRIBUTING.md](CONTRIBUTING.md).
Full policy/reviewer guidance: <https://github.com/mbtiongson1/gaia-skill-tree/wiki> (repo: <https://github.com/mbtiongson1/gaia-skill-tree.wiki.git>).

## Contributors

Thank you to everyone who has expanded the Gaia registry.

| Contributor | Contribution |
|---|---|
| [@mbtiongson1](https://github.com/mbtiongson1) | Creator and maintainer: graph design, CLI, MCP server, curation pipeline |
| [@rico-tiongson](https://github.com/rico-tiongson) | Early contributor |
| [@karpathy](https://github.com/karpathy) | Origin named skill: `karpathy/autoresearch` |
| [@mattpocock](https://github.com/mattpocock) | Named skills: diagnose, tdd, to-prd, triage, zoom-out, and 6 others |
| [@intelligentcode-ai](https://github.com/intelligentcode-ai) | Named skills: database-engineer, devops-engineer, mcp-client, security-engineer, and 5 others |
| [@ruvnet](https://github.com/ruvnet) | Named skill: `ruvnet/flow-nexus-swarm` |
| [@GLINCKER](https://github.com/GLINCKER) | Named skill: `glincker/readme-generator` |
| [@spring-ai-alibaba](https://github.com/spring-ai-alibaba) | Named skill: `spring-ai/readme-generate` |
| [@balukosuri](https://github.com/balukosuri) | Evidence: community reproduction of Karpathy's autoresearch as a universal skill |

---

## License

MIT: see [LICENSE](LICENSE).

---

*Graph is canonical. Everything else is a shadow.*
 
