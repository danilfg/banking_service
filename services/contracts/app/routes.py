from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, status

from shared.security import require_roles

from .schemas import ContractCreateRequest, ContractResponse, ContractTemplate

public_router = APIRouter(prefix="/api/contracts", tags=["contracts"], include_in_schema=False)
router = APIRouter(
    prefix="/api/contracts",
    tags=["contracts"],
    dependencies=[Depends(require_roles("office", "admin"))],
)

_TEMPLATES = [
    ContractTemplate(id="tpl_standard", template_name="Standard Banking", version="1.0", effective_from=datetime.now(tz=timezone.utc)),
]
_CONTRACTS: dict[str, ContractResponse] = {}


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "contracts"}


@router.get("/templates", response_model=list[ContractTemplate])
async def templates() -> list[ContractTemplate]:
    return _TEMPLATES


@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(payload: ContractCreateRequest) -> ContractResponse:
    contract_id = str(uuid4())
    contract = ContractResponse(
        id=contract_id,
        user_id=payload.user_id,
        status="draft",
        product_code=payload.product_code,
        signed_at=None,
        version_id=payload.template_id,
    )
    _CONTRACTS[contract_id] = contract
    return contract


@router.post("/{contract_id}/activate", response_model=ContractResponse)
async def activate_contract(contract_id: str) -> ContractResponse:
    contract = _CONTRACTS[contract_id]
    updated = contract.model_copy(update={"status": "active", "signed_at": datetime.now(tz=timezone.utc)})
    _CONTRACTS[contract_id] = updated
    return updated


routers = [public_router, router]
