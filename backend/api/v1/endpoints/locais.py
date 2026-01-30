from fastapi import APIRouter, HTTPException, status
import uuid
from datetime import datetime
from domain_core.schemas.local import Local, LocalCreate

router = APIRouter()

@router.post("/", response_model=Local, status_code=status.HTTP_201_CREATED)
async def criar_local(local_in: LocalCreate):
    novo_local = Local(id=str(uuid.uuid4()), data_criacao=datetime.now(), **local_in.model_dump())
    return novo_local

@router.put("/{local_id}", response_model=Local)
async def atualizar_local(local_id: str, local_in: LocalCreate):
    # Mock update
    novo_local = Local(id=local_id, data_criacao=datetime.now(), **local_in.model_dump())
    return novo_local

@router.delete("/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_local(local_id: str):
    return None