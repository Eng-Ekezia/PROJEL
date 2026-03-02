import math
from typing import Optional

class CalculoCorrente:
    """
    Calcula corrente elétrica da carga ou do circuito.
    """
    @staticmethod
    def calcular_corrente_projeto(
        potencia_W: float, 
        tensao_V: float, 
        fator_potencia: float,
        fases: int = 1
    ) -> float:
        """
        IB = P / (V * FP * sqrt(fases if fases == 3 else 1))
        (Simplificação para o projeto didático: fases 1(F-N) ou 2(F-F) = V, trifásico = V * sqrt(3))
        """
        divisor_fase = math.sqrt(3) if fases == 3 else 1.0
        return potencia_W / (tensao_V * fator_potencia * divisor_fase)
        
    @staticmethod
    def aplicar_fator_agrupamento(corrente_ib: float, fator_agrupamento: float) -> float:
        if fator_agrupamento <= 0: return corrente_ib
        return corrente_ib / fator_agrupamento
        
    @staticmethod
    def aplicar_fator_temperatura(corrente: float, fator_temperatura: float) -> float:
        if fator_temperatura <= 0: return corrente
        return corrente / fator_temperatura
