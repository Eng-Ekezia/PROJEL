from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum
from datetime import datetime
from .carga import Carga
from .zona import Zona

class StatusProposta(str, Enum):
    RASCUNHO = "rascunho"
    REVISADA = "revisada"
    ACEITA = "aceita"
    DESCARTADA = "descartada"

class PropostaCircuitoBase(BaseModel):
    """Modelo base com campos comuns de leitura e escrita"""
    descricao_intencao: str = Field(..., description="Descrição da intenção de agrupamento")
    observacoes_normativas: Optional[str] = Field(None, description="Anotações sobre critérios normativos ou conflitos de zonas")

class PropostaCircuitoCreate(PropostaCircuitoBase):
    """Input para criação de proposta (geralmente via Wizard)"""
    cargas_ids: List[str] = Field(..., min_length=1, description="Lista de cargas a agrupar")
    autor: str = Field(..., description="Identificador do autor da proposta")

    @field_validator('cargas_ids')
    def validar_cargas_nao_vazias(cls, v):
        if not v:
            raise ValueError('Uma Proposta de Circuito deve conter pelo menos uma Carga.')
        return v

class PropostaCircuito(PropostaCircuitoBase):
    """Entidade completa de Proposta (Output)"""
    id: str
    data_criacao: datetime
    status: StatusProposta = Field(default=StatusProposta.RASCUNHO)
    
    cargas_ids: List[str]
    
    # Atributos Derivados (Calculados pelo Backend com base nas Cargas)
    # Não são atributos elétricos, são atributos de Rastreabilidade Espacial/Normativa
    locais_ids: List[str] = Field(..., description="IDs dos locais envolvidos (derivado)")
    zonas_ids: List[str] = Field(..., description="IDs das zonas envolvidas (derivado)")
    
    autor: str

    class Config:
        from_attributes = True

class AnalisePropostaRequest(BaseModel):
    """Payload enviado pelo Frontend contendo as cargas selecionadas para rascunho"""
    cargas_selecionadas: List[Carga] = Field(..., description="Cargas que o utilizador deseja agrupar")
    zonas_do_projeto: List[Zona] = Field(..., description="Zonas existentes no projeto para contexto normativo")

class AnalisePropostaResponse(BaseModel):
    """Resposta do Motor de Domínio com os efeitos do agrupamento"""
    potencia_total_va: float
    potencia_total_w: float
    locais_envolvidos_ids: List[str]
    zonas_envolvidas_ids: List[str]
    alertas_normativos: List[str]
    is_valida: bool