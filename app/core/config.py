from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str
    environment: str

    # Database (Postgres)
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        extra = "forbid"   # explicit & safe


settings = Settings()
