"""AI Model Registry — factory & multi-model routing."""

from __future__ import annotations

from typing import Optional

from loguru import logger

from reagent.ai.base import BaseAIAdapter
from reagent.ai.schema import ModelProvider, ModelRequest, ModelInfo
from reagent.ai.openai_adapter import OpenAIAdapter
from reagent.ai.claude_adapter import ClaudeAdapter
from reagent.ai.local_adapter import LocalAdapter
from reagent.shared.config import settings


class AIAdapterRegistry:
    """Registry & factory for AI model adapters.

    Supports:
    - Multiple providers registered simultaneously
    - Dynamic model switching per request
    - Health check / availability query
    """

    def __init__(self):
        self._adapters: dict[str, BaseAIAdapter] = {}
        self._default_provider: ModelProvider = ModelProvider(settings.ai_default_provider)
        self._initialize_defaults()

    def _initialize_defaults(self) -> None:
        """Register default adapters from settings."""
        if settings.openai_api_key:
            self.register(
                f"openai:{settings.openai_default_model}",
                OpenAIAdapter(
                    api_key=settings.openai_api_key,
                    base_url=settings.openai_base_url or "https://api.openai.com/v1",
                    model=settings.openai_default_model,
                ),
            )
        if settings.anthropic_api_key:
            self.register(
                f"anthropic:{settings.anthropic_default_model}",
                ClaudeAdapter(
                    api_key=settings.anthropic_api_key,
                    model=settings.anthropic_default_model,
                ),
            )
        # Always register local adapter (low-cost fallback)
        self.register(
            f"local:{settings.local_default_model}",
            LocalAdapter(
                base_url=settings.local_api_base or "http://localhost:11434/v1",
                api_key=settings.local_api_key,
                model=settings.local_default_model,
            ),
        )
        logger.info(f"AI Registry initialized with {len(self._adapters)} adapters")

    def register(self, key: str, adapter: BaseAIAdapter) -> None:
        """Register an adapter under a key (e.g., 'openai:gpt-4o')."""
        self._adapters[key] = adapter
        logger.debug(f"Registered adapter: {key}")

    def get_adapter(self, key: str) -> Optional[BaseAIAdapter]:
        """Get adapter by full key."""
        return self._adapters.get(key)

    def resolve(self, request: ModelRequest) -> BaseAIAdapter:
        """Resolve an adapter for a given request.

        Resolution order:
        1. If request has 'openai:' / 'anthropic:' / 'local:' prefix → exact match
        2. Else → match by provider name
        3. Fallback → default provider
        """
        # Try exact key match
        for key, adapter in self._adapters.items():
            if key.startswith(f"{request.provider.value}:") and request.model in key:
                return adapter
            if key == f"{request.provider.value}:{request.model}":
                return adapter

        # Try provider-based match
        for key, adapter in self._adapters.items():
            if key.startswith(f"{request.provider.value}:"):
                return adapter

        # Fallback to default
        default_key = f"{self._default_provider.value}:{settings.openai_default_model}"
        adapter = self._adapters.get(default_key)
        if adapter:
            return adapter

        # Last resort: first available adapter
        if self._adapters:
            return next(iter(self._adapters.values()))

        raise RuntimeError("No AI adapters registered")

    async def generate(self, request: ModelRequest) -> str:
        """Generate text from the best-matching model."""
        adapter = self.resolve(request)
        result = await adapter.generate(request)
        return result.text

    async def list_available_models(self) -> list[ModelInfo]:
        """List all registered models and their capabilities."""
        models = []
        for key, adapter in self._adapters.items():
            info = await adapter.get_model_info()
            models.append(info)
        return models


# Global registry singleton
registry = AIAdapterRegistry()
