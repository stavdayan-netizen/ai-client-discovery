"""SQLite access and the numbered-SQL migration runner."""

import re
import sqlite3
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
_MIGRATION_NAME = re.compile(r"^(\d{4})_[a-z0-9_]+\.sql$")


def utc_now() -> str:
    """UTC timestamp as ISO-8601 text, the storage format for every timestamp."""
    return datetime.now(UTC).isoformat(timespec="seconds")


def new_id() -> str:
    """Opaque unique ID (uuid4 hex)."""
    return uuid.uuid4().hex


def connect(path: Path | str) -> sqlite3.Connection:
    """Open a connection with foreign keys on. Transactions are explicit (see `transaction`)."""
    location = str(path)
    if location != ":memory:":
        Path(location).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(location, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    if location != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Run a block in one write transaction: commit on success, roll back on any error."""
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")


def migration_files() -> list[Path]:
    files = sorted(p for p in MIGRATIONS_DIR.iterdir() if p.suffix == ".sql")
    for file in files:
        if not _MIGRATION_NAME.match(file.name):
            raise ValueError(f"Bad migration file name: {file.name} (expected NNNN_name.sql)")
    return files


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Apply every migration not yet applied, each in its own transaction. Returns their names."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations ("
        "version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)"
    )
    applied = {row["version"] for row in conn.execute("SELECT version FROM schema_migrations")}
    newly_applied: list[str] = []
    for file in migration_files():
        if file.name in applied:
            continue
        script = file.read_text(encoding="utf-8")
        try:
            conn.executescript(
                "BEGIN IMMEDIATE;\n"
                + script
                + f"\nINSERT INTO schema_migrations (version, applied_at) "
                f"VALUES ('{file.name}', '{utc_now()}');\nCOMMIT;"
            )
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        newly_applied.append(file.name)
    return newly_applied
