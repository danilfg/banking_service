from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class RatesQuery(BaseModel):
    base: str
    symbols: list[str]


class RatesResponse(BaseModel):
    base: str
    rates: dict[str, Decimal]
    as_of: datetime
    source: str


class ExchangeRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: Decimal


class ExchangeResponse(BaseModel):
    rate: Decimal
    amount_debited: Decimal
    amount_credited: Decimal
    executed_at: datetime
