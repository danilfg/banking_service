from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends

from shared.security import get_current_user

from .schemas import PayRequest, PayResponse, ProviderResponse

public_router = APIRouter(prefix="/api/utilities", tags=["utilities"], include_in_schema=False)
router = APIRouter(prefix="/api/utilities", tags=["utilities"], dependencies=[Depends(get_current_user)])

_PROVIDERS = [
    ProviderResponse(id="prov_water", name="Городские водоканалы", code="WATER", category="water"),
    ProviderResponse(id="prov_energy", name="Электроснабжение", code="ENERGY", category="energy"),
]


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "utilities"}


@router.get("/providers", response_model=list[ProviderResponse])
async def providers() -> list[ProviderResponse]:
    return _PROVIDERS


@router.post("/pay", response_model=PayResponse)
async def pay(payload: PayRequest) -> PayResponse:
    return PayResponse(status="executed", payment_id=str(uuid4()), processed_at=datetime.now(tz=timezone.utc))


routers = [public_router, router]
