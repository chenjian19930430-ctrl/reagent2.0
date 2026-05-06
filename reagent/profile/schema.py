"""Profile analysis schemas."""

from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class IndustryType(str, Enum):
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    REAL_ESTATE = "real_estate"
    TRAVEL = "travel"
    GAMING = "gaming"
    SAAS = "saas"
    GENERAL = "general"


class UserProfile(BaseModel):
    """Complete user profile with analysis."""
    user_id: str
    segments: list[str] = []
    traits: dict[str, object] = Field(default_factory=dict)
    preferences: dict[str, str] = Field(default_factory=dict)
    lifetime_value: float = 0.0
    churn_risk: float = 0.0
    engagement_score: float = 0.0
    recent_interactions: list[dict] = []
    industry: IndustryType = IndustryType.GENERAL
    tags: list[str] = []


class ProfileAnalysisRequest(BaseModel):
    """Request to analyze user profile data."""
    user_id: str
    raw_data: dict = Field(default_factory=dict)
    industry: IndustryType = IndustryType.GENERAL
    include_ai_insights: bool = True


class ProfileAnalysisResponse(BaseModel):
    """Results of profile analysis."""
    user_id: str
    profile: UserProfile
    ai_insights: Optional[str] = None
    recommended_segment: Optional[str] = None
    next_best_action: Optional[str] = None


class SegmentCriteria(BaseModel):
    """Criteria for user segmentation."""
    name: str
    description: str = ""
    rules: list[dict] = Field(default_factory=list)
    industry: Optional[IndustryType] = None


class IndustryTemplate(BaseModel):
    """Industry-specific profile template."""
    industry: IndustryType
    name: str
    default_segments: list[SegmentCriteria] = []
    key_traits: list[str] = []
    description: str = ""
