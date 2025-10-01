from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProviderResponse(BaseModel):
    id: str
    name: str
    code: str
    category: str


class PayRequest(BaseModel):
    provider_code: str
    personal_account: str
    amount: Decimal
    currency: str


class PayResponse(BaseModel):
    status: str
    payment_id: str
    processed_at: datetime
