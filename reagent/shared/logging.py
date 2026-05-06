"""Logging configuration."""

from __future__ import annotations

import sys

from loguru import logger
from reagent.shared.config import settings


def setup_logging() -> None:
    """Configure Loguru for the application."""
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:^8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    )
    logger.add(
        "logs/reagent_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level="DEBUG",
        format="{time} | {level:^8} | {name}:{function}:{line} | {message}",
    )
    logger.info(f"🚀 {settings.app_name} v2.0.0 — logging initialized")
