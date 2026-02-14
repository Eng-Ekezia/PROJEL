from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import uuid
from datetime import datetime

from domain_core.schemas.zona import Zona, ZonaCreate
from domain_core.enums.influencias import (
    TemperaturaAmbiente, PresencaAgua, PresencaSolidos, 
    CompetenciaPessoas, MateriaisConstrucao, EstruturaEdificacao,
    DESCRICOES_INFLUENCIAS
)

router = APIRouter()

# --- PRESETS (Mantidos) ---
PRESETS = {
    "residencial": [
        {"id": "res_seca", "nome": "Área Seca (Sala/Quarto)", "descricao": "Ambientes internos sem risco de água.", "influencias": {"temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1", "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"}, "cor": "#81C784"},
        {"id": "res_molhada", "nome": "Área Molhada (Banheiro/Cozinha)", "descricao": "Locais com presença de água. Exige DR.", "influencias": {"temp_ambiente": "AA4", "presenca_agua": "AD2", "presenca_solidos": "AE1", "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"}, "cor": "#64B5F6"},
        {"id": "res_garagem", "nome": "Garagem / Área de Serviço", "descricao": "Umidade eventual e poeira.", "influencias": {"temp_ambiente": "AA4", "presenca_agua": "AD2", "presenca_solidos": "AE2", "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"}, "cor": "#FFB74D"},
        {"id": "res_externa", "nome": "Área Externa", "descricao": "Exposição ao tempo.", "influencias": {"temp_ambiente": "AA4", "presenca_agua": "AD4", "presenca_solidos": "AE2", "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"}, "cor": "#A1887F"}
    ],
    "comercial": [
        {"id": "com_admin", "nome": "Área Administrativa", "descricao": "Escritórios.", "influencias": {"temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1", "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"}, "cor": "#90CAF9"},
        {"id": "com_publico", "nome": "Atendimento ao Público", "descricao": "Lojas e recepções.", "influencias": {"temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1", "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"}, "cor": "#CE93D8"}
    ]
}

def find_preset(preset_id: str):
    for cat in PRESETS.values():
        for p in cat:
            if p['id'] == preset_id: return p
    return None

@router.get("/presets/{tipo_projeto}", response_model=List[Dict[str, Any]])
async def listar_presets(tipo_projeto: str):
    return PRESETS.get(tipo_projeto.lower(), [])

@router.get("/opcoes-influencias", response_model=Dict[str, List[Dict[str, str]]])
async def listar_opcoes_influencias():
    def enum_to_list(enum_cls):
        return [{"codigo": e.value, "descricao": DESCRICOES_INFLUENCIAS.get(e.value, e.value)} for e in enum_cls]
    return {
        "temperatura": enum_to_list(TemperaturaAmbiente),
        "agua": enum_to_list(PresencaAgua),
        "solidos": enum_to_list(PresencaSolidos),
        "pessoas": enum_to_list(CompetenciaPessoas),
        "materiais": enum_to_list(MateriaisConstrucao),
        "estrutura": enum_to_list(EstruturaEdificacao),
    }

@router.post("/", response_model=Zona, status_code=status.HTTP_201_CREATED)
async def validar_criar_zona(zona_in: ZonaCreate):
    dados_finais = zona_in.model_dump()
    if zona_in.origem == 'preset' and zona_in.preset_id:
        preset = find_preset(zona_in.preset_id)
        if preset:
            dados_finais.update(preset['influencias'])
            dados_finais['cor_identificacao'] = preset['cor']
            if not zona_in.nome: dados_finais['nome'] = preset['nome']
        else:
            dados_finais['origem'] = 'custom'

    nova_zona = Zona(id=str(uuid.uuid4()), data_criacao=datetime.now(), **dados_finais)
    return nova_zona

@router.put("/{zona_id}", response_model=Zona)
async def atualizar_zona(zona_id: str, zona_in: ZonaCreate):
    # Simula update: Recria objeto mantendo ID
    # Em produção: DB UPDATE ... WHERE id = zona_id
    zona_atualizada = await validar_criar_zona(zona_in)
    zona_atualizada.id = zona_id # Mantém ID antigo
    return zona_atualizada

@router.delete("/{zona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_zona(zona_id: str):
    return None