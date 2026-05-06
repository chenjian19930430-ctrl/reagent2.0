"""Tests for AI Model Adapter Layer."""

import pytest
from reagent.ai.schema import (
    ModelProvider, ModelRequest, ModelResponse, Message, MessageRole,
    ModelCapability, ModelInfo,
)
from reagent.ai.base import BaseAIAdapter, GenerationResult
from reagent.ai.openai_adapter import OpenAIAdapter
from reagent.ai.claude_adapter import ClaudeAdapter
from reagent.ai.local_adapter import LocalAdapter
from reagent.ai.registry import AIAdapterRegistry


class TestModelSchemas:
    """Test AI schema models."""

    def test_message_creation(self):
        msg = Message(role=MessageRole.USER, content="Hello")
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"

    def test_model_request(self):
        req = ModelRequest(
            provider=ModelProvider.OPENAI,
            model="gpt-4o",
            messages=[Message(role=MessageRole.USER, content="test")],
            system_prompt="Be helpful",
        )
        assert req.provider == ModelProvider.OPENAI
        assert len(req.messages) == 1
        assert req.system_prompt == "Be helpful"

    def test_model_response(self):
        resp = ModelResponse(
            provider=ModelProvider.OPENAI,
            model="gpt-4o",
            content="Hello!",
        )
        assert resp.content == "Hello!"
        assert resp.finish_reason == "stop"

    def test_generation_result(self):
        info = ModelInfo(
            provider=ModelProvider.OPENAI,
            model_id="gpt-4o",
            display_name="GPT-4o",
        )
        result = GenerationResult(
            text="Generated text",
            model_info=info,
            usage={"prompt_tokens": 10, "completion_tokens": 20},
        )
        assert result.text == "Generated text"
        response = result.to_response()
        assert response.content == "Generated text"
        assert response.usage["total_tokens"] == 30


class TestRegistry:
    """Test AI adapter registry."""

    def test_registry_initialization(self):
        registry = AIAdapterRegistry()
        # Should have at least local adapter registered
        assert len(registry._adapters) >= 1
        assert any("local:" in key for key in registry._adapters)

    def test_resolve_fallback(self):
        registry = AIAdapterRegistry()
        req = ModelRequest(provider=ModelProvider.OPENAI, messages=[])
        adapter = registry.resolve(req)
        assert adapter is not None

    def test_list_models_smoke(self):
        import asyncio
        registry = AIAdapterRegistry()

        async def test():
            models = await registry.list_available_models()
            assert len(models) >= 1
            for m in models:
                assert m.model_id
                assert m.provider in ModelProvider

        asyncio.run(test())
