# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working norms

- **Keep this file under 200 lines.** Update it when you learn something that future sessions would need — but trim, consolidate, or remove stale content to stay within the limit.
- **Before planning any non-trivial task, ask clarifying questions until you are 95% confident you understand the full scope.** Do not begin implementation until that bar is met.

## Commands

### Python CLI

```bash
# Install the CLI (run from repo root)
pip install -e .

# Install with semantic search support (strongly recommended)
pip install -e ".[embeddings]"
gaia embed   # run once after install; re-run when graph changes

# Run validation (schema + DAG + reference integrity + evidence)
python scripts/validate.py

# Regenerate all derived files from graph/gaia.json
python scripts/generateProjections.py
python scripts/exportGexf.py

# Validate intake batches
python scripts/validate_intake.py

# Run Python tests
pytest
```

### MCP Server (TypeScript)

```bash
cd mcp-server
npm install
npm run build          # compile TypeScript
npm test               # vitest run
npm run dev            # watch mode
```

### Plugin (TypeScript wrapper)

```bash
cd plugin
npm install
npm test
```

### Git hooks (maintainers)

```bash
bash scripts/install-git-hooks.sh
```

The pre-commit hook auto-regenerates projections, exports GEXF, renders SVG, mirrors docs assets, and stages them whenever `graph/gaia.json` or schema files are staged.

## Architecture

### Golden rule

`graph/gaia.json` is the **only file humans ever directly edit**. Every other file (`skills/**`, `registry.md`, `combinations.md`, `tree.md`, `graph/named/index.json`) is a generated projection. CI fails if generated files are stale relative to `gaia.json`. Never hand-edit generated files.

### Component map

| Component | Location | Role |
|---|---|---|
| Canonical graph | `graph/gaia.json` | Single source of truth — skills array + edges array |
| Validator | `scripts/validate.py` | JSON schema, DAG cycle detection, reference integrity, evidence thresholds |
| Projection generator | `scripts/generateProjections.py` | Produces `skills/**/*.md`, `registry.md`, `combinations.md`, `tree.md`, user skill-tree projections |
| Named index generator | `scripts/generateNamedIndex.py` | Produces `graph/named/index.json` |
| Python CLI | `src/gaia_cli/` | `pip install -e .` → `gaia` command; handles init/scan/push/name/install/embed/search/graph/fuse |
| MCP server | `mcp-server/` | TypeScript; exposes `gaia_lookup`, `gaia_suggest`, `gaia_scan_context`, `gaia_my_tree`, `gaia_propose` tools + `gaia://registry` resource; fetches live graph from GitHub raw URL |
| TypeScript plugin wrapper | `plugin/src/` | Thin Node.js shim delegating to the Python CLI; used in the GitHub Action |
| GitHub Action | `plugin/github-action/` | Scans repo on push, opens PRs for skill tree updates |
| Schemas | `schema/` | `skill.schema.json`, `combination.schema.json`, `skillTree.schema.json`, `pluginConfig.schema.json` |
| User skill trees | `users/[username]/skill-tree.json` | Personal progression; validated against `skillTree.schema.json` |
| Named skills | `graph/named/{contributor}/{skill-name}.md` | Community implementations of generic skills; YAML frontmatter + markdown body |
| Crawlers | `scripts/crawlers/` | Bot crawlers for HuggingFace, MCP registries, npm, VS Code Marketplace |
| Intake batches | `intake/skill-batches/` | Draft proposals from `gaia push`; reviewed before promotion into `gaia.json` |

### Skill data model

Three tiers in `gaia.json`:
- `atomic` (○ Intrinsic) — primitive, no prerequisites required
- `composite` (◇ Extra) — requires ≥2 prerequisite skill IDs
- `legendary` (◆ Ultimate) — requires ≥3 prerequisites, ≥3 Class A/B evidence sources, 2 maintainer approvals, `status: "validated"` at merge

Skill IDs use `kebab-case` (e.g., `web-scrape`, `parse-json`). Display names use Title Case.

Level progression (`"level"` field): `"0"` Basic → `"I"` Awakened → `"II"` Named → `"III"` Evolved → `"IV"` Hardened → `"V"` Transcendent → `"VI"` Transcendent ★

Evidence classes: `A` (peer-reviewed paper/benchmark), `B` (reproducible open-source demo), `C` (credible vendor/community demo). Levels 0 and I require no evidence; Level II+ requires the corresponding class floor.

Rarity (`common`, `uncommon`, `rare`, `epic`, `legendary`) is **computed** from real agent prevalence data via `scripts/computeRarity.py` — never declared by contributors.

### MCP server internals

The MCP server (`mcp-server/src/`) is pure TypeScript using `@modelcontextprotocol/sdk`. It fetches `graph/gaia.json` from the GitHub raw URL with ETag-based caching (`src/config/cache.ts`). Semantic similarity uses pre-computed `graph/similarity.json` — the server never runs `sentence-transformers` at query time. The DAG traversal utilities (`src/graph/dag.ts`) handle ancestor/descendant walks, lineage depth, and type filtering.

### CLI internals

The Python CLI (`src/gaia_cli/`) is a pip package (`gaia-cli`). Key modules:
- `scanner.py` — reads `.gaia/config.json` scan paths, tokenizes skill references
- `resolver.py` — matches tokens against canonical skill IDs
- `combinator.py` — detects fusion candidates: composite/legendary skills whose prerequisites are all present in detected + owned skills
- `embeddings.py` / `semantic_search.py` — local vector search using `all-MiniLM-L6-v2` (384-dim); embeddings stored in `graph/embeddings.json`
- `treeManager.py` — load/save `users/[username]/skill-tree.json`
- `prWriter.py` — opens GitHub PRs for intake batches and tree updates

### Named skills lifecycle

```
gaia push → intake/skill-batches/<id>.json (lifecycle: "pending")
         → reviewer accepts → lifecycle: "awakened"
         → gaia name <batch> <index> <contributor/skill-name>
         → graph/named/{contributor}/{skill-name}.md (lifecycle: "named")
```

Named skills have YAML frontmatter with required fields: `id`, `name`, `contributor`, `origin`, `genericSkillRef`, `status`, `level`, `description`. The `genericSkillRef` must resolve to a skill ID in `gaia.json`. Level must be II or above. Exactly one entry per `genericSkillRef` bucket may have `origin: true`.

### CI workflows

- **`generate.yml`** — triggers on `graph/**` or `schema/**` changes; runs `generateProjections.py` + `exportGexf.py`; fails if committed generated files differ from freshly generated ones
- **`verify-evidence.yml`** — weekly; checks all evidence URLs, opens an issue when dead links are found
- **`crawl-*.yml`** — scheduled crawlers proposing candidate skills from external sources

### Contribution PR title format

```
[atomic|composite|legendary|reclassify|fusion] skill-id — brief rationale
```

PR templates live in `.github/PULL_REQUEST_TEMPLATE/`. All canonical graph PRs edit only `graph/gaia.json`; generated files must be committed alongside if the pre-commit hook is not installed.

### Slash commands (Claude Code)

Two Claude Code skills ship in `.claude/skills/`:
- `/gaia-curate` — full end-to-end curation pipeline: research → classify → write → validate → PR
- `/gaia-draft-curate` — read-only triage of `intake/skill-batches/` and open `draft-skills` PRs
