from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr


class CreateEmployeeRequest(BaseModel):
    email: EmailStr
    phone: str
    role: str = "office"


class CreateClientRequest(BaseModel):
    email: EmailStr
    phone: str


class AccountLifecycleResponse(BaseModel):
    account_id: str
    status: str
    processed_at: datetime


class EmployeeResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    created_at: datetime
