from typing import Optional, List
from domain_core.engine.normative_repository import NormativeRepository
from domain_core.engine.contexto_instalacao import FatorCorrecao

class SelecaoCondutor:
    """
    Selecionar seção mínima do condutor cruzando a corrente com Tabelas da NBR 5410.
    """
    
    def __init__(self):
        self.repo = NormativeRepository()
        
    def iterar_secoes(self, material: str, isolacao: str, metodo: str, num_condutores: int) -> List[float]:
        tabela = self.repo.get_tabela_ampacidade(material, isolacao, metodo, num_condutores)
        if not tabela:
            return []
            
        secoes = list(tabela.keys())
        secoes.sort()
        return secoes
        
    def selecionar_secao_por_corrente(
        self, 
        corrente_corrigida: float,
        material: str, 
        isolacao: str, 
        metodo: str, 
        num_condutores: int,
        is_iluminacao: bool = False
    ) -> Optional[float]:
        """
        Seleciona a menor seção cuja Iz seja maior ou igual a IB corrigida (Iz_cabo >= IB_corrigida).
        Respeita também seções mínimas dadas na norma. (ex: Ilum 1.5, TUG 2.5).
        """
        tabela = self.repo.get_tabela_ampacidade(material, isolacao, metodo, num_condutores)
        if not tabela:
            return None
            
        secao_minima_norma = 1.5 if is_iluminacao else 2.5
        
        secoes = list(tabela.keys())
        secoes.sort()
        
        for secao in secoes:
            if secao >= secao_minima_norma:
                capacidade_conducao = tabela[secao]
                if capacidade_conducao >= corrente_corrigida:
                    return secao
                    
        return None  # Nenhuma seção suporta (projetista excedeu as tabelas do app)
