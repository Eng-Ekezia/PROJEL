from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LocalBase(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do cômodo (ex: Sala de Estar)")
    
    # Geometria Básica para Cálculos de Iluminação/TUGs
    area_m2: float = Field(..., gt=0, description="Área em metros quadrados")
    perimetro_m: float = Field(..., gt=0, description="Perímetro em metros")
    pe_direito_m: float = Field(default=2.80, gt=1.5, description="Altura do teto em metros")
    
    # Vínculo com a Zona de Influência
    zona_id: str = Field(..., description="ID da Zona que define as regras ambientais deste local")

class LocalCreate(LocalBase):
    pass

class Local(LocalBase):
    id: str
    projeto_id: str
    data_criacao: datetime

    class Config:
        from_attributes = True