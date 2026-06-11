"""Router for plan matching."""

from app.models import MatchingRequest, MatchingResult
from app.services.matching_service import match_plans
from fastapi import APIRouter

router = APIRouter()


@router.post("/match", response_model=MatchingResult)
async def match(request: MatchingRequest) -> MatchingResult:
    """Match recommended loan plans for a customer."""
    return match_plans(request)