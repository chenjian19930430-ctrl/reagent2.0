"""Profile analyzer — 用户画像分析引擎。"""

from __future__ import annotations

import json
from loguru import logger

from reagent.ai.registry import registry
from reagent.ai.schema import ModelRequest
from reagent.profile.schema import (
    UserProfile,
    ProfileAnalysisRequest,
    ProfileAnalysisResponse,
    IndustryType,
)

# Segmentation rules by industry
INDUSTRY_SEGMENT_RULES: dict[IndustryType, list[tuple[str, str]]] = {
    IndustryType.ECOMMERCE: [
        ("高价值客户", "年消费 > 5000, 复购率 > 60%"),
        ("活跃用户", "近30天有3次以上访问"),
        ("流失风险", "近90天未购买"),
        ("新用户", "注册 < 30天, 1次以内购买"),
    ],
    IndustryType.EDUCATION: [
        ("高活跃学习者", "月学习时长 > 20h"),
        ("付费用户", "有付费课程记录"),
        ("潜在转化", "免费内容浏览中"),
        ("休眠用户", "近60天未登录"),
    ],
    IndustryType.FINANCE: [
        ("高净值客户", "资产 > 50w"),
        ("理财活跃", "月交易 > 5次"),
        ("信用卡潜在", "有储蓄但无信用卡"),
        ("保险潜在", "近30天浏览保险产品"),
    ],
    IndustryType.GENERAL: [
        ("高活跃", "高频互动用户"),
        ("潜在流失", "互动下降趋势"),
        ("价值用户", "高生命周期价值"),
        ("新用户", "注册 < 30天"),
    ],
}


class ProfileAnalyzer:
    """User profile analysis engine.

    Handles:
    - Multi-dimensional profile analysis
    - Automatic segmentation
    - AI-powered insights
    - Churn risk prediction
    """

    ANALYSIS_SYSTEM_PROMPT = """你是 ReAgent 用户画像分析师。请基于用户数据生成洞察。

分析维度：
1. 用户行为模式
2. 价值评估
3. 流失风险评估
4. 个性化推荐依据

请输出 JSON 格式（包含 segments、traits、preferences、lifetime_value、churn_risk 字段）。"""

    async def analyze(self, request: ProfileAnalysisRequest) -> ProfileAnalysisResponse:
        """Analyze user profile data."""
        logger.info(f"Analyzing profile: user={request.user_id}, industry={request.industry}")

        # Build user profile from raw data
        profile = self._build_profile(request)

        # AI-powered insights (if requested)
        ai_insights = None
        recommended_segment = None
        next_best_action = None

        if request.include_ai_insights:
            try:
                insights = await self._generate_insights(request, profile)
                ai_insights = insights.get("summary", "")
                recommended_segment = insights.get("recommended_segment")
                next_best_action = insights.get("next_best_action")
            except Exception as e:
                logger.warning(f"AI insight generation failed: {e}")

        # If AI failed or not requested, use rule-based segmentation
        if not recommended_segment:
            recommended_segment = self._rule_based_segmentation(profile)

        return ProfileAnalysisResponse(
            user_id=request.user_id,
            profile=profile,
            ai_insights=ai_insights,
            recommended_segment=recommended_segment,
            next_best_action=next_best_action,
        )

    def _build_profile(self, request: ProfileAnalysisRequest) -> UserProfile:
        """Build a UserProfile from raw data."""
        raw = request.raw_data

        segments = []
        # Simple rule-based segmentation
        if raw.get("total_purchases", 0) > 10:
            segments.append("高频购买")
        if raw.get("total_spent", 0) > 5000:
            segments.append("高价值")
        if raw.get("days_since_last_activity", 999) < 7:
            segments.append("活跃用户")

        return UserProfile(
            user_id=request.user_id,
            segments=segments,
            traits=raw.get("traits", {}),
            preferences=raw.get("preferences", {}),
            lifetime_value=raw.get("total_spent", 0),
            churn_risk=min(1.0, raw.get("days_since_last_activity", 0) / 180),
            engagement_score=min(1.0, raw.get("total_purchases", 0) / 50),
            recent_interactions=raw.get("recent_interactions", []),
            industry=request.industry,
            tags=raw.get("tags", []),
        )

    async def _generate_insights(self, request: ProfileAnalysisRequest, profile: UserProfile) -> dict:
        """Generate AI-powered insights."""
        user_data = json.dumps({
            "user_id": request.user_id,
            "industry": request.industry.value,
            "raw_data": request.raw_data,
            "profile_segments": profile.segments,
        }, ensure_ascii=False)

        ai_request = ModelRequest(
            model="",
            messages=[],
            system_prompt=self.ANALYSIS_SYSTEM_PROMPT,
            temperature=0.3,
        )
        # We need to include user data in a different way
        # Create a modified request with user message
        import copy
        from reagent.ai.schema import Message, MessageRole
        enhanced_request = copy.deepcopy(ai_request)
        enhanced_request.messages.append(
            Message(role=MessageRole.USER, content=f"请分析以下用户数据：\n{user_data}")
        )

        result = await registry.generate(enhanced_request)

        try:
            text = result.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except (json.JSONDecodeError, IndexError):
            return {"summary": result[:500]}

    def _rule_based_segmentation(self, profile: UserProfile) -> str:
        """Simple rule-based segmentation."""
        if profile.lifetime_value > 5000:
            return "高价值客户"
        if profile.engagement_score > 0.7:
            return "活跃客户"
        if profile.churn_risk > 0.5:
            return "需要挽回"
        return "普通客户"
