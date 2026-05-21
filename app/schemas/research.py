from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=5)
    audience: str = "technical leadership"
    depth: int = Field(default=3, ge=1, le=5)


class ResearchTask(BaseModel):
    id: str
    question: str
    intent: str


class SourceNote(BaseModel):
    source_id: str
    title: str
    url: str
    quote: str
    relevance: float


class Claim(BaseModel):
    text: str
    source_ids: list[str]
    confidence: float


class Critique(BaseModel):
    issue: str
    severity: str
    recommendation: str


class ResearchReport(BaseModel):
    id: str
    topic: str
    tasks: list[ResearchTask]
    claims: list[Claim]
    critiques: list[Critique]
    markdown: str
