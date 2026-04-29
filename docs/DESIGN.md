# DESIGN.md — Gaia Skill Registry
**Version:** 0.1.0-draft  
**Status:** In Review  
**Last Updated:** 2026-04-26

---

## 1. Design Philosophy

Gaia has two modes of existence simultaneously: a **dataset** and a **game**. The design must honor both without letting either compromise the other. The graph is rigorous and evidence-backed. The progression is satisfying and portable. These are not in tension — they reinforce each other. You can only unlock a legendary skill if the evidence is real.

Four principles guide every design decision:

1. **Graph is canonical. Everything else is a shadow.** `gaia.json` is the only file humans should ever directly edit. All other representations are generated.
2. **Identity is portable. Not repo-local.** Your skill tree follows your username, not your current working directory.
3. **Detection before declaration.** The system tells you what you've earned. You confirm or reject.
4. **Zero friction for contributors. High bar for data quality.** PRs should be easy to open. Hard to merge badly.

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        GAIA REGISTRY                             │
│                   github.com/gaia-registry/gaia                  │
│                                                                  │
│  ┌─────────────────┐    ┌──────────────────┐                     │
│  │  graph/         │    │  users/          │                     │
│  │  gaia.json      │◄───│  mbtiongson1/    │                     │
│  │  (canonical)    │    │  skill-tree.json │                     │
│  └────────┬────────┘    └──────────────────┘                     │
│           │ generateProjections.py                               │
│           ▼                                                      │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  skills/atomic/*.md                                 │        │
│  │  skills/composite/*.md       ← generated outputs   │        │
│  │  skills/legendary/*.md                              │        │
│  │  registry.md                                        │        │
│  │  combinations.md                                    │        │
│  └─────────────────────────────────────────────────────┘        │
└──────────────────────────┬───────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │    GAIA PLUGIN          │
              │    (installed per repo) │
              │                         │
              │  .gaia/config.json      │
              │  gaia init              │
              │  gaia scan              │
              │  gaia status            │
              │  gaia tree              │
              └────────────┬────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
    mbtiongson1/repo-A      mbtiongson1/repo-B
    (same skill tree)       (same skill tree)
```

### 2.1 Components

| Component | Location | Responsibility |
|---|---|---|
| Canonical graph | `graph/gaia.json` | Single source of truth for all skills and edges |
| Projection generator | `scripts/generateProjections.py` | Generates all `.md` and `.gexf` outputs from canonical graph |
| Validator | `scripts/validate.py` | Schema + DAG + reference integrity checks |
| Combination detector | `scripts/detectCombinations.py` | Core logic shared between CI and the plugin |
| Gaia CLI | `src/gaia_cli/` | User-facing commands — pip-installable Python package (`init`, `scan`, `push`, `name`, `install`, `embed`, `search`, `graph`, …) |
| TypeScript wrapper | `plugin/src/` | Thin Node.js shim that delegates to the Python CLI; used in the GitHub Action |
| GitHub Action | `plugin/github-action/` | Runs scan + detection on push, opens PRs for tree updates |
| User trees | `users/[username]/` | Personal skill progression records |
| Schemas | `schema/` | JSON Schema definitions for nodes, edges, user trees, plugin config |

---

## 3. Data Flow

### 3.1 Skill Creation (Contributor → Registry)

```
Contributor writes new skill node
         │
         ▼
Opens PR against gaia/graph/gaia.json
         │
         ▼
CI runs:
  1. JSON Schema validation
  2. DAG cycle detection
  3. Reference integrity (all parent IDs exist)
  4. Evidence threshold check (by level)
  5. Legendary approval count check (if applicable)
  6. Regenerate projections and check for drift
         │
    PASS │ FAIL → PR blocked with specific error
         ▼
Maintainer reviews using rubric in CONTRIBUTING.md
         │
         ▼
Merge → projections auto-regenerate via CI
```

### 3.2 User Skill Detection (Plugin → Registry)

```
Developer pushes to their repo
         │
         ▼
Gaia GitHub Action triggers
         │
         ▼
Plugin reads .gaia/config.json
         │
         ▼
Plugin scans declared scanPaths for skill references
  - Skill .md files
  - MCP tool declarations
  - Agent config files
  - CONTRIBUTING-style skill claims
         │
         ▼
Resolve detected skill IDs against gaia.json
         │
         ▼
Compare against user's current skill-tree.json
         │
    ┌────┴────────────────────┐
    │                         │
New skills found         Combination candidates found
    │                         │
    ▼                         ▼
Add to unlockedSkills    Add to pendingCombinations
    │                         │
    └────────────┬────────────┘
                 │
                 ▼
    Plugin prompts user in CLI or PR comment:
    "Combine [A] + [B] + [C] → [Skill D]? [Y/n]"
                 │
       YES       │       NO
         ┌───────┴───────┐
         ▼               ▼
  Fusion confirmed   Stays pending
         │
         ▼
  Plugin opens PR to gaia:
  users/mbtiongson1/skill-tree.json updated
         │
         ▼
  User merges PR → skill tree updated
```

### 3.3 Skill Tree Load (Any Repo)

```
gaia load mbtiongson1
         │
         ▼
Fetch users/mbtiongson1/skill-tree.json from Gaia registry
         │
         ▼
Cache locally in .gaia/skill-tree.cache.json
         │
         ▼
gaia status → renders summary
gaia tree --depth 3 → renders lineage up to depth 3
```

---

## 4. Repository Structure

```
gaia/
│
├── README.md                        ← Project overview + quickstart
├── CONTRIBUTING.md                  ← Contribution rules, evidence rubric, PR templates
│
├── graph/
│   ├── gaia.json                    ← CANONICAL. The only file humans edit directly.
│   ├── gaia.gexf                    ← Generated Gephi export
│   └── render/                      ← Versioned static graph snapshots
│       ├── v0.1.0.json
│       └── v0.1.0.png
│
├── skills/                          ← GENERATED. Do not edit manually.
│   ├── atomic/
│   │   ├── tokenize.md
│   │   ├── classify.md
│   │   └── ...
│   ├── composite/
│   │   ├── webScrape.md
│   │   ├── research.md
│   │   └── ...
│   └── legendary/
│       ├── recursiveSelfImprovement.md
│       └── ...
│
├── users/                           ← Personal skill trees by GitHub username
│   ├── mbtiongson1/
│   │   ├── skill-tree.json          ← Validated against skillTree.schema.json
│   │   └── skill-tree.md            ← Generated human-readable projection
│   └── .gitkeep
│
├── registry.md                      ← GENERATED. Flat index of all skills.
├── combinations.md                  ← GENERATED. Fusion recipe matrix.
│
├── schema/
│   ├── skill.schema.json            ← Validates skill nodes
│   ├── combination.schema.json      ← Validates fusion recipes / edges
│   ├── skillTree.schema.json        ← Validates user skill trees
│   └── pluginConfig.schema.json     ← Validates .gaia/config.json
│
├── src/gaia_cli/                    ← Python package source (pip install -e .)
│   ├── __init__.py
│   ├── main.py                      ← CLI entrypoint
│   ├── scanner.py                   ← Repo scan logic
│   ├── resolver.py                  ← Skill ID resolution against registry
│   ├── combinator.py                ← Combination detection logic
│   ├── treeManager.py               ← Load/save/diff skill trees
│   ├── prWriter.py                  ← Opens PRs to Gaia for tree updates
│   ├── embeddings.py                ← Semantic embedding generation
│   ├── semantic_search.py           ← Local vector search
│   ├── install.py                   ← Named-skill install/sync/uninstall
│   ├── name.py                      ← Promote intake entry to named skill
│   └── data/                        ← Bundled graph data shipped with the package
│       ├── graph/gaia.json
│       └── graph/named/
│
├── pyproject.toml                   ← Package metadata; optional [embeddings] extra
│
├── plugin/                          ← TypeScript wrapper + GitHub Action
│   ├── src/                         ← Node.js shim that delegates to Python CLI
│   └── github-action/
│       ├── action.yml
│       └── entrypoint.sh
│
└── scripts/
    ├── validate.py                  ← Schema + DAG + reference checks
    ├── generateProjections.py       ← Builds all .md and .gexf from gaia.json
    ├── generateNamedIndex.py        ← Rebuilds graph/named/index.json
    ├── exportGexf.py                ← GEXF serializer
    ├── renderGraphSvg.py            ← Renders graph/gaia.svg
    ├── syncDocsGraphAssets.py       ← Mirrors graph assets into docs/graph/
    ├── detectCombinations.py        ← Shared combination logic (used by plugin + CI)
    └── computeRarity.py             ← Derives rarity from user tree prevalence data
```

---

## 5. Skill Node — Rendered Output Design

Each skill gets a generated `.md` page. Structure:

```markdown
# Web Scrape
**ID:** webScrape  
**Type:** Composite  
**Level:** III — Competent  
**Rarity:** Uncommon  
**Status:** Validated

---

## Description
Retrieves and structures data from web pages into usable entities.

## Prerequisites
- [Web Search](../atomic/webSearch.md)
- [Parse HTML](../atomic/parseHtml.md)
- [Extract Entities](../atomic/extractEntities.md)

## Unlocks
- [Knowledge Harvest](knowledgeHarvest.md)

## Fusion Condition
Structured output mode must be enabled at call time.

## Evidence
| Class | Source | Evaluator | Date |
|---|---|---|---|
| B | https://... | mbtiongson1 | 2025-04-01 |

## Known Agents
_None verified yet._

---
*Generated from gaia.json v1.0.0 on 2026-04-26. Do not edit directly.*
```

---

## 6. User Skill Tree — Rendered Output Design

```markdown
# Skill Tree — mbtiongson1
**Last Updated:** 2026-04-26  
**Total Skills Unlocked:** 14  
**Highest Rarity:** Rare  
**Deepest Lineage:** 5

---

## Unlocked Skills

| Skill | Type | Level | Rarity | Unlocked In | Date |
|---|---|---|---|---|---|
| webScrape | Composite | III | Uncommon | tracker-automation | 2026-03-10 |
| research | Composite | III | Uncommon | gaia | 2026-04-01 |

---

## Pending Combinations

> **autonomousDebug** — combine `codeGeneration` + `executeBash` + `errorInterpretation`  
> Level floor: III · Detected in: tracker-automation  
> Run `gaia fuse autonomousDebug` to confirm.

---
*Generated from skill-tree.json. Do not edit directly.*
```

---

## 7. Gaia CLI Interface Design

```
gaia init [--user <username>] [--scan <path>] [--yes]
  Initializes .gaia/config.json in the current repo.
  Prompts for GitHub username and scan paths (use --yes for non-interactive defaults).

gaia doctor
  Checks CLI, config, registry path, skill tree, embeddings, and scan paths.

gaia scan
  Scans repo for skill references.
  Resolves against Gaia registry.
  Outputs: new skills detected, combination candidates flagged.

gaia push [--dry-run] [--no-pr]
  Writes a batch intake record under intake/skill-batches/.
  --dry-run prints the JSON without writing files.
  --no-pr writes the intake file without opening a GitHub PR.

gaia name <batch-file> <index> <contributor/skill-name>
  Promotes an awakened skill from intake to a named skill in graph/named/.

gaia install <contributor/skill-name>
  Downloads a named skill into the repo and global cache.

gaia install --list
  Lists all installed named skills.

gaia sync
  Updates installed named skills from their registry origin.

gaia uninstall <contributor/skill-name>
  Removes an installed named skill.

gaia embed
  Pre-computes semantic embeddings for all skills (requires [embeddings] extra).
  Run once after install; re-run when graph changes.

gaia search <query>
  Semantic search across generic and named skills (requires embeddings).

gaia graph [--format svg|json] [-o <path>] [--no-open]
  Generates graph/gaia.svg and opens it in the browser.
  Use --format json to write the D3/Cytoscape render JSON instead.

gaia status
  Displays summary of the configured user's skill tree.
  Shows total unlocked, highest rarity, pending combinations.

gaia tree [--depth N] [--type atomic|composite|legendary] [--rarity common|...]
  Displays the user's skill tree with optional filters.
  Default depth: full.

gaia fuse <skillId>
  Confirms a pending combination and opens a PR to update the skill tree.
```

---

## 8. Combination Detection Design

The combinator is the heart of the gamification loop.

### 8.1 Algorithm

```
Input:
  detectedSkills — set of skill IDs found in the current repo scan
  ownedSkills    — set of skill IDs in the user's current skill tree
  gaiaGraph      — full gaia.json

For each composite/legendary skill S in gaiaGraph:
  If S is NOT in ownedSkills:
    If all prerequisites of S are in (detectedSkills ∪ ownedSkills):
      Add S to pendingCombinations with levelFloor = S.levelFloor
```

### 8.2 Edge Cases

| Case | Behavior |
|---|---|
| Prerequisite skill exists but user doesn't own it | Still counts if detected in the current scan |
| Skill already owned at a lower level | Flag as level-up candidate rather than new fusion |
| Multiple candidates for the same skill | Present all; user picks which evidence justifies |
| Legendary candidate detected | Flagged but marked as requiring maintainer review before merge |

---

## 9. CI Pipeline Design

```yaml
# .github/workflows/gaia-ci.yml (simplified)

on: [pull_request]

jobs:
  validate:
    steps:
      - Checkout
      - Run scripts/validate.py
          - Schema validation (skill nodes, edges, user trees)
          - DAG cycle detection (DFS from all nodes)
          - Reference integrity (all parent IDs resolvable)
          - Evidence threshold by level
          - Legendary approval count
      
  generate:
    needs: validate
    steps:
      - Run scripts/generateProjections.py
      - Fail if generated output differs from committed files
      
  dag-checks:
    needs: validate
    steps:
      - Verify no composite has fewer than 2 parents
      - Verify no legendary is merged without validated status
      - Verify no deprecated skill is referenced as active prerequisite
```

---

## 10. Graph Export Formats

### 10.1 JSON (D3/Cytoscape)
```json
{
  "nodes": [
    { "id": "webScrape", "label": "Web Scrape", "type": "composite", "level": "III", "rarity": "uncommon" }
  ],
  "edges": [
    { "source": "webSearch", "target": "webScrape", "type": "prerequisite" }
  ],
  "meta": {
    "version": "0.1.0",
    "generatedAt": "2026-04-26T00:00:00Z",
    "totalNodes": 142,
    "totalEdges": 310
  }
}
```

### 10.2 GEXF (Gephi)
Standard GEXF 1.2 with custom attribute namespaces for `level`, `rarity`, `status`, and `type`. Generated by `scripts/exportGexf.py`.

---

## 11. Security and Trust Model

| Concern | Design Decision |
|---|---|
| A user writing to another user's tree | `users/[username]/` is protected by CODEOWNERS — only the owner (via OAuth-verified GitHub Actions) can open PRs against their own path |
| Malicious skill definitions | All content is validated by schema + DAG checks; human reviewer required for `validated` status |
| Legendary inflation | Legendary merges require two maintainer approvals in addition to CI pass |
| Rarity gaming | Rarity is computed server-side from real skill tree prevalence, not declared by contributors |
| Plugin accessing private repos | Plugin only reads declared `scanPaths` — no network calls except to the Gaia registry API |

---

## 12. Design Decisions Log

| Decision | Rationale | Alternatives Considered |
|---|---|---|
| `gaia.json` as single canonical file | Keeps the graph queryable in one shot; diff-friendly; trivially versioned | Multiple files per skill (rejected: high fan-out, merge conflicts) |
| Markdown as generated output | Ensures human-readable docs never drift from data; removes double-maintenance | Hand-edited skill pages (rejected: inevitable divergence) |
| Username = identity | Ties skill progression to verifiable GitHub identity; no new account system needed | Email-based (rejected: not verifiable without OAuth) |
| Rarity computed, not declared | Eliminates contributor bias; grounds rarity in real agent prevalence data | Declared by contributor (rejected: inevitably inflated) |
| PR-based tree updates | Auditable, reversible, git-native; skill tree history is implicit in commit log | Direct API writes (rejected: no audit trail) |
| Combination requires user confirmation | Prevents accidental fusions; user must acknowledge what they earned | Auto-fuse on detection (rejected: removes agency and gamification feel) |

---

## 13. Named Skills Architecture

Named skills are real, user-contributed implementations of generic skills. They represent specific tools, agents, or workflows created by community members.

### 13.1 Generic vs Named

| Aspect | Generic Skill | Named Skill |
|---|---|---|
| Location | `graph/gaia.json` | `graph/named/{contributor}/{skill-name}.md` |
| Identity | Abstract capability (e.g., `autonomous-research-agent`) | Concrete implementation (e.g., `karpathy/autoresearch`) |
| Level restriction | All levels (I–VI) | Level II ("Named") and above only |
| Origin | Defined by taxonomy maintainers | Attributed to first contributor |
| Edit | Direct PR to `gaia.json` | PR to `graph/named/` |

### 13.2 Bucket System

Named skills are grouped into "buckets" by their `genericSkillRef` field. Each bucket has exactly one **origin** contributor — the first person to create that named implementation. Subsequent similar implementations can join the same bucket by referencing the same `genericSkillRef`.

The generated `graph/named/index.json` provides fast lookup of all named implementations for a given generic skill ID. It is regenerated by `scripts/generateNamedIndex.py` and must not be edited manually.

### 13.3 Lifecycle

```
gaia push → intake/skill-batches/ (lifecycle: "pending")
         → reviewer accepts (lifecycle: "awakened")
         → gaia name <batch> <index> <contributor/skill-name>
         → graph/named/{contributor}/{skill-name}.md (lifecycle: "named")
```

Level 0 (Basic) and Level I (Awakened) skills are generic-only. A skill only becomes "named" in the sense of Level II once a contributor claims it via `gaia name`. Basic skills (Level 0) are universal LLM primitives and do not accept named implementations.

### 13.4 Install & Sync

Named skills can be installed into any repository:

```bash
gaia install karpathy/autoresearch   # install from registry
gaia install --list                  # show installed skills
gaia sync                            # pull latest versions
gaia uninstall karpathy/autoresearch # remove
```

Storage:
- **Global cache**: `~/.gaia/skills/{contributor}/{skill-name}.md`
- **Repo reference**: `.gaia/named-skills/{contributor}/{skill-name}.md` (symlink on Unix, copy on Windows)
- **Manifest**: `.gaia/install-manifest.json` (tracks id, installedAt, sourceRef, sha256)

### 13.5 Semantic Search

Skills are embedded using `sentence-transformers` (model: `all-MiniLM-L6-v2`, 384 dimensions). The embedding input is `"{name}: {description}"` for each skill.

- Pre-computed embeddings: `graph/embeddings.json`
- Pairwise similarity scores (threshold 0.3): `graph/similarity.json`
- The MCP server reads pre-computed data only — it does not run the model at query time
- The CLI `gaia search <query>` embeds queries in real-time (requires `sentence-transformers` installed)
- `gaia embed` regenerates the embeddings store