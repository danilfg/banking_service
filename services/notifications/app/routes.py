from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends

from shared.logging import get_logger
from shared.security import require_roles

from .schemas import NotificationRequest, NotificationResponse

public_router = APIRouter(prefix="/api/notifications", tags=["notifications"], include_in_schema=False)
router = APIRouter(
    prefix="/api/notifications",
    tags=["notifications"],
    dependencies=[Depends(require_roles("office", "admin"))],
)
_logger = get_logger()


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "notifications"}


@router.post("/send", response_model=NotificationResponse)
async def send(payload: NotificationRequest) -> NotificationResponse:
    notification_id = str(uuid4())
    _logger.info("notification.sent", notification_id=notification_id, channel=payload.channel)
    return NotificationResponse(notification_id=notification_id, status="queued", created_at=datetime.now(tz=timezone.utc))


routers = [public_router, router]
