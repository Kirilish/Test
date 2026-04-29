from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    telegram_token: str = Field(alias="TELEGRAM_BOT_TOKEN")
    hf_api_token: str = Field(default="", alias="HF_API_TOKEN")
    hf_model: str = Field(default="HuggingFaceH4/zephyr-7b-beta", alias="HF_MODEL")


settings = Settings()
