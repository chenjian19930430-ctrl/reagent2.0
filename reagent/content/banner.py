"""Banner image generation module — PIL-based assembly (Phase 1 MVP)."""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

from loguru import logger
from PIL import Image, ImageDraw, ImageFont

from reagent.content.schema import (
    BannerRequest,
    BannerResponse,
    BannerFormat,
)
from reagent.shared.config import settings


# Banner size map
BANNER_SIZES = {
    BannerFormat.SOCIAL_MEDIA: (1080, 1080),
    BannerFormat.LANDSCAPE: (1200, 628),
    BannerFormat.PORTRAIT: (720, 1280),
    BannerFormat.LEADERBOARD: (728, 90),
}


class BannerGenerator:
    """Banner / image generation module.

    Phase 1 MVP: PIL-based image composition.
    Phase 2+: Integration with MiniMax / Midjourney / DALL-E.
    """

    def __init__(self):
        self._output_dir = Path(settings.content_output_dir) / "banners"
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def generate(self, request: BannerRequest) -> BannerResponse:
        """Generate a banner image."""
        width, height = BANNER_SIZES.get(request.format, (1200, 628))
        logger.info(f"Generating banner: {width}x{height}, style={request.style}")

        # Run PIL in thread pool to avoid blocking event loop
        image_path = await asyncio.to_thread(
            self._render_image,
            request, width, height,
        )

        return BannerResponse(
            image_path=str(image_path),
            width=width,
            height=height,
            format=request.format,
        )

    def _render_image(self, request: BannerRequest, width: int, height: int) -> Path:
        """Render banner image using PIL."""
        primary_rgb = self._hex_to_rgb(request.primary_color)

        # Create background
        img = Image.new("RGB", (width, height), primary_rgb)
        draw = ImageDraw.Draw(img)

        # Draw gradient overlay (if gradient)
        if request.background_type == "gradient":
            secondary_rgb = self._hex_to_rgb(request.secondary_color)
            for y in range(height):
                ratio = y / height
                r = int(primary_rgb[0] * (1 - ratio) + secondary_rgb[0] * ratio)
                g = int(primary_rgb[1] * (1 - ratio) + secondary_rgb[1] * ratio)
                b = int(primary_rgb[2] * (1 - ratio) + secondary_rgb[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Draw headline text (centered)
        font_size = max(24, min(width, height) // 12)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
        except (IOError, OSError):
            font = ImageFont.load_default()

        # Simple text layout
        headline = request.headline[:50]
        text_bbox = draw.textbbox((0, 0), headline, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (width - text_width) // 2
        text_y = height // 3

        # Shadow for readability
        shadow_color = (0, 0, 0, 128)
        draw.text((text_x + 2, text_y + 2), headline, font=font, fill=shadow_color)
        draw.text((text_x, text_y), headline, font=font, fill="white")

        # Draw body copy
        copy_font_size = max(16, font_size // 2)
        try:
            copy_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", copy_font_size)
        except (IOError, OSError):
            copy_font = ImageFont.load_default()

        body = (request.copy_text or request.headline)[:100]
        copy_bbox = draw.textbbox((0, 0), body, font=copy_font)
        copy_width = copy_bbox[2] - copy_bbox[0]
        copy_x = (width - copy_width) // 2
        copy_y = text_y + text_height + 30

        draw.text((copy_x + 1, copy_y + 1), body, font=copy_font, fill=(0, 0, 0, 100))
        draw.text((copy_x, copy_y), body, font=copy_font, fill=(230, 230, 230))

        # Save
        filename = f"banner_{uuid.uuid4().hex[:8]}.png"
        output_path = self._output_dir / filename
        img.save(output_path, "PNG")
        logger.info(f"Banner saved: {output_path}")

        return output_path

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Convert hex color string to RGB tuple.
        Handles #RGB and #RRGGBB formats.
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        if len(hex_color) < 6:
            hex_color = hex_color.ljust(6, "0")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
