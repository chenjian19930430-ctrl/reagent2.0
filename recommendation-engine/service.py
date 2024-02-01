"""Recommendation engine service."""
from typing import Optional, List
from .models import RecommendationContext, RecommendationResponse, RecommendationItem
from .hybrid import HybridRecommender


class RecommendationService:
    def __init__(self, recommender: Optional[HybridRecommender] = None):
        self.recommender = recommender or HybridRecommender()
    
    def get_recommendations(self, ctx: RecommendationContext) -> RecommendationResponse:
        results = self.recommender.recommend(ctx.customer_id, ctx.limit)
        items = [
            RecommendationItem(
                id=r["item_id"],
                title=f"Recommendation {i+1}",
                description="AI-driven recommendation",
                score=r["score"],
                reason=r["source"],
                category="default"
            )
            for i, r in enumerate(results)
        ]
        return RecommendationResponse(
            items=items,
            total=len(items),
            context_id=ctx.customer_id,
            generated_at=__import__('datetime').datetime.utcnow()
        )
