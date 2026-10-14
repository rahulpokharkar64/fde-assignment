from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "healthcare_readmission"
    db_user: str = "postgres"
    db_password: str = "postgres"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()


@contextmanager
def get_connection() -> Generator[psycopg.Connection, None, None]:
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        yield conn

