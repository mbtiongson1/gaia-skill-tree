# ARCHITECTURE.md — System Reference

## Overview

Gaia is a collaborative AI agent skill registry. Contributors curate skills in a DAG-structured JSON graph; a Python CLI validates, indexes, and embeds skills; a TypeScript MCP server exposes semantic search; a GitHub Action scans contributor repos for skill patterns; a single-page frontend visualizes the registry with real-time skill tree detection and an explorer overlay for deep dives.

---

## Component Map

| Component | Location | Purpose |
|---|---|---|
| **Canonical graph** | `graph/gaia.json` | Single source of truth: skills array + edges array |
| **Validator** | `scripts/validate.py` | JSON schema, DAG cycles, reference integrity, evidence thresholds |
| **Projection generator** | `scripts/generateProjections.py` | Produces skill markdown files, registry index, combinations, tree view |
| **Named index generator** | `scripts/generateNamedIndex.py` | Produces `graph/named/index.json` |
| **Python CLI** | `src/gaia_cli/` | `gaia` command: init, scan, push, name, install, embed, search, graph, fuse |
| **MCP server** | `mcp-server/` | TypeScript SDK; tools: lookup, suggest, scan_context, my_tree, propose; resource: gaia://registry |
| **Node wrapper** | `plugin/src/` | Thin shim delegating to Python CLI; consumed by GitHub Action |
| **GitHub Action** | `plugin/github-action/` | Scans repo on push; opens PRs for skill tree updates |
| **Schemas** | `schema/` | `skill.schema.json`, `combination.schema.json`, `skillTree.schema.json`, `pluginConfig.schema.json` |
| **User skill trees** | `users/[username]/skill-tree.json` | Personal progression; validated against `skillTree.schema.json` |
| **Named skills** | `graph/named/{contributor}/{skill-name}.md` | Community skill implementations; YAML frontmatter + markdown |
| **Crawlers** | `scripts/crawlers/` | Bot scanners for HuggingFace, MCP registries, npm, VS Code Marketplace |
| **Intake batches** | `intake/skill-batches/` | Proposed skills from `gaia push`; reviewed before promotion to graph |

---

## Data Flow

### Skill Creation (Contributor → Registry)

1. Contributor proposes skill → `gaia push` → intake batch created with lifecycle `"pending"`
2. Maintainer reviews → PR approval → lifecycle → `"awakened"`
3. `gaia name <batch> <index> <contributor/skill-name>` → `graph/named/{contributor}/{skill-name}.md` → lifecycle → `"named"`
4. Periodic crawler or manual PR edits `graph/gaia.json` → promoted to canonical registry
5. CI runs `generateProjections.py` → all downstream files auto-regenerated

### User Skill Detection (Plugin → Registry)

1. GitHub Action on push → Node wrapper → Python CLI
2. CLI reads `.gaia/config.json` scan paths → tokenizes detected skill references
3. `resolver.py` matches tokens against canonical skill IDs
4. `combinator.py` identifies fused skills (composites whose prerequisites all present)
5. Opens PR with updated `users/[username]/skill-tree.json`

---

## Frontend (docs/index.html)

Single-file SPA with three JS modules and embedded CSS:

| Module | Role |
|---|---|
| Graph renderer | Canvas-based 3D sphere layout; nodes colored by tier/level; edges + hover highlight |
| Scroll reveal | Viewport observer; animates sections on appearance; fade-in + translate |
| Named skills + explorer | Loads `graph/named/index.json` → populates skill explorer overlay; tab-based UI |

**Data sources:**
- `graph/gaia.json` — skill definitions, edges
- `graph/named/index.json` — named skill registry
- `graph/embeddings.json` — 384-dim vectors for semantic search (client-side)

**Skill Explorer overlay:**
- Hash routing: `#/explorer/:skillId` → opens overlay with tabs (Overview, Prerequisites, Evidence, Flowchart, Timeline)
- Flowchart: SVG grid layout with bezier edges connecting prerequisites → target
- GitHub timeline: Fetches commit history for the skill's canonical markdown file
<<<<<<< HEAD
- 6★ shimmer + 5★ pulse animations
=======
<<<<<<< Updated upstream
- Level VI shimmer + Level V pulse animations
=======
- 6★ shimmer + 5★ pulse animations
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split

---

## Golden Rule

**`graph/gaia.json` is the only file humans ever directly edit.**  
Every other file is generated; CI fails if generated files are stale relative to `gaia.json`.

---

## Key Entry Points

| Command | Effect |
|---|---|
| `pip install -e .` | Install Python CLI; run `gaia` commands |
| `npm run build` (mcp-server) | Compile TypeScript MCP server; run tests with `npm test` |
| `python scripts/validate.py` | Validate schema, DAG, references, evidence |
| `python scripts/generateProjections.py` | Regenerate all derived files from graph |
| `python scripts/computeRarity.py` | Derive rarity tiers from agent prevalence data |
