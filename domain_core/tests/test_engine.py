import pytest
import os
import sys

# Corrige imports adicionando raiz do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain_core.engine.calculo_corrente import CalculoCorrente
from domain_core.engine.calculo_queda_tensao import CalculoQuedaTensao
from domain_core.engine.selecao_condutor import SelecaoCondutor
from domain_core.engine.selecao_disjuntor import SelecaoDisjuntor

def test_calculo_corrente():
    ib = CalculoCorrente.calcular_corrente_projeto(potencia_W=4400, tensao_V=220, fator_potencia=1.0)
    assert ib == 20.0
    
def test_calculo_queda_tensao():
    # 20A, cabo 2.5mm2, 10m cobre, 220V
    # dV_V = 2 * 0.0225 * 10 * 20 / 2.5 = 3.6V (1.63%)
    pct = CalculoQuedaTensao.calcular_queda_tensao_percentual(20, 2.5, 10, 220, 1)
    assert round(pct, 2) == 1.64
    
def test_selecao_condutor():
    # Cobre PVC A1 2 condutores na tabela
    # Seção 1.5 aguenta 14.5
    # Seção 2.5 aguenta 19.5
    # Seção 4.0 aguenta 26.0
    engine = SelecaoCondutor()
    
    # Exige TUG (minimo 2.5) e corrente 12 -> Retorna 2.5
    res1 = engine.selecionar_secao_por_corrente(12.0, "cobre", "PVC_70C", "A1", 2, is_iluminacao=False)
    assert res1 == 2.5
    
    # Exige 21A -> Retorna 4.0
    res2 = engine.selecionar_secao_por_corrente(21.0, "cobre", "PVC_70C", "A1", 2, is_iluminacao=False)
    assert res2 == 4.0
    
def test_selecao_disjuntor():
    # 20A projeto, cabo 4.0 (aguenta 26A) -> disp 20A ou 25A
    # Comerciais: 10, 16, 20, 25, 32
    # test IB <= IN <= IZ -> 14 <= IN <= 26 -> 16 ou 20 ou 25 comercial entra, seleciona o primeiro que cober no loop
    in_sel = SelecaoDisjuntor.selecionar_in_disjuntor(14.0, 26.0)
    assert in_sel == 16.0 
