"""FastAPI application factory."""

import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR, Settings, load_settings
from app.db import connect, migrate
from app.network import (
    HostHeaderMiddleware,
    LoopbackOnlyMiddleware,
    SecurityHeadersMiddleware,
    ensure_loopback_bind,
    requested_bind_host,
)

STATIC_DIR = BASE_DIR / "static"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or load_settings()
    ensure_loopback_bind(settings.host)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        conn = connect(settings.database_path)
        try:
            migrate(conn)
        finally:
            conn.close()
        yield

    # The interactive API docs load scripts from a CDN, which the CSP and the "no external
    # requests" rule forbid, so they are disabled.
    app = FastAPI(
        title="AI Client Discovery",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    app.state.settings = settings

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        conn = connect(settings.database_path)
        try:
            conn.execute("SELECT 1").fetchone()
        finally:
            conn.close()
        return {"status": "ok"}

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html", media_type="text/html; charset=utf-8")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # Added innermost first: the last one added is the outermost layer.
    app.add_middleware(LoopbackOnlyMiddleware)
    app.add_middleware(HostHeaderMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    return app


def _create_default_app() -> FastAPI:
    # `uvicorn app.main:app --host 0.0.0.0` would bypass the launcher's check, so the command line
    # is inspected here too (best effort). The per-request peer-address check still applies.
    requested = requested_bind_host(sys.argv, os.environ)
    if requested is not None:
        ensure_loopback_bind(requested)
    return create_app()


app = _create_default_app()
