from uuid import uuid4
from app.schemas.research import ResearchRequest, ResearchTask


def plan(request: ResearchRequest) -> list[ResearchTask]:
    base_questions = [
        f"What is the strategic context for {request.topic}?",
        f"What architecture or operating model makes {request.topic} production-ready?",
        f"What risks, controls, and evaluation methods matter for {request.topic}?",
        f"What implementation roadmap should leadership consider for {request.topic}?",
        f"What metrics prove {request.topic} is working?",
    ]
    return [
        ResearchTask(id=str(uuid4()), question=question, intent=intent)
        for question, intent in zip(base_questions[: request.depth], ["context", "architecture", "risk", "roadmap", "metrics"])
    ]
