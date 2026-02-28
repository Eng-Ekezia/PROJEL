class CalculoQuedaTensao:
    """
    Calcula queda percentual de tensão.
    Não decide seção, apenas avalia as consequências elétricas.
    """
    
    # Resistividade do cobre a 70°C (Ohm.m^2/m)
    RHO_COBRE = 0.0225 
    RHO_ALUMINIO = 0.036
    
    @staticmethod
    def calcular_queda_tensao_percentual(
        corrente_A: float,
        secao_mm2: float,
        comprimento_m: float,
        tensao_V: float,
        fases: int,
        material: str = "cobre"
    ) -> float:
        """
        Calcula a queda de tensão percentual (DeltaV %).
        Monofásico / Bifásico: DeltaV = 2 * rho * L * I / S
        Trifásico: DeltaV = sqrt(3) * rho * L * I / S
        E então converte para % da tensão base.
        """
        if secao_mm2 <= 0:
            return float('inf')
            
        rho = CalculoQuedaTensao.RHO_COBRE if material.lower() == "cobre" else CalculoQuedaTensao.RHO_ALUMINIO
        fator_fases = 1.732 if fases == 3 else 2.0
        
        # Queda em Volts
        queda_V = (fator_fases * rho * comprimento_m * corrente_A) / secao_mm2
        
        # Em percentual da tensao base
        return (queda_V / tensao_V) * 100.0
