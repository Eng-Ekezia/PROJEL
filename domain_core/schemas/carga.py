from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime
from ..enums.cargas import TipoCarga

class CargaBase(BaseModel):
    """Modelo base de leitura (Output)"""
    nome: str = Field(..., description="Descrição da carga")
    tipo: TipoCarga = Field(default=TipoCarga.TUG)
    quantidade: int = Field(default=1, gt=0)
    
    # No Output, sempre devolvemos tudo calculado
    potencia_va: float 
    potencia_w: float
    fator_potencia: float
    
    local_id: str

class CargaCreate(BaseModel):
    """Modelo de entrada (Input Inteligente)"""
    nome: str
    tipo: TipoCarga = Field(default=TipoCarga.TUG)
    quantidade: int = Field(default=1, gt=0)
    local_id: str
    
    # Input flexível: Usuário informa um, o sistema calcula o outro
    potencia: float = Field(..., gt=0, description="Valor da potência")
    unidade: Literal['W', 'VA'] = Field(..., description="Unidade da potência informada")
    fator_potencia: float = Field(default=1.0, ge=0, le=1, description="Fator de Potência")

class Carga(CargaBase):
    id: str
    data_criacao: datetime

    class Config:
        from_attributes = True