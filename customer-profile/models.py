"""Customer profile data models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    tags: list[str] = []


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime
    profile_score: float = 0.0
    segment: str = "unknown"

    class Config:
        from_attributes = True


class ProfileEnrichment(BaseModel):
    customer_id: str
    social_profiles: dict = {}
    purchase_history: list = []
    browsing_patterns: dict = {}
    demographic_data: dict = {}
