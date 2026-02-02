import os

# ==============================================================================
# SCRIPT DE CORREÇÃO: LINT ERRORS & TYPE SYNC
# ==============================================================================
# 1. Atualiza Interface TypeScript para refletir o Backend real.
# 2. Corrige erros de tipagem (String vs Number).
# 3. Remove imports e variáveis não utilizadas.
# ==============================================================================

files_content = {

    # --------------------------------------------------------------------------
    # 1. FRONTEND TYPES (Sincronização com Backend/Pydantic)
    # --------------------------------------------------------------------------
    "frontend/src/types/project.ts": r'''
export interface Zona {
  id: string;
  projeto_id: string;
  nome: string;
  descricao?: string;
  
  // UX Metadata
  origem: 'preset' | 'ajustada' | 'custom';
  preset_id?: string;
  
  // Influences
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

export interface Carga {
  id: string;
  local_id: string; // Adicionado
  nome: string;
  tipo: string; // Backend usa "tipo", não "tipo_carga"
  potencia_w: number; // Backend usa lowercase
  potencia_va: number; // Adicionado
  fator_potencia: number; // Adicionado
  quantidade: number;
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
  
  zonas: Zona[];
  locais: Local[];
  cargas: Carga[];
}

export interface PresetZona {
    id: string;
    nome: string;
    descricao: string;
    influencias: {
        temp_ambiente: string;
        presenca_agua: string;
        presenca_solidos: string;
        competencia_pessoas: string;
        materiais_construcao: string;
        estrutura_edificacao: string;
    };
    cor: string;
}
''',

    # --------------------------------------------------------------------------
    # 2. PROJECT DETAILS (Fix Lint & Types)
    # --------------------------------------------------------------------------
    "frontend/src/pages/ProjectDetails.tsx": r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Chip, Paper
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import ScienceIcon from '@mui/icons-material/Science';
import FlashOnIcon from '@mui/icons-material/FlashOn';

import { useProjectStore } from '../store/useProjectStore';
import { ProjectService, OpcoesInfluencias, CargaCreateDTO } from '../api/client';
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

// --- COMPONENTE DE CARGA ---
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
  // Removed unused selectedPreset state
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
    // Removed unused setSelectedPreset
    setNewZona({
        nome: preset.nome,
        descricao: preset.descricao,
        origem: 'preset',
        preset_id: preset.id,
        cor_identificacao: preset.cor 
    });
    setViewState('form_custom'); 
  };

  const handleSaveZona = async () => {
    try {
      if (!newZona.nome) { setErrorMsg("Nome é obrigatório."); return; }
      setErrorMsg(null);
      
      const payload = {
          projeto_id: project.id,
          nome: newZona.nome,
          descricao: newZona.descricao,
          origem: newZona.origem,
          preset_id: newZona.preset_id,
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
            // FIX: Convertendo para Number explicitamente
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
                     
                     {errorMsg && <Alert severity="error" sx={{mb:2}}>{errorMsg}</Alert>}

                     <TextField fullWidth margin="normal" label="Nome" value={newZona.nome || ''} onChange={e => setNewZona({...newZona, nome: e.target.value})} />
                     
                     {newZona.origem === 'custom' && (
                         <Box sx={{ mt: 2 }}>
                             <Alert severity="warning" sx={{ mb: 2 }}>Modo Avançado: Você é responsável pela conformidade normativa.</Alert>
                             <TextField select fullWidth label="Presença de Água" value={newZona.presenca_agua || ''} onChange={e => setNewZona({...newZona, presenca_agua: e.target.value})}>
                                {opcoes?.agua.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.descricao}</MenuItem>)}
                             </TextField>
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
                            <Grid item xs={6}><TextField fullWidth size="small" margin="dense" type="number" label="Area" value={newLocal.area_m2 || ''} onChange={e => setNewLocal({...newLocal, area_m2: Number(e.target.value)})} /></Grid>
                            <Grid item xs={6}><TextField fullWidth size="small" margin="dense" type="number" label="Perim" value={newLocal.perimetro_m || ''} onChange={e => setNewLocal({...newLocal, perimetro_m: Number(e.target.value)})} /></Grid>
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
                            
                            {addingCargaToLocalId === local.id && (
                                <CargaForm localId={local.id} projectId={project.id} onClose={() => setAddingCargaToLocalId(null)} />
                            )}

                            <Box sx={{ mt: 2 }}>
                                {project.cargas?.filter(c => c.local_id === local.id).map(carga => (
                                    <Box key={carga.id} display="flex" justifyContent="space-between" sx={{ borderBottom: '1px solid #eee', py: 1 }}>
                                        {/* FIX: Usando tipo e potencia_w/potencia_va corretos */}
                                        <Typography variant="body2">{carga.nome} ({carga.tipo})</Typography>
                                        <Typography variant="body2" fontWeight="bold">
                                            {carga.quantidade}x {carga.potencia_w}W / {carga.potencia_va}VA
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
    base_dir = os.getcwd()
    for file_path, content in files_content.items():
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"✅ Arquivo corrigido: {file_path}")
        except Exception as e:
            print(f"❌ Erro ao escrever {file_path}: {e}")

if __name__ == "__main__":
    main()