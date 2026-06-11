"""Report summarization service using template-based generation (MVP).

Reserves an LLM integration point for future enhancement.
"""

from app.models import ReviewData, SummaryResult


def generate_summary(review: ReviewData) -> SummaryResult:
    """
    Generate a natural-language summary of the review using a template engine.

    Returns a SummaryResult with the full summary text and key points.
    """
    highlights_text = "、".join(review.highlights) if review.highlights else "无特别亮点"

    # Build credit status assessment
    if review.credit_status == "正常":
        credit_assessment = "征信记录正常，信用状况良好"
    elif review.credit_status in ("当前逾期", "呆账", "代偿", "法诉"):
        credit_assessment = f"征信存在{review.credit_status}，信用风险较高"
    else:
        credit_assessment = f"征信状态为{review.credit_status}，需进一步关注"

    # Build match assessment
    if review.can_match:
        match_assessment = "可推荐匹配方案"
    else:
        match_assessment = "暂不推荐匹配方案"

    # Build overall assessment
    if review.credit_status == "正常" and review.total_debt < review.loan_amount * 0.5:
        overall = "综合资质优良，建议优先推进"
    elif review.credit_status in ("当前逾期", "呆账"):
        overall = "综合资质较差，建议暂缓审批"
    else:
        overall = "综合资质一般，建议审慎评估后决定"

    summary = (
        f"客户{review.customer_name}，{review.gender}，{review.age}岁，"
        f"{review.marital_status}，需求额度{review.loan_amount:.0f}元。"
        f"{credit_assessment}。"
        f"负债总额{review.total_debt:.0f}元，"
        f"近1月征信查询{review.credit_query_1m}次，"
        f"近3月{review.credit_query_3m}次，"
        f"近6月{review.credit_query_6m}次。"
        f"个人亮点：{highlights_text}。"
        f"{match_assessment}。综合评估：{overall}。"
    )

    key_points = [
        f"客户：{review.customer_name}，{review.gender}，{review.age}岁",
        credit_assessment,
        f"需求额度：{review.loan_amount:.0f}元，负债总额：{review.total_debt:.0f}元",
        f"个人亮点：{highlights_text}",
        overall,
    ]

    return SummaryResult(summary=summary, key_points=key_points)