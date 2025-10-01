from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: str
    user_id: str
    currency: str
    iban: str
    status: str
    balance: Decimal
    created_at: datetime


class CardResponse(BaseModel):
    id: str
    account_id: str
    pan_masked: str
    status: str
    created_at: datetime


class AccountDetailsResponse(AccountResponse):
    cards: list[CardResponse]
