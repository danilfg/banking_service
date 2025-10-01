from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ContractTemplate(BaseModel):
    id: str
    template_name: str
    version: str
    effective_from: datetime


class ContractResponse(BaseModel):
    id: str
    user_id: str
    status: str
    product_code: str
    signed_at: datetime | None
    version_id: str


class ContractCreateRequest(BaseModel):
    user_id: str
    product_code: str
    template_id: str
