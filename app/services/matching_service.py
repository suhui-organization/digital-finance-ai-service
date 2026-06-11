"""Plan matching service using rule-based engine (MVP)."""

from app.models import MatchingRequest, MatchingResult, PlanRecommendation


def match_plans(request: MatchingRequest) -> MatchingResult:
    """
    Match recommended loan plans based on credit status and loan amount.

    Returns 1-3 recommended plans with rates, amount ranges, and reasons.
    """
    plans: list[PlanRecommendation] = []

    if request.credit_status in ("正常",):
        plans.append(
            PlanRecommendation(
                name="优选信用贷",
                rate="3.5% - 5.5%",
                amount_range=f"{max(10000, request.loan_amount * 0.5):.0f} - {request.loan_amount:.0f}",
                reason="征信记录良好，符合优质客户标准",
            )
        )
        plans.append(
            PlanRecommendation(
                name="公积金专项贷",
                rate="3.2% - 4.8%",
                amount_range=f"{max(50000, request.loan_amount * 0.6):.0f} - {request.loan_amount * 1.2:.0f}",
                reason="征信正常，如有公积金可享更低利率",
            )
        )
    elif request.credit_status in ("关注", "其他", "情况说明"):
        plans.append(
            PlanRecommendation(
                name="抵押担保贷",
                rate="5.5% - 8.0%",
                amount_range=f"{max(30000, request.loan_amount * 0.4):.0f} - {request.loan_amount * 0.8:.0f}",
                reason="征信有关注项，建议提供抵押或担保以降低利率",
            )
        )
    elif request.credit_status in ("当前逾期", "呆账", "代偿", "法诉"):
        plans.append(
            PlanRecommendation(
                name="资产抵押贷",
                rate="8.0% - 15.0%",
                amount_range=f"{max(10000, request.loan_amount * 0.3):.0f} - {request.loan_amount * 0.5:.0f}",
                reason="征信存在不良记录，仅可申请抵押类高息产品",
            )
        )

    # Add highlight-based plan
    if "不动产" in request.highlights:
        plans.append(
            PlanRecommendation(
                name="房产抵押贷",
                rate="3.8% - 5.0%",
                amount_range=f"{request.loan_amount * 0.5:.0f} - {request.loan_amount * 2:.0f}",
                reason="持有不动产，可申请大额房产抵押贷款",
            )
        )

    if "公积金" in request.highlights:
        plans.append(
            PlanRecommendation(
                name="公积金信用贷",
                rate="3.0% - 4.5%",
                amount_range=f"{request.loan_amount * 0.5:.0f} - {request.loan_amount:.0f}",
                reason="有公积金缴存记录，可享受优惠利率",
            )
        )

    return MatchingResult(recommended_plans=plans[:3])