"""OpenAI API adapter implementation."""

from __future__ import annotations

from typing import AsyncGenerator

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionChunk

from loguru import logger

from reagent.ai.base import BaseAIAdapter, GenerationResult
from reagent.ai.schema import (
    ModelRequest,
    ModelProvider,
    ModelInfo,
    ModelCapability,
)


class OpenAIAdapter(BaseAIAdapter):
    """Adapter for OpenAI-compatible API (GPT-4o, GPT-4, etc.)."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o",
    ):
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._model = model
        self._model_info = ModelInfo(
            provider=ModelProvider.OPENAI,
            model_id=model,
            display_name=f"OpenAI {model}",
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.IMAGE_UNDERSTANDING,
                ModelCapability.TOOL_USE,
                ModelCapability.STRUCTURED_OUTPUT,
            ],
            max_tokens=16384,
        )
        logger.info(f"OpenAI adapter initialized: model={model}, base_url={base_url}")

    async def generate(self, request: ModelRequest) -> GenerationResult:
        """Send a chat completion request to OpenAI."""
        messages = self._build_messages(request)
        kwargs = {
            "model": request.model or self._model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if request.tools:
            kwargs["tools"] = request.tools

        response = await self._client.chat.completions.create(**kwargs)
        choice = response.choices[0]

        text = choice.message.content or ""
        usage = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        }

        return GenerationResult(
            text=text,
            model_info=self._model_info,
            usage=usage,
            raw=response.model_dump() if hasattr(response, "model_dump") else {},
        )

    async def generate_stream(self, request: ModelRequest) -> AsyncGenerator[str, None]:
        """Stream tokens from OpenAI."""
        messages = self._build_messages(request)
        kwargs = {
            "model": request.model or self._model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True,
        }
        if request.tools:
            kwargs["tools"] = request.tools

        stream: AsyncGenerator[ChatCompletionChunk, None] = await self._client.chat.completions.create(**kwargs)
        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield delta.content

    async def get_model_info(self) -> ModelInfo:
        return self._model_info

    def _build_messages(self, request: ModelRequest) -> list[dict]:
        """Build OpenAI-format messages from ModelRequest."""
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        for msg in request.messages:
            messages.append({"role": msg.role.value, "content": msg.content})
        return messages
