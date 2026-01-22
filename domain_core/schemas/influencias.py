from pydantic import BaseModel, Field, conint
from domain_core.enums.influencias import CategoriaInfluencia

class InfluenciaNormativa(BaseModel):
    categoria: CategoriaInfluencia
    codigo: str = Field(..., description="Ex: AC, BA, CE")
    classe: conint(ge=1, le=4)
    descricao: str = Field(..., min_length=5)
