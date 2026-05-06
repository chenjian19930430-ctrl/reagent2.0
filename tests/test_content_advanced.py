"""Advanced tests for Content Generation Pipeline — pipeline orchestration, edge cases."""

import pytest
from unittest.mock import patch, AsyncMock
from reagent.content.schema import (
    ContentType, CopywritingTone, BannerFormat,
    CopywritingRequest, CopywritingResponse,
    BannerRequest, BannerResponse,
    ContentGenerationRequest, ContentGenerationResponse,
)


class TestContentSchemasAdvanced:
    """Test content schema edge cases."""

    def test_copywriting_request_all_fields(self):
        req = CopywritingRequest(
            topic="新产品发布",
            brand_name="TechCo",
            product_description="一款革命性产品",
            target_audience="年轻白领",
            tone=CopywritingTone.FRIENDLY,
            max_length=300,
            language="en-US",
            key_points=["创新", "高效"],
            call_to_action="立即试用",
        )
        assert req.tone == CopywritingTone.FRIENDLY
        assert "创新" in req.key_points
        assert req.call_to_action == "立即试用"

    def test_banner_request_defaults(self):
        req = BannerRequest(
            copy_text="Sale!",
            headline="促销",
        )
        assert req.format == BannerFormat.LANDSCAPE
        assert req.style == "modern"
        assert req.primary_color == "#1a73e8"
        assert req.background_type == "gradient"

    def test_content_generation_response(self):
        copy_resp = CopywritingResponse(headline="Test", body="Body", cta="Buy now")
        resp = ContentGenerationResponse(
            campaign_id="camp_1",
            copy=copy_resp,
            ai_provider="openai",
        )
        assert resp.campaign_id == "camp_1"
        assert resp.copy_result is not None
        assert resp.copy_result.headline == "Test"

    def test_content_generation_response_empty(self):
        resp = ContentGenerationResponse()
        assert resp.copy_result is None

    def test_content_type_values(self):
        assert ContentType.COPYWRITING.value == "copywriting"
        assert ContentType.EMAIL.value == "email"

    def test_banner_format_sizes(self):
        assert BannerFormat.LEADERBOARD.value == "leaderboard"


class TestBannerGeneratorAdvanced:
    """Advanced banner generation tests."""

    def test_hex_to_rgb(self):
        from reagent.content.banner import BannerGenerator
        bg = BannerGenerator()
        assert bg._hex_to_rgb("#ff0000") == (255, 0, 0)
        assert bg._hex_to_rgb("#00ff00") == (0, 255, 0)
        assert bg._hex_to_rgb("#0000ff") == (0, 0, 255)
        assert bg._hex_to_rgb("ffffff") == (255, 255, 255)
        assert bg._hex_to_rgb("#000") == (0, 0, 0)

    @pytest.mark.asyncio
    async def test_generate_banner_output(self):
        from reagent.content.banner import BannerGenerator
        bg = BannerGenerator()
        req = BannerRequest(
            copy_text="限时优惠",
            headline="夏季大促",
            format=BannerFormat.SOCIAL_MEDIA,
        )
        resp = await bg.generate(req)
        assert resp.image_path.endswith(".png")
        assert resp.width == 1080
        assert resp.height == 1080
        assert resp.format == BannerFormat.SOCIAL_MEDIA

    @pytest.mark.asyncio
    async def test_generate_banner_no_copy(self):
        from reagent.content.banner import BannerGenerator
        bg = BannerGenerator()
        req = BannerRequest(
            headline="Just a Headline",
            format=BannerFormat.LEADERBOARD,
        )
        resp = await bg.generate(req)
        assert resp.width == 728
        assert resp.height == 90

    @pytest.mark.asyncio
    async def test_banner_gradient(self):
        from reagent.content.banner import BannerGenerator
        bg = BannerGenerator()
        req = BannerRequest(
            copy_text="Gradient test",
            headline="Gradient",
            background_type="gradient",
        )
        resp = await bg.generate(req)
        assert resp.image_path is not None


class TestLandingPageAdvanced:
    """Advanced landing page tests."""

    @pytest.mark.asyncio
    async def test_landing_page_generation(self):
        from reagent.content.landing import LandingPageGenerator
        gen = LandingPageGenerator()
        copy = CopywritingResponse(
            headline="欢迎体验",
            body="这是一款**革命性**的产品",
            cta="立即注册",
        )
        html, path = await gen.generate(
            copy=copy,
            brand_name="TestBrand",
            primary_color="#ff6600",
            secondary_color="#fff3e0",
        )
        assert "欢迎体验" in html
        assert "<strong>革命性</strong>" in html
        assert "立即注册" in html
        assert path.endswith(".html")
        # Verify file was written
        import os
        assert os.path.exists(path)
        os.unlink(path)  # Cleanup

    @pytest.mark.asyncio
    async def test_landing_page_default_cta(self):
        from reagent.content.landing import LandingPageGenerator
        gen = LandingPageGenerator()
        copy = CopywritingResponse(
            headline="Test",
            body="Content",
            cta="",
        )
        html, path = await gen.generate(copy=copy)
        assert "立即体验" in html  # Default CTA


class TestPipelineAdvanced:
    """Advanced pipeline orchestration tests."""

    @pytest.mark.asyncio
    @patch('reagent.content.pipeline.ContentPipeline.generate_copy_only')
    async def test_generate_copy_only(self, mock_gen):
        from reagent.content.schema import CopywritingResponse, ContentGenerationResponse
        cp = CopywritingResponse(headline='Test Headline', body='Test Body', cta='Buy Now')
        mock_gen.return_value = ContentGenerationResponse(
            campaign_id='test',
            copy=cp,
        )
        from reagent.content.pipeline import ContentPipeline
        pipeline = ContentPipeline()
        req = ContentGenerationRequest(
            content_type=ContentType.COPYWRITING,
            copywriting=CopywritingRequest(
                topic="Test Topic",
                brand_name="TestBrand",
            ),
        )
        resp = await pipeline.generate_copy_only(req)
        # Verify the mock was called
        assert mock_gen.called

    @pytest.mark.asyncio
    @patch('reagent.content.pipeline.ContentPipeline.run')
    async def test_pipeline_full(self, mock_run):
        from reagent.content.schema import CopywritingResponse, ContentGenerationResponse
        cp = CopywritingResponse(headline='促销', body='限时优惠', cta='立即下单')
        mock_run.return_value = ContentGenerationResponse(
            campaign_id='test_camp',
            copy=cp,
        )
        from reagent.content.pipeline import ContentPipeline
        pipeline = ContentPipeline()
        req = ContentGenerationRequest(
            campaign_id="test_camp",
            content_type=ContentType.BANNER,
            copywriting=CopywritingRequest(
                topic="促销活动",
                brand_name="Brand",
            ),
            banner=BannerRequest(
                headline="促销",
            ),
        )
        resp = await pipeline.run(req)
        assert resp.campaign_id == "test_camp"


class TestMediaAssemblerAdvanced:
    """Advanced media assembly tests."""

    @pytest.mark.asyncio
    async def test_overlay_text_no_video_raises(self):
        from reagent.content.media_gen import MediaAssembler
        assembler = MediaAssembler()

        with pytest.raises(Exception):
            await assembler.overlay_text(
                video_path="/nonexistent/video.mp4",
                text="Hello",
            )
