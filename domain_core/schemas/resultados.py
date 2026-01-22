from pydantic import BaseModel, Field

class ResultadoDimensionamento(BaseModel):
    corrente_projeto_A: float
    secao_condutor_mm2: float
    dispositivo_protecao: str
    queda_tensao_percentual: float
    alertas: list[str] = Field(default_factory=list)
    referencias_normativas: list[str] = Field(default_factory=list)
