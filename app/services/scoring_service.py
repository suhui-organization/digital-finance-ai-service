"""Qualification scoring service using rule-based engine (MVP).

Scoring dimensions:
  - Credit status: 40 points
  - Debt ratio: 30 points
  - Personal highlights: 20 points
  - Age / marital: 10 points
"""

from app.models import ReviewData, ScoringResult


def score_review(review: ReviewData) -> ScoringResult:
    """
    Score a customer review on a 0-100 scale using rule-engine logic.

    Returns a ScoringResult with score, level (A/B/C/D), and contributing factors.
    """
    factors: list[str] = []

    # --- Credit status (40 pts) ---
    credit_score = 0.0
    credit_map = {
        "正常": 40,
        "关注": 25,
        "其他": 15,
        "当前逾期": 5,
        "呆账": 0,
        "代偿": 0,
        "法诉": 0,
        "情况说明": 10,
    }
    credit_score = float(credit_map.get(review.credit_status, 20))
    factors.append(f"征信状态 '{review.credit_status}' → {credit_score:.0f}/40")

    # --- Debt ratio (30 pts) ---
    debt_ratio = review.total_debt / review.loan_amount if review.loan_amount > 0 else 0
    if debt_ratio <= 0.3:
        debt_score = 30.0
    elif debt_ratio <= 0.6:
        debt_score = 20.0
    elif debt_ratio <= 1.0:
        debt_score = 10.0
    else:
        debt_score = 0.0
    factors.append(f"负债率 {debt_ratio:.1%} → {debt_score:.0f}/30")

    # --- Highlights (20 pts) ---
    highlight_count = len(review.highlights)
    highlight_score = min(highlight_count * 3.5, 20.0)
    factors.append(f"亮点数量 {highlight_count} → {highlight_score:.0f}/20")

    # --- Age & marital (10 pts) ---
    age_marital_score = 5.0  # base
    if 25 <= review.age <= 50:
        age_marital_score += 2.5
    if review.marital_status == "已婚":
        age_marital_score += 2.5
    factors.append(f"年龄 {review.age} + 婚姻 '{review.marital_status}' → {age_marital_score:.0f}/10")

    total = credit_score + debt_score + highlight_score + age_marital_score
    total = max(0, min(100, round(total)))

    if total >= 75:
        level = "A"
    elif total >= 55:
        level = "B"
    elif total >= 35:
        level = "C"
    else:
        level = "D"

    return ScoringResult(score=total, level=level, factors=factors)