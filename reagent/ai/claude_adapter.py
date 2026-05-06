"""Anthropic Claude API adapter implementation."""

from __future__ import annotations

from typing import AsyncGenerator

from anthropic import AsyncAnthropic

from loguru import logger

from reagent.ai.base import BaseAIAdapter, GenerationResult
from reagent.ai.schema import (
    ModelRequest,
    ModelProvider,
    ModelInfo,
    ModelCapability,
)


class ClaudeAdapter(BaseAIAdapter):
    """Adapter for Anthropic Claude API."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
    ):
        self._client = AsyncAnthropic(api_key=api_key)
        self._model = model
        self._model_info = ModelInfo(
            provider=ModelProvider.ANTHROPIC,
            model_id=model,
            display_name=f"Anthropic {model}",
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.TOOL_USE,
                ModelCapability.STRUCTURED_OUTPUT,
            ],
            max_tokens=8192,
        )
        logger.info(f"Claude adapter initialized: model={model}")

    async def generate(self, request: ModelRequest) -> GenerationResult:
        """Send a message to Claude."""
        system = request.system_prompt or ""
        messages = [{"role": m.role.value, "content": m.content} for m in request.messages]

        kwargs = {
            "model": request.model or self._model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system

        response = await self._client.messages.create(**kwargs)

        text = ""
        for block in response.content:
            if block.type == "text":
                text += block.text

        usage = {
            "prompt_tokens": response.usage.input_tokens if response.usage else 0,
            "completion_tokens": response.usage.output_tokens if response.usage else 0,
            "total_tokens": (response.usage.input_tokens if response.usage else 0)
                          + (response.usage.output_tokens if response.usage else 0),
        }

        return GenerationResult(
            text=text,
            model_info=self._model_info,
            usage=usage,
            raw=response.model_dump() if hasattr(response, "model_dump") else {},
        )

    async def generate_stream(self, request: ModelRequest) -> AsyncGenerator[str, None]:
        """Stream tokens from Claude."""
        system = request.system_prompt or ""
        messages = [{"role": m.role.value, "content": m.content} for m in request.messages]

        async with self._client.messages.stream(
            model=request.model or self._model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=system or None,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def get_model_info(self) -> ModelInfo:
        return self._model_info
