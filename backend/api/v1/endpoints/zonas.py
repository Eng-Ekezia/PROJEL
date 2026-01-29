from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import uuid
from datetime import datetime

from domain_core.schemas.zona import Zona, ZonaCreate
from domain_core.enums.influencias import (
    TemperaturaAmbiente, PresencaAgua, PresencaSolidos, 
    CompetenciaPessoas, MateriaisConstrucao, EstruturaEdificacao,
    DESCRICOES
)

router = APIRouter()

# --- PRESETS OFICIAIS ---
PRESETS = {
    "residencial": [
        {
            "id": "res_seca",
            "nome": "Área Seca (Sala/Quarto)",
            "descricao": "Ambientes internos sem risco de água. Caso base da norma.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#81C784"
        },
        {
            "id": "res_molhada",
            "nome": "Área Molhada (Banheiro/Cozinha)",
            "descricao": "Locais com presença de água. Exige cuidados com choque (DR).",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD2", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#64B5F6"
        },
        {
            "id": "res_garagem",
            "nome": "Garagem / Área de Serviço",
            "descricao": "Umidade eventual e possibilidade de poeira.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD2", "presenca_solidos": "AE2",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#FFB74D"
        },
        {
            "id": "res_externa",
            "nome": "Área Externa (Jardim/Quintal)",
            "descricao": "Exposição ao tempo, chuva e intempéries.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD4", "presenca_solidos": "AE2",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#A1887F"
        }
    ],
    "comercial": [
        {
            "id": "com_admin",
            "nome": "Área Administrativa",
            "descricao": "Escritórios e salas de reunião. Ambiente controlado.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#90CAF9"
        },
        {
            "id": "com_publico",
            "nome": "Atendimento ao Público",
            "descricao": "Lojas e recepções. Atenção à segurança de terceiros.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#CE93D8"
        },
        {
            "id": "com_tecnica",
            "nome": "Área Técnica Restrita",
            "descricao": "Servidores/Máquinas. Acesso apenas por qualificados.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA5", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#B0BEC5"
        }
    ],
    "industrial": []
}

@router.get("/presets/{tipo_projeto}", response_model=List[Dict[str, Any]])
async def listar_presets(tipo_projeto: str):
    """
    Retorna os presets disponíveis para o tipo de projeto.
    """
    tipo = tipo_projeto.lower()
    return PRESETS.get(tipo, [])

@router.post("/", response_model=Zona, status_code=status.HTTP_201_CREATED)
async def validar_criar_zona(zona_in: ZonaCreate):
    """
    Factory de Zonas: Valida e cria uma nova Zona (Stateless).
    """
    nova_zona = Zona(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **zona_in.model_dump()
    )
    return nova_zona

@router.put("/{zona_id}", response_model=Zona)
async def validar_atualizar_zona(zona_id: str, zona_in: ZonaCreate):
    """
    Validador de Edição: Recebe os dados editados, valida contra o Schema e devolve o objeto.
    Como o backend é stateless, ele não 'salva' no banco, mas garante que a edição é válida.
    """
    # Aqui poderíamos checar regras complexas de transição se necessário.
    
    zona_atualizada = Zona(
        id=zona_id,
        data_criacao=datetime.now(), # Mantém ou atualiza data? UI decide. Backend apenas valida estrutura.
        **zona_in.model_dump()
    )
    return zona_atualizada

@router.get("/opcoes-influencias", response_model=Dict[str, List[Dict[str, str]]])
async def listar_opcoes_influencias():
    """
    Retorna opções da NBR 5410 para Dropdowns.
    """
    def enum_to_list(enum_cls):
        return [{"codigo": e.value, "descricao": DESCRICOES.get(e.value, e.value)} for e in enum_cls]

    return {
        "temperatura": enum_to_list(TemperaturaAmbiente),
        "agua": enum_to_list(PresencaAgua),
        "solidos": enum_to_list(PresencaSolidos),
        "pessoas": enum_to_list(CompetenciaPessoas),
        "materiais": enum_to_list(MateriaisConstrucao),
        "estrutura": enum_to_list(EstruturaEdificacao),
    }