from enum import Enum

class EsquemaAterramento(str, Enum):
    TT = "TT"
    TN_S = "TN-S"
    TN_C = "TN-C"
    TN_C_S = "TN-C-S"
    IT = "IT"
