from app.schemas.research import Claim, Critique, ResearchRequest, ResearchTask, SourceNote


def write_report(request: ResearchRequest, tasks: list[ResearchTask], claims: list[Claim], critiques: list[Critique], notes: list[SourceNote]) -> str:
    source_lookup = {note.source_id: note for note in notes}
    lines = [f"# Research Brief: {request.topic}", "", f"Audience: {request.audience}", "", "## Executive Summary"]
    top_claims = sorted(claims, key=lambda claim: claim.confidence, reverse=True)[:4]
    if top_claims:
        for claim in top_claims:
            citation = claim.source_ids[0]
            lines.append(f"- {claim.text} [{citation}] Confidence: {claim.confidence:.2f}")
    else:
        lines.append("- No source-grounded claims were generated for this topic.")
    lines.extend(["", "## Research Questions"])
    for task in tasks:
        lines.append(f"- {task.question}")
    lines.extend(["", "## Quality Review"])
    for item in critiques:
        lines.append(f"- {item.severity.upper()}: {item.issue}. {item.recommendation}")
    lines.extend(["", "## Sources"])
    if source_lookup:
        for source_id, note in source_lookup.items():
            lines.append(f"- [{source_id}] {note.title}: {note.url}")
    else:
        lines.append("- No sources matched the requested topic.")
    return "\n".join(lines)
