from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TopupRequest(BaseModel):
    account_id: str
    amount: Decimal
    currency: str
    source: str


class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: Decimal
    currency: str
    reference: str | None = None


class TransactionResponse(BaseModel):
    transaction_id: str
    type: str
    status: str
    created_at: datetime


class LedgerEntry(BaseModel):
    entry_id: str
    account_id: str
    amount: Decimal
    currency: str
    created_at: datetime


class TransactionsListResponse(BaseModel):
    account_id: str
    transactions: list[TransactionResponse]
