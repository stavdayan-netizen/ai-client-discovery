"""The application has no authentication, so it must only ever be reachable from this machine."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.network import (
    UnsafeBindError,
    ensure_loopback_bind,
    is_loopback_host,
    requested_bind_host,
    split_host_header,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("host", ["127.0.0.1", "::1", "[::1]", "localhost", "127.0.0.5"])
def test_loopback_hosts_are_accepted(host):
    ensure_loopback_bind(host)
    assert is_loopback_host(host)


@pytest.mark.parametrize("host", ["0.0.0.0", "::", "192.168.1.20", "10.0.0.5", "example.com", ""])
def test_non_loopback_hosts_are_refused(host):
    with pytest.raises(UnsafeBindError):
        ensure_loopback_bind(host)


def test_create_app_refuses_a_non_loopback_host(settings):
    unsafe = type(settings)(host="0.0.0.0", database_path=settings.database_path)
    with pytest.raises(UnsafeBindError):
        create_app(unsafe)


def test_requested_bind_host_reads_the_uvicorn_command_line():
    assert requested_bind_host(["uvicorn", "app.main:app", "--host", "0.0.0.0"], {}) == "0.0.0.0"
    assert requested_bind_host(["uvicorn", "app.main:app", "--host=::"], {}) == "::"
    assert (
        requested_bind_host(["uvicorn", "app.main:app"], {"UVICORN_HOST": "0.0.0.0"}) == "0.0.0.0"
    )
    assert requested_bind_host(["pytest"], {}) is None


def _run(args, extra_env):
    env = {**os.environ, **extra_env}
    return subprocess.run(
        [sys.executable, *args],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_launcher_refuses_to_start_on_a_non_loopback_host(tmp_path):
    result = _run(["-m", "app"], {"HOST": "0.0.0.0", "DATABASE_PATH": str(tmp_path / "x.db")})
    assert result.returncode == 2
    assert "Refusing to listen" in result.stderr


def test_direct_uvicorn_start_on_a_non_loopback_host_fails_fast(tmp_path):
    """The bypass path: `uvicorn app.main:app --host 0.0.0.0` must not start serving."""
    result = _run(
        ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8765"],
        {"DATABASE_PATH": str(tmp_path / "x.db")},
    )
    assert result.returncode != 0
    assert "Refusing to listen" in result.stderr


@pytest.mark.parametrize(
    "peer", ["192.168.1.20", "10.0.0.5", "203.0.113.7", "2001:db8::1", "::ffff:192.168.1.20"]
)
def test_requests_from_other_machines_are_refused_even_with_a_forged_host_header(settings, peer):
    """If someone binds to all interfaces anyway, remote peers are still refused."""
    app = create_app(settings)
    with TestClient(app, base_url="http://localhost:8000", client=(peer, 50000)) as remote:
        response = remote.get("/healthz", headers={"Host": "localhost"})
    assert response.status_code == 403


@pytest.mark.parametrize("peer", ["127.0.0.1", "127.0.0.9", "::1", "::ffff:127.0.0.1"])
def test_requests_from_the_local_machine_are_allowed(settings, peer):
    app = create_app(settings)
    with TestClient(app, base_url="http://localhost:8000", client=(peer, 50000)) as local:
        assert local.get("/healthz").status_code == 200


@pytest.mark.parametrize("host", ["localhost", "localhost:8000", "127.0.0.1:8000", "[::1]:8000"])
def test_localhost_host_headers_are_accepted(client, host):
    assert client.get("/healthz", headers={"Host": host}).status_code == 200


@pytest.mark.parametrize(
    "host", ["evil.example", "evil.example:8000", "192.168.1.20:8000", "localhost.evil.example", ""]
)
def test_foreign_host_headers_are_rejected(client, host):
    assert client.get("/healthz", headers={"Host": host}).status_code == 400


def test_split_host_header():
    assert split_host_header("LocalHost:8000") == "localhost"
    assert split_host_header("[::1]:8000") == "[::1]"
    assert split_host_header("127.0.0.1") == "127.0.0.1"
