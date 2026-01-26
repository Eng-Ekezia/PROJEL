from enum import Enum

# --- ENUMS (VALORES PUROS PARA O BANCO DE DADOS) ---

class TemperaturaAmbiente(str, Enum):
    AA1 = "AA1"
    AA2 = "AA2"
    AA3 = "AA3"
    AA4 = "AA4"
    AA5 = "AA5"
    AA6 = "AA6"
    AA7 = "AA7"
    AA8 = "AA8"

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

class CompetenciaPessoas(str, Enum):
    BA1 = "BA1"
    BA2 = "BA2"
    BA3 = "BA3"
    BA4 = "BA4"
    BA5 = "BA5"

class MateriaisConstrucao(str, Enum):
    CA1 = "CA1"
    CA2 = "CA2"

class EstruturaEdificacao(str, Enum):
    CB1 = "CB1"
    CB2 = "CB2"
    CB3 = "CB3"
    CB4 = "CB4"

# --- MAPA DE DESCRIÇÕES (PARA A UI) ---

DESCRICOES = {
    # Temperatura
    "AA1": "AA1 - Frigorífico (-60°C a +5°C)",
    "AA2": "AA2 - Muito Frio (-40°C a +5°C)",
    "AA3": "AA3 - Frio (-25°C a +5°C)",
    "AA4": "AA4 - Temperada (-5°C a +40°C)",
    "AA5": "AA5 - Quente (+5°C a +40°C)",
    "AA6": "AA6 - Muito Quente (+5°C a +60°C)",
    "AA7": "AA7 - Extrema (-25°C a +55°C)",
    "AA8": "AA8 - Faixa Expandida (-50°C a +40°C)",
    
    # Água
    "AD1": "AD1 - Desprezível (Locais secos, IPX0)",
    "AD2": "AD2 - Gotejamento (Queda vertical, IPX1/IPX2)",
    "AD3": "AD3 - Aspersão (Chuva até 60°, IPX3)",
    "AD4": "AD4 - Projeções (Lavagens c/ mangueira, IPX4)",
    "AD5": "AD5 - Jatos (Jatos de água, IPX5)",
    "AD6": "AD6 - Ondas (Beira-mar, IPX6)",
    "AD7": "AD7 - Imersão (Piscinas/Espelhos d'água, IPX7)",
    "AD8": "AD8 - Submersão (Mergulho profundo, IPX8)",

    # Sólidos
    "AE1": "AE1 - Desprezível (Ambiente doméstico)",
    "AE2": "AE2 - Pequenos objetos (2.5mm)",
    "AE3": "AE3 - Objetos muito pequenos (1mm - Fios)",
    "AE4": "AE4 - Poeira leve",
    "AE5": "AE5 - Poeira moderada",
    "AE6": "AE6 - Poeira intensa (Cimento/Moinhos)",

    # Pessoas
    "BA1": "BA1 - Comuns (Pessoas não advertidas)",
    "BA2": "BA2 - Crianças (Creches/Escolas infantis)",
    "BA3": "BA3 - Deficientes (Hospitais/Asilos)",
    "BA4": "BA4 - Advertidas (Zeladores/Manutenção)",
    "BA5": "BA5 - Qualificadas (Engenheiros/Técnicos)",

    # Construção
    "CA1": "CA1 - Não combustíveis (Alvenaria, concreto)",
    "CA2": "CA2 - Combustíveis (Madeira)",
    
    # Estrutura
    "CB1": "CB1 - Riscos desprezíveis",
    "CB2": "CB2 - Sujeita a propagação de incêndio",
    "CB3": "CB3 - Sujeita a movimentação",
    "CB4": "CB4 - Flexíveis ou instáveis"
}