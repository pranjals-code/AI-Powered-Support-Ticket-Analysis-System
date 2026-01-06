from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # ------------------
    # Application
    # ------------------
    app_name: str
    environment: str

    # ------------------
    # Database
    # ------------------
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    # ------------------
    # JWT / Security
    # ------------------
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # prevents crashes from unused env vars
    )


settings = Settings()
