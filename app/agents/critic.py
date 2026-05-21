from collections import Counter
from app.schemas.research import Claim, Critique


def critique(claims: list[Claim]) -> list[Critique]:
    critiques: list[Critique] = []
    if not claims:
        return [Critique(issue="No relevant sources found", severity="high", recommendation="Narrow the topic to AI, reliability, security, RAG, or event-driven systems, or connect an external source provider.")]
    source_counts = Counter(source_id for claim in claims for source_id in claim.source_ids)
    if len(source_counts) < 2:
        critiques.append(Critique(issue="Source diversity is low", severity="medium", recommendation="Add at least two independent source families."))
    weak = [claim for claim in claims if claim.confidence < 0.65]
    if weak:
        critiques.append(Critique(issue="Some claims have weak retrieval support", severity="medium", recommendation="Re-run retrieval with narrower questions."))
    repeated = [source for source, count in source_counts.items() if count >= 3]
    if repeated:
        critiques.append(Critique(issue="Report leans heavily on a small source set", severity="low", recommendation="Balance citations before external publication."))
    if not critiques:
        critiques.append(Critique(issue="No blocking quality issues found", severity="info", recommendation="Proceed to editorial review."))
    return critiques
