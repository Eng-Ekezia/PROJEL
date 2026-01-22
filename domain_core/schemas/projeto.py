from pydantic import BaseModel, Field
from domain_core.enums.aterramento import EsquemaAterramento

class ProjetoEletrico(BaseModel):
    id: str
    nome: str = Field(..., min_length=3)
    tipo_instalacao: str
    tensao_sistema: str
    sistema: str
    esquema_aterramento: EsquemaAterramento
    descricao_aterramento: str | None = None
