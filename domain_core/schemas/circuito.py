from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from domain_core.enums.circuitos import TipoCircuito, CriticidadeCircuito

class Circuito(BaseModel):
    id: str
    identificador: str = Field(..., description="Ex: C1, TUG-01")
    tipo_circuito: TipoCircuito
    zona_id: str
    sobrescreve_influencias: bool = False
    tensao_nominal: float = Field(..., gt=0)
    comprimento_m: float = Field(..., gt=0)
    metodo_instalacao: str = Field(..., description="A1...F")
    material_condutor: str = Field(..., description="cobre/aluminio")
    isolacao: str = Field(..., description="PVC/EPR/XLPE")
    temperatura_ambiente: float = Field(..., gt=0)
    circuitos_agrupados: int = Field(..., ge=1)
    
    # [NOVO] Rastreabilidade da Proposta (Opcional p/ Migração Incremental)
    proposta_id: Optional[str] = Field(default=None, description="ID da Proposta de origem")
    
    # [NOVO] Lista de Cargas (Mantida/Explicitada para compatibilidade)
    # Na arquitetura final, esta lista será populada a partir da Proposta,
    # mas o circuito precisa saber quais cargas possui.
    cargas_ids: List[str] = Field(default=[], description="Lista de IDs das cargas agrupadas")

    potencia_instalada_W: float | None = Field(default=None, gt=0)
    corrente_nominal_A: float | None = Field(default=None, gt=0)
    
    criticidade: CriticidadeCircuito = CriticidadeCircuito.NORMAL

    @model_validator(mode='after')
    def validar_potencia_ou_corrente(self):
        p = self.potencia_instalada_W
        i = self.corrente_nominal_A

        if p is None and i is None:
            raise ValueError("Obrigatorio informar 'potencia_instalada_W' OU 'corrente_nominal_A'")
        if p is not None and i is not None:
            raise ValueError("Conflito: Informe APENAS um. O sistema calculará o outro.")
        return self