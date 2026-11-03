"""Supported local launcher: `python -m app`."""

import sys

from app.config import load_settings
from app.network import UnsafeBindError, ensure_loopback_bind


def main() -> int:
    try:
        settings = load_settings()
        ensure_loopback_bind(settings.host)
    except (UnsafeBindError, ValueError) as error:
        print(f"Cannot start: {error}", file=sys.stderr)
        return 2

    import uvicorn

    from app.main import create_app

    # proxy_headers=False: the client address must be the real TCP peer, never a header value.
    uvicorn.run(
        create_app(settings),
        host=settings.host,
        port=settings.port,
        proxy_headers=False,
        server_header=False,
    )
    return 0
