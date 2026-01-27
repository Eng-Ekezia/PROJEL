from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..enums.cargas import TipoCarga

class CargaBase(BaseModel):
    nome: str = Field(..., description="Descrição da carga (ex: Lâmpada Centro, Tomada Geladeira)")
    tipo: TipoCarga = Field(default=TipoCarga.TUG)
    potencia_va: float = Field(..., gt=0, description="Potência Aparente (VA)")
    potencia_w: float = Field(..., gt=0, description="Potência Ativa (W)")
    fator_potencia: float = Field(default=1.0, ge=0, le=1, description="Fator de Potência (cos fi)")
    quantidade: int = Field(default=1, gt=0)
    
    # Vínculos
    local_id: str = Field(..., description="ID do Local onde a carga está instalada")
    # Nota: circuito_id será adicionado na Phase 07

class CargaCreate(CargaBase):
    pass

class Carga(CargaBase):
    id: str
    data_criacao: datetime

    class Config:
        from_attributes = True