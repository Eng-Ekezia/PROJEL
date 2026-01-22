from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PROJEL API"
    API_V1_STR: str = "/api/v1"
    
    # Em produção, isso deve ser restrito ao domínio do Frontend (Vercel)
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()