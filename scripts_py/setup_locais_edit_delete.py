import os

# ==============================================================================
# SCRIPT: IMPLEMENTAÇÃO DE EDIÇÃO E EXCLUSÃO DE LOCAIS (CÔMODOS)
# ==============================================================================

files_content = {
    # --------------------------------------------------------------------------
    # 1. BACKEND - ENDPOINT PUT PARA LOCAIS
    # --------------------------------------------------------------------------
    "backend/api/v1/endpoints/locais.py": r'''
from fastapi import APIRouter, HTTPException, status
import uuid
from datetime import datetime

from domain_core.schemas.local import Local, LocalCreate

router = APIRouter()

@router.post("/", response_model=Local, status_code=status.HTTP_201_CREATED)
async def validar_criar_local(local_in: LocalCreate):
    """
    Factory de Locais: Valida geometria básica.
    """
    validar_geometria(local_in)

    novo_local = Local(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **local_in.model_dump()
    )
    return novo_local

@router.put("/{local_id}", response_model=Local)
async def validar_atualizar_local(local_id: str, local_in: LocalCreate):
    """
    Validador de Edição de Local.
    """
    validar_geometria(local_in)
    
    local_atualizado = Local(
        id=local_id,
        data_criacao=datetime.now(), 
        **local_in.model_dump()
    )
    return local_atualizado

def validar_geometria(local_in: LocalCreate):
    if local_in.area_m2 <= 0:
        raise HTTPException(status_code=400, detail="A área deve ser maior que zero.")
    
    if local_in.perimetro_m <= 0:
        raise HTTPException(status_code=400, detail="O perímetro deve ser maior que zero.")

    # Validação Geométrica Básica (Evita dados impossíveis)
    if local_in.perimetro_m < (local_in.area_m2 ** 0.5) * 2:
         raise HTTPException(status_code=400, detail="Perímetro muito pequeno para a área informada (Geometria impossível).")
''',

    # --------------------------------------------------------------------------
    # 2. FRONTEND - API CLIENT (UPDATE LOCAL)
    # --------------------------------------------------------------------------
    "frontend/src/api/client.ts": r'''
import axios from 'axios';
import { Zona, Local, PresetZona } from '../types/project';

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

export const ProjectService = {
  getOpcoesInfluencias: async (): Promise<OpcoesInfluencias> => {
    const response = await api.get<OpcoesInfluencias>('/zonas/opcoes-influencias');
    return response.data;
  },

  getPresets: async (tipoProjeto: string): Promise<PresetZona[]> => {
    const response = await api.get<PresetZona[]>(`/zonas/presets/${tipoProjeto}`);
    return response.data;
  },

  createZona: async (zona: Omit<Zona, 'id' | 'data_criacao'>): Promise<Zona> => {
    const response = await api.post<Zona>('/zonas/', zona);
    return response.data;
  },

  updateZona: async (id: string, zona: Omit<Zona, 'id' | 'data_criacao'>): Promise<Zona> => {
    const response = await api.put<Zona>(`/zonas/${id}`, zona);
    return response.data;
  },

  createLocal: async (local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.post<Local>('/locais/', local);
    return response.data;
  },

  updateLocal: async (id: string, local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.put<Local>(`/locais/${id}`, local);
    return response.data;
  }
};
''',

    # --------------------------------------------------------------------------
    # 3. FRONTEND - STORE (ACTIONS LOCAL)
    # --------------------------------------------------------------------------
    "frontend/src/store/useProjectStore.ts": r'''
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Projeto, Zona, Local, Carga } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  addProject: (project: Projeto) => void;
  updateProject: (id: string, data: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  
  // ZONAS
  addZonaToProject: (projetoId: string, zona: Zona) => void;
  updateZonaInProject: (projetoId: string, zonaId: string, zona: Zona) => void;
  removeZonaFromProject: (projetoId: string, zonaId: string) => void;

  // LOCAIS
  addLocalToProject: (projetoId: string, local: Local) => void;
  updateLocalInProject: (projetoId: string, localId: string, local: Local) => void;
  removeLocalFromProject: (projetoId: string, localId: string) => void;
  
  // CARGAS
  addCargaToProject: (projetoId: string, carga: Carga) => void;
  removeCargaFromProject: (projetoId: string, cargaId: string) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set) => ({
      projects: [],
      
      addProject: (project) => set((state) => ({ 
        projects: [...state.projects, { ...project, zonas: [], locais: [], cargas: [] }] 
      })),

      updateProject: (id, data) => set((state) => ({
        projects: state.projects.map((p) => (p.id === id ? { ...p, ...data, ultima_modificacao: new Date().toISOString() } : p)),
      })),

      deleteProject: (id) => set((state) => ({
        projects: state.projects.filter((p) => p.id !== id),
      })),

      // --- ZONAS ---
      addZonaToProject: (projetoId, zona) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const zonasAtuais = p.zonas || [];
          return { ...p, zonas: [...zonasAtuais, zona], ultima_modificacao: new Date().toISOString() };
        })
      })),

      updateZonaInProject: (projetoId, zonaId, zonaAtualizada) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          return {
             ...p,
             zonas: p.zonas.map(z => z.id === zonaId ? zonaAtualizada : z),
             ultima_modificacao: new Date().toISOString()
          };
        })
      })),

      removeZonaFromProject: (projetoId, zonaId) => set((state) => ({
        projects: state.projects.map(p => {
            if (p.id !== projetoId) return p;
            return {
                ...p,
                zonas: p.zonas.filter(z => z.id !== zonaId),
                ultima_modificacao: new Date().toISOString()
            };
        })
      })),

      // --- LOCAIS ---
      addLocalToProject: (projetoId, local) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const locaisAtuais = p.locais || [];
          return { ...p, locais: [...locaisAtuais, local], ultima_modificacao: new Date().toISOString() };
        })
      })),

      updateLocalInProject: (projetoId, localId, localAtualizado) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          return {
             ...p,
             locais: (p.locais || []).map(l => l.id === localId ? localAtualizado : l),
             ultima_modificacao: new Date().toISOString()
          };
        })
      })),

      removeLocalFromProject: (projetoId, localId) => set((state) => ({
        projects: state.projects.map(p => {
            if (p.id !== projetoId) return p;
            return {
                ...p,
                locais: (p.locais || []).filter(l => l.id !== localId),
                ultima_modificacao: new Date().toISOString()
            };
        })
      })),

      // --- CARGAS ---
      addCargaToProject: (projetoId, carga) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const cargasAtuais = p.cargas || [];
          return { ...p, cargas: [...cargasAtuais, carga], ultima_modificacao: new Date().toISOString() };
        })
      })),

      removeCargaFromProject: (projetoId, cargaId) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          return { 
            ...p, 
            cargas: (p.cargas || []).filter(c => c.id !== cargaId), 
            ultima_modificacao: new Date().toISOString() 
          };
        })
      })),
    }),
    {
      name: 'projel-storage',
    }
  )
);
''',

    # --------------------------------------------------------------------------
    # 4. FRONTEND - UI (PROJECT DETAILS COM EDIT/DELETE DE LOCAIS)
    # --------------------------------------------------------------------------
    "frontend/src/pages/ProjectDetails.tsx": r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Chip, Divider, 
  Paper, IconButton, Tooltip
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import ScienceIcon from '@mui/icons-material/Science';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

import { useProjectStore } from '../store/useProjectStore';
import { ProjectService, OpcoesInfluencias } from '../api/client';
import { Zona, Local, PresetZona } from '../types/project';

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

// --- SUB-COMPONENTS ---

interface ZoneCardProps {
    zona: Zona;
    onEdit: (zona: Zona) => void;
    onDelete: (zonaId: string) => void;
}

const ZoneCard: React.FC<ZoneCardProps> = ({ zona, onEdit, onDelete }) => {
    const origemSafe = zona.origem || 'custom'; 
    const corSafe = zona.cor_identificacao || '#ccc';

    return (
        <Card variant="outlined" sx={{ mb: 2, borderLeft: `6px solid ${corSafe}` }}>
            <CardContent sx={{ pb: 1 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Box display="flex" alignItems="center" gap={1}>
                        <Typography variant="h6">{zona.nome}</Typography>
                        <Chip 
                            label={origemSafe.toUpperCase()} 
                            size="small" 
                            color={origemSafe === 'preset' ? 'primary' : 'default'} 
                        />
                    </Box>
                    <Box>
                        <Tooltip title="Editar">
                            <IconButton size="small" onClick={() => onEdit(zona)}><EditIcon fontSize="small" /></IconButton>
                        </Tooltip>
                        <Tooltip title="Excluir">
                            <IconButton size="small" color="error" onClick={() => onDelete(zona.id)}><DeleteIcon fontSize="small" /></IconButton>
                        </Tooltip>
                    </Box>
                </Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                    {zona.descricao || 'Sem descrição'}
                </Typography>
                <Divider sx={{ my: 1 }} />
                <Box display="flex" gap={1} flexWrap="wrap">
                    <Chip label={zona.temp_ambiente || 'AA?'} size="small" variant="outlined" />
                    <Chip 
                        label={zona.presenca_agua || 'AD?'} 
                        size="small" 
                        variant="outlined" 
                        color={(zona.presenca_agua && zona.presenca_agua !== 'AD1') ? 'info' : 'default'} 
                    />
                    <Chip label={zona.presenca_solidos || 'AE?'} size="small" variant="outlined" />
                    <Chip 
                        label={zona.competencia_pessoas || 'BA?'} 
                        size="small" 
                        variant="outlined" 
                        color={(zona.competencia_pessoas && zona.competencia_pessoas !== 'BA1') ? 'warning' : 'default'} 
                    />
                </Box>
            </CardContent>
        </Card>
    );
};

const ProjectDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const { 
      projects, 
      addZonaToProject, updateZonaInProject, removeZonaFromProject, 
      addLocalToProject, updateLocalInProject, removeLocalFromProject 
  } = useProjectStore();
  
  const project = projects.find(p => p.id === id);
  const [tabValue, setTabValue] = useState(0);
  const [opcoes, setOpcoes] = useState<OpcoesInfluencias | null>(null);
  
  // --- STATES DE INTERFACE ---
  const [viewState, setViewState] = useState<'list' | 'method_select' | 'preset_select' | 'form_custom'>('list');
  const [availablePresets, setAvailablePresets] = useState<PresetZona[]>([]);
  const [selectedPreset, setSelectedPreset] = useState<PresetZona | null>(null);
  
  // States de Formulário ZONA
  const [editingZonaId, setEditingZonaId] = useState<string | null>(null);
  const [newZona, setNewZona] = useState<Partial<Zona>>({});
  
  // States de Formulário LOCAL
  const [editingLocalId, setEditingLocalId] = useState<string | null>(null);
  const [newLocal, setNewLocal] = useState<Partial<Local>>({});
  
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!project) return;
    ProjectService.getOpcoesInfluencias().then(setOpcoes).catch(console.error);
    ProjectService.getPresets(project.tipo_instalacao).then(setAvailablePresets).catch(console.error);
  }, [project]);

  if (!project) return <Container sx={{mt:4}}><Typography>Projeto não encontrado.</Typography></Container>;

  // --- ACTIONS: NAVEGAÇÃO E PRESETS ---

  const handleStartCreateZona = () => {
    setEditingZonaId(null);
    setNewZona({});
    setErrorMsg(null);

    if (project.tipo_instalacao.toLowerCase() === 'industrial') {
        setViewState('form_custom');
        setNewZona({ origem: 'custom', cor_identificacao: '#E0E0E0' });
    } else {
        setViewState('method_select');
    }
  };

  const handleStartEditZona = (zona: Zona) => {
      setEditingZonaId(zona.id);
      setNewZona({ ...zona });
      setSelectedPreset(null);
      setViewState('form_custom');
      setErrorMsg(null);
  };

  const handleDeleteZona = (zonaId: string) => {
      if (window.confirm("Tem certeza que deseja excluir esta zona?")) {
          removeZonaFromProject(project.id, zonaId);
      }
  };

  const handleSelectPreset = (preset: PresetZona) => {
    setSelectedPreset(preset);
    setNewZona({
        nome: preset.nome,
        descricao: preset.descricao,
        temp_ambiente: preset.influencias.temp_ambiente,
        presenca_agua: preset.influencias.presenca_agua,
        presenca_solidos: preset.influencias.presenca_solidos,
        competencia_pessoas: preset.influencias.competencia_pessoas,
        materiais_construcao: preset.influencias.materiais_construcao,
        estrutura_edificacao: preset.influencias.estrutura_edificacao,
        cor_identificacao: preset.cor,
        origem: 'preset',
        preset_id: preset.id
    });
    setViewState('form_custom');
  };

  const handleCreateCustom = () => {
    setNewZona({ origem: 'custom', cor_identificacao: '#E0E0E0' });
    setViewState('form_custom');
  };

  // --- ACTION: SALVAR ZONA (CREATE OU UPDATE) ---

  const handleSaveZona = async () => {
    try {
      if (!newZona.nome) { setErrorMsg("Nome é obrigatório."); return; }
      
      let finalOrigem = newZona.origem || 'custom';
      
      if (selectedPreset && finalOrigem === 'preset') {
          if (newZona.presenca_agua !== selectedPreset.influencias.presenca_agua || 
              newZona.competencia_pessoas !== selectedPreset.influencias.competencia_pessoas) {
              finalOrigem = 'ajustada';
          }
      }

      const payload = {
          projeto_id: project.id,
          nome: newZona.nome,
          descricao: newZona.descricao,
          origem: finalOrigem as any,
          preset_id: newZona.preset_id,
          temp_ambiente: newZona.temp_ambiente || 'AA4',
          presenca_agua: newZona.presenca_agua || 'AD1',
          presenca_solidos: newZona.presenca_solidos || 'AE1',
          competencia_pessoas: newZona.competencia_pessoas || 'BA1',
          materiais_construcao: newZona.materiais_construcao || 'CA2',
          estrutura_edificacao: newZona.estrutura_edificacao || 'CB1',
          cor_identificacao: newZona.cor_identificacao || '#ccc'
      };

      if (editingZonaId) {
          const zonaAtualizada = await ProjectService.updateZona(editingZonaId, payload as any);
          updateZonaInProject(project.id, editingZonaId, zonaAtualizada);
      } else {
          const zonaCriada = await ProjectService.createZona(payload as any);
          addZonaToProject(project.id, zonaCriada);
      }
      
      setViewState('list');
      setEditingZonaId(null);
    } catch (error: any) {
        console.error(error);
        setErrorMsg("Erro ao salvar zona.");
    }
  };

  // --- ACTIONS: LOCAIS (CREATE, UPDATE, DELETE) ---

  const handleStartEditLocal = (local: Local) => {
      setEditingLocalId(local.id);
      setNewLocal({ ...local });
      setErrorMsg(null);
  };

  const handleDeleteLocal = (localId: string) => {
      if (window.confirm("Tem certeza que deseja excluir este cômodo?")) {
          removeLocalFromProject(project.id, localId);
      }
  };

  const handleSaveLocal = async () => {
    try {
      if (!newLocal.nome || !newLocal.zona_id) { setErrorMsg("Preencha dados obrigatórios."); return; }
      
      const payload = {
        projeto_id: project.id,
        zona_id: newLocal.zona_id,
        nome: newLocal.nome,
        area_m2: Number(newLocal.area_m2),
        perimetro_m: Number(newLocal.perimetro_m),
        pe_direito_m: 2.8
      };

      if (editingLocalId) {
          const localAtualizado = await ProjectService.updateLocal(editingLocalId, payload as any);
          updateLocalInProject(project.id, editingLocalId, localAtualizado);
          setEditingLocalId(null);
      } else {
          const localCriado = await ProjectService.createLocal(payload as any);
          addLocalToProject(project.id, localCriado);
      }
      
      setNewLocal({});
      setErrorMsg(null);
    } catch (e: any) { 
        const msg = e.response?.data?.detail || "Erro ao salvar local.";
        setErrorMsg(msg); 
    }
  };

  const handleCancelLocal = () => {
      setEditingLocalId(null);
      setNewLocal({});
      setErrorMsg(null);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} sx={{ mb: 2 }}>
        Dashboard
      </Button>
      
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">
            {project.nome} 
            <Chip label={project.tipo_instalacao} sx={{ ml: 2, verticalAlign: 'middle' }} color="primary" variant="outlined"/>
        </Typography>
      </Box>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="1. Ambientes (Zonas)" />
          <Tab label="2. Arquitetura (Locais)" />
        </Tabs>
      </Box>

      {/* ABA 1: ZONAS */}
      <CustomTabPanel value={tabValue} index={0}>
        
        {viewState === 'list' && (
            <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                    {project.zonas?.map(z => (
                        <ZoneCard 
                            key={z.id} 
                            zona={z} 
                            onEdit={handleStartEditZona} 
                            onDelete={handleDeleteZona}
                        />
                    ))}
                    {(!project.zonas || project.zonas.length === 0) && 
                        <Alert severity="info">Nenhuma zona definida. Comece criando os ambientes do projeto.</Alert>
                    }
                </Grid>
                <Grid item xs={12} md={4}>
                    <Button 
                        variant="contained" 
                        size="large" 
                        fullWidth 
                        startIcon={<AddCircleOutlineIcon />}
                        onClick={handleStartCreateZona}
                    >
                        Nova Zona
                    </Button>
                    <Typography variant="caption" display="block" sx={{ mt: 2, color: 'text.secondary' }}>
                        Dica: Crie zonas agrupando cômodos com características semelhantes (ex: Áreas Molhadas).
                    </Typography>
                </Grid>
            </Grid>
        )}

        {viewState === 'method_select' && (
            <Grid container spacing={2} justifyContent="center">
                <Grid item xs={12}>
                    <Typography variant="h5" align="center" gutterBottom>Como deseja definir esta zona?</Typography>
                </Grid>
                <Grid item xs={12} md={5}>
                    <Paper 
                        sx={{ p: 3, cursor: 'pointer', '&:hover': { bgcolor: '#f5f5f5' }, textAlign: 'center' }}
                        onClick={() => setViewState('preset_select')}
                        elevation={3}
                    >
                        <ScienceIcon fontSize="large" color="primary" />
                        <Typography variant="h6" mt={1}>Usar Preset Oficial</Typography>
                        <Typography variant="body2" color="text.secondary">
                            Recomendado. Use modelos prontos baseados na NBR 5410 (ex: Área Molhada, Garagem).
                        </Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={5}>
                    <Paper 
                        sx={{ p: 3, cursor: 'pointer', '&:hover': { bgcolor: '#f5f5f5' }, textAlign: 'center' }}
                        onClick={handleCreateCustom}
                        elevation={3}
                    >
                        <SettingsIcon fontSize="large" color="secondary" />
                        <Typography variant="h6" mt={1}>Zona Personalizada</Typography>
                        <Typography variant="body2" color="text.secondary">
                            Defina cada influência manualmente. Ideal para casos específicos.
                        </Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Button onClick={() => setViewState('list')}>Cancelar</Button>
                </Grid>
            </Grid>
        )}

        {viewState === 'preset_select' && (
            <Box>
                <Typography variant="h6" gutterBottom>Selecione um Preset ({project.tipo_instalacao})</Typography>
                <Grid container spacing={2}>
                    {availablePresets.map(preset => (
                        <Grid item xs={12} sm={6} md={4} key={preset.id}>
                            <Card 
                                sx={{ cursor: 'pointer', '&:hover': { boxShadow: 6 }, borderLeft: `5px solid ${preset.cor}` }}
                                onClick={() => handleSelectPreset(preset)}
                            >
                                <CardContent>
                                    <Typography variant="subtitle1" fontWeight="bold">{preset.nome}</Typography>
                                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{preset.descricao}</Typography>
                                    <Box display="flex" gap={0.5} flexWrap="wrap">
                                        <Chip label={preset.influencias.presenca_agua} size="small" />
                                        <Chip label={preset.influencias.competencia_pessoas} size="small" />
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
                <Button sx={{ mt: 3 }} onClick={() => setViewState('method_select')}>Voltar</Button>
            </Box>
        )}

        {viewState === 'form_custom' && (
            <Card variant="outlined" sx={{ maxWidth: 800, mx: 'auto' }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                        {editingZonaId ? 'Editar Zona' : (newZona.origem === 'preset' ? 'Revisar Zona (Baseado em Preset)' : 'Nova Zona Personalizada')}
                    </Typography>
                    
                    {errorMsg && <Alert severity="error" sx={{ mb: 2 }}>{errorMsg}</Alert>}
                    
                    <TextField fullWidth label="Nome da Zona" value={newZona.nome || ''} 
                        onChange={e => setNewZona({...newZona, nome: e.target.value})} margin="normal" />
                    
                    <TextField fullWidth label="Descrição" value={newZona.descricao || ''} 
                        onChange={e => setNewZona({...newZona, descricao: e.target.value})} margin="normal" />

                    <Typography variant="subtitle2" sx={{ mt: 3, mb: 1 }}>Influências Externas</Typography>
                    <Grid container spacing={2}>
                        <Grid item xs={6}>
                            <TextField select fullWidth label="Água (AD)" 
                                value={newZona.presenca_agua || ''} 
                                onChange={e => setNewZona({...newZona, presenca_agua: e.target.value})}
                            >
                                {opcoes?.agua.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={6}>
                             <TextField select fullWidth label="Pessoas (BA)" 
                                value={newZona.competencia_pessoas || ''} 
                                onChange={e => setNewZona({...newZona, competencia_pessoas: e.target.value})}
                            >
                                {opcoes?.pessoas.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={6}>
                             <TextField select fullWidth label="Sólidos (AE)" 
                                value={newZona.presenca_solidos || ''} 
                                onChange={e => setNewZona({...newZona, presenca_solidos: e.target.value})}
                            >
                                {opcoes?.solidos.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                            </TextField>
                        </Grid>
                    </Grid>

                    <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
                        <Button variant="outlined" onClick={() => { setViewState('list'); setEditingZonaId(null); }}>Cancelar</Button>
                        <Button variant="contained" onClick={handleSaveZona}>{editingZonaId ? 'Salvar Alterações' : 'Criar Zona'}</Button>
                    </Box>
                </CardContent>
            </Card>
        )}

      </CustomTabPanel>

      {/* ABA 2: LOCAIS */}
      <CustomTabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
           <Grid item xs={12} md={4}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>{editingLocalId ? 'Editar Cômodo' : 'Novo Cômodo'}</Typography>
                {errorMsg && <Alert severity="error">{errorMsg}</Alert>}

                <TextField fullWidth label="Nome (ex: Suíte)" margin="dense"
                    value={newLocal.nome || ''} onChange={e => setNewLocal({...newLocal, nome: e.target.value})} />
                
                <TextField select fullWidth label="Zona Pertencente" margin="dense"
                   value={newLocal.zona_id || ''} onChange={e => setNewLocal({...newLocal, zona_id: e.target.value})}>
                   {project.zonas?.map(z => <MenuItem key={z.id} value={z.id}>{z.nome}</MenuItem>)}
                </TextField>

                <Grid container spacing={1}>
                  <Grid item xs={6}>
                    <TextField fullWidth label="Área (m²)" type="number" margin="dense"
                        value={newLocal.area_m2 || ''} onChange={e => setNewLocal({...newLocal, area_m2: Number(e.target.value)})} />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField fullWidth label="Perímetro (m)" type="number" margin="dense"
                        value={newLocal.perimetro_m || ''} onChange={e => setNewLocal({...newLocal, perimetro_m: Number(e.target.value)})} />
                  </Grid>
                </Grid>

                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                    {editingLocalId && <Button variant="outlined" fullWidth onClick={handleCancelLocal}>Cancelar</Button>}
                    <Button variant="contained" fullWidth onClick={handleSaveLocal}>
                        {editingLocalId ? 'Salvar' : 'Criar Cômodo'}
                    </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
           <Grid item xs={12} md={8}>
            <Typography variant="h6">Cômodos Cadastrados</Typography>
            {project.locais?.map(l => (
               <Card key={l.id} sx={{ mb: 1, p: 1 }}>
                 <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Box>
                        <Box display="flex" alignItems="center" gap={1}>
                             <Typography fontWeight="bold">{l.nome}</Typography>
                             <Typography variant="caption" sx={{ bgcolor: '#e3f2fd', px: 1, borderRadius: 1 }}>
                                {project.zonas?.find(z => z.id === l.zona_id)?.nome || 'Zona removida'}
                            </Typography>
                        </Box>
                        <Typography variant="body2">Área: {l.area_m2}m² | Perímetro: {l.perimetro_m}m</Typography>
                    </Box>
                    <Box>
                        <IconButton size="small" onClick={() => handleStartEditLocal(l)}><EditIcon fontSize="small" /></IconButton>
                        <IconButton size="small" color="error" onClick={() => handleDeleteLocal(l.id)}><DeleteIcon fontSize="small" /></IconButton>
                    </Box>
                 </Box>
               </Card>
            ))}
            {(!project.locais || project.locais.length === 0) && <Typography color="text.secondary">Nenhum cômodo cadastrado.</Typography>}
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
    base_dir = os.getcwd()
    print(f"--- Iniciando implementação de Edit/Delete de Locais em: {base_dir} ---")

    for file_path, content in files_content.items():
        full_path = os.path.join(base_dir, file_path)
        dir_name = os.path.dirname(full_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"✅ Atualizado: {file_path}")
        except Exception as e:
            print(f"❌ Erro ao atualizar {file_path}: {e}")

    print("\n--- Atualização Concluída ---")
    print("1. Reinicie o Backend (uvicorn)")
    print("2. A UI agora permite editar e excluir locais (cômodos).")

if __name__ == "__main__":
    main()