from enum import Enum

class CategoriaInfluencia(str, Enum):
    A = "A"  # Meio ambiente
    B = "B"  # Utilizacao
    C = "C"  # Construcao da edificacao

class InfluenciaMeioAmbiente(str, Enum):
    AA = "AA" # Temperatura
    AB = "AB" # Altitude
    AC = "AC" # Agua
    AD = "AD" # Corpos solidos
    AE = "AE" # Substancias corrosivas
    AF = "AF" # Impactos
    AG = "AG" # Vibracoes
    AH = "AH" # Radiacao solar
    AJ = "AJ" # Descargas atmosfericas
