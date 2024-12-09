from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    AWS_REGION_NAME: str
    AWS_COGNITO_APP_CLIENT_ID: str
    AWS_COGNITO_USER_POOL_ID: str
    APP_ENV: str

    model_config = SettingsConfigDict(env_file=".env")
    load_dotenv()


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
