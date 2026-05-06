"""JWT Authentication module for ReAgent API."""

from __future__ import annotations

import time
from typing import Optional

import jwt
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from reagent.shared.config import settings


def create_jwt_token(user_id: str, role: str = "user") -> str:
    """Create a JWT access token."""
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,  # 7 days
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_jwt_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def jwt_auth_middleware(request: Request, call_next):
    """FastAPI middleware for JWT authentication.

    Public endpoints (no auth required):
    - /docs, /redoc, /openapi.json
    - /api/v1/health
    - /api/v1/auth/login
    """
    # Skip auth for public endpoints
    public_prefixes = ("/docs", "/redoc", "/openapi.json", "/api/v1/health", "/api/v1/auth")

    path = request.url.path
    if any(path.startswith(prefix) for prefix in public_prefixes):
        return await call_next(request)

    # Extract and validate token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing or invalid Authorization header"},
        )

    token = auth_header.removeprefix("Bearer ")
    try:
        payload = decode_jwt_token(token)
        request.state.user_id = payload.get("sub")
        request.state.user_role = payload.get("role", "user")
    except HTTPException:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or expired token"},
        )

    return await call_next(request)


class LoginRequest(BaseModel):
    """Login request payload."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response with JWT token."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
