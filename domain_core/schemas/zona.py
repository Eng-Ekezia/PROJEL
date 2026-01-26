from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

# Importando os Enums corretos de influencias.py
from ..enums.influencias import (
    TemperaturaAmbiente, 
    PresencaAgua, 
    PresencaSolidos, 
    CompetenciaPessoas,
    MateriaisConstrucao,   # Classificação CA
    EstruturaEdificacao    # Classificação CB
)

class ZonaBase(BaseModel):
    nome: str = Field(..., description="Nome descritivo da zona (ex: Área Molhada, Oficina)")
    descricao: Optional[str] = None
    
    # --- Influências Ambientais (Defaults Seguros - NBR 5410) ---
    
    # AA - Temperatura
    temp_ambiente: TemperaturaAmbiente = Field(default=TemperaturaAmbiente.AA4)
    
    # AD - Água
    presenca_agua: PresencaAgua = Field(default=PresencaAgua.AD1)
    
    # AE - Sólidos/Poeira
    presenca_solidos: PresencaSolidos = Field(default=PresencaSolidos.AE1)
    
    # BA - Pessoas
    competencia_pessoas: CompetenciaPessoas = Field(default=CompetenciaPessoas.BA1)
    
    # CA - Materiais de Construção (Corrigido)
    materiais_construcao: MateriaisConstrucao = Field(default=MateriaisConstrucao.CA2)
    
    # CB - Estrutura da Edificação (Adicionado para completar)
    estrutura_edificacao: EstruturaEdificacao = Field(default=EstruturaEdificacao.CB1)
    
    # --- UI Helper ---
    cor_identificacao: str = Field(default="#E0E0E0", description="Cor para representar a zona na planta/dashboard")

class ZonaCreate(ZonaBase):
    projeto_id: str

class ZonaUpdate(BaseModel):
    nome: Optional[str] = None
    presenca_agua: Optional[PresencaAgua] = None
    competencia_pessoas: Optional[CompetenciaPessoas] = None
    # Adicione outros campos opcionais conforme necessidade de atualização parcial

class Zona(ZonaBase):
    id: str
    projeto_id: str
    data_criacao: datetime

    class Config:
        from_attributes = True