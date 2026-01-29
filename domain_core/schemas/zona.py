from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

# Importando os Enums
from ..enums.influencias import (
    TemperaturaAmbiente, 
    PresencaAgua, 
    PresencaSolidos, 
    CompetenciaPessoas,
    MateriaisConstrucao,
    EstruturaEdificacao
)

class ZonaBase(BaseModel):
    nome: str = Field(..., description="Nome descritivo da zona (ex: Área Molhada, Oficina)")
    descricao: Optional[str] = None
    
    # Metadados de UX/Rastreabilidade
    origem: Literal['preset', 'ajustada', 'custom'] = Field(default='custom', description="Origem da definição da zona")
    preset_id: Optional[str] = Field(default=None, description="ID do preset utilizado, se houver")

    # --- Influências Ambientais (Defaults Seguros - NBR 5410) ---
    temp_ambiente: TemperaturaAmbiente = Field(default=TemperaturaAmbiente.AA4)
    presenca_agua: PresencaAgua = Field(default=PresencaAgua.AD1)
    presenca_solidos: PresencaSolidos = Field(default=PresencaSolidos.AE1)
    competencia_pessoas: CompetenciaPessoas = Field(default=CompetenciaPessoas.BA1)
    materiais_construcao: MateriaisConstrucao = Field(default=MateriaisConstrucao.CA2)
    estrutura_edificacao: EstruturaEdificacao = Field(default=EstruturaEdificacao.CB1)
    
    # --- UI Helper ---
    cor_identificacao: str = Field(default="#E0E0E0")

class ZonaCreate(ZonaBase):
    projeto_id: str

class ZonaUpdate(BaseModel):
    nome: Optional[str] = None
    presenca_agua: Optional[PresencaAgua] = None
    competencia_pessoas: Optional[CompetenciaPessoas] = None
    origem: Optional[str] = None

class Zona(ZonaBase):
    id: str
    projeto_id: str
    data_criacao: datetime

    class Config:
        from_attributes = True