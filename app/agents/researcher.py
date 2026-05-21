from app.corpus.local_sources import search_sources
from app.schemas.research import Claim, ResearchTask, SourceNote


def research(task: ResearchTask) -> tuple[list[SourceNote], list[Claim]]:
    notes = search_sources(task.question)
    claims = []
    for note in notes:
        claim_text = f"For {task.intent}, {note.quote}"
        confidence = min(0.92, 0.45 + note.relevance)
        claims.append(Claim(text=claim_text, source_ids=[note.source_id], confidence=round(confidence, 3)))
    return notes, claims
