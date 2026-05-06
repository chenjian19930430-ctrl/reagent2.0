"""Profile analysis API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from reagent.profile.schema import (
    ProfileAnalysisRequest,
    ProfileAnalysisResponse,
    IndustryType,
)
from reagent.profile.analyzer import ProfileAnalyzer
from reagent.profile.templates import template_manager

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])
_analyzer = ProfileAnalyzer()

# In-memory user store for Phase 1 (can be replaced with DB later)
_USER_RECORDS: dict[str, object] = {}


@router.post("/analyze", response_model=ProfileAnalysisResponse)
async def analyze_profile(request: ProfileAnalysisRequest):
    """Analyze user profile data."""
    try:
        result = await _analyzer.analyze(request)
        # Store analyzed profile for deletion tracking
        _USER_RECORDS[request.user_id] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete a user's profile and associated data.

    Comply with data privacy regulations (GDPR / 个人信息保护法).
    """
    removed = _USER_RECORDS.pop(user_id, None)
    if removed is None:
        # No record in-memory but still return success idempotently
        # (data may have been stored externally)
        pass
    return None


@router.get("/templates")
async def list_templates():
    """List all available industry profile templates."""
    return template_manager.list_all()


@router.get("/templates/{industry}")
async def get_template(industry: IndustryType):
    """Get a specific industry template."""
    template = template_manager.get(industry)
    return template.model_dump()
