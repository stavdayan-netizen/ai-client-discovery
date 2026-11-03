"""Localhost-only protections.

The application has no admin authentication yet, so it must never become reachable from other
machines. Three independent layers protect it:

1. The supported launcher (`python -m app`) refuses to bind to a non-loopback address.
2. Starting `uvicorn app.main:app --host <non-loopback>` directly fails at import time
   (best effort: it inspects the command line and the UVICORN_HOST variable).
3. Whatever the bind address, every request is checked against its TCP peer address and refused
   unless it comes from the local machine. This is the authoritative layer. It cannot be forged
   through request headers.

A Host-header allow-list is added on top, against DNS-rebinding from a web page open in the
local browser. It is not a network access control: a remote client can send any Host header.
"""

import ipaddress
from collections.abc import Mapping, Sequence

from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

ALLOWED_HOST_NAMES = frozenset({"localhost", "127.0.0.1", "[::1]"})

SECURITY_HEADERS = {
    "content-security-policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
        "font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; "
        "form-action 'self'; frame-ancestors 'none'"
    ),
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
    "x-frame-options": "DENY",
}


class UnsafeBindError(RuntimeError):
    """Raised when the server would listen on a non-loopback address."""


def is_loopback_address(value: str) -> bool:
    """True for IPv4/IPv6 loopback addresses (including IPv4-mapped IPv6)."""
    candidate = value.strip().strip("[]")
    try:
        address = ipaddress.ip_address(candidate)
    except ValueError:
        return False
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    return address.is_loopback


def is_loopback_host(host: str) -> bool:
    """True for a bind host that is `localhost` or a loopback IP address."""
    return host.strip().lower() == "localhost" or is_loopback_address(host)


def ensure_loopback_bind(host: str) -> None:
    if not is_loopback_host(host):
        raise UnsafeBindError(
            f"Refusing to listen on {host!r}: the application has no authentication and may only "
            "listen on a loopback address (127.0.0.1, ::1 or localhost)."
        )


def requested_bind_host(argv: Sequence[str], environ: Mapping[str, str]) -> str | None:
    """Best-effort: the bind host a `uvicorn` command line or UVICORN_HOST asks for."""
    host = environ.get("UVICORN_HOST") or None
    args = list(argv)
    for index, arg in enumerate(args):
        if arg == "--host" and index + 1 < len(args):
            host = args[index + 1]
        elif arg.startswith("--host="):
            host = arg.partition("=")[2]
    return host


def split_host_header(value: str) -> str:
    """Host name part of a Host header, without the port, lowercased."""
    value = value.strip().lower()
    if value.startswith("["):
        end = value.find("]")
        return value[: end + 1] if end != -1 else value
    if value.count(":") == 1:
        return value.partition(":")[0]
    return value


class LoopbackOnlyMiddleware:
    """Refuse requests whose TCP peer is not the local machine (authoritative layer)."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            client = scope.get("client")
            # `client` is None for Unix sockets, which are local by definition.
            if client is not None and not is_loopback_address(client[0]):
                await _refuse(scope, receive, send, 403, "Forbidden: local access only.")
                return
        await self.app(scope, receive, send)


class HostHeaderMiddleware:
    """Allow only localhost-style Host headers (DNS-rebinding defense)."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope.get("headers", []))
            raw = headers.get(b"host", b"").decode("latin-1")
            if split_host_header(raw) not in ALLOWED_HOST_NAMES:
                await _refuse(scope, receive, send, 400, "Invalid host header.")
                return
        await self.app(scope, receive, send)


class SecurityHeadersMiddleware:
    """Add the restrictive response headers from architecture.md section 9.1."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                present = {name.lower() for name, _ in headers}
                for name, value in SECURITY_HEADERS.items():
                    if name.encode() not in present:
                        headers.append((name.encode(), value.encode()))
                message = {**message, "headers": headers}
            await send(message)

        await self.app(scope, receive, send_with_headers)


async def _refuse(scope: Scope, receive: Receive, send: Send, status: int, text: str) -> None:
    if scope["type"] == "websocket":
        await send({"type": "websocket.close", "code": 1008})
        return
    await PlainTextResponse(text, status_code=status)(scope, receive, send)
