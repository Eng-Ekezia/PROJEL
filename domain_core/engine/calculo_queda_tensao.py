class CalculoQuedaTensao:
    """
    Calcula queda percentual de tensão.
    Não decide seção, apenas avalia as consequências elétricas.
    """
    
    @staticmethod
    def calcular_queda_tensao_percentual(
        corrente_A: float,
        secao_mm2: float,
        comprimento_m: float,
        tensao_V: float,
        fases: int,
        rho: float
    ) -> float:
        """
        Calcula a queda de tensão percentual (DeltaV %).
        Monofásico / Bifásico: DeltaV = 2 * rho * L * I / S
        Trifásico: DeltaV = sqrt(3) * rho * L * I / S
        E então converte para % da tensão base.
        """
        if secao_mm2 <= 0:
            return float('inf')
            
        fator_fases = 1.732 if fases == 3 else 2.0
        
        # Queda em Volts
        queda_V = (fator_fases * rho * comprimento_m * corrente_A) / secao_mm2
        
        # Em percentual da tensao base
        return (queda_V / tensao_V) * 100.0
