"""Router for risk warning analysis."""

from app.models import ReviewData, RiskWarningResult
from app.services.risk_service import analyze_risk
from fastapi import APIRouter

router = APIRouter()


@router.post("/analyze", response_model=RiskWarningResult)
async def analyze(review: ReviewData) -> RiskWarningResult:
    """Analyze risk level for a customer review."""
    return analyze_risk(review)