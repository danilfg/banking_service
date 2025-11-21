from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> Dict[str, str]:
    return {"status": "ok"}
