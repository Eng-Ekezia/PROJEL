import os

# ==============================================================================
# 1. REFACTOR DOS ENUMS (SEPARAR CÓDIGO DA DESCRIÇÃO)
# ==============================================================================
# Agora o Enum vale apenas o código (ex: "AA4"). 
# As descrições ficam num dicionário auxiliar.

influencias_content = r'''
from enum import Enum

# --- ENUMS (VALORES PUROS PARA O BANCO DE DADOS) ---

class TemperaturaAmbiente(str, Enum):
    AA1 = "AA1"
    AA2 = "AA2"
    AA3 = "AA3"
    AA4 = "AA4"
    AA5 = "AA5"
    AA6 = "AA6"
    AA7 = "AA7"
    AA8 = "AA8"

class PresencaAgua(str, Enum):
    AD1 = "AD1"
    AD2 = "AD2"
    AD3 = "AD3"
    AD4 = "AD4"
    AD5 = "AD5"
    AD6 = "AD6"
    AD7 = "AD7"
    AD8 = "AD8"

class PresencaSolidos(str, Enum):
    AE1 = "AE1"
    AE2 = "AE2"
    AE3 = "AE3"
    AE4 = "AE4"
    AE5 = "AE5"
    AE6 = "AE6"

class CompetenciaPessoas(str, Enum):
    BA1 = "BA1"
    BA2 = "BA2"
    BA3 = "BA3"
    BA4 = "BA4"
    BA5 = "BA5"

class MateriaisConstrucao(str, Enum):
    CA1 = "CA1"
    CA2 = "CA2"

class EstruturaEdificacao(str, Enum):
    CB1 = "CB1"
    CB2 = "CB2"
    CB3 = "CB3"
    CB4 = "CB4"

# --- MAPA DE DESCRIÇÕES (PARA A UI) ---

DESCRICOES = {
    # Temperatura
    "AA1": "AA1 - Frigorífico (-60°C a +5°C)",
    "AA2": "AA2 - Muito Frio (-40°C a +5°C)",
    "AA3": "AA3 - Frio (-25°C a +5°C)",
    "AA4": "AA4 - Temperada (-5°C a +40°C)",
    "AA5": "AA5 - Quente (+5°C a +40°C)",
    "AA6": "AA6 - Muito Quente (+5°C a +60°C)",
    "AA7": "AA7 - Extrema (-25°C a +55°C)",
    "AA8": "AA8 - Faixa Expandida (-50°C a +40°C)",
    
    # Água
    "AD1": "AD1 - Desprezível (Locais secos, IPX0)",
    "AD2": "AD2 - Gotejamento (Queda vertical, IPX1/IPX2)",
    "AD3": "AD3 - Aspersão (Chuva até 60°, IPX3)",
    "AD4": "AD4 - Projeções (Lavagens c/ mangueira, IPX4)",
    "AD5": "AD5 - Jatos (Jatos de água, IPX5)",
    "AD6": "AD6 - Ondas (Beira-mar, IPX6)",
    "AD7": "AD7 - Imersão (Piscinas/Espelhos d'água, IPX7)",
    "AD8": "AD8 - Submersão (Mergulho profundo, IPX8)",

    # Sólidos
    "AE1": "AE1 - Desprezível (Ambiente doméstico)",
    "AE2": "AE2 - Pequenos objetos (2.5mm)",
    "AE3": "AE3 - Objetos muito pequenos (1mm - Fios)",
    "AE4": "AE4 - Poeira leve",
    "AE5": "AE5 - Poeira moderada",
    "AE6": "AE6 - Poeira intensa (Cimento/Moinhos)",

    # Pessoas
    "BA1": "BA1 - Comuns (Pessoas não advertidas)",
    "BA2": "BA2 - Crianças (Creches/Escolas infantis)",
    "BA3": "BA3 - Deficientes (Hospitais/Asilos)",
    "BA4": "BA4 - Advertidas (Zeladores/Manutenção)",
    "BA5": "BA5 - Qualificadas (Engenheiros/Técnicos)",

    # Construção
    "CA1": "CA1 - Não combustíveis (Alvenaria, concreto)",
    "CA2": "CA2 - Combustíveis (Madeira)",
    
    # Estrutura
    "CB1": "CB1 - Riscos desprezíveis",
    "CB2": "CB2 - Sujeita a propagação de incêndio",
    "CB3": "CB3 - Sujeita a movimentação",
    "CB4": "CB4 - Flexíveis ou instáveis"
}
'''

# ==============================================================================
# 2. ATUALIZAR ENDPOINT (USAR AS NOVAS DESCRIÇÕES)
# ==============================================================================

endpoint_zonas_content = r'''
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
    Usa o dicionário DESCRICOES para fornecer o texto amigável.
    """
    def enum_to_list(enum_cls):
        # codigo = Valor do Enum (ex: "AA4")
        # descricao = Texto do Dict (ex: "AA4 - Temperada...")
        return [{
            "codigo": e.value, 
            "descricao": DESCRICOES.get(e.value, e.value) 
        } for e in enum_cls]

    return {
        "temperatura": enum_to_list(TemperaturaAmbiente),
        "agua": enum_to_list(PresencaAgua),
        "solidos": enum_to_list(PresencaSolidos),
        "pessoas": enum_to_list(CompetenciaPessoas),
        "materiais": enum_to_list(MateriaisConstrucao),
        "estrutura": enum_to_list(EstruturaEdificacao),
    }
'''

# ==============================================================================
# 3. CORRIGIR FRONTEND (MUI CHILDREN ERROR)
# ==============================================================================

project_details_content = r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Divider
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useProjectStore } from '../store/useProjectStore';
import { ProjectService } from '../api/client';
import type { OpcoesInfluencias } from '../api/client';
import type { Zona, Local } from '../types/project';

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
      const msg = error.response?.data?.detail 
        ? JSON.stringify(error.response.data.detail)
        : "Erro ao criar zona.";
      setErrorMsg(msg);
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
                 <Typography variant="caption" display="block">
                   Água: {opcoes?.agua.find(x => x.codigo === z.presenca_agua)?.descricao || z.presenca_agua}
                 </Typography>
                 <Typography variant="caption" display="block">
                   Pessoas: {opcoes?.pessoas.find(x => x.codigo === z.competencia_pessoas)?.descricao || z.competencia_pessoas}
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
                
                {/* CORREÇÃO DO ERRO MUI: Se não houver zonas, mostra item desabilitado */}
                <TextField select fullWidth label="Zona Pertencente" margin="dense"
                   value={newLocal.zona_id || ''} onChange={e => setNewLocal({...newLocal, zona_id: e.target.value})}>
                   
                   {project.zonas && project.zonas.length > 0 ? (
                     project.zonas.map(z => <MenuItem key={z.id} value={z.id}>{z.nome}</MenuItem>)
                   ) : (
                     <MenuItem disabled value="">Cadastre uma Zona primeiro</MenuItem>
                   )}

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
'''

def main():
    base_dir = os.getcwd()
    
    # 1. Atualizar Influencias (Backend)
    with open(os.path.join(base_dir, "domain_core/enums/influencias.py"), "w", encoding="utf-8") as f:
        f.write(influencias_content.strip())
    print("✅ domain_core/enums/influencias.py atualizado.")

    # 2. Atualizar Endpoint Zonas (Backend)
    with open(os.path.join(base_dir, "backend/api/v1/endpoints/zonas.py"), "w", encoding="utf-8") as f:
        f.write(endpoint_zonas_content.strip())
    print("✅ backend/api/v1/endpoints/zonas.py atualizado.")
    
    # 3. Atualizar Frontend (Corrigir MUI e Exibir Descrições)
    with open(os.path.join(base_dir, "frontend/src/pages/ProjectDetails.tsx"), "w", encoding="utf-8") as f:
        f.write(project_details_content.strip())
    print("✅ frontend/src/pages/ProjectDetails.tsx atualizado.")

if __name__ == "__main__":
    main()