"""Pydantic data models for the AI service."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DebtDetail(BaseModel):
    """A single debt record."""

    institution: str = Field(..., description="贷款机构名称")
    total_amount: float = Field(..., description="贷款总额")
    balance: float = Field(..., description="当前余额")
    loan_method: str = Field(..., description="贷款方式")
    loan_due: str = Field(..., description="贷款期至")
    repayment_method: str = Field(..., description="还款方式")


class ReviewData(BaseModel):
    """Complete review data for AI analysis."""

    customer_name: str = Field(..., description="客户姓名")
    gender: str = Field(..., description="客户性别")
    age: int = Field(..., ge=18, le=120, description="客户年龄")
    marital_status: str = Field(..., description="婚姻状况")
    loan_amount: float = Field(..., ge=0, description="需求额度")
    is_enterprise: bool = Field(default=False, description="是否为企业客户")
    main_bank: str = Field(..., description="主要银行")
    total_debt: float = Field(default=0, ge=0, description="负债总额")
    credit_status: str = Field(..., description="征信状态")
    credit_query_1m: int = Field(default=0, ge=0, description="近1月查询次数")
    credit_query_3m: int = Field(default=0, ge=0, description="近3月查询次数")
    credit_query_6m: int = Field(default=0, ge=0, description="近6月查询次数")
    spouse_info: str = Field(..., description="配偶情况说明")
    spouse_cooperate: bool = Field(default=False, description="配偶是否配合")
    highlights: List[str] = Field(default_factory=list, description="个人亮点")
    can_match: bool = Field(default=False, description="是否可匹配方案")
    debt_details: List[DebtDetail] = Field(default_factory=list, description="负债明细")


class ScoringResult(BaseModel):
    """Qualification scoring result."""

    score: int = Field(..., ge=0, le=100, description="评分 0-100")
    level: str = Field(..., description="等级 A/B/C/D")
    factors: List[str] = Field(..., description="评分因素列表")


class PlanRecommendation(BaseModel):
    """A single recommended loan plan."""

    name: str = Field(..., description="方案名称")
    rate: str = Field(..., description="利率范围")
    amount_range: str = Field(..., description="额度范围")
    reason: str = Field(..., description="推荐理由")


class MatchingRequest(BaseModel):
    """Plan matching request."""

    loan_amount: float = Field(..., ge=0, description="需求额度")
    credit_status: str = Field(..., description="征信状态")
    highlights: List[str] = Field(default_factory=list, description="个人亮点")


class MatchingResult(BaseModel):
    """Plan matching result."""

    recommended_plans: List[PlanRecommendation] = Field(default_factory=list, description="推荐方案列表")


class RiskWarningResult(BaseModel):
    """Risk warning analysis result."""

    risk_level: str = Field(..., description="风险等级：低/中/高/极高")
    warnings: List[str] = Field(..., description="预警项列表")
    score: int = Field(..., ge=0, le=100, description="风险评分")


class SummaryResult(BaseModel):
    """Report summarization result."""

    summary: str = Field(..., description="自然语言摘要")
    key_points: List[str] = Field(..., description="关键点列表")