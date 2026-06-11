"""Risk warning analysis service using rule-based engine (MVP)."""

from app.models import ReviewData, RiskWarningResult


def analyze_risk(review: ReviewData) -> RiskWarningResult:
    """
    Analyze risk level based on credit status, debt ratio, and credit query frequency.

    Returns a RiskWarningResult with risk level, warning list, and risk score.
    """
    warnings: list[str] = []
    risk_score = 0.0

    # Credit status risk
    high_risk_statuses = ("当前逾期", "呆账", "代偿", "法诉")
    medium_risk_statuses = ("关注", "其他", "情况说明")

    if review.credit_status in high_risk_statuses:
        warnings.append(f"征信存在严重问题：{review.credit_status}")
        risk_score += 50
    elif review.credit_status in medium_risk_statuses:
        warnings.append(f"征信有关注项：{review.credit_status}")
        risk_score += 25

    # Debt ratio risk
    debt_ratio = review.total_debt / review.loan_amount if review.loan_amount > 0 else 0
    if debt_ratio > 1.0:
        warnings.append(f"负债率过高（{debt_ratio:.1%}），超出需求额度")
        risk_score += 30
    elif debt_ratio > 0.6:
        warnings.append(f"负债率偏高（{debt_ratio:.1%}）")
        risk_score += 15

    # Credit query frequency risk
    if review.credit_query_1m > 3:
        warnings.append(f"近1月征信查询次数过多（{review.credit_query_1m}次）")
        risk_score += 10
    if review.credit_query_3m > 6:
        warnings.append(f"近3月征信查询次数过多（{review.credit_query_3m}次）")
        risk_score += 8
    if review.credit_query_6m > 10:
        warnings.append(f"近6月征信查询次数过多（{review.credit_query_6m}次）")
        risk_score += 5

    risk_score = min(100, risk_score)

    if risk_score >= 60:
        risk_level = "极高"
    elif risk_score >= 35:
        risk_level = "高"
    elif risk_score >= 15:
        risk_level = "中"
    else:
        risk_level = "低"

    if not warnings:
        warnings.append("未发现明显风险项，客户资质良好")

    return RiskWarningResult(risk_level=risk_level, warnings=warnings, score=int(risk_score))