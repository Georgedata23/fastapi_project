from pydantic import model_validator, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DATABASE_URL: str = Field(default="")

    @model_validator(mode="after")
    def get_database_url(cls, values):
        values.DATABASE_URL = (
            f"postgresql+asyncpg://{values.DB_USER}:{values.DB_PASSWORD}@{values.DB_HOST}:{values.DB_PORT}/{values.DB_NAME}"
        )
        return values

    class Config:
        env_file = ".env"

settings = Settings()

print(settings.DATABASE_URL)