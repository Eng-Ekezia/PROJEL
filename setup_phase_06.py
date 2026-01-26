import os
import pathlib

# ==============================================================================
# DEFINIÇÃO DO CONTEÚDO DOS ARQUIVOS (BACKEND & FRONTEND)
# ==============================================================================

files_content = {
    # --------------------------------------------------------------------------
    # 1. BACKEND - ENDPOINT ZONAS
    # --------------------------------------------------------------------------
    "backend/api/v1/endpoints/zonas.py": r'''
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import uuid
from datetime import datetime

# Imports do Domínio
from domain_core.schemas.zona import Zona, ZonaCreate
from domain_core.enums.influencias import (
    TemperaturaAmbiente, PresencaAgua, PresencaSolidos, 
    CompetenciaPessoas, MateriaisConstrucao, EstruturaEdificacao
)

router = APIRouter()

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

@router.get("/opcoes-influencias", response_model=Dict[str, List[Dict[str, str]]])
async def listar_opcoes_influencias():
    """
    Retorna opções da NBR 5410 para Dropdowns do Frontend.
    """
    def enum_to_list(enum_cls):
        return [{"codigo": e.name, "descricao": e.value} for e in enum_cls]

    return {
        "temperatura": enum_to_list(TemperaturaAmbiente),
        "agua": enum_to_list(PresencaAgua),
        "solidos": enum_to_list(PresencaSolidos),
        "pessoas": enum_to_list(CompetenciaPessoas),
        "materiais": enum_to_list(MateriaisConstrucao),
        "estrutura": enum_to_list(EstruturaEdificacao),
    }
''',

    # --------------------------------------------------------------------------
    # 2. BACKEND - ENDPOINT LOCAIS
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
    if local_in.area_m2 <= 0:
        raise HTTPException(status_code=400, detail="A área deve ser maior que zero.")
    
    if local_in.perimetro_m <= 0:
        raise HTTPException(status_code=400, detail="O perímetro deve ser maior que zero.")

    # Validação Geométrica Básica (Evita dados impossíveis)
    if local_in.perimetro_m < (local_in.area_m2 ** 0.5) * 2:
         raise HTTPException(status_code=400, detail="Perímetro muito pequeno para a área informada (Geometria impossível).")

    novo_local = Local(
        id=str(uuid.uuid4()),
        data_criacao=datetime.now(),
        **local_in.model_dump()
    )
    return novo_local
''',

    # --------------------------------------------------------------------------
    # 3. BACKEND - INIT (PACKAGE)
    # --------------------------------------------------------------------------
    "backend/api/v1/endpoints/__init__.py": "",

    # --------------------------------------------------------------------------
    # 4. BACKEND - API ROUTER (ATUALIZADO)
    # --------------------------------------------------------------------------
    "backend/api/v1/api.py": r'''
from fastapi import APIRouter
from backend.api.v1.endpoints import system, zonas, locais 

api_router = APIRouter()

# Rotas de Sistema
api_router.include_router(system.router, prefix="/system", tags=["system"])

# Rotas de Domínio (Phase 06)
api_router.include_router(zonas.router, prefix="/zonas", tags=["zonas - influências"])
api_router.include_router(locais.router, prefix="/locais", tags=["locais - arquitetura"])
''',

    # --------------------------------------------------------------------------
    # 5. FRONTEND - TYPES (PROJECT.TS)
    # --------------------------------------------------------------------------
    "frontend/src/types/project.ts": r'''
export interface Zona {
  id: string;
  projeto_id: string;
  nome: string;
  descricao?: string;
  temp_ambiente: string;
  presenca_agua: string;
  presenca_solidos: string;
  competencia_pessoas: string;
  materiais_construcao: string;
  estrutura_edificacao: string;
  cor_identificacao: string;
  data_criacao: string;
}

export interface Local {
  id: string;
  projeto_id: string;
  zona_id: string;
  nome: string;
  area_m2: number;
  perimetro_m: number;
  pe_direito_m: number;
  data_criacao: string;
}

export interface Projeto {
  id: string;
  nome: string;
  tipo_instalacao: string;
  tensao_sistema: string;
  sistema: string;
  esquema_aterramento: string;
  descricao_aterramento?: string;
  data_criacao: string;
  ultima_modificacao: string;
  
  // Listas de entidades filhas
  zonas: Zona[];
  locais: Local[];
}
''',

    # --------------------------------------------------------------------------
    # 6. FRONTEND - STORE (ZUSTAND)
    # --------------------------------------------------------------------------
    "frontend/src/store/useProjectStore.ts": r'''
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Projeto, Zona, Local } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  addProject: (project: Projeto) => void;
  updateProject: (id: string, data: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  
  // Actions da Fase 06
  addZonaToProject: (projetoId: string, zona: Zona) => void;
  addLocalToProject: (projetoId: string, local: Local) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set) => ({
      projects: [],
      
      addProject: (project) => set((state) => ({ 
        projects: [...state.projects, { ...project, zonas: [], locais: [] }] 
      })),

      updateProject: (id, data) => set((state) => ({
        projects: state.projects.map((p) => (p.id === id ? { ...p, ...data, ultima_modificacao: new Date().toISOString() } : p)),
      })),

      deleteProject: (id) => set((state) => ({
        projects: state.projects.filter((p) => p.id !== id),
      })),

      addZonaToProject: (projetoId, zona) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const zonasAtuais = p.zonas || [];
          return { ...p, zonas: [...zonasAtuais, zona], ultima_modificacao: new Date().toISOString() };
        })
      })),

      addLocalToProject: (projetoId, local) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const locaisAtuais = p.locais || [];
          return { ...p, locais: [...locaisAtuais, local], ultima_modificacao: new Date().toISOString() };
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
    # 7. FRONTEND - API CLIENT
    # --------------------------------------------------------------------------
    "frontend/src/api/client.ts": r'''
import axios from 'axios';
import { Zona, Local } from '../types/project';

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

  createZona: async (zona: Omit<Zona, 'id' | 'data_criacao'>): Promise<Zona> => {
    const response = await api.post<Zona>('/zonas/', zona);
    return response.data;
  },

  createLocal: async (local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.post<Local>('/locais/', local);
    return response.data;
  }
};
''',

    # --------------------------------------------------------------------------
    # 8. FRONTEND - PAGE PROJECT DETAILS
    # --------------------------------------------------------------------------
    "frontend/src/pages/ProjectDetails.tsx": r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Divider
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useProjectStore } from '../store/useProjectStore';
import { ProjectService, OpcoesInfluencias } from '../api/client';
import { Zona, Local } from '../types/project';

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

const ProjectDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { projects, addZonaToProject, addLocalToProject } = useProjectStore();
  
  const project = projects.find(p => p.id === id);
  const [tabValue, setTabValue] = useState(0);
  const [opcoes, setOpcoes] = useState<OpcoesInfluencias | null>(null);
  
  // Forms States
  const [newZona, setNewZona] = useState<Partial<Zona>>({});
  const [newLocal, setNewLocal] = useState<Partial<Local>>({});
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!project) return;
    ProjectService.getOpcoesInfluencias().then(setOpcoes).catch(err => console.error("Erro API:", err));
  }, [project]);

  if (!project) return <Container sx={{mt:4}}><Typography>Projeto não encontrado.</Typography></Container>;

  const handleAddZona = async () => {
    try {
      if (!newZona.nome) { setErrorMsg("Nome da zona é obrigatório."); return; }
      
      const zonaCriada = await ProjectService.createZona({
        projeto_id: project.id,
        nome: newZona.nome,
        temp_ambiente: newZona.temp_ambiente || 'AA4',
        presenca_agua: newZona.presenca_agua || 'AD1',
        presenca_solidos: newZona.presenca_solidos || 'AE1',
        competencia_pessoas: newZona.competencia_pessoas || 'BA1',
        materiais_construcao: newZona.materiais_construcao || 'CA2',
        estrutura_edificacao: newZona.estrutura_edificacao || 'CB1',
        cor_identificacao: '#ddd'
      } as any);
      
      addZonaToProject(project.id, zonaCriada);
      setNewZona({});
      setErrorMsg(null);
    } catch (error: any) {
      console.error(error);
      setErrorMsg("Erro ao criar zona. Verifique o console.");
    }
  };

  const handleAddLocal = async () => {
    try {
      if (!newLocal.nome || !newLocal.zona_id) {
        setErrorMsg("Preencha o nome e selecione uma zona.");
        return;
      }
      const localCriado = await ProjectService.createLocal({
        projeto_id: project.id,
        zona_id: newLocal.zona_id,
        nome: newLocal.nome,
        area_m2: Number(newLocal.area_m2),
        perimetro_m: Number(newLocal.perimetro_m),
        pe_direito_m: 2.8
      } as any);

      addLocalToProject(project.id, localCriado);
      setNewLocal({});
      setErrorMsg(null);
    } catch (error: any) {
        const msg = error.response?.data?.detail || "Erro ao criar local (verifique geometria).";
        setErrorMsg(msg);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} sx={{ mb: 2 }}>
        Voltar para Dashboard
      </Button>
      
      <Typography variant="h4" gutterBottom>
        {project.nome} 
        <Typography component="span" variant="subtitle1" color="text.secondary" sx={{ ml: 2 }}>
          ({project.tipo_instalacao})
        </Typography>
      </Typography>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="1. Ambientes (Zonas)" />
          <Tab label="2. Arquitetura (Locais)" />
        </Tabs>
      </Box>

      {/* ABA ZONAS */}
      <CustomTabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={5}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>Nova Zona de Influência</Typography>
                {errorMsg && <Alert severity="error" sx={{ mb: 2 }}>{errorMsg}</Alert>}
                
                <TextField fullWidth label="Nome (ex: Área Molhada)" margin="dense" 
                    value={newZona.nome || ''} onChange={e => setNewZona({...newZona, nome: e.target.value})} />
                
                {opcoes ? (
                  <>
                    <TextField select fullWidth label="Água (AD)" margin="dense"
                      value={newZona.presenca_agua || ''} onChange={e => setNewZona({...newZona, presenca_agua: e.target.value})}>
                      {opcoes.agua.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                    </TextField>
                    <TextField select fullWidth label="Pessoas (BA)" margin="dense"
                      value={newZona.competencia_pessoas || ''} onChange={e => setNewZona({...newZona, competencia_pessoas: e.target.value})}>
                      {opcoes.pessoas.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                    </TextField>
                  </>
                ) : <Typography variant="caption">Carregando opções da norma...</Typography>}
                
                <Button variant="contained" fullWidth sx={{ mt: 2 }} onClick={handleAddZona}>Salvar Zona</Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={7}>
            <Typography variant="h6" gutterBottom>Zonas Cadastradas</Typography>
            {project.zonas?.map(z => (
               <Card key={z.id} sx={{ mb: 1, p: 1, bgcolor: '#f5f5f5' }}>
                 <Typography fontWeight="bold">{z.nome}</Typography>
                 <Typography variant="caption">
                   {z.presenca_agua} • {z.competencia_pessoas} • {z.temp_ambiente}
                 </Typography>
               </Card>
            ))}
            {(!project.zonas || project.zonas.length === 0) && <Typography color="text.secondary">Nenhuma zona definida.</Typography>}
          </Grid>
        </Grid>
      </CustomTabPanel>

      {/* ABA LOCAIS */}
      <CustomTabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
           <Grid item xs={12} md={5}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>Novo Cômodo</Typography>
                {errorMsg && <Alert severity="error" sx={{ mb: 2 }}>{errorMsg}</Alert>}

                <TextField fullWidth label="Nome (ex: Suíte Master)" margin="dense"
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

                <Button variant="contained" fullWidth sx={{ mt: 2 }} onClick={handleAddLocal}>Criar Cômodo</Button>
              </CardContent>
            </Card>
          </Grid>
           <Grid item xs={12} md={7}>
            <Typography variant="h6" gutterBottom>Cômodos Cadastrados</Typography>
            {project.locais?.map(l => (
               <Card key={l.id} sx={{ mb: 1, p: 1 }}>
                 <Box display="flex" justifyContent="space-between">
                    <Typography fontWeight="bold">{l.nome}</Typography>
                    <Typography variant="caption" sx={{ bgcolor: '#e3f2fd', px: 1, borderRadius: 1 }}>
                        {project.zonas?.find(z => z.id === l.zona_id)?.nome}
                    </Typography>
                 </Box>
                 <Typography variant="body2">Área: {l.area_m2}m² | Perímetro: {l.perimetro_m}m</Typography>
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
''',

    # --------------------------------------------------------------------------
    # 9. FRONTEND - ROUTER APP.TSX
    # --------------------------------------------------------------------------
    "frontend/src/App.tsx": r'''
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ProjectDetails from './pages/ProjectDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/project/:id" element={<ProjectDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
'''
}

# ==============================================================================
# EXECUÇÃO DA CRIAÇÃO
# ==============================================================================

def main():
    base_dir = os.getcwd()
    print(f"--- Iniciando configuração da Phase 06 em: {base_dir} ---")

    # Verificação simples de segurança
    if not os.path.exists(os.path.join(base_dir, "backend")) or not os.path.exists(os.path.join(base_dir, "frontend")):
        print("ERRO CRÍTICO: Você não parece estar na raiz do projeto (pastas backend/frontend não encontradas).")
        return

    for file_path, content in files_content.items():
        full_path = os.path.join(base_dir, file_path)
        dir_name = os.path.dirname(full_path)

        # 1. Criar diretório se não existir
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 Diretório criado: {dir_name}")

        # 2. Escrever arquivo (Overwrite)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"✅ Arquivo criado/atualizado: {file_path}")
        except Exception as e:
            print(f"❌ Erro ao criar {file_path}: {e}")

    print("\n--- Processo concluído com sucesso! ---")
    print("1. Reinicie o Backend (Ctrl+C -> uvicorn main:app --reload)")
    print("2. Reinicie o Frontend (Ctrl+C -> npm run dev)")
    print("3. Teste a criação de Zonas e Cômodos na nova página.")

if __name__ == "__main__":
    main()