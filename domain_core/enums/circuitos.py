from enum import Enum

class TipoCircuito(str, Enum):
    ILUMINACAO = "iluminacao"
    TUG = "tomadas_uso_geral"
    TUE = "tomadas_uso_especifico"
    DISTRIBUICAO = "distribuicao"
    MOTOR = "motor"

class CriticidadeCircuito(str, Enum):
    NORMAL = "normal"
    IMPORTANTE = "importante"
    ESSENCIAL = "essencial"

class MetodoInstalacao(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

# Descrições para UI (Human Readable)
DESCRICOES_METODOS = {
    MetodoInstalacao.A1: "Condutores isolados em eletroduto de seção circular embutido em parede termicamente isolante",
    MetodoInstalacao.A2: "Cabo multipolar em eletroduto de seção circular embutido em parede termicamente isolante",
    MetodoInstalacao.B1: "Condutores isolados em eletroduto de seção circular embutido em alvenaria",
    MetodoInstalacao.B2: "Cabo multipolar em eletroduto de seção circular embutido em alvenaria",
    MetodoInstalacao.C: "Cabos unipolares ou cabo multipolar sobre parede de madeira",
    MetodoInstalacao.D: "Cabo multipolar em eletroduto enterrado no solo",
    MetodoInstalacao.E: "Cabo multipolar ao ar livre",
    MetodoInstalacao.F: "Cabos unipolares justapostos ao ar livre",
    MetodoInstalacao.G: "Cabos unipolares espaçados ao ar livre"
}