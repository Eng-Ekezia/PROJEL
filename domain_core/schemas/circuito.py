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
    
    # [FASE 2] Rastreabilidade da Proposta e Contexto Físico
    proposta_id: str = Field(..., description="ID da Proposta de origem (Obrigatório)")
    
    # [NOVO] Listas de mapeamento espacial para cálculo e agrupamento
    cargas_ids: List[str] = Field(default=[], description="Lista de IDs das cargas agrupadas")
    locais_ids: List[str] = Field(default=[], description="Lista de IDs dos locais abrangidos pelo circuito")
    zonas_ids: List[str] = Field(default=[], description="Lista de IDs das zonas interceptadas")
    
    # [NOVO] O contexto dominante que governará as influências
    zona_governante_id: str = Field(..., description="ID da Zona mais severa que governa este circuito")
    perfil_normativo_aplicavel: str = Field(default='padrao', description="Perfil normativo aplicável ao circuito (Cap. 9)")

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