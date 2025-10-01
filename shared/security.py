from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .config import load_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class TokenPayload(dict):
    sub: str
    exp: int
    roles: list[str]


def create_access_token(subject: str, roles: list[str] | None = None, expires_delta: timedelta | None = None) -> str:
    settings = load_settings()
    if roles is None:
        roles = []
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    payload: dict[str, Any] = {"sub": subject, "roles": roles, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> TokenPayload:
    settings = load_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials") from exc
    if "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return TokenPayload(payload)


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> TokenPayload:
    payload = decode_token(token)
    request.state.user = payload
    return payload


def require_roles(*roles: str):
    async def checker(payload: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if not any(role in payload.get("roles", []) for role in roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return payload

    return checker
