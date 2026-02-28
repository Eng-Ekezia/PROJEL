from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

from domain_core.schemas.projeto import ProjetoEletrico
from domain_core.schemas.local import Local
from domain_core.schemas.zona import Zona
from domain_core.schemas.circuito import Circuito
from domain_core.schemas.resultados import ResultadoDimensionamento
from domain_core.engine.dimensionador_projeto import DimensionadorProjeto

router = APIRouter()

class SimulacaoRequest(BaseModel):
    projeto: ProjetoEletrico
    locais: List[Local]
    zona_governante: Zona
    circuito: Circuito
    has_dr: bool = False

@router.post("/simular", response_model=ResultadoDimensionamento)
async def simular_dimensionamento(req: SimulacaoRequest):
    """
    Endpoint Fase 10:
    Recebe um Contexto (Projeto, Locais, Zona, Circuito) e executa o Motor de Cálculo NBR 5410.
    """
    try:
        engine = DimensionadorProjeto()
        
        # Como o engine é stateless, repassamos os dados de UI
        resultado = engine.processar_circuito(
            projeto=req.projeto,
            locais=req.locais,
            zona_governante=req.zona_governante,
            circuito=req.circuito,
            has_dr=req.has_dr
        )
        
        return resultado
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro fatal no Motor de Cálculo NBR 5410: {str(e)}"
        )