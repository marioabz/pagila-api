from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_time_expiration_in_mins: int

    debug: bool = False
    app_name: str = "Pagila API"

    database_user: str
    database_password: str
    database_url: str
    database_port: int
    database_db: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )
