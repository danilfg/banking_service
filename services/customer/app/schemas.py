from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountSummary(BaseModel):
    id: str
    currency: str
    balance: Decimal


class DashboardResponse(BaseModel):
    accounts: list[AccountSummary]
    recent_transactions: list[dict]


class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: Decimal
    currency: str
    description: str | None = None


class FxExchangeRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: Decimal


class FxExchangeResponse(BaseModel):
    rate: Decimal
    amount_debited: Decimal
    amount_credited: Decimal
    executed_at: datetime


class UtilityPaymentRequest(BaseModel):
    provider_code: str
    personal_account: str
    amount: Decimal
    currency: str


class UtilityPaymentResponse(BaseModel):
    status: str
    transaction_id: str
    paid_at: datetime
