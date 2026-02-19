from fastapi import APIRouter
from domain_core.schemas.proposta import AnalisePropostaRequest, AnalisePropostaResponse
from domain_core.services.analisador_proposta import AnalisadorProposta

router = APIRouter()

@router.post("/analisar-rascunho", response_model=AnalisePropostaResponse)
async def analisar_rascunho_proposta(request: AnalisePropostaRequest):
    """
    Recebe um conjunto de cargas e zonas, e devolve a análise normativa
    deste agrupamento (derivação de locais, zonas e alertas de conflito).
    """
    return AnalisadorProposta.analisar_agrupamento(request)