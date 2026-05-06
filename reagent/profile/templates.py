"""Industry templates management — 行业模板的加载与自定义。"""

from __future__ import annotations

from typing import Optional

from loguru import logger

from reagent.profile.schema import IndustryTemplate, IndustryType
from reagent.profile.segmenter import INDUSTRY_TEMPLATES


class TemplateManager:
    """Industry template management.

    Supports:
    - Built-in industry templates (ecommerce, education, finance, saas, etc.)
    - Custom user-defined templates
    - Template recommendation based on business type
    """

    def __init__(self):
        self._templates: dict[str, IndustryTemplate] = {
            t.industry.value: t for t in INDUSTRY_TEMPLATES.values()
        }
        self._custom_templates: dict[str, IndustryTemplate] = {}
        logger.info(f"TemplateManager initialized with {len(self._templates)} built-in templates")

    def get(self, industry: IndustryType) -> IndustryTemplate:
        """Get template for an industry (custom first, then built-in)."""
        key = industry.value
        return self._custom_templates.get(key) or self._templates.get(key, self._templates["general"])

    def register_custom(self, template: IndustryTemplate) -> None:
        """Register a custom industry template."""
        self._custom_templates[template.industry.value] = template
        logger.info(f"Custom template registered: {template.name}")

    def list_all(self) -> list[dict]:
        """List all available templates with metadata."""
        result = []
        for t in self._templates.values():
            result.append({
                "industry": t.industry.value,
                "name": t.name,
                "description": t.description,
                "builtin": True,
                "segments": len(t.default_segments),
            })
        for t in self._custom_templates.values():
            result.append({
                "industry": t.industry.value,
                "name": t.name,
                "description": t.description,
                "builtin": False,
                "segments": len(t.default_segments),
            })
        return result


# Singleton
template_manager = TemplateManager()
