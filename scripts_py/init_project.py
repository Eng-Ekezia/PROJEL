import os
import sys
from pathlib import Path

# --- DEFINIÇÃO DO CONTEÚDO DOS ARQUIVOS (VERSÃO CORRIGIDA) ---

FILES = {
    "requirements.txt": "pydantic>=2.0\nfastapi\nuvicorn\n",
    
    "README.md": "# WebApp Dimensionamento NBR 5410\n\nProjeto de dimensionamento elétrico com foco didático.\n",

    # --- DOMAIN CORE: ENUMS ---
    "domain_core/enums/__init__.py": "",
    
    "domain_core/enums/aterramento.py": """from enum import Enum

class EsquemaAterramento(str, Enum):
    TT = "TT"
    TN_S = "TN-S"
    TN_C = "TN-C"
    TN_C_S = "TN-C-S"
    IT = "IT"
""",

    "domain_core/enums/circuitos.py": """from enum import Enum

class TipoCircuito(str, Enum):
    ILUMINACAO = "iluminacao"
    TUG = "tomadas_uso_geral"
    TUE = "tomadas_uso_especifico"

class CriticidadeCircuito(str, Enum):
    NORMAL = "normal"
    IMPORTANTE = "importante"
    ESSENCIAL = "essencial"
""",

    "domain_core/enums/zonas.py": """from enum import Enum

class TipoZona(str, Enum):
    RESIDENCIAL = "residencial"
    COMERCIAL = "comercial"
    INDUSTRIAL = "industrial"
    TECNICA = "tecnica"
    EXTERNA = "externa"
    PERSONALIZADA = "personalizada"
""",

    "domain_core/enums/influencias.py": """from enum import Enum

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
""",

    # --- DOMAIN CORE: SCHEMAS ---
    "domain_core/__init__.py": "",
    "domain_core/schemas/__init__.py": "",

    "domain_core/schemas/influencias.py": """from pydantic import BaseModel, Field, conint
from domain_core.enums.influencias import CategoriaInfluencia

class InfluenciaNormativa(BaseModel):
    categoria: CategoriaInfluencia
    codigo: str = Field(..., description="Ex: AC, BA, CE")
    classe: conint(ge=1, le=4)
    descricao: str = Field(..., min_length=5)
""",

    "domain_core/schemas/zona.py": """from pydantic import BaseModel, Field
from domain_core.enums.zonas import TipoZona
from .influencias import InfluenciaNormativa

class GrupoInfluencias(BaseModel):
    descricao_local: str = Field(
        ..., 
        description="Descricao do ambiente real. Ex: 'Parede externa sujeita a chuva'"
    )
    influencias: list[InfluenciaNormativa]

class ZonaDeInfluencia(BaseModel):
    id: str
    nome: str = Field(..., min_length=3)
    tipo_zona: TipoZona
    descricao: str | None = None
    influencias_externas: GrupoInfluencias

    def codigos_normativos(self) -> list[str]:
        return [
            f"{inf.codigo}{inf.classe}"
            for inf in self.influencias_externas.influencias
        ]
""",

    "domain_core/schemas/circuito.py": """from pydantic import BaseModel, Field, model_validator
from domain_core.enums.circuitos import TipoCircuito, CriticidadeCircuito

class Circuito(BaseModel):
    id: str
    identificador: str = Field(..., description="Ex: C1, TUG-01")
    tipo_circuito: TipoCircuito
    zona_id: str
    sobrescreve_influencias: bool = False
    tensao_nominal: float = Field(..., gt=0)
    comprimento_m: float = Field(..., gt=0)
    metodo_instalacao: str = Field(..., description="A1...F")
    material_condutor: str = Field(..., description="cobre/aluminio")
    isolacao: str = Field(..., description="PVC/EPR/XLPE")
    temperatura_ambiente: float = Field(..., gt=0)
    circuitos_agrupados: int = Field(..., ge=1)
    
    potencia_instalada_W: float | None = Field(default=None, gt=0)
    corrente_nominal_A: float | None = Field(default=None, gt=0)
    
    criticidade: CriticidadeCircuito = CriticidadeCircuito.NORMAL

    @model_validator(mode='after')
    def validar_potencia_ou_corrente(self):
        p = self.potencia_instalada_W
        i = self.corrente_nominal_A

        if p is None and i is None:
            raise ValueError("Obrigatorio informar 'potencia_instalada_W' OU 'corrente_nominal_A'")
        if p is not None and i is not None:
            raise ValueError("Conflito: Informe APENAS um. O sistema calculará o outro.")
        return self
""",

    "domain_core/schemas/projeto.py": """from pydantic import BaseModel, Field
from domain_core.enums.aterramento import EsquemaAterramento

class ProjetoEletrico(BaseModel):
    id: str
    nome: str = Field(..., min_length=3)
    tipo_instalacao: str
    tensao_sistema: str
    sistema: str
    esquema_aterramento: EsquemaAterramento
    descricao_aterramento: str | None = None
""",

    "domain_core/schemas/resultados.py": """from pydantic import BaseModel, Field

class ResultadoDimensionamento(BaseModel):
    corrente_projeto_A: float
    secao_condutor_mm2: float
    dispositivo_protecao: str
    queda_tensao_percentual: float
    alertas: list[str] = Field(default_factory=list)
    referencias_normativas: list[str] = Field(default_factory=list)
""",

    # --- SCRIPT DE TESTE AUTOMATICO ---
    "verify_setup.py": """import sys
import os

# Adiciona o diretorio atual ao path
sys.path.append(os.getcwd())

try:
    from pydantic import ValidationError
    from domain_core.schemas.circuito import Circuito
    from domain_core.enums.circuitos import TipoCircuito
    
    print("✅ [SETUP] Importações do Python e Pydantic OK.")

    # Teste 1: Criação Válida
    c1 = Circuito(
        id="uuid-1", identificador="C1", tipo_circuito=TipoCircuito.TUG, zona_id="z1",
        tensao_nominal=127, comprimento_m=10, metodo_instalacao="B1", material_condutor="cobre",
        isolacao="PVC", temperatura_ambiente=30, circuitos_agrupados=1,
        potencia_instalada_W=1200 # Apenas potencia
    )
    print(f"✅ [DOMINIO] Circuito válido criado com sucesso: {c1.identificador}")

    # Teste 2: Regra de Engenharia (Potencia E Corrente juntos = Erro)
    try:
        c_erro = Circuito(
            id="uuid-2", identificador="C_ERR", tipo_circuito=TipoCircuito.TUG, zona_id="z1",
            tensao_nominal=127, comprimento_m=10, metodo_instalacao="B1", material_condutor="cobre",
            isolacao="PVC", temperatura_ambiente=30, circuitos_agrupados=1,
            potencia_instalada_W=1000,
            corrente_nominal_A=10 # ERRO PROPOSITAL
        )
        print("❌ [FALHA] O sistema permitiu Potência e Corrente simultâneos (violação da regra).")
    except ValidationError as e:
        print("✅ [REGRAS] Validação de Potência vs Corrente funcionando! O sistema barrou dados ambíguos.")

    print("\\n🚀 TUDO PRONTO! O SETUP ESTÁ FUNCIONAL.")

except ImportError as e:
    print(f"❌ [ERRO] Falta instalar dependências. Rode: pip install -r requirements.txt\\nDetalhe: {e}")
except Exception as e:
    print(f"❌ [ERRO] Falha inesperada: {e}")
"""
}

def create_structure():
    base_dirs = ["frontend", "backend", "domain_core", "domain_core/enums", "domain_core/schemas", "docs"]
    
    print("--- INICIANDO SETUP DO PROJETO ---")
    
    # 1. Criar Pastas
    for d in base_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"📁 Pasta criada: {d}")

    # 2. Criar Arquivos
    for filename, content in FILES.items():
        path = Path(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Arquivo gerado: {filename}")

if __name__ == "__main__":
    create_structure()
    print("\n--- CONCLUSÃO ---")
    print("1. Crie/ative seu venv:  python -m venv .venv")
    print("2. Instale dependências: pip install -r requirements.txt")
    print("3. Rode o teste:         python verify_setup.py")