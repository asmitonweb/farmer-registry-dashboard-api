from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Farmer Registry Dashboard API"
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
