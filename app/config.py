"""Settings loaded from environment variables and an optional local .env file."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "app.db"
SUPPORTED_AI_PROVIDERS = ("mock",)


@dataclass(frozen=True)
class Settings:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    database_path: Path = DEFAULT_DATABASE_PATH
    ai_provider: str = "mock"


def read_env_file(path: Path) -> dict[str, str]:
    """Parse simple KEY=VALUE lines. Blank lines, comments and empty values are ignored."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and value:
            values[key] = value
    return values


def load_settings(
    environ: Mapping[str, str] | None = None, env_file: Path | None = None
) -> Settings:
    """Environment variables override the .env file; both override the defaults."""
    environ = os.environ if environ is None else environ
    merged = read_env_file(PROJECT_ROOT / ".env" if env_file is None else env_file)
    merged.update({k: v for k, v in environ.items() if v})

    ai_provider = merged.get("AI_PROVIDER", "mock")
    if ai_provider not in SUPPORTED_AI_PROVIDERS:
        raise ValueError(
            f"AI_PROVIDER={ai_provider!r} is not available. Only {SUPPORTED_AI_PROVIDERS} "
            "is supported; a real provider needs explicit owner approval."
        )
    database_path = merged.get("DATABASE_PATH")
    return Settings(
        host=merged.get("HOST", DEFAULT_HOST),
        port=int(merged.get("PORT", DEFAULT_PORT)),
        database_path=Path(database_path) if database_path else DEFAULT_DATABASE_PATH,
        ai_provider=ai_provider,
    )
