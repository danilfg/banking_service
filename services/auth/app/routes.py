from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from shared.logging import get_logger
from shared.security import create_access_token, get_current_user

from .schemas import ActivateRequest, LoginRequest, RegisterRequest, TokenResponse, UserProfile

router = APIRouter(prefix="/api/auth", tags=["auth"])

_fake_users: dict[str, UserProfile] = {}
_logger = get_logger()


@router.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "auth"}


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest) -> UserProfile:
    user_id = str(uuid4())
    profile = UserProfile(
        id=user_id,
        email=payload.email,
        phone=payload.phone,
        status="pending",
        roles=["customer"],
        created_at=datetime.now(tz=timezone.utc),
    )
    _fake_users[user_id] = profile
    _logger.info("user.registered", user_id=user_id)
    return profile


@router.post("/activate", response_model=UserProfile)
async def activate(payload: ActivateRequest) -> UserProfile:
    if not _fake_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_id = next(iter(_fake_users))
    profile = _fake_users[user_id]
    profile.status = "active"
    _logger.info("user.activated", user_id=user_id, token=payload.token)
    return profile


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    user = next((_user for _user in _fake_users.values() if _user.email == payload.email), None)
    if user is None or user.status != "active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.id, roles=user.roles)
    _logger.info("user.logged_in", user_id=user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserProfile)
async def me(payload=Depends(get_current_user)) -> UserProfile:
    user_id = payload["sub"]
    profile = _fake_users.get(user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile
