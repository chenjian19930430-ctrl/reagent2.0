"""Customer Profile API router."""
from fastapi import APIRouter, HTTPException
from .models import Customer, CustomerCreate
from .service import CustomerProfileService

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])
service = CustomerProfileService()


@router.post("/", response_model=Customer)
async def create_profile(data: CustomerCreate):
    return service.create_profile(data)


@router.get("/{customer_id}", response_model=Customer)
async def get_profile(customer_id: str):
    profile = service.get_profile(customer_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile


@router.get("/segment/{segment}", response_model=list[Customer])
async def list_by_segment(segment: str):
    return service.list_by_segment(segment)
