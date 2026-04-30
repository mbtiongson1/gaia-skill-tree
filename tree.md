# Gaia Skill Tree

```
GAIA SKILL TREE  v1.0.0  ·  generated 2026-04-30
══════════════════════════════════════════════════════════════════════
Upgrade paths — each legendary shows its full prerequisite chain.
Shared prerequisites marked (↑ see above) on second occurrence.
══════════════════════════════════════════════════════════════════════

◆ karpathy/autoresearch - Wisdom King: Autonomous Research Agent  [VI]
─────────────────────────────────────────────────────────────────
  ├─ ◇ /research  [III]
  │  ├─ ○ /web-search  [I]
  │  ├─ ○ /summarize  [0]
  │  └─ ○ /cite-sources  [I]
  ├─ ◇ /knowledge-harvest  [IV]
  │  ├─ ◇ /web-scrape  [III]
  │  │  ├─ ○ /web-search  [I]  (↑ see above)
  │  │  ├─ ○ /parse-html  [I]
  │  │  └─ ○ /extract-entities  [I]
  │  ├─ ○ /extract-entities  [I]  (↑ see above)
  │  └─ ○ /embed-text  [I]
  └─ ◇ /ghostwrite  [IV]
     ├─ ◇ /research  [III]  (↑ see above)
     ├─ ○ glincker/readme-generator - Write Report  [I]
     └─ ○ /audience-model  [I]

◆ ruvnet/flow-nexus-swarm - Grand Conductor: Multi-Agent Orchestration  [V]
─────────────────────────────────────────────────────────────────
  ├─ ◇ /plan-and-execute  [IV]
  │  ├─ ○ /route-intent  [I]
  │  ├─ ○ /plan-decompose  [I]
  │  └─ ○ /tool-select  [I]
  ├─ ○ /route-intent  [I]  (↑ see above)
  └─ ○ /tool-select  [I]  (↑ see above)

◆ /full-stack-developer  [V]
─────────────────────────────────────────────────────────────────
  ├─ ◇ /code-review-pipeline  [III]
  │  ├─ ○ /code-generation  [I]
  │  ├─ ○ /diff-content  [I]
  │  └─ ○ /evaluate-output  [I]
  ├─ ◇ 0xdarkmatter/pytest-patterns - Automated Testing  [III]
  │  ├─ ○ upsonic/unittest-generator - Generate Test  [II]
  │  ├─ ○ /execute-bash  [I]
  │  └─ ○ /error-interpretation  [I]
  └─ ○ mattpocock/improve-codebase-architecture - Refactor Code  [II]

◆ /scientific-discovery  [V]
─────────────────────────────────────────────────────────────────
  ├─ ○ /hypothesis-generate  [II]
  ├─ ◇ /research  [III]
  │  ├─ ○ /web-search  [I]
  │  ├─ ○ /summarize  [0]
  │  └─ ○ /cite-sources  [I]
  └─ ○ /math-reason  [II]

◆ /real-time-voice-assistant  [V]
─────────────────────────────────────────────────────────────────
  ├─ ◇ /voice-agent  [III]
  │  ├─ ○ /speech-to-text  [II]
  │  ├─ ○ /question-answer  [0]
  │  └─ ○ /text-to-speech  [II]
  ├─ ○ /memory-manage  [II]
  └─ ◇ /plan-and-execute  [IV]
     ├─ ○ /route-intent  [I]
     ├─ ○ /plan-decompose  [I]
     └─ ○ /tool-select  [I]

◆ /autonomous-data-scientist  [V]
─────────────────────────────────────────────────────────────────
  ├─ ◇ /data-analysis  [III]
  │  ├─ ○ /generate-sql  [II]
  │  ├─ ○ /data-visualize  [II]
  │  └─ ○ /summarize  [0]
  ├─ ○ /math-reason  [II]
  └─ ◇ /research  [III]
     ├─ ○ /web-search  [I]
     ├─ ○ /summarize  [0]  (↑ see above)
     └─ ○ /cite-sources  [I]

◆ /recursive-self-improvement  [V]
─────────────────────────────────────────────────────────────────
  ├─ ◇ devin-ai/autonomous-swe - Autonomous Debug  [IV]
  │  ├─ ○ /code-generation  [I]
  │  ├─ ○ /execute-bash  [I]
  │  └─ ○ /error-interpretation  [I]
  ├─ ○ /evaluate-output  [I]
  └─ ◇ /plan-and-execute  [IV]
     ├─ ○ /route-intent  [I]
     ├─ ○ /plan-decompose  [I]
     └─ ○ /tool-select  [I]

══════════════════════════════════════════════════════════════════════
Pure / Undeveloped — atomic skills not yet wired into any upgrade path.
══════════════════════════════════════════════════════════════════════

  ○ /code-execution  [II · Named]
  ○ mattpocock/zoom-out - Code Explain  [II · Named]
  ○ /context-compression  [III · Evolved]
  ○ /detect-anomaly  [II · Named]
  ○ anthropic/pptx - Document Editing  [0 · Basic]
  ○ /few-shot-learning  [IV · Hardened]
  ○ /fine-tune  [IV · Hardened]
  ○ laravel/upgrade-laravel-v13 - Framework Upgrade  [0 · Basic]
  ○ /image-generate  [II · Named]
  ○ mattpocock/triage - Issue Triage  [IV · Hardened]
  ○ /object-detection  [II · Named]
  ○ /ocr  [II · Named]
  ○ /prompt-injection-defense  [III · Evolved]
  ○ /reward-modeling  [II · Named]
  ○ /self-consistency  [IV · Hardened]
  ○ /semantic-cache  [IV · Hardened]
  ○ vercel/find-skills - Skill Discovery  [0 · Basic]
  ○ /statistical-analysis  [III · Evolved]
  ○ addy-osmani/test-driven-development - Test-Driven Development  [0 · Basic]
  ○ martin-stepanoski/nielsen-heuristics-audit - UX Audit  [0 · Basic]
  ○ /vision-qa  [III · Evolved]

```

*Generated from gaia.json v1.0.0 on 2026-04-30. Do not edit directly.*
