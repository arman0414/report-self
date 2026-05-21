from uuid import uuid4
from app.agents.critic import critique
from app.agents.planner import plan
from app.agents.researcher import research
from app.agents.writer import write_report
from app.schemas.research import Claim, ResearchReport, ResearchRequest, SourceNote

REPORTS: dict[str, ResearchReport] = {}


async def run_research(request: ResearchRequest) -> ResearchReport:
    tasks = plan(request)
    notes: list[SourceNote] = []
    claims: list[Claim] = []
    for task in tasks:
        task_notes, task_claims = research(task)
        notes.extend(task_notes)
        claims.extend(task_claims)
    critiques = critique(claims)
    markdown = write_report(request, tasks, claims, critiques, notes)
    report = ResearchReport(id=str(uuid4()), topic=request.topic, tasks=tasks, claims=claims, critiques=critiques, markdown=markdown)
    REPORTS[report.id] = report
    return report
