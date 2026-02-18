from fastapi import APIRouter
from backend.api.v1.endpoints import system, zonas, locais, cargas, circuitos, calculos

api_router = APIRouter()

api_router.include_router(system.router, tags=["system"])
api_router.include_router(zonas.router, prefix="/zonas", tags=["zonas"])
api_router.include_router(locais.router, prefix="/locais", tags=["locais"])
api_router.include_router(cargas.router, prefix="/cargas", tags=["cargas"])
api_router.include_router(circuitos.router, prefix="/circuitos", tags=["circuitos"])
# [NOVO] Rota de Cálculos
api_router.include_router(calculos.router, prefix="/calculos", tags=["calculos"])