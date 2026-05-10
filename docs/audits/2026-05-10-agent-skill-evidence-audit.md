# Agent Skill Evidence Audit — 2026-05-10

## Scope

Quick evidence-quality audit for the four skills added in commit `9f3a965`:

- `skill-authoring`
- `skill-performance-benchmarking`
- `skill-security-analysis`
- `mcp-server-creation`

## Method

- Checked each evidence URL for resolvability.
- Confirmed whether the evidence directly supports the claimed capability, rather than merely an adjacent engineering workflow.
- Preferred direct agent-skill papers, official SDKs, and reproducible repositories over broad or archived sources.

## Verdict

<<<<<<< HEAD
Overall evidence quality is now acceptable for provisional 4★ nodes: every skill has at least one directly relevant Class A or Class B source, and the weakest sources from the initial pass were replaced or supplemented.
=======
<<<<<<< Updated upstream
Overall evidence quality is now acceptable for provisional Level IV nodes: every skill has at least one directly relevant Class A or Class B source, and the weakest sources from the initial pass were replaced or supplemented.
=======
Overall evidence quality is now acceptable for provisional 4★ nodes: every skill has at least one directly relevant Class A or Class B source, and the weakest sources from the initial pass were replaced or supplemented.
>>>>>>> Stashed changes
>>>>>>> schema/star-tiers-split

## Findings and corrections

| Skill | Audit result | Correction |
|---|---|---|
| `skill-authoring` | Good. The Anthropic `skill-creator` SKILL.md directly demonstrates authoring, iteration, and evaluation; the arXiv ecosystem paper supports the skill abstraction. | No registry change. |
| `skill-performance-benchmarking` | Good after supplement. The arXiv AgentSkillOS paper is directly relevant, but the original second source reused `skill-creator`; adding the AgentSkillOS repository makes the benchmark implementation evidence reproducible. | Added `https://github.com/ynulihao/AgentSkillOS` as Class B evidence. |
| `skill-security-analysis` | Improved. The original `security-and-hardening` SKILL.md was too generic because it covered application security, not third-party agent-skill package review. | Removed the generic hardening source and added `https://arxiv.org/abs/2604.25109`, which directly studies pre-load auditing of untrusted Agent Skills. |
| `mcp-server-creation` | Improved. Anthropic `mcp-builder` is strong direct evidence, but `modelcontextprotocol/create-python-server` is archived and therefore a weak current implementation source. | Replaced the archived scaffold with active official `https://github.com/modelcontextprotocol/python-sdk` evidence. |

## Remaining caveat

Gaia currently treats arXiv papers as Class A evidence throughout the registry. These entries are suitable under that repository convention, but several are preprints rather than independently peer-reviewed publications; keep `status: "provisional"` until maintainer review.
