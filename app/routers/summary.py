"""Router for report summarization."""

from app.models import ReviewData, SummaryResult
from app.services.summary_service import generate_summary
from fastapi import APIRouter

router = APIRouter()


@router.post("/summarize", response_model=SummaryResult)
async def summarize(review: ReviewData) -> SummaryResult:
    """Generate a natural-language summary of a review."""
    return generate_summary(review)