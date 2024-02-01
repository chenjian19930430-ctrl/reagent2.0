"""Profile enrichment engine - enriches raw customer data with AI."""
import hashlib
import json
from datetime import datetime
from typing import Optional


class ProfileEnricher:
    """Enriches customer profiles using available data sources."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._cache: dict = {}
    
    def enrich(self, customer_id: str, raw_data: dict) -> dict:
        """Enrich profile with computed attributes."""
        enriched = dict(raw_data)
        enriched["enriched_at"] = datetime.utcnow().isoformat()
        enriched["computed_segment"] = self._compute_segment(raw_data)
        enriched["engagement_score"] = self._compute_engagement(raw_data)
        enriched["lookalike_candidates"] = self._find_lookalikes(raw_data)
        return enriched
    
    def _compute_segment(self, data: dict) -> str:
        score = data.get("engagement_score", 0)
        if score > 0.8:
            return "high_value"
        elif score > 0.5:
            return "active"
        elif score > 0.2:
            return "engaging"
        return "cold"
    
    def _compute_engagement(self, data: dict) -> float:
        visits = data.get("page_visits", 0)
        clicks = data.get("click_count", 0)
        purchases = data.get("purchase_count", 0)
        return min(1.0, (visits * 0.01 + clicks * 0.05 + purchases * 0.2))
    
    def _find_lookalikes(self, data: dict) -> list:
        key = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
        return self._cache.get(key, [])
