from __future__ import annotations

from fastapi import FastAPI

from shared.api import create_app

from .routes import router


def build_app() -> FastAPI:
    return create_app("auth", [router])


app = build_app()
