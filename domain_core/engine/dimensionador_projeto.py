from typing import List, Optional
from domain_core.schemas.projeto import ProjetoEletrico
from domain_core.schemas.local import Local
from domain_core.schemas.zona import Zona
from domain_core.schemas.circuito import Circuito
from domain_core.schemas.resultados import ResultadoDimensionamento

from domain_core.engine.contexto_instalacao import ContextoInstalacao
from domain_core.engine.regras_zona import RegrasZonaEngine
from domain_core.engine.calculo_corrente import CalculoCorrente
from domain_core.engine.selecao_condutor import SelecaoCondutor
from domain_core.engine.calculo_queda_tensao import CalculoQuedaTensao
from domain_core.engine.selecao_disjuntor import SelecaoDisjuntor
from domain_core.engine.validacoes_normativas import ValidacoesNormativas
from domain_core.engine.resultado_builder import ResultadoBuilder

class DimensionadorProjeto:
    """
    Orquestra o dimensionamento completo de um Circuito embasado no Contexto de um Projeto.
    100% dependente do domínio e do repositório normativo.
    """
    def __init__(self):
        self.regras_engine = RegrasZonaEngine()
        self.selecionador_cabo = SelecaoCondutor()

    def processar_circuito(
        self,
        projeto: ProjetoEletrico,
        locais: List[Local],
        zona_governante: Zona,
        circuito: Circuito,
        has_dr: bool = False # Flag provisória de UI até estar embedada melhor
    ) -> ResultadoDimensionamento:
        
        # 1. Montar Contexto
        contexto = ContextoInstalacao(
             projeto=projeto,
             locais=locais,
             zona_governante=zona_governante,
             circuito=circuito
        )
        
        # 2. Avaliar Regras e extrair restrições do ambiente
        restricoes = self.regras_engine.aplicar_regras(contexto)
        contexto.restricoes = restricoes
        
        # Iniciar o criador de fatos documentais
        builder = ResultadoBuilder(circuito.id)
        builder.adicionar_passo("== INÍCIO: Análise e Dimensionamento NBR 5410 ==")
        if restricoes.observacoes:
             builder.adicionar_passo("Restrições Ambientais Identificadas: ")
             for obs in restricoes.observacoes:
                  builder.adicionar_passo(f"- {obs}")
         
        # Faltas graves (sem pot/corrente explicita)
        pot = circuito.potencia_instalada_W
        cor = circuito.corrente_nominal_A
        if pot is None and cor is None:
             builder.resultado.erros_entrada.append("Falta de carga no circuito.")
             return builder.compilar()
             
        # 3. Matemática da Corrente
        corrente_projeto = cor
        if corrente_projeto is None:
             corrente_projeto = CalculoCorrente.calcular_corrente_projeto(
                  potencia_W=pot, 
                  tensao_V=circuito.tensao_nominal
             )
        builder.resultado.corrente_projeto_ib = corrente_projeto
        builder.adicionar_passo(f"IB (Corrente Nominal de Projeto) = {corrente_projeto:.2f} A")
        
        # Fator de Correcao de Temperatura
        fc_temperatura = 1.0 # default
        for fc in restricoes.fatores_correcao:
            if fc.tipo == 'temperatura':
               # Para simplificar aqui, hardcodearemos o valor que estaria na tabela
               # Em um futuro mais detalhado, normatively resvolveríamos FC em função do cabo/isolação
               fc_temperatura = 0.87
               break
               
        builder.adicionar_passo(f"Corrigindo IB. Fatores de Correcao -> Agrapamento: {circuito.circuitos_agrupados}, Temperatura: {fc_temperatura:.2f}")
        # Simplificacao didatica: se ha arranjo > 1 agrupado no conduíte, o FC tbm reduz a amperagem ideal
        corrente_corrigida = corrente_projeto
        # Aplicamos do Agrupamento (0.8 generico por padrao simplificado para multiplos em conduíte para exibição)
        fc_agrup = 1.0 if circuito.circuitos_agrupados == 1 else 0.8  
        
        corrente_corrigida = (corrente_projeto / fc_agrup) / fc_temperatura
        builder.resultado.corrente_corrigida_iz = corrente_corrigida
        builder.adicionar_passo(f"IZ (Corrente Requerida na Tabela p/ Cabo) = {corrente_corrigida:.2f} A")

        # 4. Seleção Condutor
        num_conds = 2 # Padrao simplificado de fase-neutro
        is_ilum = (circuito.identificador and "ilum" in circuito.identificador.lower()) or (circuito.tipo_circuito.value == "iluminacao")
        secao = self.selecionador_cabo.selecionar_secao_por_corrente(
             corrente_corrigida=corrente_corrigida,
             material=circuito.material_condutor,
             isolacao=circuito.isolacao,
             metodo=circuito.metodo_instalacao,
             num_condutores=num_conds,
             is_iluminacao=is_ilum
        )
        builder.resultado.secao_condutor_mm2 = secao
        
        tabela = self.selecionador_cabo.repo.get_tabela_ampacidade(
             circuito.material_condutor, circuito.isolacao, circuito.metodo_instalacao, num_conds
        )
        capacidade_teorica = tabela.get(secao, 0)
        
        if not secao:
             builder.resultado.erros_entrada.append("A tabela normativa (Tabela 36-39 NBR 5410) não suportou a corrente.")
             return builder.compilar()
             
        builder.adicionar_passo(f"Seção Selecionada: {secao}mm² - Suporta teoricamente {capacidade_teorica}A")
             
        val_conducao = ValidacoesNormativas.validar_capacidade_conducao(
            corrente_projeto, capacidade_teorica * fc_temperatura * fc_agrup, fc_temperatura * fc_agrup
        )
        builder.add_validacao(val_conducao)
        
        # 5. Dimensionar Queda de Tensão
        fases_calculo = 1 # F-N
        queda = CalculoQuedaTensao.calcular_queda_tensao_percentual(
            corrente_A=corrente_projeto,
            secao_mm2=secao,
            comprimento_m=circuito.comprimento_m,
            tensao_V=circuito.tensao_nominal,
            fases=fases_calculo,
            material=circuito.material_condutor
        )
        builder.resultado.queda_tensao_pct = queda
        val_queda = ValidacoesNormativas.validar_queda_tensao(queda, restricoes.limite_queda_tensao_pct)
        builder.add_validacao(val_queda)
        builder.adicionar_passo(f"Queda de Tensão Calculada DeltaV = {queda:.2f}% (Limite {restricoes.limite_queda_tensao_pct:.2f}%)")

        # 6. Seleção Proteção Sobrecorrente (Disjuntores)
        disjuntor_in = SelecaoDisjuntor.selecionar_in_disjuntor(corrente_projeto, capacidade_teorica * fc_temperatura * fc_agrup)
        builder.resultado.disjuntor_nominal_in = disjuntor_in
        if disjuntor_in:
            builder.adicionar_passo(f"Dispositivo de Proteção Selecionado: IN = {disjuntor_in}A")
            val_prot = ValidacoesNormativas.validar_protecao_sobrecorrente(
                disjuntor_in, corrente_projeto, capacidade_teorica * fc_temperatura * fc_agrup
            )
            builder.add_validacao(val_prot)
        else:
            builder.resultado.erros_entrada.append("Impossível achar Disjuntor que crie coordenação de sobrecorrente. Rever Parâmetros ou Condutor.")

        # 7. Regras de Dispositivos Adicionais (DR)
        val_dr = ValidacoesNormativas.verificar_presenca_dr(restricoes.exige_dr_30ma, has_dr)
        builder.add_validacao(val_dr)
        if restricoes.exige_dr_30ma:
             builder.adicionar_passo(f"Conferência Dispositivo DR: {'Fornecido' if has_dr else 'Faltante (BLOQUEANTE)'}")
             
        return builder.compilar()
