from typing import Optional

class SelecaoDisjuntor:
    """
    Selecionar dispositivo de proteção (Disjuntor Termomagnético).
    """
    
    # Valores comerciais padrão de disjuntores DIN no Brasil (Amperes)
    DISJUNTORES_COMERCIAIS = [10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125]
    
    @staticmethod
    def selecionar_in_disjuntor(corrente_projeto_ib: float, capacidade_cabo_iz: float) -> Optional[float]:
        """
        Coordenação de proteção contra sobrecarga da NBR 5410:
        IB <= IN <= IZ
        
        Onde:
        IB: Corrente de projeto calculada.
        IN: Corrente nominal do dispositivo de proteção (disjuntor).
        IZ: Capacidade de condução do cabo selecionado sob as condições vigentes.
        """
        for in_comercial in SelecaoDisjuntor.DISJUNTORES_COMERCIAIS:
            if corrente_projeto_ib <= in_comercial <= capacidade_cabo_iz:
                return float(in_comercial)
                
        # Se nenhum comercial cober, não selecionamos para expor o conflito.
        return None
