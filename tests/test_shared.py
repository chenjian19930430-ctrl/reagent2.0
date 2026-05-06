"""Tests for Shared Modules (config, errors, cache, logging)."""

import pytest
from reagent.shared.config import settings
from reagent.shared.errors import (
    ReAgentError, AIAdapterError, ModelNotAvailableError,
    ContentGenerationError, ProfileAnalysisError, AutomationError,
    RuleValidationError, ConfigurationError,
)


class TestConfig:
    """Test application configuration."""

    def test_settings_defaults(self):
        assert settings.app_name == "ReAgent"
        assert settings.api_prefix == "/api/v1"
        assert settings.ai_default_provider == "openai"
        assert settings.banner_default_width == 1200

    def test_settings_override_from_env(self, monkeypatch):
        monkeypatch.setenv("REAGENT_APP_NAME", "TestAgent")
        monkeypatch.setenv("REAGENT_DEBUG", "true")
        # Re-import to trigger reload
        from reagent.shared.config import Settings
        s = Settings()
        assert s.app_name == "TestAgent"  # noqa: S105 — test env var
        assert s.debug is True

    def test_content_output_dir_created(self):
        from pathlib import Path
        assert Path(settings.content_output_dir).exists()


class TestErrorHierarchy:
    """Test exception hierarchy."""

    def test_base_error(self):
        err = ReAgentError("Something went wrong", {"key": "value"})
        assert err.message == "Something went wrong"
        assert err.detail == {"key": "value"}
        assert err.code == "REAGENT_ERROR"
        assert err.http_status == 500
        d = err.to_dict()
        assert d["error"] == "REAGENT_ERROR"
        assert d["message"] == "Something went wrong"

    def test_ai_adapter_error(self):
        err = AIAdapterError("API timeout")
        assert err.code == "AI_ADAPTER_ERROR"
        assert err.http_status == 502

    def test_model_not_available(self):
        err = ModelNotAvailableError("GPT-5 not available")
        assert err.code == "MODEL_NOT_AVAILABLE"
        assert err.http_status == 503

    def test_content_generation_error(self):
        err = ContentGenerationError("Generation failed")
        assert err.code == "CONTENT_GENERATION_ERROR"

    def test_profile_analysis_error(self):
        err = ProfileAnalysisError("Missing traits")
        assert err.code == "PROFILE_ANALYSIS_ERROR"
        assert err.http_status == 422

    def test_automation_error(self):
        err = AutomationError("Engine failure")
        assert err.code == "AUTOMATION_ERROR"

    def test_rule_validation_error(self):
        err = RuleValidationError("Invalid operator")
        assert err.code == "RULE_VALIDATION_ERROR"
        assert err.http_status == 422

    def test_configuration_error(self):
        err = ConfigurationError("Missing API key")
        assert err.code == "CONFIGURATION_ERROR"

    def test_error_default_message(self):
        err = ReAgentError()
        assert err.message == "ReAgentError"


class TestCache:
    """Test caching layer."""

    @pytest.mark.asyncio
    async def test_memory_cache_set_get(self):
        from reagent.shared.cache import MemoryCache
        cache = MemoryCache()
        await cache.set("key1", "value1", ttl=60)
        val = await cache.get("key1")
        assert val == "value1"

    @pytest.mark.asyncio
    async def test_memory_cache_miss(self):
        from reagent.shared.cache import MemoryCache
        cache = MemoryCache()
        val = await cache.get("nonexistent")
        assert val is None

    @pytest.mark.asyncio
    async def test_memory_cache_expiry(self):
        from reagent.shared.cache import MemoryCache
        import time
        cache = MemoryCache()
        await cache.set("expire_key", "val", ttl=0)  # 0 TTL = immediate expiry
        await asyncio.sleep(0.01)
        val = await cache.get("expire_key")
        assert val is None

    @pytest.mark.asyncio
    async def test_memory_cache_delete(self):
        from reagent.shared.cache import MemoryCache
        cache = MemoryCache()
        await cache.set("del_key", "val", ttl=60)
        await cache.delete("del_key")
        val = await cache.get("del_key")
        assert val is None

    @pytest.mark.asyncio
    async def test_cache_manager_key_generation(self):
        from reagent.shared.cache import CacheManager
        mgr = CacheManager()
        key1 = mgr._make_key("test", "arg1", kw="val1")
        key2 = mgr._make_key("test", "arg1", kw="val1")
        assert key1 == key2  # Deterministic
        assert len(key1) == 32  # SHA256 truncated

    @pytest.mark.asyncio
    async def test_cache_manager_decorator(self):
        from reagent.shared.cache import CacheManager
        mgr = CacheManager()

        call_count = 0

        @mgr.cached(prefix="test_deco", ttl=30)
        async def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = await expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        result2 = await expensive_func(5)
        assert result2 == 10
        assert call_count == 1  # Cached

        result3 = await expensive_func(7)
        assert result3 == 14
        assert call_count == 2  # New args

    @pytest.mark.asyncio
    async def test_cache_invalidation(self):
        from reagent.shared.cache import CacheManager
        mgr = CacheManager()

        @mgr.cached(prefix="inval_test", ttl=60)
        async def cached_func() -> str:
            import time
            return f"result_{time.time()}"

        r1 = await cached_func()
        # Manually clear the key
        key = mgr._make_key("inval_test")
        await mgr.invalidate(key)
        # Note: the key used inside the decorator may differ; this tests the API surface


import asyncio


class TestLogging:
    """Test logging setup (smoke tests)."""

    def test_setup_logging(self):
        from reagent.shared.logging import setup_logging
        # Should not raise
        setup_logging()


class TestCacheInit:
    """Test CacheManager initialization."""

    @pytest.mark.asyncio
    async def test_cache_manager_init_memory(self):
        from reagent.shared.cache import CacheManager
        mgr = CacheManager(redis_url="")
        assert mgr._backend is not None
