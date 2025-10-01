from __future__ import annotations

from typing import Any, Awaitable, Callable, Coroutine

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import load_settings
from .logging import configure_logging, get_logger


def create_app(name: str, routers: list[APIRouter], lifespan: Callable[[FastAPI], Awaitable[Callable[[], Coroutine[Any, Any, None]]]] | None = None) -> FastAPI:
    settings = load_settings()
    configure_logging(name)

    app = FastAPI(title=f"{name.title()} Service", lifespan=lifespan)
    app.state.logger = get_logger()

    for router in routers:
        app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
