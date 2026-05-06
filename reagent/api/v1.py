"""v1 API router — aggregates all module routes under /api/v1."""

from __future__ import annotations

from fastapi import APIRouter

from reagent.api.ai_routes import router as ai_router
from reagent.api.content_routes import router as content_router
from reagent.api.profile_routes import router as profile_router
from reagent.api.automation_routes import router as automation_router

v1_router = APIRouter(prefix="/api/v1")

# Sub-routers (each has its own prefix)
v1_router.include_router(ai_router)
v1_router.include_router(content_router)
v1_router.include_router(profile_router)
v1_router.include_router(automation_router)


@v1_router.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "2.0.0",
        "service": "ReAgent",
    }
