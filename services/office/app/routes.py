from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, status

from shared.logging import get_logger
from shared.security import require_roles

from .schemas import AccountLifecycleResponse, CreateClientRequest, CreateEmployeeRequest, EmployeeResponse

public_router = APIRouter(prefix="/api/office", tags=["office"], include_in_schema=False)
router = APIRouter(
    prefix="/api/office",
    tags=["office"],
    dependencies=[Depends(require_roles("office", "admin"))],
)
_logger = get_logger()


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "office"}


@router.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
async def create_employee(payload: CreateEmployeeRequest) -> EmployeeResponse:
    employee_id = str(uuid4())
    _logger.info("employee.created", employee_id=employee_id, role=payload.role)
    return EmployeeResponse(
        id=employee_id,
        email=payload.email,
        role=payload.role,
        created_at=datetime.now(tz=timezone.utc),
    )


@router.post("/users", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_client(payload: CreateClientRequest) -> EmployeeResponse:
    client_id = str(uuid4())
    _logger.info("customer.created", user_id=client_id)
    return EmployeeResponse(
        id=client_id,
        email=payload.email,
        role="customer",
        created_at=datetime.now(tz=timezone.utc),
    )


@router.post("/accounts/{user_id}/open", response_model=AccountLifecycleResponse)
async def open_account(user_id: str) -> AccountLifecycleResponse:
    account_id = str(uuid4())
    _logger.info("account.opened", account_id=account_id, user_id=user_id)
    return AccountLifecycleResponse(
        account_id=account_id,
        status="opened",
        processed_at=datetime.now(tz=timezone.utc),
    )


@router.post("/accounts/{account_id}/close", response_model=AccountLifecycleResponse)
async def close_account(account_id: str) -> AccountLifecycleResponse:
    _logger.info("account.closed", account_id=account_id)
    return AccountLifecycleResponse(
        account_id=account_id,
        status="closed",
        processed_at=datetime.now(tz=timezone.utc),
    )


routers = [public_router, router]
