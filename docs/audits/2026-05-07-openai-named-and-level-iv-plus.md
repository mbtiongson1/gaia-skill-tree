<<<<<<< HEAD
# Gaia audit: OpenAI named skills and 4⭐+ meta-audit

**Date:** 2026-05-07  
**Auditors:** openai-codex  
**Scope:** `/gaia-audit` on all `openai/*` real-skill catalog items and generated named-skill projections; `/gaia-meta-audit` on every canonical Gaia skill at 4⭐ or above.
=======
<<<<<<< Updated upstream
# Gaia audit: OpenAI named skills and Level IV+ meta-audit

**Date:** 2026-05-07  
**Auditors:** openai-codex  
**Scope:** `/gaia-audit` on all `openai/*` real-skill catalog items and generated named-skill projections; `/gaia-meta-audit` on every canonical Gaia skill at Level IV or above.
=======
# Gaia audit: OpenAI named skills and 4★+ meta-audit

**Date:** 2026-05-07  
**Auditors:** openai-codex  
**Scope:** `/gaia-audit` on all `openai/*` real-skill catalog items and generated named-skill projections; `/gaia-meta-audit` on every canonical Gaia skill at 4★ or above.
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split

## `/gaia-audit`: OpenAI named-skill claims

### Finding

The OpenAI skill entries are valid real-skill catalog candidates, but they should not be promoted as Gaia named skills until there is independently reviewable usage evidence. The reachable `officialskills.sh/openai/skills/*` pages describe the skills, but this audit did not find a corresponding `registry/named/openai/*.md` source file or published usage trace sufficient to substantiate a named-skill claim.

### Source-of-truth correction

Retain every OpenAI item in `registry/real-skills.json` as a catalog item, remove any `promotedNamedSkillId`, and add a review note explaining that the item is catalog-only pending usage evidence. Regenerated named-skill projections must therefore contain no `openai` contributor bucket.

### Audited OpenAI items

| Catalog item | Previous promoted named skill | Result |
|---|---:|---|
| `openai-openai-docs` | `openai/openai-docs` | Demoted to catalog-only |
| `openai-gh-fix-ci` | `openai/gh-fix-ci` | Demoted to catalog-only |
| `openai-yeet` | `openai/yeet` | Demoted to catalog-only |
| `openai-chatgpt-apps` | None | Retained catalog-only and review note added |
| `openai-playwright` | `openai/playwright` | Demoted to catalog-only |
| `openai-sentry` | `openai/sentry` | Demoted to catalog-only |
| `openai-security-threat-model` | `openai/security-threat-model` | Demoted to catalog-only |
| `openai-security-ownership-map` | `openai/security-ownership-map` | Demoted to catalog-only |
| `openai-security-best-practices` | `openai/security-best-practices` | Demoted to catalog-only |

<<<<<<< HEAD
## `/gaia-meta-audit`: 4⭐+ skills

### Summary

The registry validates structurally, but the 4⭐+ audit found a recurring evidence-hygiene issue: several high-level skills depend on old `gaia-registry/gaia` seed evidence URLs that currently resolve as missing GitHub pages. Those entries should be prioritized for replacement with current evidence or demotion in a follow-up source-of-truth change.
=======
<<<<<<< Updated upstream
## `/gaia-meta-audit`: Level IV+ skills

### Summary

The registry validates structurally, but the Level IV+ audit found a recurring evidence-hygiene issue: several high-level skills depend on old `gaia-registry/gaia` seed evidence URLs that currently resolve as missing GitHub pages. Those entries should be prioritized for replacement with current evidence or demotion in a follow-up source-of-truth change.
=======
## `/gaia-meta-audit`: 4★+ skills

### Summary

The registry validates structurally, but the 4★+ audit found a recurring evidence-hygiene issue: several high-level skills depend on old `gaia-registry/gaia` seed evidence URLs that currently resolve as missing GitHub pages. Those entries should be prioritized for replacement with current evidence or demotion in a follow-up source-of-truth change.
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split

### Priority review candidates

| Skill | Level | Evidence concern | Recommended next action |
|---|---:|---|---|
| `ghostwrite` | IV | Only listed evidence is a `gaia-registry/gaia` seed document URL that resolves as missing. | Replace with live evidence or demote below Hardened. |
| `autonomous-debug` | IV | Only listed evidence is a `gaia-registry/gaia` seed document URL that resolves as missing. | Replace with live evidence or demote below Hardened. |
| `plan-and-execute` | IV | Only listed evidence is a `gaia-registry/gaia` seed document URL that resolves as missing. | Replace with live evidence or demote below Hardened. |
| `knowledge-harvest` | IV | Only listed evidence is a `gaia-registry/gaia` seed document URL that resolves as missing. | Replace with live evidence or demote below Hardened. |
<<<<<<< HEAD
| `recursive-self-improvement` | V | Uses `gaia-registry/gaia` seed evidence for a Transcendent Ultimate claim. | Require live, composable evidence before retaining 5⭐. |
| `multi-agent-orchestration-v` | V | Uses `gaia-registry/gaia` seed evidence for a Transcendent Ultimate claim. | Require live, composable evidence before retaining 5⭐. |
=======
<<<<<<< Updated upstream
| `recursive-self-improvement` | V | Uses `gaia-registry/gaia` seed evidence for a Transcendent Ultimate claim. | Require live, composable evidence before retaining Level V. |
| `multi-agent-orchestration-v` | V | Uses `gaia-registry/gaia` seed evidence for a Transcendent Ultimate claim. | Require live, composable evidence before retaining Level V. |
>>>>>>> schema/star-tiers-split
| `autonomous-research-agent` | VI | One evidence source is `gaia-registry/gaia` seed evidence; the named external repo is reachable. | Replace seed evidence with current primary evidence before retaining apex confidence. |

### Lower-risk 4⭐+ entries

<<<<<<< HEAD
The remaining 4⭐+ entries have at least one live or externally identifiable source in the local registry metadata, such as arXiv papers, active GitHub projects, or specific skill-library `SKILL.md` files. They remain candidates for future freshness checks, but this pass did not identify the same immediate source-of-truth break as the seed-evidence entries above.
=======
The remaining Level IV+ entries have at least one live or externally identifiable source in the local registry metadata, such as arXiv papers, active GitHub projects, or specific skill-library `SKILL.md` files. They remain candidates for future freshness checks, but this pass did not identify the same immediate source-of-truth break as the seed-evidence entries above.
=======
| `recursive-self-improvement` | V | Uses `gaia-registry/gaia` seed evidence for a Transcendent Ultimate claim. | Require live, composable evidence before retaining 5★. |
| `multi-agent-orchestration-v` | V | Uses `gaia-registry/gaia` seed evidence for a Transcendent Ultimate claim. | Require live, composable evidence before retaining 5★. |
| `autonomous-research-agent` | VI | One evidence source is `gaia-registry/gaia` seed evidence; the named external repo is reachable. | Replace seed evidence with current primary evidence before retaining apex confidence. |

### Lower-risk 4★+ entries

The remaining 4★+ entries have at least one live or externally identifiable source in the local registry metadata, such as arXiv papers, active GitHub projects, or specific skill-library `SKILL.md` files. They remain candidates for future freshness checks, but this pass did not identify the same immediate source-of-truth break as the seed-evidence entries above.
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split
