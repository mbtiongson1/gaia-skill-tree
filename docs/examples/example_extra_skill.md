# Example: New Extra Skill Submission

This is a filled-out example of a `new_extra_skill.md` PR for reference.

---

## New Extra Skill

### Skill Details
- **ID:** `dataAnalysisPipeline`
- **Name:** Data Analysis Pipeline
- **Level:** III
- **Prerequisites:** `parseCsv`, `summarize`, `formatOutput`, `evaluateOutput`
- **Description:** End-to-end data analysis workflow that ingests structured data, produces statistical summaries, evaluates output quality, and formats results for consumption.
- **Fusion Condition:** Input must be tabular data in a recognized format.

### Evidence
| Class | Source | Evaluator | Date | Notes |
|---|---|---|---|---|
| B | https://github.com/example/analysis-pipeline/blob/main/demo.md | mbtiongson1 | 2026-04-26 | Reproducible demo showing ingestion of 3 CSV datasets with summary output and quality checks. |

### Rationale
The individual skills (`parseCsv`, `summarize`, `formatOutput`, `evaluateOutput`) each handle one step of data processing. When combined, they produce an emergent pipeline capability: the agent can take raw data and deliver a complete, quality-checked analytical summary without human intervention at intermediate steps. This is more than "running them in sequence" — it requires the agent to make routing decisions about which summarization strategy fits the data shape and to self-evaluate output before formatting.

### Checklist

**Contributor:**
- [x] Skill ID uses `camelCase` with no vendor references.
- [x] Description describes an emergent capability, not just "all parents at once."
- [x] At least 2 prerequisites listed, all referencing existing skill IDs.
- [x] Evidence meets the minimum threshold (3⭐ = Evidence Tier B+).
- [x] Fusion condition is specified.
- [x] I have run `python scripts/validate.py` locally and it passes.
- [x] I have NOT edited any files in `skills/`, `registry.md`, or `combinations.md`.
