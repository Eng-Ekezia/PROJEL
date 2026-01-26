from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import uuid
from datetime import datetime

from domain_core.schemas.zona import Zona, ZonaCreate
from domain_core.enums.influencias import (
    TemperaturaAmbiente, PresencaAgua, PresencaSolidos, 
    CompetenciaPessoas, MateriaisConstrucao, EstruturaEdificacao,
    DESCRICOES
)

router = APIRouter()

@router.post("/", response_model=Zona, status_code=status.HTTP_201_CREATED)
async def validar_criar_zona(zona_in: ZonaCreate):
    """
    Factory de Zonas: Valida e cria uma nova Zona (Stateless).
    """
    nova_zona = Zona(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **zona_in.model_dump()
    )
    return nova_zona

@router.get("/opcoes-influencias", response_model=Dict[str, List[Dict[str, str]]])
async def listar_opcoes_influencias():
    """
    Retorna opções da NBR 5410 para Dropdowns do Frontend.
    Usa o dicionário DESCRICOES para fornecer o texto amigável.
    """
    def enum_to_list(enum_cls):
        # codigo = Valor do Enum (ex: "AA4")
        # descricao = Texto do Dict (ex: "AA4 - Temperada...")
        return [{
            "codigo": e.value, 
            "descricao": DESCRICOES.get(e.value, e.value) 
        } for e in enum_cls]

    return {
        "temperatura": enum_to_list(TemperaturaAmbiente),
        "agua": enum_to_list(PresencaAgua),
        "solidos": enum_to_list(PresencaSolidos),
        "pessoas": enum_to_list(CompetenciaPessoas),
        "materiais": enum_to_list(MateriaisConstrucao),
        "estrutura": enum_to_list(EstruturaEdificacao),
    }