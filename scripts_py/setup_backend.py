import os
from pathlib import Path

# --- ESTRUTURA DO BACKEND STATELESS ---

FILES = {
    # 1. Configurações Gerais
    "backend/core/__init__.py": "",
    "backend/core/config.py": """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PROJEL API"
    API_V1_STR: str = "/api/v1"
    
    # Em produção, isso deve ser restrito ao domínio do Frontend (Vercel)
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()
""",

    # 2. Endpoints de Sistema (Health/Version)
    "backend/api/__init__.py": "",
    "backend/api/v1/__init__.py": "",
    
    "backend/api/v1/endpoints/__init__.py": "",
    "backend/api/v1/endpoints/system.py": """
from fastapi import APIRouter
from backend.core.config import settings

router = APIRouter()

@router.get("/health", status_code=200)
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

@router.get("/version", status_code=200)
def version():
    return {"version": "0.1.0", "engine": "NBR5410-Stateless"}
""",

    # 3. Roteador Principal
    "backend/api/v1/api.py": """
from fastapi import APIRouter
from backend.api.v1.endpoints import system

api_router = APIRouter()
api_router.include_router(system.router, tags=["system"])
# Futuramente: api_router.include_router(calculo.router, prefix="/calculo", tags=["calculo"])
""",

    # 4. App Principal (Entrypoint)
    "backend/main.py": """
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- HACK PARA MONOREPO ---
# Garante que o backend consiga enxergar a pasta 'domain_core' na raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.config import settings
from backend.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuração de CORS (Crucial para o Frontend chamar o Backend)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "PROJEL API is running. Go to /docs for Swagger."}
"""
}

def setup_backend():
    print("--- CONFIGURANDO BACKEND (FASE 03) ---")
    
    # Criar pastas necessárias
    dirs = [
        "backend/core",
        "backend/api/v1/endpoints"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"📁 Pasta verificada: {d}")

    # Criar arquivos
    for filename, content in FILES.items():
        path = Path(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"📄 Arquivo gerado: {filename}")
        
    print("\n✅ Backend configurado.")
    print("Para testar, execute no terminal:")
    print("   uvicorn backend.main:app --reload")

if __name__ == "__main__":
    setup_backend()