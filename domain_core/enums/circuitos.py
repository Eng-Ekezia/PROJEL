from enum import Enum

class TipoCircuito(str, Enum):
    ILUMINACAO = "iluminacao"
    TUG = "tomadas_uso_geral"
    TUE = "tomadas_uso_especifico"

class CriticidadeCircuito(str, Enum):
    NORMAL = "normal"
    IMPORTANTE = "importante"
    ESSENCIAL = "essencial"
