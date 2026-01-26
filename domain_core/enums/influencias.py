from enum import Enum

# ==============================================================================
# 1. MEIO AMBIENTE (CÓDIGO A)
# ==============================================================================

class TemperaturaAmbiente(str, Enum):
    """
    Classificação AA - NBR 5410 (Tabela 1)
    Define a capacidade de condução de corrente dos cabos.
    """
    AA1 = "AA1 - Frigorífico (-60°C a +5°C)"
    AA2 = "AA2 - Muito Frio (-40°C a +5°C)"
    AA3 = "AA3 - Frio (-25°C a +5°C)"
    AA4 = "AA4 - Temperada (-5°C a +40°C)" # Padrão Geral BR
    AA5 = "AA5 - Quente (+5°C a +40°C)"
    AA6 = "AA6 - Muito Quente (+5°C a +60°C)"
    AA7 = "AA7 - Extrema (-25°C a +55°C)"
    AA8 = "AA8 - Faixa Expandida (-50°C a +40°C)"

class UmidadeAtmosferica(str, Enum):
    """
    Classificação AB - NBR 5410 (Tabela 2)
    Influencia na isolação e corrosão.
    """
    AB1 = "AB1 - Desprezível (Umidade relativa < 5% a 75%)"
    AB2 = "AB2 - Normal (Umidade relativa 10% a 75%)"
    AB3 = "AB3 - Alta (Umidade relativa 10% a 90%)"
    AB4 = "AB4 - Muito Alta (Umidade relativa 5% a 95% - Locais abrigados sem controle)"
    AB5 = "AB5 - Extrema (Umidade relativa 5% a 100% - Locais abrigados com controle)"
    AB6 = "AB6 - Condensação (Umidade relativa 10% a 100% - Externo)"
    AB7 = "AB7 - Alta variação (Umidade relativa 10% a 100% - Interno/Externo)"
    AB8 = "AB8 - Extrema variação (Umidade relativa 15% a 100%)"

class Altitude(str, Enum):
    """
    Classificação AC - NBR 5410 (Tabela 3)
    Afeta a rigidez dielétrica e refrigeração.
    """
    AC1 = "AC1 - Baixa (≤ 2.000 m)"
    AC2 = "AC2 - Alta (> 2.000 m)"

class PresencaAgua(str, Enum):
    """
    Classificação AD - NBR 5410 (Tabela 4)
    Define o Grau de Proteção (IP) mínimo dos equipamentos.
    """
    AD1 = "AD1 - Desprezível (Locais secos, IPX0)"
    AD2 = "AD2 - Gotejamento (Queda vertical, IPX1/IPX2)"
    AD3 = "AD3 - Aspersão (Chuva até 60°, IPX3)"
    AD4 = "AD4 - Projeções (Lavagens c/ mangueira, IPX4)"
    AD5 = "AD5 - Jatos (Jatos de água, IPX5)"
    AD6 = "AD6 - Ondas (Beira-mar, IPX6)"
    AD7 = "AD7 - Imersão (Piscinas/Espelhos d'água, IPX7)"
    AD8 = "AD8 - Submersão (Mergulho profundo, IPX8)"

class PresencaSolidos(str, Enum):
    """
    Classificação AE - NBR 5410 (Tabela 5)
    Define proteção contra poeira e corpos estranhos.
    """
    AE1 = "AE1 - Desprezível (Ambiente doméstico)"
    AE2 = "AE2 - Pequenos objetos (2.5mm)"
    AE3 = "AE3 - Objetos muito pequenos (1mm - Fios)"
    AE4 = "AE4 - Poeira leve"
    AE5 = "AE5 - Poeira moderada"
    AE6 = "AE6 - Poeira intensa (Cimento/Moinhos)"

class PresencaCorrosivos(str, Enum):
    """
    Classificação AF - NBR 5410 (Tabela 6)
    Afeta a escolha de materiais (eletrodutos, caixas).
    """
    AF1 = "AF1 - Desprezível"
    AF2 = "AF2 - Atmosférica (Presença de agentes corrosivos no ar)"
    AF3 = "AF3 - Intermitente (Contato acidental com químicos)"
    AF4 = "AF4 - Permanente (Indústria química)"

class ImpactosMecanicos(str, Enum):
    """
    Classificação AG - NBR 5410 (Tabela 7)
    Define a resistência mecânica (IK) dos equipamentos.
    """
    AG1 = "AG1 - Fracos (Impacto ≤ 0.225J - Doméstico/Escritório)"
    AG2 = "AG2 - Médios (Impacto ≤ 2J - Industrial leve)"
    AG3 = "AG3 - Severos (Impacto ≤ 20J - Industrial pesado)"

class Vibracoes(str, Enum):
    """
    Classificação AH - NBR 5410 (Tabela 8)
    """
    AH1 = "AH1 - Fracas (Doméstico)"
    AH2 = "AH2 - Médias (Industrial normal)"
    AH3 = "AH3 - Severas (Proximidade de máquinas pesadas)"

class PresencaFlora(str, Enum):
    """
    Classificação AK - NBR 5410 (Tabela 9)
    """
    AK1 = "AK1 - Desprezível (Sem risco de danos)"
    AK2 = "AK2 - Prejudicial (Risco de crescimento de fungos/plantas)"

class PresencaFauna(str, Enum):
    """
    Classificação AL - NBR 5410 (Tabela 10)
    """
    AL1 = "AL1 - Desprezível"
    AL2 = "AL2 - Prejudicial (Roedores, cupins, aves)"

class InfluenciaEletromagnetica(str, Enum):
    """
    Classificação AM - NBR 5410 (Tabela 11)
    Perturbações eletromagnéticas, eletrostáticas ou ionizantes.
    """
    AM1_1 = "AM1-1 - Harmônicas - Nível controlado"
    AM1_2 = "AM1-2 - Harmônicas - Nível normal"
    AM1_3 = "AM1-3 - Harmônicas - Nível alto"
    AM2_2 = "AM2-2 - Sinais de comando - Nível médio"
    AM3_1 = "AM3-1 - Flutuação de tensão - Nível controlado"
    AM3_2 = "AM3-2 - Flutuação de tensão - Nível normal"
    AM4 = "AM4 - Desequilíbrio de tensão"
    AM5 = "AM5 - Variação de frequência"
    AM8_1 = "AM8-1 - Campos magnéticos - Nível médio"
    AM8_2 = "AM8-2 - Campos magnéticos - Nível alto"
    AM9_1 = "AM9-1 - Campos elétricos - Nível baixo"
    AM9_2 = "AM9-2 - Campos elétricos - Nível médio"
    AM9_3 = "AM9-3 - Campos elétricos - Nível alto"
    AM22_1 = "AM22-1 - Descargas eletrostáticas - Ambiente protegido"
    AM23_2 = "AM23-2 - Descargas atmosféricas - Nível médio"
    AM24_1 = "AM24-1 - Transientes conduzidos - Nível médio"
    AM31_1 = "AM31-1 - Ondas oscilatórias - Nível baixo"
    AM41_1 = "AM41-1 - Radiações ionizantes - Sem risco significativo"
    # Nota: Existem muitos subníveis, listados os principais.

class RadiacaoSolar(str, Enum):
    """
    Classificação AN - NBR 5410 (Tabela 13)
    """
    AN1 = "AN1 - Desprezível"
    AN2 = "AN2 - Média (500 < I ≤ 700 W/m²)"
    AN3 = "AN3 - Alta (700 < I ≤ 1120 W/m²)"

class DescargasAtmosfericas(str, Enum):
    """
    Classificação AQ - NBR 5410 (Tabela 14)
    Define necessidade de SPDA e DPS.
    """
    AQ1 = "AQ1 - Desprezíveis (≤ 25 dias de trovoadas/ano)"
    AQ2 = "AQ2 - Indiretas (> 25 dias/ano - Riscos da rede)"
    AQ3 = "AQ3 - Diretas (Riscos de atingir a estrutura)"

class MovimentoAr(str, Enum):
    """
    Classificação AR - NBR 5410 (Tabela 15)
    """
    AR1 = "AR1 - Desprezível (v ≤ 1 m/s)"
    AR2 = "AR2 - Médio (1 < v ≤ 5 m/s)"
    AR3 = "AR3 - Forte (5 < v ≤ 10 m/s)"

class Vento(str, Enum):
    """
    Classificação AS - NBR 5410 (Tabela 16)
    """
    AS1 = "AS1 - Desprezível (v ≤ 20 m/s)"
    AS2 = "AS2 - Médio (20 < v ≤ 30 m/s)"
    AS3 = "AS3 - Forte (30 < v ≤ 50 m/s)"

# ==============================================================================
# 2. UTILIZAÇÃO (CÓDIGO B)
# ==============================================================================

class CompetenciaPessoas(str, Enum):
    """
    Classificação BA - NBR 5410 (Tabela 17)
    Define a necessidade de proteções adicionais contra choque.
    """
    BA1 = "BA1 - Comuns (Pessoas não advertidas)"
    BA2 = "BA2 - Crianças (Creches/Escolas infantis)"
    BA3 = "BA3 - Deficientes (Hospitais/Asilos)"
    BA4 = "BA4 - Advertidas (Zeladores/Manutenção)"
    BA5 = "BA5 - Qualificadas (Engenheiros/Técnicos)"

class ResistenciaCorpoHumano(str, Enum):
    """
    Classificação BB - NBR 5410 (Tabela 18)
    Relacionada às condições da pele (seca/molhada).
    """
    BB1 = "BB1 - Alta (Pele seca)"
    BB2 = "BB2 - Normal (Pele úmida/suada)"
    BB3 = "BB3 - Baixa (Pele molhada)"
    BB4 = "BB4 - Muito baixa (Pessoas imersas)"

class ContatoTerra(str, Enum):
    """
    Classificação BC - NBR 5410 (Tabela 19)
    Frequência de contato de pessoas com potencial de terra.
    """
    BC1 = "BC1 - Nulo (Locais não condutores)"
    BC2 = "BC2 - Raro (Situação comum em áreas secas)"
    BC3 = "BC3 - Frequente (Pessoas em contato com estruturas metálicas)"
    BC4 = "BC4 - Contínuo (Recintos condutores exíguos - Caldeiras)"

class CondicoesFuga(str, Enum):
    """
    Classificação BD - NBR 5410 (Tabela 20)
    Evacuação em caso de emergência.
    """
    BD1 = "BD1 - Normal (Baixa densidade, fuga fácil - Residencial)"
    BD2 = "BD2 - Longa (Baixa densidade, fuga difícil - Prédios altos)"
    BD3 = "BD3 - Tumultuada (Alta densidade, fuga fácil - Shoppings/Teatros)"
    BD4 = "BD4 - Longa e tumultuada (Alta densidade, fuga difícil - Hospitais/Estádios)"

class NaturezaMateriais(str, Enum):
    """
    Classificação BE - NBR 5410 (Tabela 21)
    Materiais processados ou armazenados.
    """
    BE1 = "BE1 - Riscos desprezíveis"
    BE2 = "BE2 - Riscos de incêndio (Papel, madeira, combustíveis)"
    BE3 = "BE3 - Riscos de explosão (Gases, poeiras explosivas)"
    BE4 = "BE4 - Riscos de contaminação (Alimentos, fármacos)"

# ==============================================================================
# 3. CONSTRUÇÃO DAS EDIFICAÇÕES (CÓDIGO C)
# ==============================================================================

class MateriaisConstrucao(str, Enum):
    """
    Classificação CA - NBR 5410 (Tabela 22)
    """
    CA1 = "CA1 - Não combustíveis (Alvenaria, concreto)"
    CA2 = "CA2 - Combustíveis (Madeira)"

class EstruturaEdificacao(str, Enum):
    """
    Classificação CB - NBR 5410 (Tabela 23)
    """
    CB1 = "CB1 - Riscos desprezíveis"
    CB2 = "CB2 - Sujeitas a propagação de incêndio (Efeito chaminé/Prédios altos)"
    CB3 = "CB3 - Sujeitas a movimentação (Estruturas longas/Solos instáveis)"
    CB4 = "CB4 - Flexíveis ou instáveis (Tendas, estruturas temporárias)"