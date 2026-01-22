from enum import Enum

class TipoZona(str, Enum):
    RESIDENCIAL = "residencial"
    COMERCIAL = "comercial"
    INDUSTRIAL = "industrial"
    TECNICA = "tecnica"
    EXTERNA = "externa"
    PERSONALIZADA = "personalizada"
