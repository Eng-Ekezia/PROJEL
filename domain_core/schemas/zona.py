from pydantic import BaseModel, Field
from domain_core.enums.zonas import TipoZona
from .influencias import InfluenciaNormativa

class GrupoInfluencias(BaseModel):
    descricao_local: str = Field(
        ..., 
        description="Descricao do ambiente real. Ex: 'Parede externa sujeita a chuva'"
    )
    influencias: list[InfluenciaNormativa]

class ZonaDeInfluencia(BaseModel):
    id: str
    nome: str = Field(..., min_length=3)
    tipo_zona: TipoZona
    descricao: str | None = None
    influencias_externas: GrupoInfluencias

    def codigos_normativos(self) -> list[str]:
        return [
            f"{inf.codigo}{inf.classe}"
            for inf in self.influencias_externas.influencias
        ]
