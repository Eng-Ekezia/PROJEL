import sys
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
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

# [FASE 2] Tratamento de Erro UX-Friendly (Contratos de Domínio)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detalhes = []
    for error in exc.errors():
        campo = ".".join([str(loc) for loc in error["loc"]])
        msg = error["msg"]
        detalhes.append(f"{campo}: {msg}")
        
    return JSONResponse(
        status_code=422,
        content={
            "erro": "DECISAO_INVALIDA",
            "mensagem": "Falha na validação do contrato de domínio. Verifique os campos informados.",
            "detalhes": detalhes
        }
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