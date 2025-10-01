from __future__ import annotations

import os
from uuid import uuid4

import httpx
from fastapi import APIRouter, HTTPException, Request, Response

router = APIRouter(prefix="/api", tags=["gateway"])

_ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
_SERVICE_DEFAULTS: dict[str, str] = {
    "auth": "http://auth:8001",
    "customer": "http://customer:8002",
    "office": "http://office:8003",
    "accounts": "http://accounts:8004",
    "ledger": "http://ledger:8005",
    "fx": "http://fx:8006",
    "utilities": "http://utilities:8007",
    "contracts": "http://contracts:8008",
    "notifications": "http://notifications:8009",
}


def _load_service_map() -> dict[str, str]:
    services: dict[str, str] = {}
    for name, default in _SERVICE_DEFAULTS.items():
        env_key = f"UPSTREAM_{name.upper()}_URL"
        services[name] = os.getenv(env_key, default).rstrip("/")
    return services


_SERVICE_MAP = _load_service_map()


@router.get("/health", summary="Health check")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "gateway"}


@router.get("/services", summary="Registered upstream services")
async def services() -> dict[str, dict[str, str]]:
    return {"services": _SERVICE_MAP}


@router.api_route("/{service}", methods=_ALLOWED_METHODS)
@router.api_route("/{service}/{path:path}", methods=_ALLOWED_METHODS)
async def proxy(service: str, request: Request, path: str | None = None) -> Response:
    upstream_base = _SERVICE_MAP.get(service)
    if upstream_base is None:
        raise HTTPException(status_code=404, detail="Unknown upstream service")

    upstream_path = f"{upstream_base}/api/{service}"
    if path:
        upstream_path = f"{upstream_path}/{path}"

    client: httpx.AsyncClient = request.app.state.http_client
    body = await request.body()
    headers = {key: value for key, value in request.headers.items() if key.lower() != "host"}

    correlation_id = headers.get("X-Request-Id") or str(uuid4())
    headers["X-Request-Id"] = correlation_id

    upstream_response = await client.request(
        request.method,
        upstream_path,
        params=request.query_params,
        headers=headers,
        content=body,
    )

    excluded = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {
        key: value for key, value in upstream_response.headers.items() if key.lower() not in excluded
    }
    response_headers["X-Request-Id"] = correlation_id

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=response_headers,
        media_type=upstream_response.headers.get("content-type"),
    )
