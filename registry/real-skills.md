# Gaia Real Skill Catalog

Curated named skills from live SKILL.md ecosystems.

## Sources

| Source | Description | URL |
|---|---|---|
| karpathy/autoresearch | Autonomous research agent that iteratively reviews academic papers and synthesizes summaries. | https://github.com/karpathy/autoresearch |
| cognition-labs/devin | Autonomous software engineering agent capable of end-to-end debugging and code generation. | https://github.com/cognition-labs/devin |
| laravel/boost | Laravel Boost -- AI-assisted Laravel framework upgrade tooling. | https://github.com/laravel/boost |
| anthropics/skills | Anthropic official Claude Code skill library. | https://github.com/anthropics/skills |
| vercel-labs/skills | Vercel Labs skill library for Claude Code and Codex CLI. | https://github.com/vercel-labs/skills |
| GLINCKER/claude-code-marketplace | GLINCKER community marketplace for Claude Code skills. | https://github.com/GLINCKER/claude-code-marketplace |
| addyosmani/agent-skills | Addy Osmani collection of agent workflow enforcement skills. | https://github.com/addyosmani/agent-skills |
| mastepanoski/claude-skills | Martin Stepanoski NPM package of UX-focused Claude skills. | https://classic.yarnpkg.com/en/package/@mastepanoski/claude-skills |
| spring-ai-alibaba/examples | Spring AI Alibaba example projects including Claude Code skills. | https://github.com/spring-ai-alibaba/examples |
| ruvnet/ruflo | Leading agent orchestration platform for Claude with multi-agent swarm deployment and event-driven workflows. | https://github.com/ruvnet/ruflo |
| gooseworks-ai/goose-skills | Library of GTM skills for Claude Code, Codex, Cursor including AI-first browser automation via Notte. | https://github.com/gooseworks-ai/goose-skills |
| yonatangross/orchestkit | Complete AI development toolkit for Claude Code with 103 skills including a production-grade RAG retrieval skill. | https://github.com/yonatangross/orchestkit |
| Upsonic/Upsonic | Framework for building autonomous AI agents in Python with prebuilt agent skills. | https://github.com/Upsonic/Upsonic |
| aiskillstore/marketplace | Security-audited skills marketplace for Claude Code and Codex CLI with quality-verified patterns. | https://github.com/aiskillstore/marketplace |

## Items

- [karpathy/autoresearch](https://github.com/karpathy/autoresearch) - Autonomous research agent that iteratively searches academic databases, reads papers, extracts findings, and produces structured research summaries. Maps to: `autonomous-research-agent`.
- [devin-ai/autonomous-swe](https://github.com/cognition-labs/devin) - Autonomous software engineering agent that combines debugging, code generation, and self-correction to resolve issues end-to-end across complex multi-file repositories. Maps to: `autonomous-debug`.
- [laravel/upgrade-laravel-v13](https://github.com/laravel/boost/issues/698) - Guides an AI agent through upgrading a Laravel 12 application to Laravel 13 safely, covering breaking changes, dependency updates, and post-upgrade validation. Maps to: `framework-upgrade`.
- [anthropic/skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) - Interviews the user to elicit skill purpose and steps, then programmatically writes a new SKILL.md file for Claude Code or Codex CLI. Maps to: `tool-creation`.
- [vercel/find-skills](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) - Searches the skills.sh registry by keyword, ranks by install count, and auto-installs the chosen skill. Maps to: `skill-discovery`.
- [glincker/readme-generator](https://github.com/GLINCKER/claude-code-marketplace/blob/main/skills/documentation/readme-generator/SKILL.md) - Analyzes project structure, manifests, and configs to generate a professional README.md with badges, install steps, and usage examples. Maps to: `write-report`.
- [anthropic/pptx](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) - Extracts, edits, and repacks PowerPoint (.pptx) files using markitdown, enabling agents to read, modify, and write structured presentations without a GUI. Maps to: `document-editing`.
- [addy-osmani/test-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md) - Forces a strict red-green-refactor TDD workflow, blocking code generation that skips the test step and enforcing coverage thresholds. Maps to: `test-driven-development`.
- [martin-stepanoski/nielsen-heuristics-audit](https://github.com/mastepanoski/claude-skills/blob/main/skills/nielsen-heuristics-audit/SKILL.md) - Audits a UI against Jakob Nielsen's 10 usability heuristics, scores each, and produces a prioritized remediation report. Maps to: `ux-audit`.
- [ruvnet/flow-nexus-swarm](https://github.com/ruvnet/ruflo) - Cloud-based AI swarm orchestration supporting hierarchical, mesh, ring, and star topologies with event-driven workflows and intelligent agent assignment. Maps to: `multi-agent-orchestration-v`.
- [gooseworks/notte-browser](https://github.com/gooseworks-ai/goose-skills) - AI-first browser automation using the Notte Browser API for session control, page scraping, form filling, and autonomous web agent execution. Maps to: `browser-automation`.
- [yonatangross/orchestkit-rag](https://github.com/yonatangross/orchestkit) - Production-grade RAG retrieval skill covering 30+ patterns: HyDE, pgvector hybrid search, cross-encoder reranking, multimodal chunking, and agentic self-RAG and corrective-RAG loops. Maps to: `rag-pipeline`.
- [upsonic/unittest-generator](https://github.com/Upsonic/Upsonic) - Autonomous Claude agent that generates comprehensive unittest.TestCase suites from source code, organised into concept-based subfolders. Maps to: `generate-test`.
- [0xdarkmatter/pytest-patterns](https://github.com/aiskillstore/marketplace) - Comprehensive pytest skill covering fixtures, parametrize, async testing, mocking, coverage strategies, and integration test patterns for pytest 7.0+ projects. Maps to: `automated-testing`.
- [spring-ai/readme-generate](https://github.com/spring-ai-alibaba/examples/blob/main/.claude/skills/readme-generate/SKILL.md) - Scans a Java Spring project for controller annotations, extracts REST API endpoint definitions, and generates structured API documentation in README format. Maps to: `write-report`.
- [mattpocock/diagnose](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnose/SKILL.md) - Enforces a five-phase debugging discipline prioritising the feedback loop above all else — refuses to proceed until a fast deterministic pass/fail signal exists. Maps to: `autonomous-debug`.
- [mattpocock/tdd](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) - Enforces strict vertical-slice TDD, blocking horizontal slicing (all tests first, then all code) and requiring tests against public interfaces only. Maps to: `test-driven-development`.
- [mattpocock/zoom-out](https://github.com/mattpocock/skills/blob/main/skills/engineering/zoom-out/SKILL.md) - Signals the agent to ascend one layer of abstraction and produce a map of all relevant modules, callers, and domain-glossary terms. Maps to: `code-explain`.
- [mattpocock/edit-article](https://github.com/mattpocock/skills/blob/main/skills/personal/edit-article/SKILL.md) - Edits articles by modelling them as a DAG of information dependencies, confirming section order, then rewriting each section with a 240-character-per-paragraph constraint. Maps to: `document-editing`.
- [mattpocock/write-a-skill](https://github.com/mattpocock/skills/blob/main/skills/productivity/write-a-skill/SKILL.md) - Guides creation of new agent skills via structured interview, producing a SKILL.md with trigger-aware description, progressive-disclosure layout, and optional bundled scripts. Maps to: `tool-creation`.
- [mattpocock/triage](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md) - Moves GitHub issues through a two-category x five-state machine with bug reproduction, agent-brief writing, and structured triage notes bearing an AI-generation disclaimer. Maps to: `issue-triage`.
- [mattpocock/to-prd](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md) - Synthesises conversation context and codebase knowledge into a fully-structured PRD with user stories, implementation decisions, and testing decisions, then publishes to the issue tracker. Maps to: `prd-generation`.
- [mattpocock/to-issues](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md) - Breaks a plan into independently-demoable vertical slices, classifies each HITL or AFK, maps dependency chains, and publishes structured GitHub issues with acceptance criteria in dependency order. Maps to: `vertical-slice-planning`.
- [mattpocock/grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) - Stress-tests a plan against the project's domain model, challenging language against CONTEXT.md, cross-referencing code, and persisting resolved decisions as inline glossary updates and ADRs. Maps to: `design-review`.
- [mattpocock/grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) - Conducts a relentless one-question-at-a-time interview walking every branch of the decision tree with a recommended answer, substituting codebase exploration wherever empirically determinable. Maps to: `design-review`.
- [mattpocock/improve-codebase-architecture](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md) - Identifies shallow modules via the deletion test, presents deepening opportunities with locality/leverage analysis, then grills the developer on the chosen candidate to design a deep-module replacement. Maps to: `refactor-code`.

*Generated from registry/real-skills.json on 2026-04-30.*
