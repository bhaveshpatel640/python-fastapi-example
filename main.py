from fastapi import FastAPI
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = Field(..., description="Application Name")
    APP_ENV: str = Field(..., description="Application Environment")
    DATABASE_URL: str = Field(..., description="Database Connection URL")

    @field_validator("APP_NAME", "APP_ENV", "DATABASE_URL", mode="before")
    @classmethod
    def non_empty(cls, v: str, info) -> str:
        if not v or v.strip() == "":
            raise ValueError(f"Field '{info.field_name}' cannot be empty")
        return v

    @classmethod
    def load(cls):
        try:
            return cls()
        except ValidationError as e:
            raise RuntimeError(f"Invalid or missing environment variables: {e}")


settings = Settings.load()

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def read_root():
    return {"app_name": settings.APP_NAME, "environment": settings.APP_ENV}
