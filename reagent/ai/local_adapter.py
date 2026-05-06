"""Local / LiteLLM adapter for running models via ollama or local endpoints."""

from __future__ import annotations

from typing import AsyncGenerator
from openai import AsyncOpenAI

from loguru import logger

from reagent.ai.base import BaseAIAdapter, GenerationResult
from reagent.ai.schema import (
    ModelRequest,
    ModelProvider,
    ModelInfo,
    ModelCapability,
)


class LocalAdapter(BaseAIAdapter):
    """Adapter for local/Ollama/LiteLLM endpoints (OpenAI-compatible)."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
        model: str = "qwen2.5:14b",
    ):
        self._client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self._model = model
        self._model_info = ModelInfo(
            provider=ModelProvider.LOCAL,
            model_id=model,
            display_name=f"Local {model}",
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
            ],
            max_tokens=8192,
            cost_per_1k_input=0,
            cost_per_1k_output=0,
        )
        logger.info(f"Local adapter initialized: model={model}, endpoint={base_url}")

    async def generate(self, request: ModelRequest) -> GenerationResult:
        """Send request to local/ollama endpoint."""
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        for msg in request.messages:
            messages.append({"role": msg.role.value, "content": msg.content})

        response = await self._client.chat.completions.create(
            model=request.model or self._model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

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
        """Stream from local endpoint."""
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        for msg in request.messages:
            messages.append({"role": msg.role.value, "content": msg.content})

        stream = await self._client.chat.completions.create(
            model=request.model or self._model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield delta.content

    async def get_model_info(self) -> ModelInfo:
        return self._model_info
