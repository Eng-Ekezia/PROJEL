from fastapi import APIRouter
from typing import Dict, List
from domain_core.enums.circuitos import MetodoInstalacao, TipoCircuito, DESCRICOES_METODOS

router = APIRouter()

@router.get("/opcoes", response_model=Dict[str, List[Dict[str, str]]])
async def listar_opcoes_circuitos():
    """
    Retorna os Enums normativos para preencher os Selects do Frontend.
    Garante que a UI use exatamente o que o Domain Core valida.
    """
    return {
        "tipos": [
            {"codigo": e.value, "descricao": e.name.replace('_', ' ').title()} 
            for e in TipoCircuito
        ],
        "metodos_instalacao": [
            {"codigo": e.value, "descricao": f"{e.value} - {DESCRICOES_METODOS.get(e, '')}"}
            for e in MetodoInstalacao
        ]
    }


# --- FUTURO: Endpoints de CRUD de Circuitos (Fase 09 ou persistência real) ---
# Por enquanto, como o PROJEL é stateless/local-first na Fase 08, 
# a persistência do circuito acontece no JSON do Frontend.
# Este endpoint serve apenas como "Oracle" de dados normativos.