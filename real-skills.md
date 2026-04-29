# Gaia Real Skill Catalog

Curated named skills from live SKILL.md ecosystems, grouped into Gaia-friendly buckets for review before promotion into the canonical graph.

## Sources

| Source | Type | Reported skills | Notes |
|---|---|---:|---|
| [VoltAgent Awesome Agent Skills](https://github.com/VoltAgent/awesome-agent-skills) | curated-index | 1100+ | Hand-picked index of official and community SKILL.md repositories across Claude Code, Codex, Gemini CLI, Cursor, and related agents. |
| [AgentSkills.me](https://agentskills.me/) | directory | 490 | Browseable directory with concrete skill pages, popularity signals, source repositories, tool filters, and SKILL.md paths. |
| [Superpowers Skills](https://github.com/paulirish/superpowers) | methodology-skillset | 13 | Popular workflow skill set centered on agent discipline: brainstorming, TDD, debugging, planning, verification, review, and parallel execution. |
| [Official Skills](https://officialskills.sh/) | official-skill-index | 1000+ | Public pages linked by the VoltAgent index for official skills from Anthropic, Vercel, Stripe, Cloudflare, OpenAI, Hugging Face, and others. |

## Agent Workflow and Superpowers

Named skills that improve how an agent plans, verifies, recovers context, and collaborates with humans.

- [superpowers/using-superpowers](https://github.com/paulirish/superpowers) - Routes each task through relevant skills before answering or editing. Source: Superpowers Skills. Path: `skills/using-superpowers/SKILL.md`. Maps to: `route-intent`, `tool-select`, `self-critique`.
- [superpowers/brainstorming](https://github.com/paulirish/superpowers) - Turns open-ended feature ideas into reviewed designs before implementation. Source: Superpowers Skills. Path: `skills/brainstorming/SKILL.md`. Maps to: `plan-decompose`, `audience-model`, `write-report`.
- [superpowers/test-driven-development](https://github.com/paulirish/superpowers) - Requires red-green-refactor implementation with failing tests before production code. Source: Superpowers Skills. Path: `skills/test-driven-development/SKILL.md`. Maps to: `generate-test`, `code-generation`, `evaluate-output`.
- [superpowers/systematic-debugging](https://github.com/paulirish/superpowers) - Frames failures around evidence, reproduction, hypothesis testing, and root cause. Source: Superpowers Skills. Path: `skills/systematic-debugging/SKILL.md`. Maps to: `error-interpretation`, `execute-bash`, `autonomous-debug`.
- [superpowers/verification-before-completion](https://github.com/paulirish/superpowers) - Prevents completion claims until direct verification commands have run. Source: Superpowers Skills. Path: `skills/verification-before-completion/SKILL.md`. Maps to: `evaluate-output`, `execute-bash`, `self-critique`.
- [session-handoff](https://agentskills.me/skill/session-handoff) - Creates durable handoff documents for long-running agent sessions and context transfers. Source: AgentSkills.me. Path: `skills/session-handoff`. Maps to: `memory-manage`, `write-report`, `format-output`.

## Engineering Execution

Skills that directly support codebase work, dependency changes, commits, reviews, and multi-agent coding workflows.

- [codex](https://agentskills.me/skill/codex) - Runs Codex CLI for code analysis, refactoring, and automated editing. Source: AgentSkills.me. Path: `skills/codex`. Maps to: `code-generation`, `refactor-code`, `execute-bash`.
- [gemini](https://agentskills.me/skill/gemini) - Runs Gemini CLI for large-context code review, planning, and analysis. Source: AgentSkills.me. Path: `skills/gemini`. Maps to: `code-review-pipeline`, `summarize`, `evaluate-output`.
- [dependency-updater](https://agentskills.me/skill/dependency-updater) - Detects project dependency managers and applies safe dependency updates. Source: AgentSkills.me. Path: `skills/dependency-updater`. Maps to: `execute-bash`, `detect-anomaly`, `automated-testing`.
- [commit-work](https://agentskills.me/skill/commit-work) - Stages intended changes, splits commits, and writes clear commit messages. Source: AgentSkills.me. Path: `skills/commit-work`. Maps to: `diff-content`, `summarize`, `format-output`.
- [superpowers/subagent-driven-development](https://github.com/paulirish/superpowers) - Coordinates independent implementation slices across parallel coding agents. Source: Superpowers Skills. Path: `skills/subagent-driven-development/SKILL.md`. Maps to: `multi-agent-orchestration-v`, `plan-decompose`, `tool-select`.

## Frontend and Product Experience

Real named skills for UI quality, framework best practices, frontend testing, product content, and design systems.

- [vercel-react-best-practices](https://agentskills.me/skill/vercel-react-best-practices) - Applies React and Next.js performance patterns from Vercel Engineering. Source: AgentSkills.me. Path: `skills/react-best-practices`. Maps to: `code-generation`, `refactor-code`, `automated-testing`.
- [frontend-design](https://agentskills.me/skill/frontend-design) - Creates distinctive, production-grade frontend interfaces. Source: AgentSkills.me. Path: `frontend-design`. Maps to: `audience-model`, `code-generation`, `multimodal-reasoning`.
- [web-design-guidelines](https://agentskills.me/skill/web-design-guidelines) - Captures modern responsive layout, accessibility, and visual hierarchy rules. Source: AgentSkills.me. Path: `skills/web-design-guidelines`. Maps to: `audience-model`, `write-report`, `evaluate-output`.
- [webapp-testing](https://officialskills.sh/anthropics/skills/webapp-testing) - Tests local web applications with browser automation. Source: VoltAgent Awesome Agent Skills. Path: `anthropics/webapp-testing`. Maps to: `automated-testing`, `computer-use`, `evaluate-output`.
- [shadcn-ui](https://officialskills.sh/google-labs-code/skills/shadcn-ui) - Guides shadcn component usage for modern web UI work. Source: VoltAgent Awesome Agent Skills. Path: `google-labs-code/shadcn-ui`. Maps to: `code-generation`, `format-output`, `refactor-code`.

## Documents, Research, and Data

Named skills for office documents, external research, scraping, data tools, and model/data discovery.

- [anthropics/docx](https://officialskills.sh/anthropics/skills/docx) - Creates, edits, and analyzes Word documents. Source: VoltAgent Awesome Agent Skills. Path: `anthropics/docx`. Maps to: `parse-pdf`, `write-report`, `document-analyst`.
- [anthropics/xlsx](https://officialskills.sh/anthropics/skills/xlsx) - Creates, edits, and analyzes spreadsheets. Source: VoltAgent Awesome Agent Skills. Path: `anthropics/xlsx`. Maps to: `data-analysis`, `data-visualize`, `generate-sql`.
- [firecrawl/firecrawl-build-search](https://officialskills.sh/firecrawl/skills/firecrawl-build-search) - Integrates query-first web discovery with optional content hydration. Source: VoltAgent Awesome Agent Skills. Path: `firecrawl/firecrawl-build-search`. Maps to: `web-search`, `web-scrape`, `research`.
- [huggingface/hf-cli](https://officialskills.sh/huggingface/skills/hf-cli) - Uses the Hugging Face Hub CLI for model, dataset, and Space workflows. Source: VoltAgent Awesome Agent Skills. Path: `huggingface/hf-cli`. Maps to: `retrieve`, `api-call`, `research`.
- [arxiv-search](https://agentskills.me/skill/arxiv-search) - Searches and summarizes arXiv papers for research tasks. Source: AgentSkills.me. Path: `skills/arxiv-search`. Maps to: `web-search`, `summarize`, `cite-sources`.

## Platform and Domain Skills

Product-specific skills with clear sources that can inform future Gaia composites or known-agent mappings.

- [stripe/stripe-best-practices](https://officialskills.sh/stripe/skills/stripe-best-practices) - Guides Stripe integration decisions and implementation patterns. Source: VoltAgent Awesome Agent Skills. Path: `stripe/stripe-best-practices`. Maps to: `api-call`, `code-generation`, `evaluate-output`.
- [cloudflare/workers-best-practices](https://officialskills.sh/cloudflare/skills/workers-best-practices) - Captures Cloudflare Workers runtime and deployment patterns. Source: VoltAgent Awesome Agent Skills. Path: `cloudflare/workers-best-practices`. Maps to: `code-generation`, `execute-bash`, `automated-testing`.
- [netlify/netlify-deploy](https://officialskills.sh/netlify/skills/netlify-deploy) - Deploys and troubleshoots Netlify applications. Source: VoltAgent Awesome Agent Skills. Path: `netlify/netlify-deploy`. Maps to: `execute-bash`, `api-call`, `evaluate-output`.
- [better-auth/create-auth](https://officialskills.sh/better-auth/skills/create-auth) - Creates authentication setup with Better Auth. Source: VoltAgent Awesome Agent Skills. Path: `better-auth/create-auth`. Maps to: `code-generation`, `api-call`, `automated-testing`.
- [veniceai/venice-chat](https://github.com/veniceai/skills/tree/main/skills/venice-chat) - Builds chat completions, multimodal inputs, tool calls, and streaming against Venice APIs. Source: VoltAgent Awesome Agent Skills. Path: `veniceai/venice-chat`. Maps to: `api-call`, `multimodal-reasoning`, `conversational-agent`.

*Generated from graph/real_skill_catalog.json on 2026-04-30.*
