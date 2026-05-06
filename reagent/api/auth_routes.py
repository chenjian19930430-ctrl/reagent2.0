"""Authentication API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from reagent.api.auth import create_jwt_token, LoginRequest, LoginResponse

# Simple user store for Phase 1
# Can be replaced with database-backed user management later
_USERS: dict[str, str] = {
    "admin": "admin123",  # Default admin user
}

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token."""
    password = _USERS.get(request.username)
    if password is None or password != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_jwt_token(user_id=request.username)
    return LoginResponse(
        access_token=token,
        user_id=request.username,
    )
