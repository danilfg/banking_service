from __future__ import annotations

from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from shared.api import create_app

from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=30.0) as client:
        app.state.http_client = client
        yield


def build_app() -> FastAPI:
    app = create_app("gateway", [router], lifespan=lifespan)
    return app


app = build_app()
