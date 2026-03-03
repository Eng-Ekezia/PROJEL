import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from domain_core.schemas.projeto import ProjetoEletrico
from domain_core.schemas.zona import Zona, CategoriaA, CategoriaB, CategoriaC
from domain_core.schemas.local import Local
from domain_core.schemas.circuito import Circuito
from domain_core.enums.circuitos import TipoCircuito
from domain_core.enums.aterramento import EsquemaAterramento
from domain_core.enums.influencias import TemperaturaAmbiente, PresencaAgua, PresencaSolidos, CompetenciaPessoas, MateriaisConstrucao, EstruturaEdificacao
from domain_core.engine.dimensionador_projeto import DimensionadorProjeto

def criar_ambiente_teste():
    # 1. Projeto
    projeto = ProjetoEletrico(
        id="proj-test",
        nome="Projeto de Teste Local",
        tipo_instalacao="residencial",
        tensao_sistema="220",
        sistema="Bifásico",
        esquema_aterramento=EsquemaAterramento.TN_S
    )

    # 2. Zona
    zona = Zona(
        id="zona-test",
        projeto_id="proj-test",
        nome="Área Interna Seca",
        origem="custom",
        influencias_categoria_a=CategoriaA(
            temp_ambiente=TemperaturaAmbiente.AA4,
            presenca_agua=PresencaAgua.AD1,
            presenca_solidos=PresencaSolidos.AE1
        ),
        influencias_categoria_b=CategoriaB(
            competencia_pessoas=CompetenciaPessoas.BA1
        ),
        influencias_categoria_c=CategoriaC(
            materiais_construcao=MateriaisConstrucao.CA1,
            estrutura_edificacao=EstruturaEdificacao.CB1
        ),
        data_criacao=datetime.now()
    )

    # 3. Local
    local = Local(
        id="local-test",
        projeto_id="proj-test",
        zona_id="zona-test",
        nome="Sala de Estar",
        area_m2=15.0,
        perimetro_m=16.0,
        pe_direito_m=2.8,
        data_criacao=datetime.now()
    )

    return projeto, zona, [local]

def simular_circuito(potencia_W, tensao_V, comp_m, material, isolacao, agrup, tipo, metodo="B1"):
    projeto, zona, locais = criar_ambiente_teste()
    
    circuito = Circuito(
        id="circ-test",
        identificador="Teste-01",
        tipo_circuito=tipo,
        zona_id=zona.id,
        proposta_id="prop-test",
        zona_governante_id=zona.id,
        tensao_nominal=tensao_V,
        comprimento_m=comp_m,
        metodo_instalacao=metodo,
        material_condutor=material,
        isolacao=isolacao,
        temperatura_ambiente=30.0,
        circuitos_agrupados=agrup,
        potencia_instalada_W=potencia_W
    )
    
    print(f"\n=======================================================")
    print(f" Simulação: Pot={potencia_W}W, L={comp_m}m, {material}/{isolacao}, Met={metodo}, Agrup={agrup}, Tipo={tipo.value}")
    print(f"=======================================================")

    engine = DimensionadorProjeto()
    try:
        resultado = engine.processar_circuito(
            projeto=projeto,
            locais=locais,
            zona_governante=zona,
            circuito=circuito,
            has_dr=True
        )
        
        # Print formatado
        print(f"Status Global       : {resultado.status_global.value.upper()}")
        print(f"Corrente Projeto IB : {resultado.corrente_projeto_ib:.2f} A")
        print(f"Corrente Iz Corrig. : {resultado.corrente_corrigida_iz:.2f} A" if resultado.corrente_corrigida_iz else "Corrente Iz Corrig. : N/A")
        print(f"Disjuntor (IN e Cv) : {resultado.curva_disjuntor} {resultado.disjuntor_nominal_in} A" if resultado.disjuntor_nominal_in else "Disjuntor           : N/A")
        print(f"Seção do Condutor   : {resultado.secao_condutor_mm2} mm²" if resultado.secao_condutor_mm2 else "Seção do Condutor   : N/A")
        print(f"Queda de Tensão     : {resultado.queda_tensao_pct:.2f} %" if resultado.queda_tensao_pct else "Queda de Tensão     : N/A")
        
        print("\n[Memória de Cálculo]")
        for passo in resultado.memoria.passos:
            print(f"  - {passo}")
            
        if resultado.erros_entrada:
            print("\n[Erros_Entrada (Críticos)]")
            for err in resultado.erros_entrada:
                print(f"  [X] {err}")
            
        print("\n[Verificações Normativas]")
        for v in resultado.verificacoes:
            status_simbolo = "Pass" if v.status == "atende" else "Warn" if v.status == "atende_com_restricao" else "Fail"
            print(f"  [{status_simbolo}] {v.criterio}: {v.mensagem} (Calc: {v.valor_calculado} | Lim: {v.limite_normativo})")
            
    except Exception as e:
        print(f"!!! Falha Excepcional no Motor !!!\nErro: {e}")

if __name__ == '__main__':
    # Teste 1: Chuveiro (TUE)
    simular_circuito(potencia_W=5500, tensao_V=220, comp_m=10, material="COBRE", isolacao="PVC", agrup=1, tipo=TipoCircuito.TUE)
    
    # Teste 2: Ar Condicionado (MOTOR, Distância Longa, Agrupado, XLPE)
    simular_circuito(potencia_W=2000, tensao_V=220, comp_m=35, material="COBRE", isolacao="XLPE", agrup=3, tipo=TipoCircuito.MOTOR)
    
    # Teste 3: TUGs (Tomadas normais)
    simular_circuito(potencia_W=1200, tensao_V=220, comp_m=15, material="COBRE", isolacao="PVC", agrup=2, tipo=TipoCircuito.TUG)
    
    # Teste 4: Iluminacao (para validar a seção mínima de 1.5mm²)
    simular_circuito(potencia_W=300, tensao_V=220, comp_m=12, material="COBRE", isolacao="PVC", agrup=1, tipo=TipoCircuito.ILUMINACAO)
    
    # Teste 5: Carga Extrema que ultrapasse a tabela (Erro na ampacidade)
    simular_circuito(potencia_W=150000, tensao_V=220, comp_m=50, material="COBRE", isolacao="PVC", agrup=1, tipo=TipoCircuito.DISTRIBUICAO, metodo="F")
