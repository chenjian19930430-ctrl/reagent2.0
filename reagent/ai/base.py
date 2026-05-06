"""Base AI Adapter — abstract interface for all model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from reagent.ai.schema import ModelRequest, ModelResponse, ModelInfo


class GenerationResult:
    """Unified result from a generation call."""

    def __init__(
        self,
        text: str,
        model_info: ModelInfo,
        usage: dict | None = None,
        raw: dict | None = None,
    ):
        self.text = text
        self.model_info = model_info
        self.usage = usage or {}
        self.raw = raw or {}

    def to_response(self) -> ModelResponse:
        usage = self.usage or {}
        pt = usage.get("prompt_tokens", usage.get("input_tokens", 0))
        ct = usage.get("completion_tokens", usage.get("output_tokens", 0))
        return ModelResponse(
            provider=self.model_info.provider,
            model=self.model_info.model_id,
            content=self.text,
            usage={
                "prompt_tokens": pt,
                "completion_tokens": ct,
                "total_tokens": pt + ct,
            },
        )


class BaseAIAdapter(ABC):
    """Abstract adapter for AI model providers."""

    @abstractmethod
    async def generate(self, request: ModelRequest) -> GenerationResult:
        """Generate a complete (non-streaming) response."""
        ...

    @abstractmethod
    async def generate_stream(self, request: ModelRequest) -> AsyncGenerator[str, None]:
        """Stream a generation response token by token."""
        ...  # pragma: no cover
        yield  # make it a generator

    @abstractmethod
    async def get_model_info(self) -> ModelInfo:
        """Return metadata about this model/provider."""
        ...
