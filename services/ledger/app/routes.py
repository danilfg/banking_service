from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, Query, status

from shared.logging import get_logger
from shared.security import get_current_user

from .schemas import LedgerEntry, TopupRequest, TransactionResponse, TransactionsListResponse, TransferRequest

public_router = APIRouter(prefix="/api/ledger", tags=["ledger"], include_in_schema=False)
router = APIRouter(prefix="/api/ledger", tags=["ledger"], dependencies=[Depends(get_current_user)])
_logger = get_logger()

_transactions: dict[str, list[TransactionResponse]] = {}
_entries: list[LedgerEntry] = []


def _append_transaction(account_id: str, tx: TransactionResponse) -> None:
    _transactions.setdefault(account_id, []).append(tx)


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "ledger"}


@router.post("/topup", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def topup(payload: TopupRequest) -> TransactionResponse:
    transaction = TransactionResponse(
        transaction_id=str(uuid4()),
        type="topup",
        status="executed",
        created_at=datetime.now(tz=timezone.utc),
    )
    _append_transaction(payload.account_id, transaction)
    _entries.append(
        LedgerEntry(
            entry_id=str(uuid4()),
            account_id=payload.account_id,
            amount=payload.amount,
            currency=payload.currency,
            created_at=transaction.created_at,
        )
    )
    _logger.info("payment.executed", transaction_id=transaction.transaction_id, account_id=payload.account_id)
    return transaction


@router.post("/transfer", response_model=TransactionResponse)
async def transfer(payload: TransferRequest) -> TransactionResponse:
    transaction = TransactionResponse(
        transaction_id=str(uuid4()),
        type="transfer",
        status="executed",
        created_at=datetime.now(tz=timezone.utc),
    )
    _append_transaction(payload.from_account, transaction)
    _append_transaction(payload.to_account, transaction)
    _logger.info("payment.executed", transaction_id=transaction.transaction_id)
    return transaction


@router.get("/transactions", response_model=TransactionsListResponse)
async def transactions(account_id: str = Query(...)) -> TransactionsListResponse:
    return TransactionsListResponse(account_id=account_id, transactions=_transactions.get(account_id, []))


routers = [public_router, router]
