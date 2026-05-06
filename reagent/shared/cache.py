"""Caching layer with multi-backend support."""

from __future__ import annotations

import json
import hashlib
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional

from loguru import logger


class CacheBackend:
    """Abstract cache backend interface."""

    async def get(self, key: str) -> Optional[str]:
        raise NotImplementedError

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        raise NotImplementedError

    async def delete(self, key: str) -> None:
        raise NotImplementedError


class MemoryCache(CacheBackend):
    """Simple in-memory cache (single-process)."""

    def __init__(self):
        self._store: dict[str, tuple[str, float]] = {}

    async def get(self, key: str) -> Optional[str]:
        import time
        if key in self._store:
            value, expiry = self._store[key]
            if time.time() < expiry:
                return value
            del self._store[key]
        return None

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        import time
        self._store[key] = (value, time.time() + ttl)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)


class RedisCache(CacheBackend):
    """Redis-backed cache."""

    def __init__(self, redis_url: str):
        import redis.asyncio as aioredis
        self._client = aioredis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        return await self._client.get(key)

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        await self._client.setex(key, ttl, value)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)


class CacheManager:
    """Cache manager with automatic backend selection."""

    def __init__(self, redis_url: str = ""):
        self._backend: CacheBackend = (
            RedisCache(redis_url) if redis_url and "redis" in redis_url
            else MemoryCache()
        )
        logger.info(f"Cache backend: {type(self._backend).__name__}")

    def _make_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate deterministic cache key."""
        raw = f"{prefix}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def cached(self, prefix: str = "", ttl: int = 300):
        """Decorator: cache function results."""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                key = self._make_key(prefix or func.__name__, args, kwargs)
                cached = await self._backend.get(key)
                if cached is not None:
                    return json.loads(cached)
                result = await func(*args, **kwargs)
                await self._backend.set(key, json.dumps(result, default=str), ttl)
                return result
            return wrapper
        return decorator

    async def invalidate(self, key: str) -> None:
        await self._backend.delete(key)


# Singleton
cache = CacheManager()
