"""Maps external marketplace entries to Gaia skill IDs using keyword matching."""

GITHUB_TOPIC_TO_SKILL = {
    "web-scraping": "web-scrape",
    "web-crawler": "web-scrape",
    "web-scraper": "web-scrape",
    "llm-agent": "generate-text",
    "llm": "generate-text",
    "language-model": "generate-text",
    "text-generation": "generate-text",
    "rag": "rag-pipeline",
    "retrieval-augmented-generation": "rag-pipeline",
    "text-embedding": "embed-text",
    "embeddings": "embed-text",
    "vector-embedding": "embed-text",
    "sentence-embeddings": "embed-text",
    "code-generation": "code-generation",
    "code-gen": "code-generation",
    "codegen": "code-generation",
    "browser-automation": "web-scrape",
    "puppeteer": "web-scrape",
    "playwright": "web-scrape",
    "workflow-orchestration": "plan-decompose",
    "task-orchestration": "plan-decompose",
    "prompt-engineering": "generate-text",
    "vector-database": "retrieve",
    "vector-search": "retrieve",
    "similarity-search": "retrieve",
    "document-parsing": "chunk-document",
    "pdf-parser": "chunk-document",
    "document-loader": "chunk-document",
    "ocr": "ocr",
    "optical-character-recognition": "ocr",
    "speech-recognition": "speech-to-text",
    "speech-to-text": "speech-to-text",
    "asr": "speech-to-text",
    "image-generation": "image-caption",
    "text-to-image": "image-caption",
    "multi-agent": "multi-agent-debate",
    "multi-agent-system": "multi-agent-debate",
    "tool-use": "tool-select",
    "function-calling": "tool-select",
    "tool-calling": "tool-select",
    "named-entity-recognition": "extract-entities",
    "ner": "extract-entities",
    "text-classification": "classify",
    "sentiment-analysis": "classify",
    "text-summarization": "summarize",
    "summarization": "summarize",
    "object-detection": "object-detection",
    "image-classification": "object-detection",
    "reward-model": "reward-modeling",
    "rlhf": "reward-modeling",
    "grounding": "grounding",
    "code-explanation": "code-explain",
}


def map_github_topics(topics: list[str]) -> list[str]:
    """Map GitHub repo topics directly to Gaia skill IDs."""
    detected = set()
    for topic in topics:
        normalized = topic.lower().strip()
        if normalized in GITHUB_TOPIC_TO_SKILL:
            detected.add(GITHUB_TOPIC_TO_SKILL[normalized])
    return list(detected)


KEYWORD_TO_SKILL = {
    "web scraping": "web-scrape",
    "scraper": "web-scrape",
    "scraping": "web-scrape",
    "crawl": "web-scrape",
    "crawler": "web-scrape",
    "rag": "rag-pipeline",
    "retrieval augmented": "rag-pipeline",
    "retrieval-augmented": "rag-pipeline",
    "code generation": "code-generation",
    "code gen": "code-generation",
    "codegen": "code-generation",
    "summarization": "summarize",
    "summarize": "summarize",
    "summarizer": "summarize",
    "entity extraction": "extract-entities",
    "ner": "extract-entities",
    "named entity": "extract-entities",
    "web search": "web-search",
    "search engine": "web-search",
    "search api": "web-search",
    "embedding": "embed-text",
    "embeddings": "embed-text",
    "vector": "embed-text",
    "tokenizer": "tokenize",
    "tokenization": "tokenize",
    "classifier": "classify",
    "classification": "classify",
    "categorization": "classify",
    "html parser": "parse-html",
    "html parsing": "parse-html",
    "dom": "parse-html",
    "json parser": "parse-json",
    "json parsing": "parse-json",
    "shell": "execute-bash",
    "terminal": "execute-bash",
    "command execution": "execute-bash",
    "subprocess": "execute-bash",
    "text generation": "generate-text",
    "language model": "generate-text",
    "llm": "generate-text",
    "chunking": "chunk-document",
    "text splitter": "chunk-document",
    "document loader": "chunk-document",
    "reranking": "rank",
    "rerank": "rank",
    "ranking": "rank",
    "retrieval": "retrieve",
    "vector search": "retrieve",
    "similarity search": "retrieve",
    "citation": "cite-sources",
    "reference": "cite-sources",
    "formatting": "format-output",
    "template": "format-output",
    "diff": "diff-content",
    "evaluation": "evaluate-output",
    "scoring": "score-relevance",
    "relevance": "score-relevance",
    "planning": "plan-decompose",
    "task decomposition": "plan-decompose",
    "routing": "route-intent",
    "intent": "route-intent",
    "report": "write-report",
    "report generation": "write-report",
    "tool use": "tool-select",
    "tool calling": "tool-select",
    "function calling": "tool-select",
    "error handling": "error-interpretation",
    "debugging": "error-interpretation",
}

CATEGORY_TO_SKILLS = {
    "Machine Learning": ["classify", "embed-text", "generate-text"],
    "Data Science": ["extract-entities", "summarize", "chunk-document"],
    "Web Development": ["parse-html", "web-search", "web-scrape"],
    "DevOps": ["execute-bash", "code-generation"],
    "NLP": ["tokenize", "classify", "summarize", "extract-entities"],
    "Search": ["web-search", "retrieve", "score-relevance"],
}


def map_to_skills(name: str, description: str, keywords: list[str] = None, category: str = None) -> list[str]:
    """Map an external entry to Gaia skill IDs based on text signals."""
    detected = set()
    text = f"{name} {description} {' '.join(keywords or [])}".lower()

    for keyword, skill_id in KEYWORD_TO_SKILL.items():
        if keyword in text:
            detected.add(skill_id)

    if category and category in CATEGORY_TO_SKILLS:
        for skill_id in CATEGORY_TO_SKILLS[category]:
            if any(kw in text for kw in [skill_id.replace("-", " "), skill_id.replace("-", "")]):
                detected.add(skill_id)

    return list(detected)
