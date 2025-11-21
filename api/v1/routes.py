"""API v1 routes for the banking service."""

from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> Dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
