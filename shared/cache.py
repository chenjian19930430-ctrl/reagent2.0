"""Distributed cache abstraction."""
from typing import Optional, Any
import json
import hashlib


class Cache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self):
        self._store: dict = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            value, expiry = self._store[key]
            if expiry is None or expiry > __import__('time').time():
                return value
            del self._store[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = 300):
        expiry = (__import__('time').time() + ttl_seconds) if ttl_seconds else None
        self._store[key] = (value, expiry)
    
    def build_key(self, prefix: str, *parts) -> str:
        raw = ":".join(str(p) for p in parts)
        return f"{prefix}:{hashlib.md5(raw.encode()).hexdigest()}"
    
    def invalidate(self, prefix: str):
        self._store = {k: v for k, v in self._store.items() if not k.startswith(prefix)}
