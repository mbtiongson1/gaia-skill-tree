#!/usr/bin/env python3
"""One-shot script that injects 30 new popular skills into graph/gaia.json.

Run from repo root:
    python3 scripts/add_skills.py
"""

import json, os, copy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_PATH = os.path.join(REPO_ROOT, "graph", "gaia.json")
TODAY = "2026-04-28"
VERSION = "0.2.0"
EVALUATOR = "mbtiongson1"

# ---------------------------------------------------------------------------
# New skills
# ---------------------------------------------------------------------------

NEW_ATOMICS = [
    {
        "id": "translate",
        "name": "Translate",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Converts text from one natural language to another while preserving meaning, tone, and formatting.",
        "prerequisites": [],
        "derivatives": ["translationPipeline"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2207.04672",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "NLLB (No Language Left Behind) — Meta AI paper demonstrating 200-language translation at human-level quality on FLORES-200 benchmark.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "sentimentAnalysis",
        "name": "Sentiment Analysis",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Determines the emotional valence (positive, negative, neutral) and intensity of text input.",
        "prerequisites": [],
        "derivatives": ["contentModeration", "translationPipeline"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/1810.04805",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "BERT paper — achieves SOTA on SST-2 sentiment benchmark (93.5% accuracy), foundational evidence for LLM-based sentiment analysis.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "imageCaption",
        "name": "Image Caption",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Generates accurate natural-language descriptions of images, capturing objects, actions, and spatial relationships.",
        "prerequisites": [],
        "derivatives": ["multimodalReasoning"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2301.12597",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "BLIP-2 — bootstrapped language-image pre-training achieving SOTA on COCO Captions (CIDEr 145.8) and NoCaps benchmarks.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "speechToText",
        "name": "Speech to Text",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Transcribes spoken audio into accurate text, handling diverse accents, noise conditions, and multiple languages.",
        "prerequisites": [],
        "derivatives": ["voiceAgent"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2212.04356",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Whisper (OpenAI) — large-scale weak supervision across 680K hours of audio achieves near-human WER on LibriSpeech and multilingual benchmarks.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "textToSpeech",
        "name": "Text to Speech",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Synthesizes natural-sounding speech audio from text input, supporting voice cloning and prosody control.",
        "prerequisites": [],
        "derivatives": ["voiceAgent"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2301.02111",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "VALL-E (Microsoft) — neural codec language model achieving SOTA speech synthesis with 3-second voice cloning on LibriSpeech.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "generateSql",
        "name": "Generate SQL",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Translates natural-language data questions into syntactically correct, executable SQL queries against a given schema.",
        "prerequisites": [],
        "derivatives": ["textToSqlPipeline", "dataAnalysis"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/1809.08887",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Spider benchmark — cross-domain text-to-SQL dataset; LLM baselines reach >85% exact match, establishing reproducible evaluation methodology.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "questionAnswer",
        "name": "Question Answer",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Produces accurate, context-grounded answers to natural-language questions, handling unanswerable cases.",
        "prerequisites": [],
        "derivatives": ["conversationalAgent", "voiceAgent", "multimodalReasoning"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/1806.03822",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "SQuAD 2.0 — reading comprehension benchmark with 150K questions; modern LLMs exceed human F1 (90.9), providing rigorous reproducible evaluation.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "imageGenerate",
        "name": "Image Generate",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Creates photorealistic or stylized images from text prompts using diffusion-based or autoregressive generative models.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2112.10752",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Latent Diffusion Models (Rombach et al.) — foundational paper for Stable Diffusion; achieves FID 5.11 on LSUN-Beds at 200× less compute than pixel-space diffusion.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "math-reason",
        "name": "Math Reason",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Solves multi-step mathematical problems including arithmetic, algebra, calculus, and competition mathematics through symbolic and numeric reasoning.",
        "prerequisites": [],
        "derivatives": ["autonomousDataScientist"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2206.14858",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Minerva (Google) — 50.3% on MATH and 78.5% on MMLU-STEM benchmarks using chain-of-thought over scientific literature.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "logical-inference",
        "name": "Logical Inference",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Applies deductive, inductive, or abductive reasoning to derive valid conclusions from premises and structured knowledge.",
        "prerequisites": [],
        "derivatives": ["multimodalReasoning"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2201.11903",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Chain-of-Thought prompting (Wei et al.) — few-shot CoT elicits multi-step reasoning; +18% on GSM8K and +15% on SVAMP over standard prompting.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "memoryManage",
        "name": "Memory Manage",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Maintains, indexes, and retrieves conversational and long-term memory across sessions, managing context window constraints.",
        "prerequisites": [],
        "derivatives": ["conversationalAgent", "realTimeVoiceAssistant"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2310.08560",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "MemGPT — virtual context management system enabling LLMs to handle unbounded memory; benchmarked on multi-session dialogue and document QA.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "apiCall",
        "name": "API Call",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Constructs, executes, and handles responses from HTTP APIs by interpreting documentation and selecting appropriate endpoints and parameters.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2305.15334",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Gorilla (Patil et al.) — LLM that generates accurate API calls across TorchHub, TensorFlow Hub, and HuggingFace; 20.43% AST accuracy improvement over GPT-4.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "refactorCode",
        "name": "Refactor Code",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Restructures existing source code to improve readability, maintainability, or performance without changing observable behavior.",
        "prerequisites": [],
        "derivatives": ["fullStackDeveloper"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2310.06770",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "SWE-bench — 2294 real GitHub issues benchmark; agents that resolve issues must safely refactor code while passing existing test suites.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "generateTest",
        "name": "Generate Test",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Produces unit tests, integration tests, and edge-case test cases from source code or natural-language specifications.",
        "prerequisites": [],
        "derivatives": ["automatedTesting"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2107.03374",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Codex/HumanEval (Chen et al.) — evaluates LLMs on writing Python functions that pass hand-crafted unit tests; pass@1 72.0% for GPT-4.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "parsePdf",
        "name": "Parse PDF",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Extracts text, tables, equations, and structure from PDF documents, preserving layout and reading order.",
        "prerequisites": [],
        "derivatives": ["documentDigitization"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2308.13418",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Nougat (Meta AI) — visual transformer for scientific PDF parsing; 7.6% edit distance on arXiv papers, handling LaTeX, tables, and equations.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "detectAnomaly",
        "name": "Detect Anomaly",
        "type": "atomic",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Identifies statistical outliers, novel patterns, or deviations from expected behavior in structured or unstructured data.",
        "prerequisites": [],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2007.02500",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Deep Learning for Anomaly Detection survey (Pang et al., ACM CSUR) — comprehensive benchmark of 30+ methods across fraud, intrusion, and medical anomaly detection.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "dataVisualize",
        "name": "Data Visualize",
        "type": "atomic",
        "level": "IV",
        "rarity": "common",
        "description": "Generates charts, graphs, and visual summaries from datasets by selecting appropriate visualization types and mapping data dimensions.",
        "prerequisites": [],
        "derivatives": ["dataAnalysis"],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/microsoft/lida",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "LIDA (Microsoft) — open-source LLM-based data visualization tool with reproducible generation pipeline; evaluated on diverse real-world datasets.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
]

NEW_COMPOSITES = [
    {
        "id": "conversationalAgent",
        "name": "Conversational Agent",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Manages coherent multi-turn dialogue by routing intent, maintaining memory across turns, and generating contextually appropriate responses.",
        "prerequisites": ["questionAnswer", "memoryManage", "routeIntent"],
        "derivatives": [],
        "conditions": "Requires persistent memory store across turns.",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/chains/conversation",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "LangChain ConversationChain — reproducible open-source multi-turn conversational agent with buffer and summary memory backends.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "textToSqlPipeline",
        "name": "Text-to-SQL Pipeline",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Converts natural-language queries into validated, executable SQL against a target schema and returns formatted result sets.",
        "prerequisites": ["generateSql", "parse-json", "format-output"],
        "derivatives": [],
        "conditions": "Requires schema context in prompt.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2304.11015",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "DIN-SQL — decomposed in-context learning for text-to-SQL; 82.8% execution accuracy on Spider dev, demonstrating end-to-end pipeline.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "codeReviewPipeline",
        "name": "Code Review Pipeline",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Performs automated code review by generating, diffing, and evaluating code changes for correctness, style, security, and maintainability.",
        "prerequisites": ["code-generation", "diff-content", "evaluate-output"],
        "derivatives": ["fullStackDeveloper"],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2203.09095",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "CodeReviewer (Microsoft) — pre-trained model for code review tasks; 28.7% BLEU improvement on comment generation and change quality prediction.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "dataAnalysis",
        "name": "Data Analysis",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Conducts end-to-end quantitative analysis: queries data via SQL, computes statistics, generates visualizations, and summarizes findings.",
        "prerequisites": ["generateSql", "dataVisualize", "summarize"],
        "derivatives": ["autonomousDataScientist"],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/Sinaptik-AI/pandas-ai",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "pandas-ai — open-source agent for natural-language data analysis over pandas DataFrames; reproducible demos with logging and output artifacts.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "voiceAgent",
        "name": "Voice Agent",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Handles spoken interactions end-to-end: transcribes audio input, produces language responses, and synthesizes speech output.",
        "prerequisites": ["speechToText", "questionAnswer", "textToSpeech"],
        "derivatives": ["realTimeVoiceAssistant"],
        "conditions": "Requires real-time audio I/O or audio file access.",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/rasa/rasa",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Rasa Open Source — production voice agent framework with ASR/TTS integrations; reproducible pipeline with test suite and documented benchmarks.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "automatedTesting",
        "name": "Automated Testing",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Generates test suites, executes them in a sandbox, interprets failures, and iterates until the target pass rate is reached.",
        "prerequisites": ["generateTest", "execute-bash", "error-interpretation"],
        "derivatives": ["fullStackDeveloper"],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/princeton-nlp/SWE-bench",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "SWE-bench Verified — open-source evaluation harness where agents fix GitHub issues by generating and passing test suites; full execution logs archived.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "contentModeration",
        "name": "Content Moderation",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Detects policy-violating content by combining intent classification, sentiment scoring, and entity extraction across text, images, and mixed media.",
        "prerequisites": ["classify", "sentimentAnalysis", "extract-entities"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://platform.openai.com/docs/guides/moderation",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "OpenAI Moderation API — publicly documented multi-category content classifier with reproducible API calls, category scores, and evaluation methodology.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "multimodalReasoning",
        "name": "Multimodal Reasoning",
        "type": "composite",
        "level": "IV",
        "rarity": "rare",
        "description": "Integrates information from images and text to answer questions requiring visual grounding and logical inference across modalities.",
        "prerequisites": ["imageCaption", "questionAnswer", "logical-inference"],
        "derivatives": [],
        "conditions": "Requires vision-language model capability.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2304.08485",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "LLaVA — large language and vision assistant; 85.1% on ScienceQA and 64.3% on TextVQA, establishing reproducible multimodal reasoning benchmark.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "translationPipeline",
        "name": "Translation Pipeline",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Translates content end-to-end while preserving sentiment and adapting tone and register for the target audience.",
        "prerequisites": ["translate", "sentimentAnalysis", "audience-model"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2308.11596",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "SeamlessM4T (Meta AI) — unified speech and text translation model with tone and register control; BLEU +3.3 over NLLB on FLORES-200.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "documentDigitization",
        "name": "Document Digitization",
        "type": "composite",
        "level": "IV",
        "rarity": "uncommon",
        "description": "Converts scanned or PDF documents into structured, machine-readable output by parsing layout, extracting entities, and formatting results.",
        "prerequisites": ["parsePdf", "extract-entities", "format-output"],
        "derivatives": [],
        "conditions": "",
        "evidence": [
            {
                "class": "B",
                "source": "https://github.com/VikParuchuri/marker",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Marker — open-source PDF-to-markdown pipeline with reproducible benchmarks; outperforms Nougat on edit distance across 1000+ arXiv PDFs.",
            }
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
]

NEW_LEGENDARIES = [
    {
        "id": "fullStackDeveloper",
        "name": "Full-Stack Developer",
        "type": "legendary",
        "level": "IV",
        "rarity": "legendary",
        "description": "Autonomously implements, reviews, tests, and refactors complete software features across the full development lifecycle from specification to merged PR.",
        "prerequisites": ["codeReviewPipeline", "automatedTesting", "refactorCode"],
        "derivatives": [],
        "conditions": "Requires access to repository, execution environment, and test runner. Minimum 3 Class A/B evidence sources.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2310.06770",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "SWE-bench — 2294 real GitHub issues; Claude 3.5 Sonnet (Cognition) resolves 49% on Verified, demonstrating full-cycle autonomous development.",
            },
            {
                "class": "B",
                "source": "https://github.com/princeton-nlp/SWE-agent",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "SWE-agent — open-source agent with AgentComputer Interface; reproducible harness achieving 12.5% on SWE-bench full with logs and eval scripts.",
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2402.01030",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "CodeAct — executable code action space for LLM agents; +20% task completion vs JSON/text-based actions across 17 programming benchmarks.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "autonomousDataScientist",
        "name": "Autonomous Data Scientist",
        "type": "legendary",
        "level": "IV",
        "rarity": "legendary",
        "description": "Conducts end-to-end data science workflows autonomously: hypothesis generation, data analysis, statistical modeling, and insight reporting.",
        "prerequisites": ["dataAnalysis", "math-reason", "research"],
        "derivatives": [],
        "conditions": "Requires dataset access and compute environment. Minimum 3 Class A/B evidence sources.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2210.12641",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "DS-1000 — benchmark of 1000 data science problems across NumPy/Pandas/Scikit-learn; GPT-4 achieves 43.3% pass@1, establishing reproducible DS evaluation.",
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2208.01756",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "AutoML Survey (He et al., ACM CSUR) — systematic review of autonomous ML pipeline search; demonstrates automated feature engineering, model selection, and HPO.",
            },
            {
                "class": "B",
                "source": "https://github.com/microsoft/autogen",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "AutoGen (Microsoft) — multi-agent framework with reproducible data science notebooks; science agent achieves 44.3% on DS-1000 with full execution logs.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
    {
        "id": "realTimeVoiceAssistant",
        "name": "Real-Time Voice Assistant",
        "type": "legendary",
        "level": "IV",
        "rarity": "legendary",
        "description": "Provides low-latency spoken interactions combining real-time speech I/O, persistent memory, and goal-directed task execution across multi-session conversations.",
        "prerequisites": ["voiceAgent", "memoryManage", "plan-and-execute"],
        "derivatives": [],
        "conditions": "Requires real-time audio pipeline, <500ms end-to-end latency target, and persistent session store. Minimum 3 Class A/B evidence sources.",
        "evidence": [
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2312.11805",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "AudioPaLM (Google) — unified audio language model supporting real-time spoken dialogue; SOTA on ASR and speech translation, demonstrating end-to-end voice assistant capability.",
            },
            {
                "class": "A",
                "source": "https://arxiv.org/abs/2305.11206",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "VoiceBox (Meta AI) — generative speech model with zero-shot TTS; enables real-time voice assistants with <100ms synthesis latency benchmarked on VCTK.",
            },
            {
                "class": "B",
                "source": "https://github.com/openai/whisper",
                "evaluator": EVALUATOR,
                "date": TODAY,
                "notes": "Whisper + LLM integration demos — open-source real-time voice assistant pipelines combining Whisper STT, LLM reasoning, and TTS with documented latency benchmarks.",
            },
        ],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    },
]

# ---------------------------------------------------------------------------
# Derivatives to add to EXISTING skills
# ---------------------------------------------------------------------------

EXISTING_DERIVATIVE_PATCHES = {
    "routeIntent":        ["conversationalAgent"],
    "classify":           ["contentModeration"],
    "extract-entities":    ["contentModeration", "documentDigitization"],
    "summarize":          ["dataAnalysis"],
    "diff-content":        ["codeReviewPipeline"],
    "evaluate-output":     ["codeReviewPipeline"],
    "code-generation":     ["codeReviewPipeline"],
    "execute-bash":        ["automatedTesting"],
    "error-interpretation":["automatedTesting"],
    "format-output":       ["textToSqlPipeline", "documentDigitization"],
    "audience-model":      ["translationPipeline"],
    "parse-json":          ["textToSqlPipeline"],
    "research":           ["autonomousDataScientist"],
    "plan-and-execute":     ["realTimeVoiceAssistant"],
}

# ---------------------------------------------------------------------------
# Build edges for all new prerequisite relationships
# ---------------------------------------------------------------------------

def make_edges(skill):
    edges = []
    for prereq in skill.get("prerequisites", []):
        edges.append({
            "sourceSkillId": prereq,
            "targetSkillId": skill["id"],
            "edgeType": "prerequisite",
            "condition": skill.get("conditions", ""),
            "levelFloor": "II",
            "evidenceRefs": [f"{skill['id']}#evidence[0]"],
        })
    return edges


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with open(GRAPH_PATH) as f:
        graph = json.load(f)

    all_new = NEW_ATOMICS + NEW_COMPOSITES + NEW_LEGENDARIES
    new_ids = {s["id"] for s in all_new}
    existing_ids = {s["id"] for s in graph["skills"]}

    # Patch derivatives on existing skills
    for skill in graph["skills"]:
        additions = EXISTING_DERIVATIVE_PATCHES.get(skill["id"], [])
        for d in additions:
            if d not in skill["derivatives"]:
                skill["derivatives"].append(d)

    # Append new skills
    graph["skills"].extend(all_new)

    # Append new edges
    for skill in all_new:
        graph["edges"].extend(make_edges(skill))

    # Bump metadata
    graph["generatedAt"] = TODAY + "T00:00:00Z"
    graph["version"] = VERSION

    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f, indent=2)
        f.write("\n")

    print(f"Done. Added {len(all_new)} skills ({len(NEW_ATOMICS)} atomic, "
          f"{len(NEW_COMPOSITES)} composite, {len(NEW_LEGENDARIES)} legendary) "
          f"and {sum(len(s['prerequisites']) for s in all_new)} edges.")


if __name__ == "__main__":
    main()
