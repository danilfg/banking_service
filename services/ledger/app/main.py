from __future__ import annotations

from fastapi import FastAPI

from shared.api import create_app

from .routes import routers


def build_app() -> FastAPI:
    return create_app("ledger", routers)


app = build_app()
