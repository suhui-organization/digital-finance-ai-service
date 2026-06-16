"""Report summarization service powered by MiniMax LLM."""

from app.models import ReviewData, SummaryResult
from app.services.llm_client import chat_completion


SYSTEM_PROMPT = """你是一位专业的金融贷款审查分析师。你的任务是根据提供的客户信息，生成一份简洁的审查摘要。

请用以下格式输出JSON：
{
  "summary": "一段自然语言的综合审查摘要（200字以内），包含客户基本信息、征信评估、负债情况、亮点和综合建议",
  "key_points": ["要点1", "要点2", "要点3", "要点4", "要点5"]
}

要求：
- 语言专业、简洁、客观
- 突出风险点和亮点
- 给出综合评估结论"""


async def generate_summary(review: ReviewData) -> SummaryResult:
    highlights_text = "、".join(review.highlights) if review.highlights else "无"

    user_message = f"""客户信息：
- 姓名：{review.customer_name}
- 性别：{review.gender}
- 年龄：{review.age}岁
- 婚姻状况：{review.marital_status}
- 需求额度：{review.loan_amount:.0f}元
- 征信状态：{review.credit_status}
- 负债总额：{review.total_debt:.0f}元
- 近1月征信查询：{review.credit_query_1m}次
- 近3月征信查询：{review.credit_query_3m}次
- 近6月征信查询：{review.credit_query_6m}次
- 个人亮点：{highlights_text}
- 是否可匹配：{"是" if review.can_match else "否"}

请生成审查摘要。"""

    try:
        import json

        response = await chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        import re

        # Parse JSON from LLM response
        response = response.strip()
        # MiniMax M3 outputs <think>...</think> reasoning blocks — strip them
        response = re.sub(r"<think>.*?</think>\s*", "", response, flags=re.DOTALL)
        # Strip markdown code fences
        if response.startswith("```"):
            response = response.split("\n", 1)[1]
            if response.endswith("```"):
                response = response[:-3]
        data = json.loads(response)
        return SummaryResult(
            summary=data["summary"],
            key_points=data["key_points"],
        )

    except Exception as e:
        import logging
        logging.getLogger("uvicorn").warning("LLM summarization failed: %s, falling back to template", e)
        return _generate_template_summary(review)


def _generate_template_summary(review: ReviewData) -> SummaryResult:
    """Template-based fallback when LLM is unavailable."""
    highlights_text = "、".join(review.highlights) if review.highlights else "无特别亮点"

    if review.credit_status == "正常":
        credit_assessment = "征信记录正常，信用状况良好"
    elif review.credit_status in ("当前逾期", "呆账", "代偿", "法诉"):
        credit_assessment = f"征信存在{review.credit_status}，信用风险较高"
    else:
        credit_assessment = f"征信状态为{review.credit_status}，需进一步关注"

    if review.can_match:
        match_assessment = "可推荐匹配方案"
    else:
        match_assessment = "暂不推荐匹配方案"

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