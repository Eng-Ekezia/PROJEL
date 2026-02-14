from fastapi import APIRouter
from backend.api.v1.endpoints import system, zonas, locais, cargas, circuitos

api_router = APIRouter()

# Rotas de Sistema
api_router.include_router(system.router, prefix="/system", tags=["system"])

# Rotas de Domínio (Phase 06)
api_router.include_router(zonas.router, prefix="/zonas", tags=["zonas - influências"])
api_router.include_router(locais.router, prefix="/locais", tags=["locais - arquitetura"])
api_router.include_router(cargas.router, prefix="/cargas", tags=["cargas - equipamentos"])
api_router.include_router(circuitos.router, prefix="/circuitos", tags=["Circuitos"])