---
name: version-update
description: Determine the correct SemVer bump (patch/minor/major) for the current branch relative to main, update all four version files in one commit. Use when the user says "bump version", "version update", "update version for PR", or explicitly types /version-update.
version: 1.0.0
---

# version-update

Determine whether the changes on the current branch require a **patch**, **minor**, or **major** SemVer bump, then update all version files and commit the result.

## Version files managed

| File | Field |
|---|---|
| `pyproject.toml` | `version = "X.Y.Z"` (line in `[project]` section) |
| `mcp-server/package.json` | `"version": "X.Y.Z"` |
| `plugin/package.json` | `"version": "X.Y.Z"` |
| `graph/gaia.json` | top-level `"version": "X.Y.Z"` (not per-skill versions) |

All four files are bumped to the **same new version** in a single commit.

---

## Step 1 — Gather context

```bash
# Current versions (read before anything else)
grep '^version' pyproject.toml
node -e "console.log(require('./mcp-server/package.json').version)"
node -e "console.log(require('./plugin/package.json').version)"
python3 -c "import json; d=json.load(open('graph/gaia.json',encoding='utf-8')); print(d['version'])"

# All commits on this branch relative to main
git log main..HEAD --oneline

# All files changed on this branch relative to main
git diff main..HEAD --name-only
```

Read the current version from `pyproject.toml` — treat it as the authoritative source. The other three files should match; if any differs, surface it to the user before bumping.

---

## Step 2 — Classify the bump

Evaluate in strict priority order (first matching rule wins):

### MAJOR — any of:
- A commit message contains `BREAKING CHANGE` (case-insensitive)
- A commit message subject ends with `!` before the colon (e.g. `feat!:`, `fix!:`)
- `schema/*.json` is in the changed file list **and** the diff removes or renames a required field, or changes an enum to remove existing values
- A skill is **removed** from `graph/gaia.json` (existing `id` deleted, not just modified)

### MINOR — any of (and no MAJOR triggers):
- A commit message starts with `feat:` or `feat(`
- PR title or any commit starts with `[basic]`, `[extra]`, `[ultimate]`, `[fusion]` — new skills or recipes added to the graph
- `graph/gaia.json` has net-new skill objects added (new `id`s not present in the base)
- A new MCP tool, CLI subcommand, or Claude Code skill is introduced

### PATCH — everything else:
- `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `perf:`, `style:`
- `[evidence]` — evidence added to an existing skill
- `[reclassify]` — level or rarity changed on an existing skill
- `docs/`, `README`, workflow YAML, or generated projection files only

> If the branch has **zero commits** ahead of main (nothing to bump), report this and stop.

---

## Step 3 — Report findings

Before making any changes, output a summary table:

```
Current version:  1.2.3
Proposed bump:    MINOR  →  1.3.0

Bump rationale:
  [minor] feat: add autonomous-debug skill (commit abc1234)
  [minor] [basic] web-eval — add 3 new basic skills (commit def5678)

Changed files driving classification:
  graph/gaia.json          → new skill IDs detected
  mcp-server/src/index.ts  → no new tools detected

Version files to update:
  pyproject.toml              1.2.3  →  1.3.0
  mcp-server/package.json     1.2.3  →  1.3.0
  plugin/package.json         1.2.3  →  1.3.0
  graph/gaia.json             1.2.3  →  1.3.0
```

Ask the user to confirm (`yes` / `no`) or override the bump level (`patch` / `minor` / `major`). Do not proceed until confirmed.

---

## Step 4 — Apply the bump

Once confirmed, update each file **in place** using the Edit tool (not sed):

**`pyproject.toml`** — replace the `version = "..."` line in the `[project]` section only (not elsewhere).

**`mcp-server/package.json`** — replace the top-level `"version"` value.

**`plugin/package.json`** — replace the top-level `"version"` value.

**`graph/gaia.json`** — replace the top-level `"version"` value. Use `encoding='utf-8'` for any Python reads. Do NOT touch per-skill `"version"` fields.

---

## Step 5 — Commit

```bash
git add pyproject.toml mcp-server/package.json plugin/package.json graph/gaia.json
git commit -m "chore: bump version to X.Y.Z"
```

The commit message must be exactly `chore: bump version to <new-version>` — no body, no extra lines. This keeps version commits easy to filter in `git log`.

Do **not** push or open a PR — the version commit rides along with the branch's existing PR.

---

## Step 6 — Output

Report:

```
✓ Version bumped: 1.2.3  →  1.3.0  (MINOR)
  pyproject.toml
  mcp-server/package.json
  plugin/package.json
  graph/gaia.json
Commit: chore: bump version to 1.3.0
```

If the bump was overridden by the user, note the override and the original recommendation.

---

## Constraints

- Never bump if `pyproject.toml` already has the proposed version (idempotent — skip with a note).
- Never touch per-skill `"version"` fields inside `graph/gaia.json` — only the top-level `"version"`.
- If any version file is missing, report it and skip that file (don't fail the whole bump).
- `graph/gaia.json` must be read and written with `encoding='utf-8'` — it contains non-ASCII characters.
- Do not run `generateProjections.py` or `validate.py` — this skill only touches version strings.
