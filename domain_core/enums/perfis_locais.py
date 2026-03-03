from enum import Enum

class PerfilNormativoLocal(str, Enum):
    """
    Identifica locais com restrições e métodos específicos segundo o Capítulo 9 da NBR 5410.
    """
    PADRAO = "padrao"
    BANHEIRO_CHUVEIRO = "banheiro_chuveiro"
    PISCINA = "piscina"
    SAUNA = "sauna"
    LOCAL_CONDUTIVO = "local_condutivo"
    AREA_EXTERNA_ESPECIAL = "area_externa_especial"
    OUTRO_ESPECIAL = "outro_especial"
