---
name: gaia-bot-curate
description: Curate Gaia bot crawler branches into real-skill catalog entries. Use when the user asks to process bot/* crawl branches, curate crawler output, clean up bot proposal branches, or explicitly types /gaia-bot-curate.
---

# gaia-bot-curate

Curate remote `bot/*` crawler branches into `registry/real-skills.json` from a fresh `origin/main` review branch.

## Workflow

1. **Start clean**
   - `git fetch --all --prune`
   - Confirm no local work will be overwritten.
   - Create `review/meta/<short-crawl-slug>` from `origin/main`; do not merge bot branches.

2. **Collect bot payloads outside the repo**
   - List remote crawler branches with `git for-each-ref refs/remotes/origin/bot`.
   - For each branch, find added `proposals/*.json` files with `git diff --name-only $(git merge-base origin/main <branch>)..<branch> -- proposals`.
   - Write raw payload copies and a compact deduplicated candidate JSON to `/tmp`.
   - Write `/tmp/gaia-bot-crawl-skill-names-<date>.md` with source branch, proposal file, candidate ID, name, evidence URL, and duplicate source refs.
   - Deduplicate by proposal `id`; if missing, use normalized lowercase `name`.

3. **Dispatch narrow triage agents**
   - Split by source type (`github`, `vscode-marketplace`, `huggingface`, or other discovered source).
   - Give each agent only the relevant `/tmp` candidate JSON subset plus the rule below; do not pass full raw payloads or unrelated history.
   - Ask for accepted/rejected JSON-like output with `id`, `name`, `contributor`, `url`, optional `sourceRepo`, `mapsToGaia`, and `reason`.

4. **Accept only real skills**
   - Accept concrete skill implementations, workflow artifacts, model capability pages, or reputable package/repo pages that map to existing Gaia IDs.
   - Prefer `registry/real-skills.json` for real-world implementations; do not create new abstract `registry/gaia.json` nodes unless `/gaia-curate` review explicitly justifies one.
   - Reject generic model listings, broad marketing wrappers, stale repos, awesome lists, templates, duplicates, and candidates without stable capability mapping.
   - Treat MCP servers, API connectors, marketplace extensions, and tool endpoints as `needs-evidence` unless they include a specific skill/workflow artifact such as `SKILL.md`, a documented agent playbook, or a concrete workflow implementation beyond “exposes tools over MCP.”

5. **Integrate centrally**
   - Main agent edits only accepted entries into `registry/real-skills.json`.
   - Regenerate with `python3 scripts/generateRealSkills.py`; run broader projection scripts only if canonical registry files changed.
   - Do not commit raw `proposals/*.json` files or local `/tmp` snapshots.

6. **Clean remote bot branches**
   - Delete consumed remote bot branches only after the `/tmp` snapshot exists and the review branch contains the curated result.
   - Verify deletion with `git ls-remote --heads origin <branch>...`.

7. **Verify and publish**
   - Run:
     ```bash
     PYTHONIOENCODING=utf-8 python3 scripts/validate.py
     python3 scripts/generateProjections.py
     python3 scripts/exportGexf.py
     ./.venv/bin/pytest tests/test_validate.py tests/test_real_skill_catalog.py tests/test_registry_layout.py
     git diff --check
     ```
   - Review `git diff --name-only origin/main`; `review/meta` branches must not touch `packages/`, `src/`, or `registry/schema/`.
   - If hooks add package/version churn on a curation-only `review/meta` branch, restore out-of-scope files from `origin/main`, rerun verification, and amend with `--no-verify` after manual validation.
   - Push the review branch and open a PR summarizing accepted, rejected, `needs-evidence`, validation, and deleted bot branches.

## Output

Report:
- PR URL.
- Temp snapshot path.
- Accepted real-skill count by source.
- Rejected and `needs-evidence` counts with reasons.
- Validation commands and outcomes.
- Remote bot branches deleted.
