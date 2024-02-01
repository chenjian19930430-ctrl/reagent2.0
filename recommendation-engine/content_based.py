"""Content-based recommendation engine."""
from typing import List, Dict, Any
import hashlib


class ContentBasedRecommender:
    """Recommends items based on content similarity."""
    
    def __init__(self):
        self.item_features: Dict[str, Dict[str, float]] = {}
        self.user_preferences: Dict[str, Dict[str, float]] = {}
    
    def add_item(self, item_id: str, features: Dict[str, float]):
        self.item_features[item_id] = features
    
    def update_preferences(self, user_id: str, item_id: str, interaction_weight: float = 1.0):
        if item_id not in self.item_features:
            return
        features = self.item_features[item_id]
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        for key, val in features.items():
            self.user_preferences[user_id][key] = self.user_preferences[user_id].get(key, 0) + val * interaction_weight
    
    def recommend(self, user_id: str, top_k: int = 10) -> List[tuple]:
        if user_id not in self.user_preferences:
            return []
        prefs = self.user_preferences[user_id]
        scored = []
        for item_id, features in self.item_features.items():
            score = sum(features.get(k, 0) * v for k, v in prefs.items())
            scored.append((item_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
