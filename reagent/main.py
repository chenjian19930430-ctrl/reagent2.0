"""ReAgent · 智能营销AI平台 — FastAPI 应用入口"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from reagent.shared.config import settings
from reagent.shared.errors import ReAgentError
from reagent.shared.logging import setup_logging
from reagent.api.v1 import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup/shutdown."""
    logger.info(f"🚀 {settings.app_name} v2.0.0 starting up...")
    logger.info(f"   Debug mode: {settings.debug}")
    logger.info(f"   API prefix: {settings.api_prefix}")
    logger.info(f"   Database:   {settings.database_url}")
    logger.info(f"   AI default: {settings.ai_default_provider}/{settings.openai_default_model}")
    yield
    logger.info(f"🛑 {settings.app_name} shutting down...")


def create_app() -> FastAPI:
    """Factory: create and configure the FastAPI application."""
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        version="2.0.0",
        description="ReAgent · 智能营销AI平台 — AI内容生成、用户画像分析、营销自动化编排",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(v1_router)

    # Global exception handlers
    @app.exception_handler(ReAgentError)
    async def reagent_exception_handler(request: Request, exc: ReAgentError) -> JSONResponse:
        logger.error(f"ReAgentError [{exc.code}]: {exc.message}")
        return JSONResponse(status_code=exc.http_status, content=exc.to_dict())

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error": "INTERNAL_ERROR", "message": str(exc)},
        )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "reagent.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
