"""Tests for Content Generation Pipeline."""

import pytest
from reagent.content.schema import (
    ContentType, CopywritingTone, BannerFormat,
    CopywritingRequest, CopywritingResponse,
    BannerRequest, BannerResponse,
    ContentGenerationRequest, ContentGenerationResponse,
    ContentType,
)


class TestContentSchemas:
    """Test content schema models."""

    def test_copywriting_request(self):
        req = CopywritingRequest(
            topic="夏季促销",
            brand_name="TestBrand",
            tone=CopywritingTone.URGENT,
            language="zh-CN",
        )
        assert req.topic == "夏季促销"
        assert req.tone == CopywritingTone.URGENT
        assert req.max_length == 500

    def test_copywriting_response(self):
        resp = CopywritingResponse(
            headline="限时优惠！",
            body="本周末全场五折",
            cta="立即购买",
            seo_keywords=["促销", "优惠"],
        )
        assert resp.headline == "限时优惠！"
        assert len(resp.seo_keywords) == 2

    def test_banner_request(self):
        req = BannerRequest(
            copy="促销文案",
            headline="大促",
            format=BannerFormat.SOCIAL_MEDIA,
        )
        assert req.format == BannerFormat.SOCIAL_MEDIA

    def test_content_generation_request(self):
        req = ContentGenerationRequest(
            content_type=ContentType.BANNER,
            copywriting=CopywritingRequest(topic="Test"),
            banner=BannerRequest(copy="test", headline="test"),
        )
        assert req.content_type == ContentType.BANNER
        assert req.copywriting.topic == "Test"


class TestBannerGenerator:
    """Test banner image generation."""

    def test_banner_sizes(self):
        from reagent.content.banner import BANNER_SIZES
        assert BANNER_SIZES[BannerFormat.LANDSCAPE] == (1200, 628)
        assert BANNER_SIZES[BannerFormat.SOCIAL_MEDIA] == (1080, 1080)
        assert BANNER_SIZES[BannerFormat.LEADERBOARD] == (728, 90)


class TestLandingPage:
    """Test landing page generation."""

    def test_template_renders(self):
        from reagent.content.landing import LANDING_TEMPLATE
        html = LANDING_TEMPLATE.render(
            headline="Test",
            body_html="<p>Body</p>",
            cta="Click",
            brand_name="TestBrand",
            primary_color="#000",
            secondary_color="#fff",
            language="zh-CN",
        )
        assert "Test" in html
        assert "TestBrand" in html
        assert "<p>Body</p>" in html


class TestMediaAssembler:
    """Test media assembly (FFmpeg wrapper)."""

    def test_initialization(self):
        from reagent.content.media_gen import MediaAssembler
        assembler = MediaAssembler()
        assert assembler is not None

    def test_concat_empty_raises(self):
        import pytest
        from reagent.content.media_gen import MediaAssembler
        assembler = MediaAssembler()

        async def test():
            with pytest.raises(ValueError, match="At least one"):
                await assembler.concat_videos([])

        import asyncio
        asyncio.run(test())
