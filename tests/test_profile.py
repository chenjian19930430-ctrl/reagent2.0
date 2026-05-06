"""Tests for User Profile Analysis Module."""

import pytest
from reagent.profile.schema import (
    UserProfile, ProfileAnalysisRequest, ProfileAnalysisResponse,
    IndustryTemplate, IndustryType, SegmentCriteria,
)
from reagent.profile.analyzer import ProfileAnalyzer
from reagent.profile.segmenter import Segmenter, INDUSTRY_TEMPLATES


class TestProfileSchemas:
    """Test profile schema models."""

    def test_user_profile(self):
        profile = UserProfile(
            user_id="u_123",
            segments=["高价值"],
            lifetime_value=10000,
            churn_risk=0.1,
            engagement_score=0.8,
        )
        assert profile.user_id == "u_123"
        assert profile.lifetime_value == 10000
        assert profile.churn_risk == 0.1

    def test_profile_analysis_request(self):
        req = ProfileAnalysisRequest(
            user_id="u_123",
            raw_data={"total_spent": 5000},
            industry=IndustryType.ECOMMERCE,
        )
        assert req.user_id == "u_123"
        assert req.industry == IndustryType.ECOMMERCE

    def test_industry_template(self):
        t = IndustryTemplate(
            industry=IndustryType.SAAS,
            name="SaaS Template",
            key_traits=["NPS", "活跃度"],
        )
        assert t.name == "SaaS Template"
        assert "NPS" in t.key_traits


class TestProfileAnalyzer:
    """Test profile analysis engine."""

    def test_build_profile(self):
        analyzer = ProfileAnalyzer()
        req = ProfileAnalysisRequest(
            user_id="u_123",
            raw_data={
                "total_purchases": 15,
                "total_spent": 8000,
                "days_since_last_activity": 3,
                "traits": {"age_group": "25-35"},
            },
        )
        profile = analyzer._build_profile(req)
        assert profile.user_id == "u_123"
        assert len(profile.segments) >= 2  # 高频购买 + 高价值 + 活跃用户
        assert "高价值" in profile.segments
        assert profile.engagement_score > 0

    def test_rule_based_segmentation_high_value(self):
        analyzer = ProfileAnalyzer()
        profile = UserProfile(
            user_id="u_123",
            lifetime_value=10000,
            engagement_score=0.5,
            churn_risk=0.2,
        )
        segment = analyzer._rule_based_segmentation(profile)
        assert segment == "高价值客户"

    def test_rule_based_segmentation_churn_risk(self):
        analyzer = ProfileAnalyzer()
        profile = UserProfile(
            user_id="u_456",
            lifetime_value=100,
            engagement_score=0.3,
            churn_risk=0.8,
        )
        segment = analyzer._rule_based_segmentation(profile)
        assert segment == "需要挽回"


class TestSegmenter:
    """Test segmentation engine."""

    def test_get_template(self):
        segmenter = Segmenter()
        template = segmenter.get_template(IndustryType.ECOMMERCE)
        assert template.industry == IndustryType.ECOMMERCE
        assert len(template.default_segments) > 0

    def test_list_templates(self):
        segmenter = Segmenter()
        templates = segmenter.list_templates()
        assert len(templates) >= 4  # At least general + ecommerce + education + saas

    def test_get_fallback_template(self):
        segmenter = Segmenter()
        template = segmenter.get_template("unknown")  # Should fallback to general
        if hasattr(template, "industry"):
            assert template.industry == IndustryType.GENERAL
