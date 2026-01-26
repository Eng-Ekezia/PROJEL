from fastapi import APIRouter, HTTPException, status
import uuid
from datetime import datetime

from domain_core.schemas.local import Local, LocalCreate

router = APIRouter()

@router.post("/", response_model=Local, status_code=status.HTTP_201_CREATED)
async def validar_criar_local(local_in: LocalCreate):
    """
    Factory de Locais: Valida geometria básica.
    """
    if local_in.area_m2 <= 0:
        raise HTTPException(status_code=400, detail="A área deve ser maior que zero.")
    
    if local_in.perimetro_m <= 0:
        raise HTTPException(status_code=400, detail="O perímetro deve ser maior que zero.")

    # Validação Geométrica Básica (Evita dados impossíveis)
    if local_in.perimetro_m < (local_in.area_m2 ** 0.5) * 2:
         raise HTTPException(status_code=400, detail="Perímetro muito pequeno para a área informada (Geometria impossível).")

    novo_local = Local(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **local_in.model_dump()
    )
    return novo_local