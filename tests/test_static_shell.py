import re
from pathlib import Path

import pytest

STATIC_DIR = Path(__file__).resolve().parents[1] / "app" / "static"
CHECKED_SUFFIXES = {".html", ".css", ".js"}  # license/readme text files may mention URLs
EXTERNAL_URL = re.compile(r"(?:https?:)?//[a-z0-9.-]+\.[a-z]{2,}", re.IGNORECASE)


def test_health_route(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shell_is_hebrew_rtl_and_mobile_ready(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    html = response.text
    assert 'lang="he"' in html
    assert 'dir="rtl"' in html
    assert 'name="viewport"' in html


def test_font_is_served_locally(client):
    css = client.get("/static/css/tokens.css").text
    assert 'font-family: "Heebo"' in css
    assert "/static/fonts/Heebo-Variable.ttf" in css
    font = client.get("/static/fonts/Heebo-Variable.ttf")
    assert font.status_code == 200
    assert font.content[:4] == b"\x00\x01\x00\x00"  # TrueType
    assert (STATIC_DIR / "fonts" / "OFL.txt").is_file()


def test_no_external_urls_in_served_assets(client):
    for path in STATIC_DIR.rglob("*"):
        if path.suffix in CHECKED_SUFFIXES:
            text = path.read_text(encoding="utf-8")
            assert not EXTERNAL_URL.search(text), f"external URL in {path}"
    served = client.get("/").text + client.get("/static/css/tokens.css").text
    assert not EXTERNAL_URL.search(served)
    assert "@import" not in served


@pytest.mark.parametrize("path", ["/", "/healthz", "/static/css/base.css", "/does-not-exist"])
def test_security_headers_are_present(client, path):
    headers = client.get(path).headers
    assert "default-src 'self'" in headers["content-security-policy"]
    assert "script-src 'self'" in headers["content-security-policy"]
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["referrer-policy"] == "no-referrer"
    assert headers["x-frame-options"] == "DENY"


def test_refusals_also_carry_security_headers(client):
    response = client.get("/healthz", headers={"Host": "evil.example"})
    assert response.status_code == 400
    assert response.headers["x-content-type-options"] == "nosniff"


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_interactive_docs_that_load_cdn_scripts_are_disabled(client, path):
    assert client.get(path).status_code == 404
