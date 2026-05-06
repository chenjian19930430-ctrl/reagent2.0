"""Landing page HTML generation module."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Optional

from loguru import logger
from jinja2 import Template

from reagent.content.schema import CopywritingResponse
from reagent.shared.config import settings


# Minimal landing page template
LANDING_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="{{ language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ headline }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, {{ primary_color }} 0%, {{ secondary_color }} 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .container {
            background: white;
            border-radius: 16px;
            padding: 3rem;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: {{ primary_color }};
        }
        .body-content {
            font-size: 1.1rem;
            color: #555;
            margin-bottom: 2rem;
        }
        .cta-button {
            display: inline-block;
            background: {{ primary_color }};
            color: white;
            padding: 1rem 2.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }
        .footer {
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #999;
            text-align: center;
        }
        @media (max-width: 600px) {
            .container { padding: 1.5rem; }
            h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ headline }}</h1>
        <div class="body-content">{{ body_html }}</div>
        <a href="#" class="cta-button">{{ cta }}</a>
        <div class="footer">{{ brand_name }} &middot; Powered by ReAgent</div>
    </div>
</body>
</html>""")


class LandingPageGenerator:
    """Landing page HTML generator.

    Phase 1: Jinja2 template rendering.
    Phase 2+: Dynamic sections, A/B testing, image integration.
    """

    def __init__(self):
        self._output_dir = Path(settings.content_output_dir) / "landing"
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def generate(
        self,
        copy: CopywritingResponse,
        brand_name: str = "",
        primary_color: str = "#1a73e8",
        secondary_color: str = "#e8f0fe",
        language: str = "zh-CN",
    ) -> tuple[str, str]:
        """Generate landing page HTML and save to file.

        Returns:
            Tuple of (html_content, file_path)
        """
        # Convert markdown body to simple HTML
        import markdown
        body_html = markdown.markdown(copy.body)

        html = LANDING_TEMPLATE.render(
            headline=copy.headline,
            body_html=body_html,
            cta=copy.cta or "立即体验",
            brand_name=brand_name or "ReAgent",
            primary_color=primary_color,
            secondary_color=secondary_color,
            language=language,
        )

        # Save to file
        filename = f"landing_{uuid.uuid4().hex[:8]}.html"
        output_path = self._output_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info(f"Landing page saved: {output_path}")
        return html, str(output_path)
