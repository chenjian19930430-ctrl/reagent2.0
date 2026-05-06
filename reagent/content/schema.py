"""Content generation schemas."""

from __future__ import annotations

from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field


class ContentType(str, Enum):
    COPYWRITING = "copywriting"
    BANNER = "banner"
    LANDING_PAGE = "landing_page"
    EMAIL = "email"
    SOCIAL_POST = "social_post"


class CopywritingTone(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    URGENT = "urgent"
    LUXURY = "luxury"
    CASUAL = "casual"
    FUNNY = "funny"


class BannerFormat(str, Enum):
    SOCIAL_MEDIA = "social_media"  # 1:1
    LANDSCAPE = "landscape"        # 16:9
    PORTRAIT = "portrait"          # 9:16
    LEADERBOARD = "leaderboard"    # 728x90


class CopywritingRequest(BaseModel):
    """Request to generate marketing copy."""
    topic: str
    brand_name: str = ""
    product_description: str = ""
    target_audience: str = ""
    tone: CopywritingTone = CopywritingTone.PROFESSIONAL
    max_length: int = 500
    language: str = "zh-CN"
    key_points: list[str] = []
    call_to_action: str = ""


class CopywritingResponse(BaseModel):
    """Generated copy output."""
    headline: str
    body: str
    cta: str = ""
    seo_keywords: list[str] = []


class BannerRequest(BaseModel):
    """Request to generate a banner image."""
    copy_text: str = Field(default="", validation_alias="copy")
    headline: str
    brand_name: str = ""
    format: BannerFormat = BannerFormat.LANDSCAPE
    style: str = "modern"  # modern, elegant, vibrant, minimal
    primary_color: str = "#1a73e8"
    secondary_color: str = "#ffffff"
    background_type: Literal["solid", "gradient", "image"] = "gradient"


class BannerResponse(BaseModel):
    """Generated banner output."""
    image_path: str
    width: int
    height: int
    format: BannerFormat


class ContentGenerationRequest(BaseModel):
    """Unified request for end-to-end content generation."""
    campaign_id: str = ""
    content_type: ContentType
    copywriting: CopywritingRequest
    banner: Optional[BannerRequest] = None
    ai_provider: str = "openai"
    ai_model: str = ""


class ContentGenerationResponse(BaseModel):
    """Unified response for content generation."""
    campaign_id: str = ""
    copy_result: Optional[CopywritingResponse] = Field(default=None, validation_alias="copy")
    banner: Optional[BannerResponse] = None
    landing_page_html: Optional[str] = None
    ai_provider: str = ""
    ai_model: str = ""
    usage: dict = Field(default_factory=dict)
