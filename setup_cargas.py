import os

# ==============================================================================
# 1. ENUMS DE CARGAS (TIPOS)
# ==============================================================================
tipo_carga_content = r'''
from enum import Enum

class TipoCarga(str, Enum):
    ILUMINACAO = "ILUMINACAO"
    TUG = "TUG" # Tomada de Uso Geral
    TUE = "TUE" # Tomada de Uso Específico (Chuveiro, Ar, etc)
'''

# ==============================================================================
# 2. SCHEMA DE CARGA
# ==============================================================================
carga_schema_content = r'''
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..enums.cargas import TipoCarga

class CargaBase(BaseModel):
    nome: str = Field(..., description="Descrição da carga (ex: Lâmpada Centro, Tomada Geladeira)")
    tipo: TipoCarga = Field(default=TipoCarga.TUG)
    potencia_va: float = Field(..., gt=0, description="Potência Aparente (VA)")
    potencia_w: float = Field(..., gt=0, description="Potência Ativa (W)")
    fator_potencia: float = Field(default=1.0, ge=0, le=1, description="Fator de Potência (cos fi)")
    quantidade: int = Field(default=1, gt=0)
    
    # Vínculos
    local_id: str = Field(..., description="ID do Local onde a carga está instalada")
    # Nota: circuito_id será adicionado na Phase 07

class CargaCreate(CargaBase):
    pass

class Carga(CargaBase):
    id: str
    data_criacao: datetime

    class Config:
        from_attributes = True
'''

# ==============================================================================
# 3. ENDPOINT DE CARGAS (CRUD + CÁLCULO)
# ==============================================================================
endpoint_cargas_content = r'''
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
import uuid
from datetime import datetime

from domain_core.schemas.carga import Carga, CargaCreate
from domain_core.enums.cargas import TipoCarga

router = APIRouter()

# Simulação de Banco de Dados em Memória (para manter consistência neste exemplo)
# Na prática real, isso viria do banco de dados persistente ou seria apenas pass-through
cargas_db: List[Carga] = []

@router.post("/", response_model=Carga, status_code=status.HTTP_201_CREATED)
async def criar_carga(carga_in: CargaCreate):
    """
    Cria uma nova carga vinculada a um local.
    """
    nova_carga = Carga(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **carga_in.model_dump()
    )
    # Em um sistema real stateless, aqui apenas devolvemos o objeto validado
    # O Frontend é responsável por armazenar no Zustand.
    return nova_carga

@router.post("/calcular-minimo-nbr", status_code=200)
async def calcular_minimo_nbr(dados: Dict[str, float]):
    """
    Recebe { "area": 10.0, "perimetro": 12.0, "eh_cozinha_servico": true/false }
    Retorna { "iluminacao_va": 160, "tugs_quantidade": 3 }
    """
    area = dados.get("area", 0)
    perimetro = dados.get("perimetro", 0)
    eh_area_umida = bool(dados.get("eh_cozinha_servico", False)) # Cozinhas, Copas, A. Serviço
    
    # 1. Regra de Iluminação (Item 9.5.2.1.2)
    # - 6m2 ou menos: 100VA
    # - Mais que 6m2: 100VA + 60VA para cada 4m2 inteiros
    potencia_ilum = 0
    if area <= 6:
        potencia_ilum = 100
    else:
        potencia_ilum = 100 + (int((area - 6) / 4) * 60)
        
    # 2. Regra de TUGs (Item 9.5.2.2.1)
    qtd_tugs = 0
    if eh_area_umida:
        # Cozinhas/Serviço: 1 tomada a cada 3,5m de perímetro
        qtd_tugs = int(perimetro / 3.5)
        if perimetro % 3.5 > 0: # Arredonda para cima
            qtd_tugs += 1 
        if qtd_tugs < 2: qtd_tugs = 2 # Mínimo sensato
    else:
        # Salas/Quartos (Áreas secas): 1 tomada a cada 5m de perímetro
        qtd_tugs = int(perimetro / 5)
        if perimetro % 5 > 0:
            qtd_tugs += 1
        if qtd_tugs < 1: qtd_tugs = 1

    return {
        "norma_iluminacao_va": potencia_ilum,
        "norma_tugs_quantidade": qtd_tugs
    }
'''

# ==============================================================================
# 4. ATUALIZAR API ROUTER
# ==============================================================================
api_router_content = r'''
from fastapi import APIRouter
from backend.api.v1.endpoints import system, zonas, locais, cargas

api_router = APIRouter()

# Rotas de Sistema
api_router.include_router(system.router, prefix="/system", tags=["system"])

# Rotas de Domínio (Phase 06)
api_router.include_router(zonas.router, prefix="/zonas", tags=["zonas - influências"])
api_router.include_router(locais.router, prefix="/locais", tags=["locais - arquitetura"])
api_router.include_router(cargas.router, prefix="/cargas", tags=["cargas - equipamentos"])
'''

def main():
    base_dir = os.getcwd()
    
    # Criar diretórios se necessário
    os.makedirs(os.path.join(base_dir, "domain_core/enums"), exist_ok=True)
    
    # Escrever Arquivos
    files = {
        "domain_core/enums/cargas.py": tipo_carga_content,
        "domain_core/schemas/carga.py": carga_schema_content,
        "backend/api/v1/endpoints/cargas.py": endpoint_cargas_content,
        "backend/api/v1/api.py": api_router_content
    }
    
    for path, content in files.items():
        full_path = os.path.join(base_dir, path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Criado/Atualizado: {path}")

    print("\n--- Backend preparado para Cargas! ---")
    print("1. Reinicie o Backend (Ctrl+C -> uvicorn main:app --reload)")
    print("2. Agora podemos criar a UI de Cargas no Frontend.")

if __name__ == "__main__":
    main()