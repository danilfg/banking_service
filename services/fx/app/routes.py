from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import httpx
from fastapi import APIRouter, Depends, Query

from shared.logging import get_logger
from shared.security import get_current_user

from .schemas import ExchangeRequest, ExchangeResponse, RatesResponse

public_router = APIRouter(prefix="/api/fx", tags=["fx"], include_in_schema=False)
router = APIRouter(prefix="/api/fx", tags=["fx"], dependencies=[Depends(get_current_user)])
_logger = get_logger()

_CACHE: dict[str, RatesResponse] = {}
_CACHE_TTL: dict[str, datetime] = {}
_TTL_SECONDS = 86400
_FRANKFURTER_URL = "https://api.frankfurter.dev/latest"


def _cache_key(base: str, symbols: list[str]) -> str:
    symbols_sorted = ",".join(sorted(symbols))
    return f"fx:latest:{base}:{symbols_sorted}"


@public_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "fx"}


async def _fetch_from_provider(base: str, symbols: list[str]) -> dict[str, Decimal]:
    params = {"base": base, "symbols": ",".join(symbols)}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(_FRANKFURTER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {currency: Decimal(str(rate)) for currency, rate in data.get("rates", {}).items()}


@router.get("/rates/latest", response_model=RatesResponse)
async def latest_rates(base: str = Query("USD"), symbols: str = Query("EUR,GBP")) -> RatesResponse:
    requested_symbols = [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]
    key = _cache_key(base.upper(), requested_symbols)
    now = datetime.now(tz=timezone.utc)

    cached = _CACHE.get(key)
    expires_at = _CACHE_TTL.get(key)
    if cached and expires_at and expires_at > now:
        return cached

    try:
        rates = await _fetch_from_provider(base.upper(), requested_symbols)
        source = "redis" if cached else "frankfurter"
    except Exception as exc:  # noqa: BLE001
        _logger.error("fx.rate_fetch_failed", error=str(exc))
        if cached:
            return cached
        rates = {symbol: Decimal("1") for symbol in requested_symbols}
        source = "fallback"

    response = RatesResponse(base=base.upper(), rates=rates, as_of=now, source=source)
    _CACHE[key] = response
    _CACHE_TTL[key] = now + timedelta(seconds=_TTL_SECONDS)
    return response


@router.post("/exchange", response_model=ExchangeResponse)
async def exchange(payload: ExchangeRequest) -> ExchangeResponse:
    rates = await latest_rates(base=payload.from_currency, symbols=payload.to_currency)
    rate = rates.rates.get(payload.to_currency.upper()) or Decimal("1")
    amount_credited = payload.amount * rate
    executed_at = datetime.now(tz=timezone.utc)
    _logger.info(
        "fx.exchanged",
        from_currency=payload.from_currency,
        to_currency=payload.to_currency,
        amount=str(payload.amount),
        rate=str(rate),
    )
    return ExchangeResponse(
        rate=rate,
        amount_debited=payload.amount,
        amount_credited=amount_credited,
        executed_at=executed_at,
    )


routers = [public_router, router]
