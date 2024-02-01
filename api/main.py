"""ReAgent API entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from customer_profile.api import router as profile_router
from recommendation_engine.api import router as rec_router
from marketing_automation.api import router as auto_router
from analytics_dashboard.api import router as analytics_router
from shared.config import settings
from shared.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI Marketing System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(rec_router)
app.include_router(auto_router)
app.include_router(analytics_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
