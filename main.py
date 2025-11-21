"""Application entrypoint for the banking service FastAPI app."""

from typing import Dict

from fastapi import FastAPI

from api.v1.routes import router as api_router
from core.config import settings

app = FastAPI(title=settings.app_name, version=settings.api_version)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["health"])
def read_root() -> Dict[str, str]:
    """Return a minimal health payload with the app name."""
    return {"status": "ok", "app": settings.app_name}
