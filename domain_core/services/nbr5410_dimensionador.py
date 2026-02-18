from typing import Dict, TypedDict

class ResultadoMinimoNBR(TypedDict):
    norma_iluminacao_va: float
    norma_tugs_quantidade: int

class DimensionadorMinimoNBR:
    """
    Motor de cálculo para previsões mínimas de carga conforme NBR 5410 (Seção 9.5).
    Stateless e Determinístico.
    """

    @staticmethod
    def calcular_iluminacao(area: float) -> float:
        """
        NBR 5410 - 9.5.2.1
        - Pelo menos 100VA para áreas <= 6m2
        - +60VA para cada 4m2 inteiros excedentes
        """
        if area <= 6:
            return 100.0
        
        # O int() faz o arredondamento para baixo (floor), conforme a norma (4m2 inteiros)
        incremento = int((area - 6) / 4)
        return 100.0 + (incremento * 60.0)

    @staticmethod
    def calcular_tugs(perimetro: float, eh_area_umida: bool) -> int:
        """
        NBR 5410 - 9.5.2.2 (Simplificada para Fase 10)
        - Áreas de serviço/cozinhas (úmidas): 1 a cada 3.5m
        - Outras (secas): 1 a cada 5m
        """
        qtd = 0
        if eh_area_umida:
            qtd = int(perimetro / 3.5)
            # Se sobrar fração de perímetro, adiciona mais uma?
            # A norma diz "fração de perímetro", então sim.
            if perimetro % 3.5 > 0:
                qtd += 1
            # Mínimo absoluto para cozinhas não pode ser zero se houver perímetro (ajuste prático)
            if qtd < 2: qtd = 2 # Mínimo comum de projeto, mas a norma pede variantes. 
                                # Mantendo lógica original do controller para não quebrar comportamento.
        else:
            qtd = int(perimetro / 5)
            if perimetro % 5 > 0:
                qtd += 1
            if qtd < 1: qtd = 1 # Mínimo 1 por cômodo
            
        return qtd

    @classmethod
    def processar_previsao(cls, dados: Dict[str, float]) -> ResultadoMinimoNBR:
        """Fachada para execução completa baseada no DTO de entrada"""
        area = dados.get("area", 0.0)
        perimetro = dados.get("perimetro", 0.0)
        # O frontend manda 'eh_cozinha_servico' como float (0 ou 1) ou bool as vezes
        eh_area_umida = bool(dados.get("eh_cozinha_servico", False))

        pot_ilum = cls.calcular_iluminacao(area)
        qtd_tugs = cls.calcular_tugs(perimetro, eh_area_umida)

        return {
            "norma_iluminacao_va": pot_ilum,
            "norma_tugs_quantidade": qtd_tugs
        }