"""Copywriting module — AI-powered marketing copy generation."""

from __future__ import annotations

import json
from loguru import logger

from reagent.ai.schema import ModelRequest, ModelProvider
from reagent.ai.registry import registry
from reagent.content.schema import (
    CopywritingRequest,
    CopywritingResponse,
    CopywritingTone,
)
from reagent.shared.cache import cache


class Copywriter:
    """AI copywriting engine with multi-model support."""

    TONE_PROMPTS = {
        CopywritingTone.PROFESSIONAL: "专业、严谨、数据驱动的语调。使用行业术语，突出ROI。",
        CopywritingTone.FRIENDLY: "友好、亲切的语调，像朋友在聊天。使用"你"而不是"您"。",
        CopywritingTone.URGENT: "紧迫感、稀缺性驱动的语调，强调限时优惠。",
        CopywritingTone.LUXURY: "高端、优雅的语调，强调品质和独特性。",
        CopywritingTone.CASUAL: "随意、轻松的语调，使用口语化表达。",
        CopywritingTone.FUNNY: "幽默、有趣的语调，适当使用段子和俏皮话。",
    }

    SYSTEM_PROMPT = """你是 ReAgent 智能营销助手，擅长创作高质量营销文案。

## 能力
1. 根据主题和产品描述创作吸引人的营销文案
2. 根据不同目标受众调整语言风格
3. 优化文案结构和节奏，提高转化率
4. 生成SEO关键词建议

## 输出格式
请严格按 JSON 格式输出，包含以下字段：
- headline: 吸引人的标题（不超过20字）
- body: 正文内容（markdown格式）
- cta: 行动号召
- seo_keywords: 3-5个SEO关键词列表
"""

    async def generate(self, request: CopywritingRequest) -> CopywritingResponse:
        """Generate marketing copy based on the request."""
        logger.info(f"Generating copy: topic='{request.topic}', tone={request.tone}")

        # Build user prompt
        tone_instruction = self.TONE_PROMPTS.get(request.tone, self.TONE_PROMPTS[CopywritingTone.PROFESSIONAL])

        user_prompt = f"""# 文案创作请求

**主题**: {request.topic}

**品牌**: {request.brand_name or '(未指定)'}
**产品描述**: {request.product_description or '(未指定)'}
**目标受众**: {request.target_audience or '通用'}

**语调**: {tone_instruction}
**最大长度**: {request.max_length}字
**语言**: {request.language}
**行动号召**: {request.call_to_action or '自动生成CTA'}

"""
        if request.key_points:
            user_prompt += f"**关键卖点**:\n" + "\n".join(f"- {kp}" for kp in request.key_points) + "\n"

        user_prompt += "\n请生成吸引人的营销文案（JSON格式）。"

        # Call AI
        ai_request = ModelRequest(
            model="",
            messages=[],
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.7,
        )

        result = await registry.generate(ai_request)

        # Parse JSON response
        try:
            # Extract JSON from markdown code block if present
            text = result.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            data = json.loads(text)
            return CopywritingResponse(
                headline=data.get("headline", request.topic),
                body=data.get("body", ""),
                cta=data.get("cta", request.call_to_action),
                seo_keywords=data.get("seo_keywords", []),
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse AI response as JSON: {e}")
            # Fallback: use raw text
            return CopywritingResponse(
                headline=request.topic,
                body=result,
                cta=request.call_to_action,
            )
