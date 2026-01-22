from fastapi import APIRouter
from backend.core.config import settings

router = APIRouter()

@router.get("/health", status_code=200)
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

@router.get("/version", status_code=200)
def version():
    return {"version": "0.1.0", "engine": "NBR5410-Stateless"}