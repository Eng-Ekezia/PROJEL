from enum import Enum

class TipoCarga(str, Enum):
    ILUMINACAO = "ILUMINACAO"
    TUG = "TUG" # Tomada de Uso Geral
    TUE = "TUE" # Tomada de Uso Específico (Chuveiro, Ar, etc)
    MOTOR = "MOTOR" # Motores elétricos, que têm características específicas de partida e demanda