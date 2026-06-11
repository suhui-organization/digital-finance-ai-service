"""Router for qualification scoring."""

from app.models import ReviewData, ScoringResult
from app.services.scoring_service import score_review
from fastapi import APIRouter

router = APIRouter()


@router.post("/score", response_model=ScoringResult)
async def score(review: ReviewData) -> ScoringResult:
    """Score a customer review and return the result."""
    return score_review(review)