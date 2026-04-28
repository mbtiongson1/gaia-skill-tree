# Skill Source Contributions (Community SKILL.md Repos)

_Last updated: 2026-04-28 (UTC)_

This document records external, high-usage repositories that publish reusable `SKILL.md` files. These are candidate sources contributors can mine for evidence, taxonomy ideas, and emerging capability patterns before proposing additions to `graph/gaia.json`.

## Selection method

- Searched GitHub-hosted repositories that explicitly reference `SKILL.md`.
- Prioritized repositories by current GitHub star count as a rough adoption signal.
- Confirmed each repo exposes `SKILL.md` files in its structure.

## Curated contributions

| Rank | Repository | Stars* | SKILL.md evidence in repo | Suggested contribution angle |
|---|---|---:|---|---|
| 1 | https://github.com/addyosmani/agent-skills | 25.2k | `skills/<skill-name>/SKILL.md` directories are documented in repo structure. | Strong signal for common engineering-oriented skill definitions and decomposition patterns. |
| 2 | https://github.com/803/skills-supply | 31 | Package layout explicitly defines subdirectories and root-level `SKILL.md` conventions. | Useful for interoperability/meta-skill proposals around distribution and discovery workflows. |
| 3 | https://github.com/simota/agent-skills | 28 | Large, explicit list of many `<name>/SKILL.md` entries in README/docs content. | Good source for long-tail and specialized composite skill candidates. |
| 4 | https://github.com/iliaal/ai-skills | 7 | README states skill unit is a markdown `SKILL.md` with YAML frontmatter. | Useful for schema and trigger-language consistency checks across community skills. |

\*Stars are point-in-time values scraped on **2026-04-28** from each repository landing page and may drift.

## Notes for Gaia contributors

- Treat star count only as a popularity heuristic, not evidence quality.
- Before proposing any new skill, map candidate behavior to existing Gaia IDs to avoid duplicates.
- If importing a concept from these sources, attach reproducible evidence per Gaia's level rubric (Class A/B/C) in the PR.
