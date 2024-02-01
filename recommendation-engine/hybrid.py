"""Hybrid recommendation engine combining collaborative + content-based."""
from typing import List, Dict, Any
from .collaborative import CollaborativeFilter
from .content_based import ContentBasedRecommender


class HybridRecommender:
    """Combines collaborative and content-based approaches with weighted ensemble."""
    
    def __init__(self, cf_weight: float = 0.6, cb_weight: float = 0.4):
        self.cf = CollaborativeFilter()
        self.cb = ContentBasedRecommender()
        self.cf_weight = cf_weight
        self.cb_weight = cb_weight
    
    def recommend(self, user_id: Any, top_k: int = 10, **kwargs) -> List[Dict]:
        cf_results = self._get_cf_recommendations(user_id, top_k * 2)
        cb_results = self._get_cb_recommendations(user_id, top_k * 2)
        
        combined: Dict[str, float] = {}
        for item_id, score in cf_results:
            combined[item_id] = combined.get(item_id, 0) + score * self.cf_weight
        for item_id, score in cb_results:
            combined[item_id] = combined.get(item_id, 0) + score * self.cb_weight
        
        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [{"item_id": iid, "score": sc, "source": "hybrid"} for iid, sc in ranked]
    
    def _get_cf_recommendations(self, user_id, limit):
        return []
    
    def _get_cb_recommendations(self, user_id, limit):
        return self.cb.recommend(str(user_id), limit)
