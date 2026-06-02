from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Pydantic BaseSettings 기반 전역 환경 변수 관리 클래스"""
    app_name: str = "My FastAPI Application"
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/db"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
