from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class StatusDimensionamento(str, Enum):
    OK = "ok"
    ALERTA = "alerta"
    ERRO = "erro"

class VerificacaoNormativa(BaseModel):
    """Representa uma verificação individual (ex: Queda de Tensão)"""
    criterio: str = Field(..., description="Nome do critério (ex: Capacidade de Condução)")
    status: StatusDimensionamento
    valor_calculado: float | str
    limite_normativo: float | str | None = None
    mensagem: str = Field(..., description="Explicação técnica do resultado")
    referencia_nbr: str = Field(..., description="Item da NBR 5410 (ex: 6.2.5)")

class MemoriaCalculo(BaseModel):
    passos: List[str] = Field(default=[], description="Passo a passo didático do cálculo")

class ResultadoDimensionamento(BaseModel):
    """Objeto consolidado de resposta do Motor de Cálculo"""
    circuito_id: Optional[str] = None
    status_global: StatusDimensionamento
    
    # Resultados Numéricos Principais
    corrente_projeto_ib: float = Field(..., description="Corrente de projeto (A)")
    corrente_corrigida_iz: Optional[float] = Field(None, description="Corrente corrigida (A)")
    disjuntor_nominal_in: Optional[float] = Field(None, description="Disjuntor selecionado (A)")
    secao_condutor_mm2: Optional[float] = Field(None, description="Seção do condutor (mm²)")
    queda_tensao_pct: Optional[float] = Field(None, description="Queda de tensão calculada (%)")
    
    # Detalhamento
    verificacoes: List[VerificacaoNormativa] = []
    memoria: MemoriaCalculo
    
    # Alertas de bloqueio (se houver erro fatal na entrada)
    erros_entrada: List[str] = []