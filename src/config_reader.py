import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

ENV_PATH = os.path.expanduser(".env")


class Settings(BaseSettings): 
    ADMIN_IDS: list[int] = [] # [000, 111, ...]
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr 
    OWNER_ID: SecretStr

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8"
    )


config = Settings()