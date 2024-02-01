"""Customer profile service layer."""
from datetime import datetime
from typing import Optional, List
from .models import Customer, CustomerCreate
from .enricher import ProfileEnricher


class CustomerProfileService:
    """Service for managing customer profiles."""
    
    def __init__(self, enricher: Optional[ProfileEnricher] = None):
        self.enricher = enricher or ProfileEnricher()
        self._store: dict[str, Customer] = {}
    
    def create_profile(self, data: CustomerCreate) -> Customer:
        customer = Customer(
            id=f"cust_{datetime.utcnow().timestamp():.0f}",
            **data.model_dump(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        enriched = self.enricher.enrich(customer.id, data.model_dump())
        customer.profile_score = enriched.get("engagement_score", 0.0)
        customer.segment = enriched.get("computed_segment", "unknown")
        self._store[customer.id] = customer
        return customer
    
    def get_profile(self, customer_id: str) -> Optional[Customer]:
        return self._store.get(customer_id)
    
    def list_by_segment(self, segment: str) -> List[Customer]:
        return [c for c in self._store.values() if c.segment == segment]
