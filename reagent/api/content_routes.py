"""Content generation API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from reagent.content.schema import (
    ContentGenerationRequest,
    ContentGenerationResponse,
    CopywritingRequest,
    CopywritingResponse,
    ContentType,
)
from reagent.content.pipeline import ContentPipeline
from reagent.content.copywriter import Copywriter

router = APIRouter(prefix="/api/v1/content", tags=["content"])

_pipeline = ContentPipeline()
_copywriter = Copywriter()


@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """End-to-end content generation (copy + banner + landing page)."""
    try:
        result = await _pipeline.run(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/copy", response_model=CopywritingResponse)
async def generate_copy(request: CopywritingRequest):
    """Generate marketing copy only."""
    try:
        result = await _copywriter.generate(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/full", response_model=ContentGenerationResponse)
async def generate_full(request: ContentGenerationRequest):
    """Full pipeline: copy + banner + landing page."""
    try:
        result = await _pipeline.generate_full(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
