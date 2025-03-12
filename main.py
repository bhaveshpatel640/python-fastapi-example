from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = Field(..., description="Application Name")
    APP_ENV: str = Field(..., description="Application Environment")
    DATABASE_URL: str = Field(..., description="Database Connection URL")

    @classmethod
    def load(cls):
        try:
            return cls()
        except ValueError as e:
            raise RuntimeError(f"Missing required environment variables: {e}")


settings = Settings.load()

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def read_root():
    return {"app_name": settings.APP_NAME, "environment": settings.APP_ENV}
