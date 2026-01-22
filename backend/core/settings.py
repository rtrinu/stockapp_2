from dotenv import load_dotenv
from pydantic.settings import BaseSettings
from pydantic import field_validator
from typing import List

load_dotenv()


class Settintgs(BaseSettings):
    ALPACA_KEY: str
    ALPACA_SECRET: str
    ALPACA_BASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    ALLOWED_ORIGINS: str = ""
    DEBUG: bool = True

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
