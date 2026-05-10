# Outdated Issues Audit — 2026-05-10

This audit checked the public GitHub issue list, current repository behavior, docs drift, and dependency freshness for issues that look stale, already fixed, or ready for narrowed follow-up.

## How this was checked

- Fetched open issues from `https://api.github.com/repos/mbtiongson1/gaia-skill-tree/issues?state=open&per_page=100` on 2026-05-10.
- Ran `python scripts/build_docs.py --check` to verify generated docs drift.
- Ran `PYTHONPATH=src:. python -m gaia_cli --registry . stats` to verify the stats command exists and works.
- Ran `PYTHONPATH=src:. python -m gaia_cli --registry . skills info /huggingface/hf-cli` to verify the leading-slash named skill issue.
- Ran `npm outdated --json` in `packages/mcp` and `packages/cli-npm` to identify dependency-update follow-ups.

## Recommended triage

| Issue | Status | Recommendation | Evidence |
| --- | --- | --- | --- |
| #65 — `gaia stats` registry health command | Outdated / appears implemented | Close after a quick maintainer review, or retitle to any remaining stats polish. | `src/gaia_cli/commands/stats.py` implements `collect_stats`, `render_stats`, and `stats_command`; `README.md` documents `gaia stats`; `tests/test_stats.py` covers collection, rendering, and CLI output. |
| #182 — docs drift after version bump | Outdated for the current checkout | Close if the issue only targets the current drift; keep a follow-up only if release automation should enforce this every bump. | `python scripts/build_docs.py --check` reports documentation is up to date. |
| #180 — leading slash breaks `gaia skills info/install` | Fixed in this branch | Close after merge. Add a changelog note if one is maintained. | Slash-prefixed named skill IDs are normalized before lookup/install, and tests cover `skills info /huggingface/hf-cli` plus `install_skill("/testuser/my-skill", ...)`. |
| #181 — packaging tests require dev tooling | Fixed in this branch | Close after merge if maintainers accept skipping packaging-only tests when `build` is unavailable. | Packaging tests now skip with an explicit dev-extra hint when `python -m build` is unavailable; `build` remains in the `dev` extra rather than `embeddings`. |
| #134 — `gaia docs build` requires `--registry` | Outdated / appears fixed | Close or update with any remaining reproduction. | The CLI docs command calls `scripts/build_docs.py` through the resolved registry, and the packaging test explicitly checks `docs build --check` can run from a registry clone without passing `--registry`. |
| #71 — display all bucket variants in lookup/docs | Partially outdated / blocked by newer command shape | Retitle around `gaia skills info` or a future `gaia lookup`; avoid assuming a top-level `lookup` command exists. | The CLI currently exposes `skills list/search/info/install/uninstall`, not a dedicated top-level `lookup`. |
| #64 — `gaia browse` interactive explorer | Still valid but should be deferred | Keep open as an enhancement; mark blocked until command surface and optional TUI dependency policy are settled. | No `browse` subcommand is registered in the CLI parser. |
| #118/#119 — promotion title and duplicate rank issues | Needs reproduction refresh | Keep open, but ask for a current screenshot/output from `gaia scan` and duplicate IDs from the latest registry. | Promotion and duplicate behavior may have shifted with the current rank/effective-level model. |
| RFC cluster #74-#79 and #115 | Not stale, but aging as design backlog | Move to a milestone/project board and assign owners; close any superseded RFCs once governance/docs lifecycle decisions are recorded. | These are process/design decisions rather than executable bugs. |

## Dependency update follow-ups

Current dependency checks do not show urgent patch updates for runtime Python dependencies, but the JavaScript packages have major-version candidates that should be planned rather than auto-bumped.

- `packages/mcp`: `@types/node` has a patch update in the current range; `typescript` latest is 6.x; `zod` latest is 4.x.
- `packages/cli-npm`: `@types/node` has a patch update in the current range; `typescript` latest is 6.x.
- Recommendation: apply safe patch/minor lockfile refreshes separately from major migrations; create dedicated issues for TypeScript 6 and Zod 4 compatibility if they are desired.

## Suggested next actions

1. Close #65, #134, and #182 if maintainers agree the current checkout satisfies them.
2. Merge the leading-slash normalization fix, then close #180.
3. Merge the packaging-test guard, then close #181 or retitle it to docs-only dev environment guidance.
4. Refresh old RFC/enhancement titles so they match the current CLI command surface (`skills info/search` rather than `lookup` unless a new command is still desired).
5. Open separate dependency-maintenance issues for TypeScript 6 and Zod 4 instead of bundling them into routine patch updates.
