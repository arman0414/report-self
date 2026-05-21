from app.schemas.research import SourceNote

SOURCES = [
    {
        "id": "sre-book",
        "title": "Site Reliability Engineering Practices",
        "url": "https://sre.google/sre-book/table-of-contents/",
        "text": "Reliable systems depend on explicit service level objectives, error budgets, automation, and blameless postmortems after incidents.",
    },
    {
        "id": "nist-ai-risk",
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "text": "AI systems should be governed, mapped, measured, and managed with attention to validity, reliability, safety, security, and accountability.",
    },
    {
        "id": "owasp-llm",
        "title": "OWASP Top 10 for LLM Applications",
        "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "text": "LLM applications face risks including prompt injection, sensitive information disclosure, insecure output handling, excessive agency, and model denial of service.",
    },
    {
        "id": "kafka-design",
        "title": "Event Streaming Architecture Notes",
        "url": "https://kafka.apache.org/documentation/",
        "text": "Event-driven systems decouple producers and consumers, support replay, and help teams process high-volume operational data streams.",
    },
    {
        "id": "rag-evaluation",
        "title": "Retrieval Augmented Generation Evaluation",
        "url": "https://arxiv.org/abs/2310.01427",
        "text": "RAG systems require retrieval quality checks, grounded answer evaluation, citation support, and robustness testing for production use.",
    },
]

DOMAIN_TERMS = {
    "ai", "rag", "llm", "agent", "agents", "incident", "response", "reliability", "sre",
    "security", "retrieval", "generation", "enterprise", "platform", "event", "streaming",
    "kafka", "automation", "postmortem", "observability", "governance",
}

BOILERPLATE_TERMS = {
    "what", "strategic", "context", "architecture", "operating", "model", "models", "makes",
    "production", "ready", "risks", "risk", "controls", "evaluation", "methods", "matter",
    "implementation", "roadmap", "leadership", "consider", "metrics", "prove", "working",
}


def _terms(query: str) -> set[str]:
    terms: set[str] = set()
    for token in query.split():
        cleaned = token.lower().strip(',.?:;()')
        if not cleaned:
            continue
        if cleaned in DOMAIN_TERMS:
            terms.add(cleaned)
            continue
        if len(cleaned) > 3 and cleaned not in BOILERPLATE_TERMS:
            terms.add(cleaned)
    return terms


def search_sources(query: str, limit: int = 3) -> list[SourceNote]:
    terms = _terms(query)
    if not (terms & DOMAIN_TERMS):
        return []
    scored = []
    for source in SOURCES:
        haystack = f"{source['title']} {source['text']}".lower()
        overlap = sum(1 for term in terms if term in haystack)
        if overlap:
            scored.append((overlap / max(len(terms), 1), source))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        SourceNote(source_id=source['id'], title=source['title'], url=source['url'], quote=source['text'], relevance=round(score, 3))
        for score, source in scored[:limit]
    ]
