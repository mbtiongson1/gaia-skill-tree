# Gaia - AI Agent Skill Registry

> The open, evidence-backed skill graph for AI agents: collect, evolve, and fuse capabilities into something legendary.

[![Validate](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml/badge.svg)](https://github.com/mbtiongson1/gaia-skill-tree/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tutorial](https://img.shields.io/badge/Tutorial-gaia.tiongson.co-38bdf8)](https://gaia.tiongson.co/)

---

## The Tree

Every AI agent capability exists somewhere on this graph. Skills start at the foundation tier, awaken through evidence, evolve through use, and fuse into things greater than the sum of their parts.

```text
GAIA SKILL TREE
=======================================================

<<<<<<< HEAD
◆ karpathy/autoresearch - Wisdom King  [6⭐]
  ├─ ◇ /research  [3⭐]
  │  ├─ ○ /web-search  [1⭐]
  │  ├─ ○ /summarize  [0⭐]
  │  └─ ○ /cite-sources  [1⭐]
  ├─ ◇ /knowledge-harvest  [4⭐]
  │  ├─ ◇ /web-scrape  [3⭐] ...
  │  └─ ○ /embed-text  [1⭐]
  └─ ◇ /ghostwrite  [4⭐] ...

◆ /recursive-self-improvement  [5⭐]
  ├─ ◇ /autonomous-debug  [4⭐]
  │  ├─ ○ /code-generation  [1⭐]
  │  ├─ ○ /execute-bash  [1⭐]
  │  └─ ○ /error-interpretation  [1⭐]
  ├─ ○ /evaluate-output  [1⭐]
  └─ ◇ /plan-and-execute  [4⭐] ...
=======
<<<<<<< Updated upstream
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
=======
◆ karpathy/autoresearch - Wisdom King  [6★]
  ├─ ◇ /research  [3★]
  │  ├─ ○ /web-search  [1★]
  │  ├─ ○ /summarize  [0★]
  │  └─ ○ /cite-sources  [1★]
  ├─ ◇ /knowledge-harvest  [4★]
  │  ├─ ◇ /web-scrape  [3★] ...
  │  └─ ○ /embed-text  [1★]
  └─ ◇ /ghostwrite  [4★] ...

◆ /recursive-self-improvement  [5★]
  ├─ ◇ /autonomous-debug  [4★]
  │  ├─ ○ /code-generation  [1★]
  │  ├─ ○ /execute-bash  [1★]
  │  └─ ○ /error-interpretation  [1★]
  ├─ ○ /evaluate-output  [1★]
  └─ ◇ /plan-and-execute  [4★] ...
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split

Full graph: registry/registry.md
Personal renders: generated-output/tree.md and generated-output/tree.html
```

> [!TIP]
> **New here?** The interactive tutorial at **[gaia.tiongson.co](https://gaia.tiongson.co/)** covers everything visually: skill tiers, the rank system, the full get-started workflow, and copy-paste commands.

---

## Skill Tiers & Ranks

| Symbol | Tier | Levels | Evidence floor |
|--------|------|--------|---------------|
<<<<<<< HEAD
| ○ Basic | Primitive, indivisible capability | 0⭐ (F) Unawakened → 1⭐ (D) Awakened | None |
| ◇ Extra | Emerges from combining 2+ basic skills | 2⭐ (C) Named → 3⭐ (B) Evolved → 4⭐ (A) Hardened | C → B → B/A |
| ◆ Ultimate | High-complexity emergent capability | 5⭐ (S) Transcendent → 6⭐ (SS) Transcendent ★ | A → A + peer review |

Skills level up through evidence, not declaration. Each demerit lowers effective level by one (floored at 1⭐, valid for 2⭐+ only).
=======
<<<<<<< Updated upstream
| ○ Basic | Primitive, indivisible capability | 0 (F) Unawakened → I (D) Awakened | None |
| ◇ Extra | Emerges from combining 2+ basic skills | II (C) Named → III (B) Evolved → IV (A) Hardened | C → B → B/A |
| ◆ Ultimate | High-complexity emergent capability | V (S) Transcendent → VI (SS) Transcendent ★ | A → A + peer review |

Skills level up through evidence, not declaration. Each demerit lowers effective level by one (floored at I, valid for II+ only).
=======
| ○ Basic | Primitive, indivisible capability | 0★ (F) Unawakened → 1★ (D) Awakened | None |
| ◇ Extra | Emerges from combining 2+ basic skills | 2★ (C) Named → 3★ (B) Evolved → 4★ (A) Hardened | C → B → B/A |
| ◆ Ultimate | High-complexity emergent capability | 5★ (S) Transcendent → 6★ (SS) Transcendent ★ | A → A + peer review |

Skills level up through evidence, not declaration. Each demerit lowers effective level by one (floored at 1★, valid for 2★+ only).
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split

---

## Install

<!-- gaia:version-start -->
Current Gaia CLI version: `3.1.1`.

Python install:

```bash
pip install gaia-cli
```

npm wrapper alternative:

```bash
npm install -g @gaia-registry/cli
```
<!-- gaia:version-end -->

For registry development, clone and install editable:
```bash
git clone https://github.com/mbtiongson1/gaia-skill-tree.git
cd gaia-skill-tree
pip install -e ".[embeddings]"
```

<details>
<summary>Troubleshooting</summary>

If pip fails, try pipx:
```bash
brew install pipx        # macOS
pipx install gaia-cli
```

Windows — if `gaia` isn't recognized after install:
```powershell
$env:PATH += ";" + (python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))")
```
</details>

## Quickstart

```bash
gaia init --user your-username
gaia update          # pull latest registry + CLI
gaia scan            # detect skills, render tree
gaia appraise        # inspect a skill card
gaia promote web-search   # promote scan-approved candidates
gaia push --dry-run  # preview intake submission
gaia push            # submit for maintainer review
```

`gaia scan` writes `generated-output/promotion-candidates.json`, renders your tree to `generated-output/tree.{html,md}`, and prints detected skills with fusion diagrams.

---

## CLI Reference

<!-- gaia:cli-start -->
```text
usage: gaia [-h] [--registry REGISTRY] [--global] [--version]
            {help,init,scan,pull,tree,push,propose,version,mcp,release,graph,stats,appraise,promote,fuse,docs,update,skills}
            ...

Gaia Registry CLI

positional arguments:
  {help,init,scan,pull,tree,push,propose,version,mcp,release,graph,stats,appraise,promote,fuse,docs,update,skills}
    help                Show command help
    init                Create or update local Gaia config
    scan                Scan configured paths for skill evidence
    pull                Refresh registry data from origin
    update              Pull latest registry and reinstall the CLI
    tree                Show your Gaia skill tree
    push                Prepare detected skills for review
    propose             Propose a single canonical skill as a named PR
    version             Print the Gaia CLI version
    mcp                 Run the bundled Gaia MCP server
    release             Bump release version files
    graph               Generate and open the Gaia skill graph
    stats               Show registry health at a glance
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
  --canon               Show canonical registry data instead of local-first view.

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
  gaia update
  gaia stats
  gaia docs build [--check]
  gaia skills <list|search|info|install|uninstall>
  gaia skills list [--exclude-pending]
  gaia skills search <query> [--exclude-pending]
  gaia skills info <skill_id> [--exclude-pending]
  gaia skills install <skill> [--global | --local]
  gaia skills uninstall <skill_id>

```
<!-- gaia:cli-end -->

---

## MCP Server

`@gaia-registry/mcp-server` connects Gaia to MCP-compatible agents (Claude Code, Cursor, VS Code, etc.).

| Agent | Install |
|-------|---------|
| Claude Code | `claude mcp add gaia -- npx @gaia-registry/mcp-server` |
| Any MCP client | Command: `npx`, args: `@gaia-registry/mcp-server` |

Set `GAIA_USER=your-github-username` and optionally `GITHUB_TOKEN` for PR tools. See [`packages/mcp/`](packages/mcp/) for full docs and agent-specific config examples.

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
 
