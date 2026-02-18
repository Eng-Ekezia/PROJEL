from fastapi import APIRouter, HTTPException, status, Body
from typing import List, Dict
import uuid
from datetime import datetime
from domain_core.schemas.carga import Carga, CargaCreate
from domain_core.services.nbr5410_dimensionador import DimensionadorMinimoNBR

router = APIRouter()

# --- Helpers utilitários (mantidos por compatibilidade temporária do CRUD) ---
def calcular_potencias(carga_in: CargaCreate):
    pot_w = 0.0
    pot_va = 0.0
    if carga_in.unidade == 'W':
        pot_w = carga_in.potencia
        fp = carga_in.fator_potencia if carga_in.fator_potencia > 0 else 1.0
        pot_va = pot_w / fp
    else: # Unidade == 'VA'
        pot_va = carga_in.potencia
        pot_w = pot_va * carga_in.fator_potencia
    return pot_w, pot_va

# --- Endpoints CRUD (Mantidos até Fase 4 - Corte Controlado) ---

@router.post("/", response_model=Carga, status_code=status.HTTP_201_CREATED)
async def criar_carga(carga_in: CargaCreate):
    pot_w, pot_va = calcular_potencias(carga_in)
    nova_carga = Carga(
        id=str(uuid.uuid4()), data_criacao=datetime.now(),
        nome=carga_in.nome, tipo=carga_in.tipo, quantidade=carga_in.quantidade,
        local_id=carga_in.local_id, potencia_va=round(pot_va, 2), potencia_w=round(pot_w, 2),
        fator_potencia=carga_in.fator_potencia,
        projeto_id=carga_in.projeto_id, # [NOVO] Repassando contexto
        zona_id=carga_in.zona_id        # [NOVO] Repassando contexto
    )
    return nova_carga

@router.put("/{carga_id}", response_model=Carga)
async def atualizar_carga(carga_id: str, carga_in: CargaCreate):
    pot_w, pot_va = calcular_potencias(carga_in)
    carga_atualizada = Carga(
        id=carga_id, data_criacao=datetime.now(), 
        nome=carga_in.nome, tipo=carga_in.tipo, quantidade=carga_in.quantidade,
        local_id=carga_in.local_id, potencia_va=round(pot_va, 2), potencia_w=round(pot_w, 2),
        fator_potencia=carga_in.fator_potencia,
        projeto_id=carga_in.projeto_id, # [NOVO]
        zona_id=carga_in.zona_id        # [NOVO]
    )
    return carga_atualizada

@router.delete("/{carga_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_carga(carga_id: str):
    return None

# --- Endpoint de Cálculo (Refatorado para usar Service) ---

@router.post("/calcular-minimo-nbr", status_code=200)
async def calcular_minimo_nbr(dados: Dict[str, float]):
    """
    Calcula potências mínimas de iluminação e quantidade de TUGs
    Delegando a lógica pura para o Domain Core.
    """
    return DimensionadorMinimoNBR.processar_previsao(dados)