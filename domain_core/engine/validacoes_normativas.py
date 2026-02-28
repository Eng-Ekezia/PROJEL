from typing import List
from domain_core.schemas.resultados import VerificacaoNormativa, StatusDimensionamento

class ValidacoesNormativas:
    """
    Realizar validação final de conformidade normativa.
    Verifica estado geral mas não sugere soluções.
    """
    
    @staticmethod
    def validar_capacidade_conducao(corrente_projeto: float, capacidade_cabo: float, temp_fc: float) -> VerificacaoNormativa:
        status = StatusDimensionamento.OK if capacidade_cabo >= corrente_projeto else StatusDimensionamento.ERRO
        msg = f"In = {corrente_projeto:.2f}A, Iz (corrigida) = {capacidade_cabo:.2f}A. Fator correção aplicado: {temp_fc:.2f}"
        
        return VerificacaoNormativa(
            criterio="Capacidade de Condução (Coordenação IB <= IZ)",
            status=status,
            valor_calculado=capacidade_cabo,
            limite_normativo=corrente_projeto,
            mensagem=msg,
            referencia_nbr="Item 6.2.5"
        )
        
    @staticmethod
    def validar_queda_tensao(queda_calculada: float, limite_normativo: float) -> VerificacaoNormativa:
        status = StatusDimensionamento.OK if queda_calculada <= limite_normativo else StatusDimensionamento.ERRO
        
        return VerificacaoNormativa(
            criterio="Queda de Tensão",
            status=status,
            valor_calculado=queda_calculada,
            limite_normativo=limite_normativo,
            mensagem=f"Queda de tensão calculada = {queda_calculada:.2f}%. Máximo permitido = {limite_normativo:.2f}%",
            referencia_nbr="Item 6.2.7"
        )
        
    @staticmethod
    def validar_protecao_sobrecorrente(disjuntor_in: float, corrente_projeto: float, capacidade_cabo: float) -> VerificacaoNormativa:
        status = StatusDimensionamento.OK
        msg = f"Condições atendidas: {corrente_projeto:.1f}A <= {disjuntor_in:.1f}A <= {capacidade_cabo:.1f}A"
        
        if disjuntor_in < corrente_projeto:
            status = StatusDimensionamento.ERRO
            msg = f"Disjuntor menor que corrente de projeto ({disjuntor_in:.1f}A < {corrente_projeto:.1f}A)"
        elif disjuntor_in > capacidade_cabo:
            status = StatusDimensionamento.ERRO
            msg = f"Disjuntor maior que a capacidade do cabo ({disjuntor_in:.1f}A > {capacidade_cabo:.1f}A)"
            
        return VerificacaoNormativa(
            criterio="Proteção contra Sobrecarga (IN)",
            status=status,
            valor_calculado=disjuntor_in,
            limite_normativo=capacidade_cabo,
            mensagem=msg,
            referencia_nbr="Item 5.3"
        )
        
    @staticmethod
    def verificar_presenca_dr(foi_exigido: bool, esta_presente: bool) -> VerificacaoNormativa:
        if not foi_exigido:
            # Optativo, se não está não tem problema.
            return VerificacaoNormativa(
                criterio="Exigência de Dispositivo DR",
                status=StatusDimensionamento.OK,
                valor_calculado="Dispensado",
                limite_normativo="N/A",
                mensagem="A zona governante não exige proteção diferencial residual limitante.",
                referencia_nbr="Item 5.1.3"
            )
            
        status = StatusDimensionamento.OK if esta_presente else StatusDimensionamento.ERRO
        msg = "Exigência de DR atendida" if esta_presente else "AMBIENTE DE RISCO. Proteção DR máxima 30mA OBRIGATÓRIA ausente!"
        
        return VerificacaoNormativa(
            criterio="Exigência de Dispositivo DR",
            status=status,
            valor_calculado="Presente" if esta_presente else "Ausente",
            limite_normativo="Limitante",
            mensagem=msg,
            referencia_nbr="Item 5.1.3"
        )

    @staticmethod
    def compor_status_global(verificacoes: List[VerificacaoNormativa]) -> StatusDimensionamento:
        for v in verificacoes:
             if v.status == StatusDimensionamento.ERRO:
                 return StatusDimensionamento.ERRO
        # Verifica Alertas
        for v in verificacoes:
             if v.status == StatusDimensionamento.ALERTA:
                 return StatusDimensionamento.ALERTA
        return StatusDimensionamento.OK
