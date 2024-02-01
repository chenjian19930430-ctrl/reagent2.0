"""Collaborative filtering engine."""
import numpy as np
from typing import List, Tuple


class CollaborativeFilter:
    """Collaborative filtering using matrix factorization."""
    
    def __init__(self, n_factors: int = 20):
        self.n_factors = n_factors
        self.user_factors: np.ndarray = np.array([])
        self.item_factors: np.ndarray = np.array([])
    
    def fit(self, ratings_matrix: np.ndarray, n_epochs: int = 50, lr: float = 0.01):
        n_users, n_items = ratings_matrix.shape
        self.user_factors = np.random.normal(0, 0.1, (n_users, self.n_factors))
        self.item_factors = np.random.normal(0, 0.1, (n_items, self.n_factors))
        
        for epoch in range(n_epochs):
            for u in range(n_users):
                for i in range(n_items):
                    if ratings_matrix[u, i] > 0:
                        pred = np.dot(self.user_factors[u], self.item_factors[i])
                        err = ratings_matrix[u, i] - pred
                        self.user_factors[u] += lr * (err * self.item_factors[i] - 0.02 * self.user_factors[u])
                        self.item_factors[i] += lr * (err * self.user_factors[u] - 0.02 * self.item_factors[i])
        
        return self
    
    def predict(self, user_id: int, item_id: int) -> float:
        return float(np.dot(self.user_factors[user_id], self.item_factors[item_id]))
    
    def recommend(self, user_id: int, item_ids: List[int], top_k: int = 10) -> List[Tuple[int, float]]:
        scores = [(iid, self.predict(user_id, iid)) for iid in item_ids]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
