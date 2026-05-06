"""Content generation pipeline — 端到端内容创作编排。

将文案撰写 → Banner生成 → 落地页生成串联为可配置管线。
"""

from __future__ import annotations

from loguru import logger

from reagent.content.schema import (
    ContentGenerationRequest,
    ContentGenerationResponse,
    ContentType,
)
from reagent.content.copywriter import Copywriter
from reagent.content.banner import BannerGenerator
from reagent.content.landing import LandingPageGenerator


class ContentPipeline:
    """Orchestrated content generation pipeline.

    Pipeline stages:
    1. Copywriting generation (AI model)
    2. Banner image generation (if requested)
    3. Landing page generation (if copy exists)

    Each stage is independently skippable for partial generation.
    """

    def __init__(self):
        self._copywriter = Copywriter()
        self._banner_gen = BannerGenerator()
        self._landing_gen = LandingPageGenerator()
        logger.info("ContentPipeline initialized")

    async def run(self, request: ContentGenerationRequest) -> ContentGenerationResponse:
        """Execute the full content generation pipeline."""
        logger.info(f"Pipeline start: type={request.content_type}, campaign={request.campaign_id}")

        response = ContentGenerationResponse(
            campaign_id=request.campaign_id,
            ai_provider=request.ai_provider,
            ai_model=request.ai_model,
        )

        # Stage 1: Copywriting
        if request.copywriting:
            logger.info("Pipeline stage 1/3: Copywriting generation")
            copy = await self._copywriter.generate(request.copywriting)
            response.copy_result = copy

            # Stage 3: Landing page (if copy exists and content type matches)
            if request.content_type == ContentType.LANDING_PAGE and copy:
                logger.info("Pipeline stage 3/3: Landing page generation")
                html, path = await self._landing_gen.generate(
                    copy=copy,
                    brand_name=request.copywriting.brand_name,
                )
                response.landing_page_html = html

        # Stage 2: Banner generation
        if request.banner and request.content_type in (ContentType.BANNER, ContentType.LANDING_PAGE):
            logger.info("Pipeline stage 2/3: Banner generation")
            banner = await self._banner_gen.generate(request.banner)
            response.banner = banner

        logger.info(f"Pipeline complete: campaign={request.campaign_id}")
        return response

    async def generate_copy_only(self, request: ContentGenerationRequest) -> ContentGenerationResponse:
        """Generate copy only, skip media generation."""
        response = ContentGenerationResponse(campaign_id=request.campaign_id)
        if request.copywriting:
            copy = await self._copywriter.generate(request.copywriting)
            response.copy_result = copy
        return response

    async def generate_full(self, request: ContentGenerationRequest) -> ContentGenerationResponse:
        """Full pipeline: copy + banner + landing page."""
        return await self.run(request)
