from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from domain_core.enums.perfis_locais import PerfilNormativoLocal

class LocalBase(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do cômodo (ex: Sala de Estar)")
    descricao: Optional[str] = Field(default=None, description="Descrição complementar do local")
    
    # Geometria Básica
    area_m2: float = Field(..., gt=0, description="Área em metros quadrados")
    perimetro_m: float = Field(..., gt=0, description="Perímetro em metros")
    pe_direito_m: float = Field(default=2.80, gt=1.5, description="Altura do teto em metros")
    
    # Vínculos e Contexto Normativo
    zona_id: str = Field(..., description="ID da Zona de Influência vinculada")
    projeto_id: str = Field(..., description="ID do Projeto pai")
    perfil_normativo_local: PerfilNormativoLocal = Field(
        default=PerfilNormativoLocal.PADRAO, 
        description="Identifica locais com restrições e métodos específicos segundo o Capítulo 9 da NBR 5410"
    )
    autor: Optional[str] = Field(default=None, description="Autor/Responsável pela definição")

class LocalCreate(LocalBase):
    pass

class Local(LocalBase):
    id: str = Field(..., description="Identificador único do local")
    data_criacao: datetime = Field(..., description="Data de criação do registro")

    class Config:
        from_attributes = True