"""Profile analysis API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from reagent.profile.schema import (
    ProfileAnalysisRequest,
    ProfileAnalysisResponse,
    IndustryType,
)
from reagent.profile.analyzer import ProfileAnalyzer
from reagent.profile.templates import template_manager

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])
_analyzer = ProfileAnalyzer()


@router.post("/analyze", response_model=ProfileAnalysisResponse)
async def analyze_profile(request: ProfileAnalysisRequest):
    """Analyze user profile data."""
    try:
        result = await _analyzer.analyze(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def list_templates():
    """List all available industry profile templates."""
    return template_manager.list_all()


@router.get("/templates/{industry}")
async def get_template(industry: IndustryType):
    """Get a specific industry template."""
    template = template_manager.get(industry)
    return template.model_dump()
