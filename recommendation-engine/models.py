"""Recommendation models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RecommendationContext(BaseModel):
    customer_id: str
    page: str
    limit: int = 10
    exclude_ids: list[str] = []


class RecommendationItem(BaseModel):
    id: str
    title: str
    description: str
    score: float
    reason: str
    category: str


class RecommendationResponse(BaseModel):
    items: list[RecommendationItem]
    total: int
    context_id: str
    generated_at: datetime
