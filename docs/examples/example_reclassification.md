# Example: Reclassification Request

This is a filled-out example of a `reclassification.md` PR for reference.

---

## Reclassification Request

### Target Skill
- **ID:** `webScrape`
- **Current Level:** III → **Proposed Level:** IV
- **Current Rarity:** Uncommon → **Proposed Rarity:** Uncommon (no change)

### Justification
<<<<<<< Updated upstream
Since the initial Level III classification, multiple independent demonstrations have shown `webScrape` handling dynamic JavaScript-rendered pages, pagination, and anti-bot measures — failure modes that were previously undocumented. The skill now meets the Level IV bar: "Handles edge cases and failures."
=======
Since the initial 3★ classification, multiple independent demonstrations have shown `webScrape` handling dynamic JavaScript-rendered pages, pagination, and anti-bot measures — failure modes that were previously undocumented. The skill now meets the 4★ bar: "Handles edge cases and failures."
>>>>>>> Stashed changes

### New Evidence
| Class | Source | Evaluator | Date | Notes |
|---|---|---|---|---|
| B | https://github.com/example/scraper-v2/blob/main/RESULTS.md | contributor1 | 2026-04-26 | Demonstrated scraping of 50 JS-rendered pages with Playwright, handling CAPTCHAs and rate limits. Logs archived. |
| B | https://github.com/example/scraper-benchmark/blob/main/benchmark.md | contributor2 | 2026-04-25 | Benchmarked across 10 anti-bot-protected sites. 92% success rate with documented failure analysis. |

### Checklist

**Contributor:**
- [x] Justification references concrete evidence, not opinion.
<<<<<<< Updated upstream
- [x] New evidence meets the threshold for Level IV (Evidence Tier B+).
- [x] Explanation of why previous Level III classification is now insufficient.
=======
- [x] New evidence meets the threshold for 4★ (Evidence Tier B+).
- [x] Explanation of why previous 3★ classification is now insufficient.
>>>>>>> Stashed changes
- [x] Rarity unchanged (prevalence data has not shifted).
- [x] I have run `python scripts/validate.py` locally and it passes.
