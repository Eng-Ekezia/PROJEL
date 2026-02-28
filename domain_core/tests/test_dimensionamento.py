import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain_core.schemas.projeto import ProjetoEletrico
from domain_core.schemas.local import Local
from domain_core.schemas.zona import Zona
from domain_core.schemas.circuito import Circuito
from domain_core.enums.circuitos import TipoCircuito
from domain_core.enums.influencias import TemperaturaAmbiente

from domain_core.engine.dimensionador_projeto import DimensionadorProjeto
from domain_core.schemas.resultados import StatusDimensionamento

def test_dimensionador_completo_basico():
    projeto = ProjetoEletrico(
        id="p1", nome="Casa", tipo_instalacao="Residencial",
        tensao_sistema="220/127", sistema="Trifásico", esquema_aterramento="TN-S"
    )
    
    zona = Zona(id="z1", projeto_id="p1", nome="Quarto", temp_ambiente=TemperaturaAmbiente.AA4, data_criacao="2024-01-01T00:00")
    local = Local(id="l1", zona_id="z1", projeto_id="p1", nome="Dormitório 1", area_m2=12.0, perimetro_m=14.0, uso="Dormitório", data_criacao="2024-01-01T00:00")
    
    # Circuito 2000W em 220V -> ~9.09V -> Cabo de 1.5 aguenta (se ilum ou TUG dependera do limite q setou 2.5) -> vamos forçar 2.5 pra TUG
    circuito = Circuito(
        id="c1", identificador="TUG-01", tipo_circuito=TipoCircuito.TUG,
        zona_id="z1", tensao_nominal=220, comprimento_m=15,
        metodo_instalacao="B1", material_condutor="cobre", isolacao="PVC_70C",
        temperatura_ambiente=30, circuitos_agrupados=1,
        potencia_instalada_W=2000, corrente_nominal_A=None
    )
    
    engine = DimensionadorProjeto()
    res = engine.processar_circuito(projeto, [local], zona, circuito, has_dr=False)
    
    # 2000 / (220 * 0.92) = ~9.88A
    assert res.corrente_projeto_ib > 9.8 and res.corrente_projeto_ib < 9.9
    assert res.secao_condutor_mm2 == 2.5
    assert res.disjuntor_nominal_in in [10, 16] # 10 ou 16 cobrem bem. Na vdd 10 coberia 9.09, o codigo pega o primeiro maior ou igual, pegou 10 provavelmente
    assert res.status_global == StatusDimensionamento.OK
    assert len(res.verificacoes) > 0
