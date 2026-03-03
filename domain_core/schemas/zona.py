from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# Importando os Enums
from ..enums.influencias import (
    TemperaturaAmbiente, 
    PresencaAgua, 
    PresencaSolidos, 
    CompetenciaPessoas,
    MateriaisConstrucao,
    EstruturaEdificacao
)

class CategoriaA(BaseModel):
    temp_ambiente: TemperaturaAmbiente = Field(..., description="Temperatura Ambiente (Ex: AA4)")
    presenca_agua: PresencaAgua = Field(..., description="Presença de Água (Ex: AD1)")
    presenca_solidos: PresencaSolidos = Field(..., description="Presença de Sólidos (Ex: AE1)")

class CategoriaB(BaseModel):
    competencia_pessoas: CompetenciaPessoas = Field(..., description="Competência das Pessoas (Ex: BA1)")

class CategoriaC(BaseModel):
    materiais_construcao: MateriaisConstrucao = Field(..., description="Materiais de Construção (Ex: CA1)")
    estrutura_edificacao: EstruturaEdificacao = Field(..., description="Estrutura da Edificação (Ex: CB1)")

class ZonaBase(BaseModel):
    nome: str = Field(..., description="Nome descritivo da zona (ex: Área Molhada, Oficina)")
    descricao: Optional[str] = None
    
    # Metadados de UX/Rastreabilidade
    origem: Literal['preset', 'ajustada', 'custom'] = Field(..., description="Origem da definição da zona")
    autor: Optional[str] = Field(default=None, description="Autor/Responsável pela definição")
    preset_id: Optional[str] = Field(default=None, description="ID do preset utilizado, se houver")

    # --- Influências Ambientais (Sem Defaults Cegos) ---
    influencias_categoria_a: CategoriaA
    influencias_categoria_b: CategoriaB
    influencias_categoria_c: CategoriaC
    
    # --- UI Helper ---
    cor_identificacao: str = Field(default="#E0E0E0")

class ZonaCreate(ZonaBase):
    projeto_id: str

class ZonaUpdate(BaseModel):
    nome: Optional[str] = None
    influencias_categoria_a: Optional[CategoriaA] = None
    influencias_categoria_b: Optional[CategoriaB] = None
    influencias_categoria_c: Optional[CategoriaC] = None
    origem: Optional[Literal['preset', 'ajustada', 'custom']] = None

class Zona(ZonaBase):
    id: str
    projeto_id: str
    data_criacao: datetime

    class Config:
        from_attributes = True