import pytest
from app.core.config import Settings


# Unit test for Settings class
def test_settings_database_url():
    settings = Settings(
        app_name="TestApp",
        environment="test",
        postgres_user="user",
        postgres_password="pass",
        postgres_db="testdb",
        postgres_host="localhost",
        postgres_port=5432,
        secret_key="secret",
        algorithm="HS256",
        access_token_expire_minutes=30,
    )
    expected_url = "postgresql+psycopg2://user:pass@localhost:5432/testdb"
    assert settings.database_url == expected_url
