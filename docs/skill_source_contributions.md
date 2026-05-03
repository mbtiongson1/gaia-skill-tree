# Skill Source Contributions (Community SKILL.md Repos)

_Last updated: 2026-05-03 (UTC)_

This document records external, high-usage repositories that publish reusable `SKILL.md` files. These are candidate sources contributors can mine for evidence, taxonomy ideas, and emerging capability patterns before proposing additions to `registry/gaia.json`.

The current curated real-skill review surface is generated from [`registry/real-skills.json`](../registry/real-skills.json) into [`real-skills.html`](../real-skills.html). Add source-backed named skills there first when the skill is real and useful but not yet ready to become a canonical Gaia DAG node.

## Selection method

- Searched GitHub-hosted repositories that explicitly reference `SKILL.md`.
- Prioritized repositories by current GitHub star count as a rough adoption signal.
- Confirmed each repo exposes `SKILL.md` files in its structure.

## Curated contributions

| Rank | Repository | Stars* | SKILL.md evidence in repo | Suggested contribution angle |
|---|---|---:|---|---|
| 1 | https://github.com/VoltAgent/awesome-agent-skills | 19.4k | README lists official and community skills, with paths and links to official skill pages. | Best broad discovery source for current real named skills across official teams and community collections. |
| 2 | https://agentskills.me/ | n/a | Directory reports 490 skills and exposes detail pages such as `codex`, `gemini`, `commit-work`, and `vercel-react-best-practices`. | Best scrape target for concrete names, popularity signals, source repos, and skill paths. |
| 3 | https://github.com/huggingface/skills | n/a | Official Hugging Face skill repository lists 13 `skills/<name>/SKILL.md` entries for Hub operations, datasets, training, evaluation, Gradio, papers, and Transformers.js. | Best source for concrete AI/ML platform workflow skills that map to existing Gaia model-training, data, research, and inference buckets. |
| 4 | https://github.com/addyosmani/agent-skills | 25.2k | `skills/<skill-name>/SKILL.md` directories are documented in repo structure. | Strong signal for common engineering-oriented skill definitions and decomposition patterns. |
| 5 | https://github.com/803/skills-supply | 31 | Package layout explicitly defines subdirectories and root-level `SKILL.md` conventions. | Useful for interoperability/meta-skill proposals around distribution and discovery workflows. |
| 6 | https://github.com/simota/agent-skills | 28 | Large, explicit list of many `<name>/SKILL.md` entries in README/docs content. | Good source for long-tail and specialized composite skill candidates. |
| 7 | https://github.com/iliaal/ai-skills | 7 | README states skill unit is a markdown `SKILL.md` with YAML frontmatter. | Useful for schema and trigger-language consistency checks across community skills. |

\*Stars are point-in-time values scraped from each repository landing page and may drift. AgentSkills.me is a directory rather than a GitHub repository, so its table row uses its reported skill count instead of stars.

## Notes for Gaia contributors

- Treat star count only as a popularity heuristic, not evidence quality.
- Before proposing any new skill, map candidate behavior to existing Gaia IDs to avoid duplicates.
- If importing a concept from these sources, attach reproducible evidence per Gaia's level rubric (Evidence Tier A/B/C) in the PR.
- Keep named-skill curation separate from DAG promotion: add real source-backed names to `registry/real-skills.json`, then promote only durable capability concepts into `registry/gaia.json`.
