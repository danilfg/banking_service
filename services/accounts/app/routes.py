from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException

from shared.security import get_current_user

from .schemas import AccountDetailsResponse, AccountResponse, CardResponse

public_router = APIRouter(prefix="/api/accounts", tags=["accounts"], include_in_schema=False)
router = APIRouter(prefix="/api/accounts", tags=["accounts"], dependencies=[Depends(get_current_user)])

_fake_accounts = {
    "acc_demo_1": AccountDetailsResponse(
        id="acc_demo_1",
        user_id="user-demo",
        currency="RUB",
        iban="RU00DEMO0000000001",
        status="active",
        balance=Decimal("100000.00"),
        created_at=datetime.now(tz=timezone.utc),
        cards=[
            CardResponse(
                id="card_demo_1",
                account_id="acc_demo_1",
                pan_masked="4111 **** **** 1111",
                status="active",
                created_at=datetime.now(tz=timezone.utc),
            )
        ],
    )
}


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "accounts"}


@router.get("/my", response_model=list[AccountResponse])
async def my_accounts() -> list[AccountResponse]:
    return [AccountResponse(**acc.model_dump(exclude={"cards"})) for acc in _fake_accounts.values()]


@router.get("/{account_id}", response_model=AccountDetailsResponse)
async def account_details(account_id: str) -> AccountDetailsResponse:
    account = _fake_accounts.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


routers = [public_router, router]
