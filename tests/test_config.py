import pytest

from app.config import DEFAULT_DATABASE_PATH, load_settings, read_env_file


def test_defaults_are_local_and_mock(tmp_path):
    settings = load_settings({}, env_file=tmp_path / "missing.env")
    assert settings.host == "127.0.0.1"
    assert settings.ai_provider == "mock"
    assert settings.database_path == DEFAULT_DATABASE_PATH


def test_env_file_is_read_and_empty_values_are_ignored(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# comment\nAI_PROVIDER=\nDATABASE_PATH=/tmp/x.db\nPORT=9001\n\nBROKEN LINE\n",
        encoding="utf-8",
    )
    assert read_env_file(env_file) == {"DATABASE_PATH": "/tmp/x.db", "PORT": "9001"}
    settings = load_settings({}, env_file=env_file)
    assert settings.port == 9001
    assert settings.ai_provider == "mock"


def test_environment_overrides_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=9001\n", encoding="utf-8")
    assert load_settings({"PORT": "9002"}, env_file=env_file).port == 9002


def test_only_the_mock_ai_provider_is_available(tmp_path):
    with pytest.raises(ValueError, match="not available"):
        load_settings({"AI_PROVIDER": "anthropic"}, env_file=tmp_path / "none.env")
