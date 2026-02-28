from domain_core.schemas.resultados import ResultadoDimensionamento, MemoriaCalculo, StatusDimensionamento
from domain_core.engine.validacoes_normativas import ValidacoesNormativas

class ResultadoBuilder:
    """
    Construir objeto final ResultadoDimensionamento explicitando como ensinar o que foi calculado.
    """
    def __init__(self, circuito_id: str):
         self.resultado = ResultadoDimensionamento(
             circuito_id=circuito_id,
             status_global=StatusDimensionamento.ERRO,
             corrente_projeto_ib=0,
             memoria=MemoriaCalculo(passos=[])
         )
         
    def adicionar_passo(self, msg: str):
        self.resultado.memoria.passos.append(msg)
        
    def add_validacao(self, validacao):
        self.resultado.verificacoes.append(validacao)

    def compilar(self) -> ResultadoDimensionamento:
        self.resultado.status_global = ValidacoesNormativas.compor_status_global(self.resultado.verificacoes)
        return self.resultado
