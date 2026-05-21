from fastapi import APIRouter, HTTPException
from app.schemas.research import ResearchReport, ResearchRequest
from app.services.orchestrator import REPORTS, run_research

router = APIRouter()


@router.post("/research", response_model=ResearchReport, status_code=201)
async def create_research_report(payload: ResearchRequest):
    return await run_research(payload)


@router.get("/reports/{report_id}", response_model=ResearchReport)
def get_report(report_id: str):
    try:
        return REPORTS[report_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Report not found") from exc


@router.get("/reports/{report_id}/markdown", response_model=str)
def get_report_markdown(report_id: str):
    try:
        return REPORTS[report_id].markdown
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Report not found") from exc
