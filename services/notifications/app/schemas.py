from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr


class NotificationRequest(BaseModel):
    channel: str
    recipient: EmailStr
    subject: str
    body: str


class NotificationResponse(BaseModel):
    notification_id: str
    status: str
    created_at: datetime
