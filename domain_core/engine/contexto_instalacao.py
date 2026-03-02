from typing import List, Dict, Any, Optional
from domain_core.schemas.projeto import ProjetoEletrico
from domain_core.schemas.local import Local
from domain_core.schemas.zona import Zona
from domain_core.schemas.circuito import Circuito
from pydantic import BaseModel, Field

class FatorCorrecao(BaseModel):
    tipo: str = Field(..., description="Ex: temperatura, agrupamento, etc.")
    valor: float = Field(..., gt=0)
    referencia: str = Field(...)

class RestricoesNormativas(BaseModel):
    fatores_correcao: List[FatorCorrecao] = Field(default_factory=list)
    limite_queda_tensao_pct: float = Field(...) # Removido default 4.0
    exige_dr_30ma: bool = Field(default=False)
    exige_dps: bool = Field(default=False)
    grau_ip_minimo: Optional[str] = None
    metodos_instalacao_proibidos: List[str] = Field(default_factory=list)
    observacoes: List[str] = Field(default_factory=list)
    
class ContextoInstalacao(BaseModel):
    """
    Consolida todas as variáveis ambientais e estruturais que influenciam o dimensionamento.
    """
    projeto: ProjetoEletrico
    locais: List[Local]
    zona_governante: Zona
    circuito: Circuito
    
    # As restrições serão preenchidas pelas engines de regras
    restricoes: Optional[RestricoesNormativas] = None
    
    @property
    def influencias_externas(self) -> Dict[str, str]:
        """
        Retorna o dicionário de influências externas ativas para a zona governante.
        """
        if hasattr(self.zona_governante, 'influencias_externas') and self.zona_governante.influencias_externas:
            # Assumindo que o model Zona devolve um dict ou as propriedades diretamente
            if isinstance(self.zona_governante.influencias_externas, dict):
                 return self.zona_governante.influencias_externas
            return self.zona_governante.influencias_externas.model_dump(exclude_unset=True)
        return {}
