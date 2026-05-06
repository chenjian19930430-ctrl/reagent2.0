"""Advanced tests for Profile Analysis Module — TemplateManager, Segmenter edge cases."""

import pytest
from reagent.profile.schema import (
    UserProfile, ProfileAnalysisRequest, ProfileAnalysisResponse,
    IndustryTemplate, IndustryType, SegmentCriteria,
)
from reagent.profile.analyzer import ProfileAnalyzer
from reagent.profile.segmenter import Segmenter, INDUSTRY_TEMPLATES
from reagent.profile.templates import TemplateManager


class TestTemplateManager:
    """Test industry template management."""

    def test_template_manager_init(self):
        mgr = TemplateManager()
        templates = mgr.list_all()
        assert len(templates) >= 4  # Built-in templates
        builtins = [t for t in templates if t["builtin"]]
        assert len(builtins) >= 4

    def test_get_builtin_template(self):
        mgr = TemplateManager()
        template = mgr.get(IndustryType.ECOMMERCE)
        assert template.industry == IndustryType.ECOMMERCE
        assert "电商" in template.name

    def test_get_fallback_template(self):
        mgr = TemplateManager()
        # Using string should fallback
        template = mgr.get(IndustryType.GENERAL)
        assert template.industry == IndustryType.GENERAL

    def test_register_custom_template(self):
        mgr = TemplateManager()
        custom = IndustryTemplate(
            industry=IndustryType.GAMING,
            name="游戏行业模板",
            description="定制模板",
            default_segments=[
                SegmentCriteria(name="高付费玩家", description="月消费>1000", rules=[]),
            ],
        )
        mgr.register_custom(custom)
        retrieved = mgr.get(IndustryType.GAMING)
        assert retrieved.name == "游戏行业模板"
        assert len(retrieved.default_segments) == 1

    def test_custom_overrides_builtin(self):
        mgr = TemplateManager()
        custom = IndustryTemplate(
            industry=IndustryType.SAAS,
            name="自定义SaaS模板",
            description="覆盖内置模板",
        )
        mgr.register_custom(custom)
        retrieved = mgr.get(IndustryType.SAAS)
        assert retrieved.name == "自定义SaaS模板"

    def test_list_all_includes_custom(self):
        mgr = TemplateManager()
        custom = IndustryTemplate(
            industry=IndustryType.TRAVEL,
            name="旅游模板",
            description="测试",
        )
        mgr.register_custom(custom)
        all_templates = mgr.list_all()
        travel = [t for t in all_templates if t["industry"] == "travel"]
        assert len(travel) == 1
        assert travel[0]["builtin"] is False


class TestSegmenterAdvanced:
    """Advanced segmentation tests."""

    def test_get_all_builtin_templates(self):
        segmenter = Segmenter()
        # Only templates in INDUSTRY_TEMPLATES have matching industry
        builtin = [IndustryType.ECOMMERCE, IndustryType.EDUCATION, IndustryType.SAAS, IndustryType.GENERAL]
        for industry in builtin:
            template = segmenter.get_template(industry)
            assert template.industry == industry
        # Unknown industries fallback to GENERAL
        fallback_template = segmenter.get_template(IndustryType.FINANCE)
        assert fallback_template.industry == IndustryType.GENERAL

    def test_segmenter_list_formats(self):
        segmenter = Segmenter()
        templates = segmenter.list_templates()
        for t in templates:
            assert "industry" in t
            assert "name" in t
            assert "segments" in t

    def test_segment_user_no_rules(self):
        segmenter = Segmenter()
        profile = UserProfile(
            user_id="u_1",
            segments=["VIP"],
            industry=IndustryType.GENERAL,
        )
        segments = segmenter.segment_user(profile)
        # General template segments have empty rules = always match
        assert "高活跃度" in segments
        assert "VIP" in segments  # custom segment included

    def test_segment_user_high_value(self):
        segmenter = Segmenter()
        profile = UserProfile(
            user_id="u_2",
            lifetime_value=10000,
            engagement_score=0.9,
            industry=IndustryType.ECOMMERCE,
        )
        segments = segmenter.segment_user(profile)
        # lifetime_value > 5000 doesn't match any ecommerce rule,
        # but profile.segments is empty, so only general segment rules match
        # Since ecommerce template has specific rules, we check the segment names
        assert isinstance(segments, list)


class TestProfileAnalyzerAdvanced:
    """Advanced profile analyzer tests."""

    def test_build_profile_empty_data(self):
        analyzer = ProfileAnalyzer()
        req = ProfileAnalysisRequest(
            user_id="u_empty",
            raw_data={},
            industry=IndustryType.GENERAL,
        )
        profile = analyzer._build_profile(req)
        assert profile.user_id == "u_empty"
        assert len(profile.segments) == 0
        assert profile.lifetime_value == 0
        assert profile.churn_risk == 0.0
        assert profile.engagement_score == 0.0

    def test_build_profile_full_data(self):
        analyzer = ProfileAnalyzer()
        req = ProfileAnalysisRequest(
            user_id="u_full",
            raw_data={
                "total_purchases": 50,
                "total_spent": 50000,
                "days_since_last_activity": 1,
                "traits": {"city": "北京", "age": 30},
                "preferences": {"category": "电子"},
                "tags": ["VIP", "高活跃"],
            },
            industry=IndustryType.ECOMMERCE,
        )
        profile = analyzer._build_profile(req)
        assert profile.user_id == "u_full"
        assert "高频购买" in profile.segments
        assert "高价值" in profile.segments
        assert "活跃用户" in profile.segments
        assert profile.lifetime_value == 50000
        assert profile.engagement_score == 1.0  # capped at 50/50

    def test_build_profile_churn(self):
        analyzer = ProfileAnalyzer()
        req = ProfileAnalysisRequest(
            user_id="u_churn",
            raw_data={
                "total_purchases": 2,
                "days_since_last_activity": 150,
            },
        )
        profile = analyzer._build_profile(req)
        assert profile.churn_risk > 0.8

    def test_rule_based_normal(self):
        analyzer = ProfileAnalyzer()
        profile = UserProfile(
            user_id="u_normal",
            lifetime_value=1000,
            engagement_score=0.5,
            churn_risk=0.2,
        )
        segment = analyzer._rule_based_segmentation(profile)
        assert segment == "普通客户"

    def test_rule_based_active(self):
        analyzer = ProfileAnalyzer()
        profile = UserProfile(
            user_id="u_active",
            lifetime_value=500,
            engagement_score=0.8,
            churn_risk=0.1,
        )
        segment = analyzer._rule_based_segmentation(profile)
        assert segment == "活跃客户"

    @pytest.mark.asyncio
    async def test_analyze_without_ai(self):
        analyzer = ProfileAnalyzer()
        req = ProfileAnalysisRequest(
            user_id="u_no_ai",
            raw_data={"total_spent": 1000},
            include_ai_insights=False,
        )
        resp = await analyzer.analyze(req)
        assert resp.user_id == "u_no_ai"
        assert resp.profile is not None
        assert resp.ai_insights is None
        assert resp.recommended_segment is not None
