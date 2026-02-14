from enum import Enum

# ============================================================
# ENUMS - VALORES "PUROS" PARA USO EM BANCO DE DADOS / MODELO
# Códigos conforme NBR 5410: AA, AB, AC, AD, AE, AF, AG, AH,
# AK, AL, AM, AN, AQ, AR, AS, BA, BB, BC, BD, BE, CA, CB.
# ============================================================

# --- Meio ambiente (A*) ---

class TemperaturaAmbiente(str, Enum):
    AA1 = "AA1"
    AA2 = "AA2"
    AA3 = "AA3"
    AA4 = "AA4"
    AA5 = "AA5"
    AA6 = "AA6"
    AA7 = "AA7"
    AA8 = "AA8"


class CondicoesClimaticas(str, Enum):
    AB1 = "AB1"
    AB2 = "AB2"
    AB3 = "AB3"
    AB4 = "AB4"
    AB5 = "AB5"
    AB6 = "AB6"
    AB7 = "AB7"
    AB8 = "AB8"


class Altitude(str, Enum):
    AC1 = "AC1"
    AC2 = "AC2"


class PresencaAgua(str, Enum):
    AD1 = "AD1"
    AD2 = "AD2"
    AD3 = "AD3"
    AD4 = "AD4"
    AD5 = "AD5"
    AD6 = "AD6"
    AD7 = "AD7"
    AD8 = "AD8"


class PresencaSolidos(str, Enum):
    AE1 = "AE1"
    AE2 = "AE2"
    AE3 = "AE3"
    AE4 = "AE4"
    AE5 = "AE5"
    AE6 = "AE6"


class SubstanciasCorrosivasPoluentes(str, Enum):
    AF1 = "AF1"
    AF2 = "AF2"
    AF3 = "AF3"
    AF4 = "AF4"


class SolicitacoesMecanicasImpacto(str, Enum):
    AG1 = "AG1"
    AG2 = "AG2"
    AG3 = "AG3"


class SolicitacoesMecanicasVibracao(str, Enum):
    AH1 = "AH1"
    AH2 = "AH2"
    AH3 = "AH3"


class FloraMofo(str, Enum):
    AK1 = "AK1"
    AK2 = "AK2"


class Fauna(str, Enum):
    AL1 = "AL1"
    AL2 = "AL2"


class FenomenosEM_BaixaFreq(str, Enum):
    # Grupo AM1 a AM9 – baixa frequência conduzida/radiada, conforme Tabela 10 e 11.
    # Aqui agrupamos em um único Enum, discriminando no texto.
    AM1_1 = "AM1-1"
    AM1_2 = "AM1-2"
    AM1_3 = "AM1-3"
    AM2_1 = "AM2-1"
    AM2_2 = "AM2-2"
    AM2_3 = "AM2-3"
    AM3_1 = "AM3-1"
    AM3_2 = "AM3-2"
    AM4   = "AM4"
    AM5   = "AM5"
    AM6   = "AM6"
    AM7   = "AM7"
    AM8_1 = "AM8-1"
    AM8_2 = "AM8-2"
    AM9_1 = "AM9-1"
    AM9_2 = "AM9-2"
    AM9_3 = "AM9-3"
    AM9_4 = "AM9-4"


class FenomenosEM_AltaFreq(str, Enum):
    # Grupo AM21, AM22, AM23, AM24, AM25 – alta frequência, transitórios, radiação.
    AM21 = "AM21"
    AM22_1 = "AM22-1"
    AM22_2 = "AM22-2"
    AM22_3 = "AM22-3"
    AM22_4 = "AM22-4"
    AM23_1 = "AM23-1"
    AM23_2 = "AM23-2"
    AM23_3 = "AM23-3"
    AM24_1 = "AM24-1"
    AM24_2 = "AM24-2"
    AM25_1 = "AM25-1"
    AM25_2 = "AM25-2"
    AM25_3 = "AM25-3"


class DescargasEletrostaticas(str, Enum):
    AM31_1 = "AM31-1"
    AM31_2 = "AM31-2"
    AM31_3 = "AM31-3"
    AM31_4 = "AM31-4"


class RadiacoesIonizantes(str, Enum):
    AM41_1 = "AM41-1"


class RadiacaoSolar(str, Enum):
    AN1 = "AN1"
    AN2 = "AN2"
    AN3 = "AN3"


class DescargasAtmosfericas(str, Enum):
    AQ1 = "AQ1"
    AQ2 = "AQ2"
    AQ3 = "AQ3"


class MovimentacaoAr(str, Enum):
    AR1 = "AR1"
    AR2 = "AR2"
    AR3 = "AR3"


class Vento(str, Enum):
    AS1 = "AS1"
    AS2 = "AS2"
    AS3 = "AS3"


# --- Utilização (B*) ---

class CompetenciaPessoas(str, Enum):
    BA1 = "BA1"
    BA2 = "BA2"
    BA3 = "BA3"
    BA4 = "BA4"
    BA5 = "BA5"


class ResistividadeCorpoHumano(str, Enum):
    BB1 = "BB1"
    BB2 = "BB2"
    BB3 = "BB3"
    BB4 = "BB4"


class ContatoPotencialTerra(str, Enum):
    BC1 = "BC1"
    BC2 = "BC2"
    BC3 = "BC3"
    BC4 = "BC4"


class FugaEmergencia(str, Enum):
    BD1 = "BD1"
    BD2 = "BD2"
    BD3 = "BD3"
    BD4 = "BD4"


class MateriaisProcessadosArmazenados(str, Enum):
    BE1 = "BE1"
    BE2 = "BE2"
    BE3 = "BE3"
    BE4 = "BE4"


# --- Construção das edificações (C*) ---

class MateriaisConstrucao(str, Enum):
    CA1 = "CA1"
    CA2 = "CA2"


class EstruturaEdificacao(str, Enum):
    CB1 = "CB1"
    CB2 = "CB2"
    CB3 = "CB3"
    CB4 = "CB4"


# ============================================================
# MAPA DE DESCRIÇÕES PARA A UI
# (Textos resumidos / adaptados para não reproduzir
# literalmente a NBR 5410. Ajuste conforme sua necessidade.)
# ============================================================

DESCRICOES_INFLUENCIAS = {
    # ---------------- Temperatura ambiente (Tabela 1) ----------------
    "TemperaturaAmbiente": {
        TemperaturaAmbiente.AA1.value: "AA1 - Frigorífico, cerca de -60 °C a +5 °C (câmaras frias e ambientes muito frios).",
        TemperaturaAmbiente.AA2.value: "AA2 - Muito frio, aproximadamente -40 °C a +5 °C.",
        TemperaturaAmbiente.AA3.value: "AA3 - Frio moderado, em torno de -25 °C a +5 °C.",
        TemperaturaAmbiente.AA4.value: "AA4 - Temperado, cerca de -5 °C a +40 °C, típico de interiores comuns.",
        TemperaturaAmbiente.AA5.value: "AA5 - Quente, de +5 °C a +40 °C em locais internos com aquecimento.",
        TemperaturaAmbiente.AA6.value: "AA6 - Muito quente, de +5 °C a +60 °C (ambientes com forte aquecimento).",
        TemperaturaAmbiente.AA7.value: "AA7 - Faixa extrema, aproximadamente -25 °C a +55 °C.",
        TemperaturaAmbiente.AA8.value: "AA8 - Faixa expandida, cerca de -50 °C a +40 °C.",
    },

    # ---------------- Condições climáticas (Tabela 2) ----------------
    "CondicoesClimaticas": {
        CondicoesClimaticas.AB1.value: "AB1 - Clima extremamente frio e seco, com possível umidade até saturação em baixas temperaturas.",
        CondicoesClimaticas.AB2.value: "AB2 - Clima frio, com temperaturas negativas moderadas e ampla faixa de umidade.",
        CondicoesClimaticas.AB3.value: "AB3 - Clima frio menos severo, com temperaturas um pouco abaixo de zero e umidade variável.",
        CondicoesClimaticas.AB4.value: "AB4 - Locais abrigados sem controle rígido de temperatura e umidade, faixa de 5 °C a 40 °C.",
        CondicoesClimaticas.AB5.value: "AB5 - Ambientes internos com temperatura ambiente controlada e umidade moderada.",
        CondicoesClimaticas.AB6.value: "AB6 - Ambientes muito quentes, internos ou externos, sujeitos a calor intenso e alta umidade.",
        CondicoesClimaticas.AB7.value: "AB7 - Locais abrigados sujeitos a radiação solar, sem controle de temperatura e umidade.",
        CondicoesClimaticas.AB8.value: "AB8 - Ambientes externos sem proteção contra intempéries, com grandes variações térmicas e de umidade.",
    },

    # ---------------- Altitude (Tabela 3) ----------------
    "Altitude": {
        Altitude.AC1.value: "AC1 - Altitude baixa, até cerca de 2000 m acima do nível do mar.",
        Altitude.AC2.value: "AC2 - Altitude elevada, acima de 2000 m, podendo exigir medidas especiais.",
    },

    # ---------------- Presença de água (Tabela 4) ----------------
    "PresencaAgua": {
        PresencaAgua.AD1.value: "AD1 - Ausência prática de água; umidade eventual, paredes que secam rapidamente.",
        PresencaAgua.AD2.value: "AD2 - Possibilidade de gotejamento vertical ou condensação em gotas.",
        PresencaAgua.AD3.value: "AD3 - Possibilidade de chuva incidindo em ângulo limitado, formando película de água.",
        PresencaAgua.AD4.value: "AD4 - Aspersão de água em qualquer direção, semelhante a chuva forçada.",
        PresencaAgua.AD5.value: "AD5 - Jatos de água sob pressão, vindos de qualquer direção.",
        PresencaAgua.AD6.value: "AD6 - Ondas de água, típico de áreas à beira-mar.",
        PresencaAgua.AD7.value: "AD7 - Imersão parcial ou total, de forma intermitente, limitada em profundidade.",
        PresencaAgua.AD8.value: "AD8 - Submersão permanente, com pressão superior a cerca de 0,1 bar.",
    },

    # ---------------- Presença de corpos sólidos (Tabela 5 / 6) ----------------
    "PresencaSolidos": {
        PresencaSolidos.AE1.value: "AE1 - Praticamente sem poeira ou corpos estranhos relevantes.",
        PresencaSolidos.AE2.value: "AE2 - Pequenos objetos sólidos, com dimensões a partir de aproximadamente 2,5 mm.",
        PresencaSolidos.AE3.value: "AE3 - Objetos muito pequenos, com dimensões a partir de cerca de 1 mm.",
        PresencaSolidos.AE4.value: "AE4 - Leve deposição de poeira por dia em superfícies.",
        PresencaSolidos.AE5.value: "AE5 - Deposição média de poeira em superfícies ao longo do dia.",
        PresencaSolidos.AE6.value: "AE6 - Deposição intensa de poeira, com acúmulo elevado diário.",
    },

    # ---------------- Substâncias corrosivas / poluentes (Tabela 7) ----------------
    "SubstanciasCorrosivasPoluentes": {
        SubstanciasCorrosivasPoluentes.AF1.value: "AF1 - Agentes corrosivos ou poluentes não significativos.",
        SubstanciasCorrosivasPoluentes.AF2.value: "AF2 - Atmosfera com agentes corrosivos ou poluentes de origem externa relevante.",
        SubstanciasCorrosivasPoluentes.AF3.value: "AF3 - Contato intermitente ou acidental com produtos químicos de uso corrente.",
        SubstanciasCorrosivasPoluentes.AF4.value: "AF4 - Presença permanente de produtos químicos corrosivos em quantidades significativas.",
    },

    # ---------------- Solicitações mecânicas (Tabela 7) ----------------
    "SolicitacoesImpacto": {
        SolicitacoesMecanicasImpacto.AG1.value: "AG1 - Impactos fracos, típicos de uso residencial e escritórios.",
        SolicitacoesMecanicasImpacto.AG2.value: "AG2 - Impactos médios, típicos de ambientes industriais usuais.",
        SolicitacoesMecanicasImpacto.AG3.value: "AG3 - Impactos severos, comuns em ambientes industriais pesados.",
    },
    "SolicitacoesVibracao": {
        SolicitacoesMecanicasVibracao.AH1.value: "AH1 - Vibrações fracas ou desprezíveis, como em uso doméstico.",
        SolicitacoesMecanicasVibracao.AH2.value: "AH2 - Vibrações médias em ambiente industrial normal.",
        SolicitacoesMecanicasVibracao.AH3.value: "AH3 - Vibrações severas em ambientes industriais severos.",
    },

    # ---------------- Flora e mofo (Tabela 8) ----------------
    "FloraMofo": {
        FloraMofo.AK1.value: "AK1 - Sem risco significativo por vegetação ou mofo.",
        FloraMofo.AK2.value: "AK2 - Possível crescimento ou abundância de vegetação e fungos com efeito prejudicial.",
    },

    # ---------------- Fauna (Tabela 9) ----------------
    "Fauna": {
        Fauna.AL1.value: "AL1 - Sem risco relevante devido a animais.",
        Fauna.AL2.value: "AL2 - Riscos associados a insetos, pássaros ou pequenos animais em quantidade ou natureza agressiva.",
    },

    # ---------------- Fenômenos EM baixa frequência (Tabelas 10 e 11) ----------------
    "FenomenosEM_BaixaFreq": {
        FenomenosEM_BaixaFreq.AM1_1.value: "AM1-1 - Harmônicas/inter-harmônicas em nível controlado (ambiente muito protegido).",
        FenomenosEM_BaixaFreq.AM1_2.value: "AM1-2 - Harmônicas/inter-harmônicas em nível normal de rede BT.",
        FenomenosEM_BaixaFreq.AM1_3.value: "AM1-3 - Harmônicas/inter-harmônicas em nível elevado, redes poluídas.",
        FenomenosEM_BaixaFreq.AM2_1.value: "AM2-1 - Tensões de sinalização residuais em ambiente muito controlado.",
        FenomenosEM_BaixaFreq.AM2_2.value: "AM2-2 - Tensões de sinalização usuais em redes residenciais, comerciais e industriais.",
        FenomenosEM_BaixaFreq.AM2_3.value: "AM2-3 - Tensões de sinalização elevadas, com possíveis ressonâncias.",
        FenomenosEM_BaixaFreq.AM3_1.value: "AM3-1 - Variações de tensão limitadas por uso de alimentação condicionada (UPS).",
        FenomenosEM_BaixaFreq.AM3_2.value: "AM3-2 - Variações/flutuações normais de tensão, afundamentos e interrupções usuais.",
        FenomenosEM_BaixaFreq.AM4.value: "AM4 - Desequilíbrio de tensão em nível normal conforme limites de rede.",
        FenomenosEM_BaixaFreq.AM5.value: "AM5 - Pequenas variações de frequência em condições usuais.",
        FenomenosEM_BaixaFreq.AM6.value: "AM6 - Tensões induzidas de baixa frequência (modo comum), contínuas ou em faltas.",
        FenomenosEM_BaixaFreq.AM7.value: "AM7 - Componentes contínuas em redes CA, associadas a retificadores.",
        FenomenosEM_BaixaFreq.AM8_1.value: "AM8-1 - Campos magnéticos radiados em nível médio, próximos a equipamentos típicos.",
        FenomenosEM_BaixaFreq.AM8_2.value: "AM8-2 - Campos magnéticos radiados em nível alto, em proximidade de linhas e subestações.",
        FenomenosEM_BaixaFreq.AM9_1.value: "AM9-1 - Campos elétricos desprezíveis.",
        FenomenosEM_BaixaFreq.AM9_2.value: "AM9-2 - Campos elétricos em nível médio, conforme tensão/localização.",
        FenomenosEM_BaixaFreq.AM9_3.value: "AM9-3 - Campos elétricos em nível alto, como perto de linhas AT.",
        FenomenosEM_BaixaFreq.AM9_4.value: "AM9-4 - Campos elétricos em nível muito alto, em forte proximidade de AT.",
    },

    # ---------------- Fenômenos EM alta frequência (Tabela 11) ----------------
    "FenomenosEM_AltaFreq": {
        FenomenosEM_AltaFreq.AM21.value: "AM21 - Tensões ou correntes oscilantes induzidas em baixa intensidade.",
        FenomenosEM_AltaFreq.AM22_1.value: "AM22-1 - Transitórios conduzidos muito baixos em ambiente protegido.",
        FenomenosEM_AltaFreq.AM22_2.value: "AM22-2 - Transitórios conduzidos de nível médio em ambiente protegido.",
        FenomenosEM_AltaFreq.AM22_3.value: "AM22-3 - Transitórios conduzidos altos por chaveamentos/curtos em BT.",
        FenomenosEM_AltaFreq.AM22_4.value: "AM22-4 - Transitórios conduzidos muito altos em subestações e indústrias pesadas.",
        FenomenosEM_AltaFreq.AM23_1.value: "AM23-1 - Sobretensões transitórias com proteção contra surtos aplicada.",
        FenomenosEM_AltaFreq.AM23_2.value: "AM23-2 - Sobretensões de origem atmosférica distante ou chaveamentos usuais.",
        FenomenosEM_AltaFreq.AM23_3.value: "AM23-3 - Sobretensões de origem atmosférica próxima ou em redes aéreas.",
        FenomenosEM_AltaFreq.AM24_1.value: "AM24-1 - Transitórios oscilantes de nível médio por manobras normais.",
        FenomenosEM_AltaFreq.AM24_2.value: "AM24-2 - Transitórios oscilantes elevados em subestações AT/MT.",
        FenomenosEM_AltaFreq.AM25_1.value: "AM25-1 - Perturbações radiadas desprezíveis (estações distantes).",
        FenomenosEM_AltaFreq.AM25_2.value: "AM25-2 - Nível médio de perturbações radiadas, com transceptores próximos.",
        FenomenosEM_AltaFreq.AM25_3.value: "AM25-3 - Nível alto de perturbações radiadas, transceptores de alta potência.",
    },

    # ---------------- Descargas eletrostáticas (Tabela 12) ----------------
    "DescargasEletrostaticas": {
        DescargasEletrostaticas.AM31_1.value: "AM31-1 - Nível baixo de descargas eletrostáticas, conforme ensaios de nível 1.",
        DescargasEletrostaticas.AM31_2.value: "AM31-2 - Nível médio de descargas eletrostáticas.",
        DescargasEletrostaticas.AM31_3.value: "AM31-3 - Nível alto de descargas eletrostáticas.",
        DescargasEletrostaticas.AM31_4.value: "AM31-4 - Nível muito alto, com descargas geradas por deslocamento sobre carpetes sintéticos.",
    },

    # ---------------- Radiações ionizantes (Tabela 13) ----------------
    "RadiacoesIonizantes": {
        RadiacoesIonizantes.AM41_1.value: "AM41-1 - Presença de radiações ionizantes perigosas, sem gradação adicional.",
    },

    # ---------------- Radiação solar (Tabela 14) ----------------
    "RadiacaoSolar": {
        RadiacaoSolar.AN1.value: "AN1 - Intensidade de radiação solar reduzida, até cerca de 500 W/m².",
        RadiacaoSolar.AN2.value: "AN2 - Radiação solar média, até cerca de 700 W/m².",
        RadiacaoSolar.AN3.value: "AN3 - Radiação solar alta, podendo ultrapassar 700 W/m².",
    },

    # ---------------- Descargas atmosféricas (Tabela 15) ----------------
    "DescargasAtmosfericas": {
        DescargasAtmosfericas.AQ1.value: "AQ1 - Influência desprezível de descargas atmosféricas (poucos dias de trovoada por ano).",
        DescargasAtmosfericas.AQ2.value: "AQ2 - Influência indireta, via rede de alimentação, com número moderado de dias de trovoada.",
        DescargasAtmosfericas.AQ3.value: "AQ3 - Influência direta em partes externas da instalação, expostas a descargas.",
    },

    # ---------------- Movimentação do ar (Tabela 16) ----------------
    "MovimentacaoAr": {
        MovimentacaoAr.AR1.value: "AR1 - Velocidade de ar desprezível, até cerca de 1 m/s.",
        MovimentacaoAr.AR2.value: "AR2 - Velocidade média do ar, entre cerca de 1 m/s e 5 m/s.",
        MovimentacaoAr.AR3.value: "AR3 - Movimentação forte de ar, acima de aproximadamente 5 m/s.",
    },

    # ---------------- Vento (Tabela 17) ----------------
    "Vento": {
        Vento.AS1.value: "AS1 - Vento fraco ou desprezível, até cerca de 20 m/s.",
        Vento.AS2.value: "AS2 - Vento médio, entre aproximadamente 20 m/s e 30 m/s.",
        Vento.AS3.value: "AS3 - Vento forte, até cerca de 50 m/s.",
    },

    # ---------------- Competência das pessoas (Tabela 18) ----------------
    "CompetenciaPessoas": {
        CompetenciaPessoas.BA1.value: "BA1 - Pessoas comuns, sem formação específica em eletricidade.",
        CompetenciaPessoas.BA2.value: "BA2 - Crianças em locais a elas destinados, como creches e escolas.",
        CompetenciaPessoas.BA3.value: "BA3 - Pessoas com limitações físicas ou cognitivas, como idosos e doentes.",
        CompetenciaPessoas.BA4.value: "BA4 - Pessoas advertidas ou supervisionadas por pessoal qualificado.",
        CompetenciaPessoas.BA5.value: "BA5 - Pessoas qualificadas tecnicamente para lidar com riscos elétricos.",
    },

    # ---------------- Resistência elétrica do corpo humano (Tabela 19) ----------------
    "ResistividadeCorpoHumano": {
        ResistividadeCorpoHumano.BB1.value: "BB1 - Condições secas, com resistência elevada da pele.",
        ResistividadeCorpoHumano.BB2.value: "BB2 - Condições úmidas, pele suada e contato significativo.",
        ResistividadeCorpoHumano.BB3.value: "BB3 - Condições molhadas, pés em água e resistência da pele reduzida.",
        ResistividadeCorpoHumano.BB4.value: "BB4 - Corpo imerso, como em banheiras ou piscinas.",
    },

    # ---------------- Contato com potencial da terra (Tabela 20) ----------------
    "ContatoPotencialTerra": {
        ContatoPotencialTerra.BC1.value: "BC1 - Locais não condutivos, com piso e paredes isolantes.",
        ContatoPotencialTerra.BC2.value: "BC2 - Contato raro com partes condutivas ou superfícies condutivas.",
        ContatoPotencialTerra.BC3.value: "BC3 - Contato frequente com elementos ou pisos condutivos.",
        ContatoPotencialTerra.BC4.value: "BC4 - Contato praticamente contínuo com superfícies metálicas, com pouca possibilidade de interrupção voluntária.",
    },

    # ---------------- Condições de fuga em emergências (Tabela 21) ----------------
    "FugaEmergencia": {
        FugaEmergencia.BD1.value: "BD1 - Rotas de fuga normais, baixa densidade de ocupação e percurso curto.",
        FugaEmergencia.BD2.value: "BD2 - Rotas de fuga longas, baixa densidade de ocupação.",
        FugaEmergencia.BD3.value: "BD3 - Situações tumultuadas com grande concentração de pessoas e percursos curtos.",
        FugaEmergencia.BD4.value: "BD4 - Fuga longa e tumultuada, em grandes edifícios de uso público.",
    },

    # ---------------- Materiais processados / armazenados (Tabela 22) ----------------
    "MateriaisProcessadosArmazenados": {
        MateriaisProcessadosArmazenados.BE1.value: "BE1 - Riscos desprezíveis quanto a incêndio ou explosão.",
        MateriaisProcessadosArmazenados.BE2.value: "BE2 - Riscos de incêndio por materiais combustíveis, como fibras ou líquidos com alto ponto de fulgor.",
        MateriaisProcessadosArmazenados.BE3.value: "BE3 - Riscos de explosão por gases, vapores ou pós combustíveis.",
        MateriaisProcessadosArmazenados.BE4.value: "BE4 - Riscos de contaminação de alimentos ou produtos sensíveis.",
    },

    # ---------------- Materiais de construção (Tabela 23) ----------------
    "MateriaisConstrucao": {
        MateriaisConstrucao.CA1.value: "CA1 - Edificações predominantemente constituídas de materiais não combustíveis.",
        MateriaisConstrucao.CA2.value: "CA2 - Edificações com materiais combustíveis, como madeira.",
    },

    # ---------------- Estrutura das edificações (Tabela 24) ----------------
    "EstruturaEdificacao": {
        EstruturaEdificacao.CB1.value: "CB1 - Riscos estruturais desprezíveis quanto à propagação de incêndio ou movimentação.",
        EstruturaEdificacao.CB2.value: "CB2 - Edificações que favorecem propagação de incêndio pela forma ou dimensões.",
        EstruturaEdificacao.CB3.value: "CB3 - Edificações sujeitas a deslocamentos relativos ou acomodação do terreno.",
        EstruturaEdificacao.CB4.value: "CB4 - Estruturas flexíveis ou instáveis, como tendas ou divisórias removíveis.",
    },
}
