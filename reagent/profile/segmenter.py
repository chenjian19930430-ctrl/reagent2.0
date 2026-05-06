"""User segmentation engine — 用户分群与细分。"""

from __future__ import annotations

import json
from typing import Optional

from loguru import logger

from reagent.profile.schema import (
    UserProfile,
    SegmentCriteria,
    IndustryType,
    IndustryTemplate,
)


# Built-in industry templates
INDUSTRY_TEMPLATES: dict[IndustryType, IndustryTemplate] = {
    IndustryType.ECOMMERCE: IndustryTemplate(
        industry=IndustryType.ECOMMERCE,
        name="电商行业模板",
        description="适用于电商平台用户画像分析",
        default_segments=[
            SegmentCriteria(name="高价值VIP", description="年度消费TOP 10%", rules=[{"metric": "total_spent", "op": "top_pct", "value": 10}]),
            SegmentCriteria(name="复购达人", description="近90天复购3次+", rules=[{"metric": "repeat_purchase_90d", "op": "gte", "value": 3}]),
            SegmentCriteria(name="新品探索者", description="近30天浏览新品占比>50%", rules=[{"metric": "new_product_view_ratio", "op": "gte", "value": 0.5}]),
        ],
        key_traits=["客单价", "品类偏好", "购买频率", "退货率", "评价倾向"],
    ),
    IndustryType.EDUCATION: IndustryTemplate(
        industry=IndustryType.EDUCATION,
        name="教育行业模板",
        description="适用于在线教育平台用户画像",
        default_segments=[
            SegmentCriteria(name="学霸型", description="月学习时长>30h", rules=[{"metric": "monthly_study_hours", "op": "gte", "value": 30}]),
            SegmentCriteria(name="试听用户", description="注册<14天，已试听", rules=[{"metric": "reg_days", "op": "lte", "value": 14}]),
        ],
        key_traits=["课程偏好", "学习时段", "完课率", "付费意愿", "互动频率"],
    ),
    IndustryType.SAAS: IndustryTemplate(
        industry=IndustryType.SAAS,
        name="SaaS行业模板",
        description="适用于SaaS产品用户画像",
        default_segments=[
            SegmentCriteria(name="Power用户", description="日活>4h", rules=[{"metric": "daily_active_hours", "op": "gte", "value": 4}]),
            SegmentCriteria(name="决策者", description="角色含owner/admin", rules=[{"metric": "role", "op": "in", "value": ["owner", "admin"]}]),
        ],
        key_traits=["活跃功能", "团队规模", "付费等级", "邀请率", "NPS"],
    ),
    IndustryType.GENERAL: IndustryTemplate(
        industry=IndustryType.GENERAL,
        name="通用行业模板",
        description="适用于通用用户画像分析",
        default_segments=[
            SegmentCriteria(name="高活跃度", description="高频互动用户", rules=[]),
            SegmentCriteria(name="新用户", description="注册<30天", rules=[]),
            SegmentCriteria(name="沉默用户", description="近30天无互动", rules=[]),
        ],
        key_traits=["活跃度", "生命周期价值", "流失风险", "偏好标签"],
    ),
}


class Segmenter:
    """User segmentation engine."""

    def __init__(self):
        self._templates = INDUSTRY_TEMPLATES
        logger.info(f"Segmenter initialized with {len(self._templates)} industry templates")

    def get_template(self, industry: object) -> IndustryTemplate:
        """Get industry-specific template."""
        if isinstance(industry, IndustryType):
            return self._templates.get(industry, self._templates[IndustryType.GENERAL])
        return self._templates[IndustryType.GENERAL]

    def list_templates(self) -> list[dict]:
        """List all available industry templates."""
        return [
            {"industry": t.industry.value, "name": t.name, "segments": len(t.default_segments)}
            for t in self._templates.values()
        ]

    def segment_user(self, profile: UserProfile) -> list[str]:
        """Segment a user based on profile data."""
        matches = []

        for segment in self.get_template(profile.industry).default_segments:
            if self._evaluate_rules(profile, segment.rules):
                matches.append(segment.name)

        # Always include custom segments from profile
        matches.extend(profile.segments)

        return list(set(matches))

    def _evaluate_rules(self, profile: UserProfile, rules: list[dict]) -> bool:
        """Evaluate segmentation rules against a profile."""
        if not rules:
            return True

        for rule in rules:
            metric = rule.get("metric", "")
            op = rule.get("op", "eq")
            value = rule.get("value")

            profile_value = self._get_metric(profile, metric)
            if profile_value is None:
                return False

            if op == "gte" and not (profile_value >= value): return False
            if op == "lte" and not (profile_value <= value): return False
            if op == "eq" and not (profile_value == value): return False
            if op == "gt" and not (profile_value > value): return False
            if op == "lt" and not (profile_value < value): return False
            if op == "in" and profile_value not in value: return False

        return True

    def _get_metric(self, profile: UserProfile, metric: str):
        """Extract a metric value from profile.

        Supports all UserProfile scalar fields plus dynamic trait/tag lookups.
        """
        mapping = {
            # Core numeric metrics
            "total_spent": profile.lifetime_value,
            "lifetime_value": profile.lifetime_value,
            "engagement": profile.engagement_score,
            "engagement_score": profile.engagement_score,
            "churn_risk": profile.churn_risk,
            "churn": profile.churn_risk,
            # Derived / common aliases
            "repeat_purchase_90d": profile.traits.get("repeat_purchase_90d", 0),
            "new_product_view_ratio": profile.traits.get("new_product_view_ratio", 0.0),
            "monthly_study_hours": profile.traits.get("monthly_study_hours", 0),
            "daily_active_hours": profile.traits.get("daily_active_hours", 0),
            "reg_days": profile.traits.get("reg_days", 999),
            "role": profile.traits.get("role", ""),
            # Preferences
            "preferred_category": profile.preferences.get("category", ""),
            "preferred_channel": profile.preferences.get("channel", ""),
            # Tags
            "tags": profile.tags,
        }

        # Fallback: try traits dict if not in standard mapping
        value = mapping.get(metric)
        if value is None:
            value = profile.traits.get(metric)

        return value
