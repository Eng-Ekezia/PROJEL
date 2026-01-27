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