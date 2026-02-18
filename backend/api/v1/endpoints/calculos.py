from fastapi import APIRouter, HTTPException, status
from domain_core.schemas.circuito import Circuito
from domain_core.schemas.resultados import (
    ResultadoDimensionamento, 
    StatusDimensionamento, 
    MemoriaCalculo,
    VerificacaoNormativa
)

router = APIRouter()

@router.post("/simular", response_model=ResultadoDimensionamento)
async def simular_dimensionamento(circuito: Circuito):
    """
    Endpoint Experimental (Fase 10):
    Recebe um Circuito (com parâmetros definidos) e executa o Motor de Cálculo.
    
    ATENÇÃO: Retorno Mockado para validação de contrato na Fase de Repair.
    """
    
    # Simulação de um processamento básico
    # Na próxima etapa, aqui entrará a chamada para 'DimensionadorCondutores.processar(circuito)'
    
    return ResultadoDimensionamento(
        circuito_id=circuito.id,
        status_global=StatusDimensionamento.OK,
        corrente_projeto_ib=10.5,  # Valor dummy
        corrente_corrigida_iz=12.0, # Valor dummy
        disjuntor_nominal_in=16.0, # Valor dummy
        secao_condutor_mm2=2.5,    # Valor dummy
        queda_tensao_pct=1.5,      # Valor dummy
        verificacoes=[
            VerificacaoNormativa(
                criterio="Capacidade de Condução",
                status=StatusDimensionamento.OK,
                valor_calculado=10.5,
                limite_normativo=24.0, # Exemplo p/ 2.5mm2
                mensagem="Condutor suporta a corrente de projeto.",
                referencia_nbr="Tabela 36"
            )
        ],
        memoria=MemoriaCalculo(
            passos=[
                "Recebido circuito para cálculo.",
                "Motor experimental acionado.",
                "Retornando valores de teste."
            ]
        )
    )