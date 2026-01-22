from fastapi import APIRouter
from backend.api.v1.endpoints import system

api_router = APIRouter()
api_router.include_router(system.router, tags=["system"])
# Futuramente: api_router.include_router(calculo.router, prefix="/calculo", tags=["calculo"])