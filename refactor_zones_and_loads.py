import os

# ==============================================================================
# SCRIPT DE REFATORAÇÃO: CORREÇÃO ARQUITETURAL (ZONAS & CARGAS)
# ==============================================================================
# Objetivo: 
# 1. Garantir que Presets sejam resolvidos no Backend (Integridade Normativa).
# 2. Implementar cálculo automático de Potência (W/VA) no Backend.
# 3. Alinhar Frontend aos novos contratos.
# ==============================================================================

files_content = {

    # --------------------------------------------------------------------------
    # 1. DOMAIN CORE - SCHEMA CARGA (Refatorado para Input Inteligente)
    # --------------------------------------------------------------------------
    "domain_core/schemas/carga.py": r'''
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime
from ..enums.cargas import TipoCarga

class CargaBase(BaseModel):
    """Modelo base de leitura (Output)"""
    nome: str = Field(..., description="Descrição da carga")
    tipo: TipoCarga = Field(default=TipoCarga.TUG)
    quantidade: int = Field(default=1, gt=0)
    
    # No Output, sempre devolvemos tudo calculado
    potencia_va: float 
    potencia_w: float
    fator_potencia: float
    
    local_id: str

class CargaCreate(BaseModel):
    """Modelo de entrada (Input Inteligente)"""
    nome: str
    tipo: TipoCarga = Field(default=TipoCarga.TUG)
    quantidade: int = Field(default=1, gt=0)
    local_id: str
    
    # Input flexível: Usuário informa um, o sistema calcula o outro
    potencia: float = Field(..., gt=0, description="Valor da potência")
    unidade: Literal['W', 'VA'] = Field(..., description="Unidade da potência informada")
    fator_potencia: float = Field(default=1.0, ge=0, le=1, description="Fator de Potência")

class Carga(CargaBase):
    id: str
    data_criacao: datetime

    class Config:
        from_attributes = True
''',

    # --------------------------------------------------------------------------
    # 2. BACKEND - ENDPOINT CARGAS (Implementa Regra de Negócio W <-> VA)
    # --------------------------------------------------------------------------
    "backend/api/v1/endpoints/cargas.py": r'''
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
import uuid
from datetime import datetime

from domain_core.schemas.carga import Carga, CargaCreate

router = APIRouter()

@router.post("/", response_model=Carga, status_code=status.HTTP_201_CREATED)
async def criar_carga(carga_in: CargaCreate):
    """
    Cria uma nova carga calculando automaticamente W e VA.
    """
    
    # 1. Lógica de Engenharia (Cálculo de Potências)
    pot_w = 0.0
    pot_va = 0.0
    
    if carga_in.unidade == 'W':
        pot_w = carga_in.potencia
        # Evita divisão por zero
        fp = carga_in.fator_potencia if carga_in.fator_potencia > 0 else 1.0
        pot_va = pot_w / fp
    else: # Unidade == 'VA'
        pot_va = carga_in.potencia
        pot_w = pot_va * carga_in.fator_potencia

    # 2. Criação do Objeto Persistente
    nova_carga = Carga(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        nome=carga_in.nome,
        tipo=carga_in.tipo,
        quantidade=carga_in.quantidade,
        local_id=carga_in.local_id,
        potencia_va=round(pot_va, 2),
        potencia_w=round(pot_w, 2),
        fator_potencia=carga_in.fator_potencia
    )
    
    return nova_carga

@router.post("/calcular-minimo-nbr", status_code=200)
async def calcular_minimo_nbr(dados: Dict[str, float]):
    """
    Cálculo de previsão de cargas (Mantido da versão anterior)
    """
    area = dados.get("area", 0)
    perimetro = dados.get("perimetro", 0)
    eh_area_umida = bool(dados.get("eh_cozinha_servico", False))
    
    # Iluminação
    potencia_ilum = 0
    if area <= 6:
        potencia_ilum = 100
    else:
        potencia_ilum = 100 + (int((area - 6) / 4) * 60)
        
    # TUGs
    qtd_tugs = 0
    if eh_area_umida:
        qtd_tugs = int(perimetro / 3.5)
        if perimetro % 3.5 > 0: qtd_tugs += 1 
        if qtd_tugs < 2: qtd_tugs = 2
    else:
        qtd_tugs = int(perimetro / 5)
        if perimetro % 5 > 0: qtd_tugs += 1
        if qtd_tugs < 1: qtd_tugs = 1

    return {
        "norma_iluminacao_va": potencia_ilum,
        "norma_tugs_quantidade": qtd_tugs
    }
''',

    # --------------------------------------------------------------------------
    # 3. BACKEND - ENDPOINT ZONAS (Blindagem Normativa)
    # --------------------------------------------------------------------------
    "backend/api/v1/endpoints/zonas.py": r'''
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import uuid
from datetime import datetime

from domain_core.schemas.zona import Zona, ZonaCreate
# Importa Enums para garantir que valores existam
from domain_core.enums.influencias import (
    TemperaturaAmbiente, PresencaAgua, PresencaSolidos, 
    CompetenciaPessoas, MateriaisConstrucao, EstruturaEdificacao,
    DESCRICOES
)

router = APIRouter()

# --- PRESETS OFICIAIS (Fonte da Verdade) ---
PRESETS = {
    "residencial": [
        {
            "id": "res_seca",
            "nome": "Área Seca (Sala/Quarto)",
            "descricao": "Ambientes internos sem risco de água.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#81C784"
        },
        {
            "id": "res_molhada",
            "nome": "Área Molhada (Banheiro/Cozinha)",
            "descricao": "Locais com presença de água. Exige DR.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD2", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#64B5F6"
        },
        {
            "id": "res_garagem",
            "nome": "Garagem / Área de Serviço",
            "descricao": "Umidade eventual e poeira.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD2", "presenca_solidos": "AE2",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#FFB74D"
        },
        {
            "id": "res_externa",
            "nome": "Área Externa",
            "descricao": "Exposição ao tempo.",
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
            "descricao": "Escritórios.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#90CAF9"
        },
        {
            "id": "com_publico",
            "nome": "Atendimento ao Público",
            "descricao": "Lojas e recepções.",
            "influencias": {
                "temp_ambiente": "AA4", "presenca_agua": "AD1", "presenca_solidos": "AE1",
                "competencia_pessoas": "BA1", "materiais_construcao": "CA1", "estrutura_edificacao": "CB1"
            },
            "cor": "#CE93D8"
        }
    ]
}

def find_preset(preset_id: str):
    for cat in PRESETS.values():
        for p in cat:
            if p['id'] == preset_id:
                return p
    return None

@router.get("/presets/{tipo_projeto}", response_model=List[Dict[str, Any]])
async def listar_presets(tipo_projeto: str):
    tipo = tipo_projeto.lower()
    return PRESETS.get(tipo, [])

@router.get("/opcoes-influencias", response_model=Dict[str, List[Dict[str, str]]])
async def listar_opcoes_influencias():
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

@router.post("/", response_model=Zona, status_code=status.HTTP_201_CREATED)
async def validar_criar_zona(zona_in: ZonaCreate):
    """
    Factory de Zonas:
    - Se vier 'preset_id', o Backend FORÇA as influências do preset (Segurança).
    - Se for 'custom', aceita o que veio do Frontend.
    """
    
    dados_finais = zona_in.model_dump()
    
    # --- LÓGICA DE BLINDAGEM ---
    if zona_in.origem == 'preset' and zona_in.preset_id:
        preset = find_preset(zona_in.preset_id)
        if preset:
            # Sobrescreve influências com a verdade normativa do Backend
            dados_finais.update(preset['influencias'])
            dados_finais['cor_identificacao'] = preset['cor']
            # Garante nome/descrição do preset se o usuário não alterou (opcional)
            if not zona_in.nome: dados_finais['nome'] = preset['nome']
        else:
            # Fallback se preset não existir (vira custom)
            dados_finais['origem'] = 'custom'

    nova_zona = Zona(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **dados_finais
    )
    return nova_zona
''',

    # --------------------------------------------------------------------------
    # 4. FRONTEND - API CLIENT (Atualizado para CargaCreate)
    # --------------------------------------------------------------------------
    "frontend/src/api/client.ts": r'''
import axios from 'axios';
import { Zona, Local, PresetZona, Carga } from '../types/project';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

export interface OpcoesInfluencias {
  temperatura: { codigo: string; descricao: string }[];
  agua: { codigo: string; descricao: string }[];
  solidos: { codigo: string; descricao: string }[];
  pessoas: { codigo: string; descricao: string }[];
  materiais: { codigo: string; descricao: string }[];
  estrutura: { codigo: string; descricao: string }[];
}

export interface CargaCreateDTO {
    projeto_id: string; // Para referência futura
    local_id: string;
    nome: string;
    tipo: string;
    quantidade: number;
    potencia: number;
    unidade: 'W' | 'VA';
    fator_potencia: number;
}

export const ProjectService = {
  getOpcoesInfluencias: async (): Promise<OpcoesInfluencias> => {
    const response = await api.get<OpcoesInfluencias>('/zonas/opcoes-influencias');
    return response.data;
  },

  getPresets: async (tipoProjeto: string): Promise<PresetZona[]> => {
    const response = await api.get<PresetZona[]>(`/zonas/presets/${tipoProjeto}`);
    return response.data;
  },

  createZona: async (zona: Partial<Zona>): Promise<Zona> => {
    // Frontend envia Partial, Backend valida e preenche
    const response = await api.post<Zona>('/zonas/', zona);
    return response.data;
  },

  createLocal: async (local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.post<Local>('/locais/', local);
    return response.data;
  },

  createCarga: async (carga: CargaCreateDTO): Promise<Carga> => {
    const response = await api.post<Carga>('/cargas/', carga);
    return response.data;
  }
};
''',

    # --------------------------------------------------------------------------
    # 5. FRONTEND - PROJECT DETAILS (UX Ajustada)
    # --------------------------------------------------------------------------
    "frontend/src/pages/ProjectDetails.tsx": r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Chip, Divider, 
  Paper, IconButton, Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import ScienceIcon from '@mui/icons-material/Science';
import DeleteIcon from '@mui/icons-material/Delete';
import FlashOnIcon from '@mui/icons-material/FlashOn';

import { useProjectStore } from '../store/useProjectStore';
import { ProjectService, OpcoesInfluencias, CargaCreateDTO } from '../api/client';
import { Zona, Local, PresetZona, Carga } from '../types/project';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

// --- COMPONENTE DE CARGA (NOVO) ---
const CargaForm: React.FC<{ localId: string, projectId: string, onClose: () => void }> = ({ localId, projectId, onClose }) => {
    const { addCargaToProject } = useProjectStore();
    const [form, setForm] = useState<CargaCreateDTO>({
        projeto_id: projectId,
        local_id: localId,
        nome: '',
        tipo: 'TUG',
        quantidade: 1,
        potencia: 100,
        unidade: 'VA',
        fator_potencia: 1.0
    });

    const handleSubmit = async () => {
        try {
            const nova = await ProjectService.createCarga(form);
            addCargaToProject(projectId, nova);
            onClose();
        } catch (error) {
            console.error(error);
            alert("Erro ao criar carga");
        }
    };

    return (
        <Box sx={{ mt: 2, p: 2, border: '1px dashed #ccc', borderRadius: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Adicionar Carga</Typography>
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                    <TextField fullWidth size="small" label="Descrição" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
                </Grid>
                <Grid item xs={6} sm={3}>
                    <TextField select fullWidth size="small" label="Tipo" value={form.tipo} onChange={e => setForm({...form, tipo: e.target.value})}>
                        <MenuItem value="ILUMINACAO">Iluminação</MenuItem>
                        <MenuItem value="TUG">TUG</MenuItem>
                        <MenuItem value="TUE">TUE</MenuItem>
                    </TextField>
                </Grid>
                <Grid item xs={6} sm={3}>
                    <TextField fullWidth size="small" type="number" label="Qtd" value={form.quantidade} onChange={e => setForm({...form, quantidade: Number(e.target.value)})} />
                </Grid>
                <Grid item xs={4}>
                    <TextField fullWidth size="small" type="number" label="Potência" value={form.potencia} onChange={e => setForm({...form, potencia: Number(e.target.value)})} />
                </Grid>
                <Grid item xs={4}>
                     <TextField select fullWidth size="small" label="Unidade" value={form.unidade} onChange={e => setForm({...form, unidade: e.target.value as any})}>
                        <MenuItem value="W">Watts (W)</MenuItem>
                        <MenuItem value="VA">VA</MenuItem>
                    </TextField>
                </Grid>
                 <Grid item xs={4}>
                    <TextField fullWidth size="small" type="number" label="F.P." value={form.fator_potencia} onChange={e => setForm({...form, fator_potencia: Number(e.target.value)})} />
                </Grid>
                <Grid item xs={12}>
                    <Button variant="contained" size="small" onClick={handleSubmit}>Salvar Carga</Button>
                    <Button size="small" onClick={onClose} sx={{ ml: 1 }}>Cancelar</Button>
                </Grid>
            </Grid>
        </Box>
    );
};

// --- COMPONENTE PRINCIPAL ---
const ProjectDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { projects, addZonaToProject, addLocalToProject } = useProjectStore();
  
  const project = projects.find(p => p.id === id);
  const [tabValue, setTabValue] = useState(0);
  const [opcoes, setOpcoes] = useState<OpcoesInfluencias | null>(null);
  
  // States Zona
  const [viewState, setViewState] = useState<'list' | 'method_select' | 'preset_select' | 'form_custom'>('list');
  const [availablePresets, setAvailablePresets] = useState<PresetZona[]>([]);
  const [selectedPreset, setSelectedPreset] = useState<PresetZona | null>(null);
  const [newZona, setNewZona] = useState<Partial<Zona>>({});
  
  // States Local
  const [newLocal, setNewLocal] = useState<Partial<Local>>({});
  
  // States Carga
  const [addingCargaToLocalId, setAddingCargaToLocalId] = useState<string | null>(null);
  
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!project) return;
    ProjectService.getOpcoesInfluencias().then(setOpcoes).catch(console.error);
    ProjectService.getPresets(project.tipo_instalacao).then(setAvailablePresets).catch(console.error);
  }, [project]);

  if (!project) return <Container sx={{mt:4}}><Typography>Projeto não encontrado.</Typography></Container>;

  // --- HANDLERS ZONA ---

  const handleSelectPreset = (preset: PresetZona) => {
    setSelectedPreset(preset);
    // UX: Preenche nome/descrição para o usuário ver, mas NÃO AS INFLUENCIAS
    // As influencias serão injetadas pelo backend baseadas no preset_id
    setNewZona({
        nome: preset.nome,
        descricao: preset.descricao,
        origem: 'preset',
        preset_id: preset.id,
        // UI helper only
        cor_identificacao: preset.cor 
    });
    setViewState('form_custom'); 
  };

  const handleSaveZona = async () => {
    try {
      if (!newZona.nome) { setErrorMsg("Nome é obrigatório."); return; }
      
      const payload = {
          projeto_id: project.id,
          nome: newZona.nome,
          descricao: newZona.descricao,
          origem: newZona.origem,
          preset_id: newZona.preset_id,
          
          // Se for Custom, manda tudo. Se for Preset, Backend ignora estes campos (mas mandamos defaults pra passar no schema Pydantic se necessário)
          temp_ambiente: newZona.temp_ambiente || 'AA4',
          presenca_agua: newZona.presenca_agua || 'AD1',
          presenca_solidos: newZona.presenca_solidos || 'AE1',
          competencia_pessoas: newZona.competencia_pessoas || 'BA1',
          materiais_construcao: newZona.materiais_construcao || 'CA2',
          estrutura_edificacao: newZona.estrutura_edificacao || 'CB1',
          cor_identificacao: newZona.cor_identificacao || '#ccc'
      };

      const zonaCriada = await ProjectService.createZona(payload);
      addZonaToProject(project.id, zonaCriada);
      setViewState('list');
      setNewZona({});
    } catch (error: any) {
        console.error(error);
        setErrorMsg("Erro ao salvar zona.");
    }
  };

  // --- HANDLERS LOCAL ---
  const handleAddLocal = async () => {
    try {
        if (!newLocal.nome || !newLocal.zona_id) { setErrorMsg("Dados incompletos."); return; }
        const criado = await ProjectService.createLocal({
            projeto_id: project.id,
            zona_id: newLocal.zona_id,
            nome: newLocal.nome,
            area_m2: Number(newLocal.area_m2),
            perimetro_m: Number(newLocal.perimetro_m),
            pe_direito_m: 2.8
        });
        addLocalToProject(project.id, criado);
        setNewLocal({});
    } catch (e) { setErrorMsg("Erro ao criar local"); }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} sx={{ mb: 2 }}>Dashboard</Button>
      <Typography variant="h4" gutterBottom>{project.nome}</Typography>
      
      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tab label="1. Ambientes (Zonas)" />
        <Tab label="2. Arquitetura e Cargas" />
      </Tabs>

      {/* ABA 1: ZONAS (Mantida lógica visual, backend blindado) */}
      <CustomTabPanel value={tabValue} index={0}>
         {viewState === 'list' && (
            <Box>
                {project.zonas?.map(z => (
                     <Card key={z.id} variant="outlined" sx={{ mb: 2, borderLeft: `6px solid ${z.cor_identificacao}` }}>
                        <CardContent>
                            <Typography variant="h6">{z.nome} <Chip size="small" label={z.origem} /></Typography>
                            <Typography variant="body2" color="text.secondary">{z.descricao}</Typography>
                            <Box mt={1} display="flex" gap={1}>
                                <Chip label={`Água: ${z.presenca_agua}`} size="small" variant="outlined"/>
                                <Chip label={`Pessoas: ${z.competencia_pessoas}`} size="small" variant="outlined"/>
                            </Box>
                        </CardContent>
                     </Card>
                ))}
                <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={() => setViewState('method_select')}>Nova Zona</Button>
            </Box>
         )}
         
         {viewState === 'method_select' && (
             <Grid container spacing={2} justifyContent="center" sx={{ mt: 2 }}>
                <Grid item xs={5}>
                    <Paper sx={{ p: 3, textAlign: 'center', cursor: 'pointer', bgcolor: '#f0f4ff' }} onClick={() => setViewState('preset_select')}>
                        <ScienceIcon fontSize="large" color="primary" />
                        <Typography variant="h6">Usar Preset (Recomendado)</Typography>
                        <Typography variant="body2">Norma aplicada automaticamente.</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={5}>
                    <Paper sx={{ p: 3, textAlign: 'center', cursor: 'pointer' }} onClick={() => { setNewZona({origem: 'custom'}); setViewState('form_custom'); }}>
                        <SettingsIcon fontSize="large" color="secondary" />
                        <Typography variant="h6">Personalizado</Typography>
                        <Typography variant="body2">Definição manual de influências.</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} textAlign="center"><Button onClick={() => setViewState('list')}>Cancelar</Button></Grid>
             </Grid>
         )}

         {viewState === 'preset_select' && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
                {availablePresets.map(p => (
                    <Grid item xs={4} key={p.id}>
                        <Card sx={{ cursor: 'pointer', borderLeft: `4px solid ${p.cor}` }} onClick={() => handleSelectPreset(p)}>
                            <CardContent>
                                <Typography fontWeight="bold">{p.nome}</Typography>
                                <Typography variant="caption">{p.descricao}</Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
         )}

         {viewState === 'form_custom' && (
             <Card sx={{ maxWidth: 600, mx: 'auto', mt: 2 }}>
                 <CardContent>
                     <Typography variant="h6">{newZona.origem === 'preset' ? 'Confirmar Zona' : 'Nova Zona'}</Typography>
                     <TextField fullWidth margin="normal" label="Nome" value={newZona.nome || ''} onChange={e => setNewZona({...newZona, nome: e.target.value})} />
                     
                     {newZona.origem === 'custom' && (
                         <Box sx={{ mt: 2 }}>
                             <Alert severity="warning" sx={{ mb: 2 }}>Modo Avançado: Você é responsável pela conformidade normativa.</Alert>
                             <TextField select fullWidth label="Presença de Água" value={newZona.presenca_agua || ''} onChange={e => setNewZona({...newZona, presenca_agua: e.target.value})}>
                                {opcoes?.agua.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                             </TextField>
                             {/* Outros selects simplificados para brevidade */}
                         </Box>
                     )}
                     
                     <Box mt={2} display="flex" justifyContent="flex-end" gap={2}>
                        <Button onClick={() => setViewState('list')}>Cancelar</Button>
                        <Button variant="contained" onClick={handleSaveZona}>Salvar</Button>
                     </Box>
                 </CardContent>
             </Card>
         )}
      </CustomTabPanel>

      {/* ABA 2: LOCAIS E CARGAS */}
      <CustomTabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
            {/* Form de Local */}
            <Grid item xs={12} md={4}>
                <Card variant="outlined">
                    <CardContent>
                        <Typography variant="subtitle1" gutterBottom>Novo Cômodo</Typography>
                        <TextField fullWidth size="small" margin="dense" label="Nome" value={newLocal.nome || ''} onChange={e => setNewLocal({...newLocal, nome: e.target.value})} />
                        <TextField select fullWidth size="small" margin="dense" label="Zona" value={newLocal.zona_id || ''} onChange={e => setNewLocal({...newLocal, zona_id: e.target.value})}>
                            {project.zonas?.map(z => <MenuItem key={z.id} value={z.id}>{z.nome}</MenuItem>)}
                        </TextField>
                        <Grid container spacing={1}>
                            <Grid item xs={6}><TextField fullWidth size="small" margin="dense" type="number" label="Area" value={newLocal.area_m2 || ''} onChange={e => setNewLocal({...newLocal, area_m2: e.target.value})} /></Grid>
                            <Grid item xs={6}><TextField fullWidth size="small" margin="dense" type="number" label="Perim" value={newLocal.perimetro_m || ''} onChange={e => setNewLocal({...newLocal, perimetro_m: e.target.value})} /></Grid>
                        </Grid>
                        <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={handleAddLocal}>Adicionar</Button>
                    </CardContent>
                </Card>
            </Grid>

            {/* Lista de Locais e Cargas */}
            <Grid item xs={12} md={8}>
                {project.locais?.map(local => (
                    <Card key={local.id} sx={{ mb: 2 }}>
                        <CardContent>
                            <Box display="flex" justifyContent="space-between" alignItems="center">
                                <Box>
                                    <Typography variant="h6">{local.nome}</Typography>
                                    <Typography variant="caption" color="text.secondary">
                                        Zona: {project.zonas?.find(z => z.id === local.zona_id)?.nome} | {local.area_m2}m²
                                    </Typography>
                                </Box>
                                <Button startIcon={<FlashOnIcon />} size="small" onClick={() => setAddingCargaToLocalId(local.id)}>
                                    Carga
                                </Button>
                            </Box>
                            
                            {/* Formulário Inline de Carga */}
                            {addingCargaToLocalId === local.id && (
                                <CargaForm localId={local.id} projectId={project.id} onClose={() => setAddingCargaToLocalId(null)} />
                            )}

                            {/* Lista de Cargas deste Local */}
                            <Box sx={{ mt: 2 }}>
                                {project.cargas?.filter(c => c.local_id === local.id).map(carga => (
                                    <Box key={carga.id} display="flex" justifyContent="space-between" sx={{ borderBottom: '1px solid #eee', py: 1 }}>
                                        <Typography variant="body2">{carga.nome} ({carga.tipo_carga})</Typography>
                                        <Typography variant="body2" fontWeight="bold">
                                            {carga.quantidade}x {carga.potencia_W}W / {carga.potencia_VA}VA
                                        </Typography>
                                    </Box>
                                ))}
                                {(!project.cargas || !project.cargas.some(c => c.local_id === local.id)) && (
                                    <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}>Nenhuma carga cadastrada.</Typography>
                                )}
                            </Box>
                        </CardContent>
                    </Card>
                ))}
            </Grid>
        </Grid>
      </CustomTabPanel>

    </Container>
  );
};

export default ProjectDetails;
'''
}

def main():
    print("--- INICIANDO REFATORAÇÃO DE ZONAS E CARGAS ---")
    base_dir = os.getcwd()

    for file_path, content in files_content.items():
        full_path = os.path.join(base_dir, file_path)
        
        # Garante diretório
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"✅ Atualizado: {file_path}")
        except Exception as e:
            print(f"❌ Erro em {file_path}: {e}")

    print("\n--- REFATORAÇÃO CONCLUÍDA ---")
    print("1. Reinicie o Backend: Ctrl+C -> uvicorn main:app --reload")
    print("2. Backend agora blinda Presets e calcula Cargas.")

if __name__ == "__main__":
    main()