from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, Depends, status

from shared.logging import get_logger
from shared.security import get_current_user

from .schemas import (
    DashboardResponse,
    FxExchangeRequest,
    FxExchangeResponse,
    TransferRequest,
    UtilityPaymentRequest,
    UtilityPaymentResponse,
)

public_router = APIRouter(prefix="/api/customer", tags=["customer"], include_in_schema=False)
router = APIRouter(prefix="/api/customer", tags=["customer"], dependencies=[Depends(get_current_user)])
_logger = get_logger()


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "customer"}


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard() -> DashboardResponse:
    return DashboardResponse(
        accounts=[
            {"id": "acc_demo_1", "currency": "RUB", "balance": Decimal("100000.00")},
            {"id": "acc_demo_2", "currency": "USD", "balance": Decimal("1200.50")},
        ],
        recent_transactions=[],
    )


@router.post("/transfer", status_code=status.HTTP_202_ACCEPTED)
async def transfer(payload: TransferRequest) -> dict[str, str]:
    transaction_id = str(uuid4())
    _logger.info(
        "payment.created",
        transaction_id=transaction_id,
        from_account=payload.from_account,
        to_account=payload.to_account,
        amount=str(payload.amount),
    )
    return {"transaction_id": transaction_id, "status": "queued"}


@router.post("/fx/exchange", response_model=FxExchangeResponse)
async def exchange(payload: FxExchangeRequest) -> FxExchangeResponse:
    rate = Decimal("0.010") if payload.to_currency == "USD" else Decimal("1.0")
    credited = payload.amount * rate
    _logger.info("fx.exchanged", amount=str(payload.amount), from_currency=payload.from_currency, to_currency=payload.to_currency)
    return FxExchangeResponse(
        rate=rate,
        amount_debited=payload.amount,
        amount_credited=credited,
        executed_at=datetime.now(tz=timezone.utc),
    )


@router.post("/utilities/pay", response_model=UtilityPaymentResponse)
async def pay_utility(payload: UtilityPaymentRequest) -> UtilityPaymentResponse:
    transaction_id = str(uuid4())
    _logger.info("utility.paid", transaction_id=transaction_id, provider_code=payload.provider_code)
    return UtilityPaymentResponse(
        status="executed",
        transaction_id=transaction_id,
        paid_at=datetime.now(tz=timezone.utc),
    )


routers = [public_router, router]
