import sqlite3
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.db import connect, migrate
from app.main import create_app


@pytest.fixture
def settings(tmp_path) -> Settings:
    return Settings(database_path=tmp_path / "test.db")


@pytest.fixture
def client(settings) -> Iterator[TestClient]:
    """A client that looks like a local browser: loopback peer address and a localhost Host."""
    app = create_app(settings)
    with TestClient(app, base_url="http://localhost:8000", client=("127.0.0.1", 50000)) as c:
        yield c


@pytest.fixture
def conn(tmp_path) -> Iterator[sqlite3.Connection]:
    connection = connect(tmp_path / "schema.db")
    migrate(connection)
    yield connection
    connection.close()
