import os

# ==============================================================================
# SCRIPT DE CORREÇÃO: TRATAMENTO DE DADOS LEGADOS (NO CRASH)
# ==============================================================================

file_content = r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Chip, Divider, 
  Paper
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import ScienceIcon from '@mui/icons-material/Science';

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

const ZoneCard: React.FC<{ zona: Zona }> = ({ zona }) => {
    // FIX: Garante que zonas antigas (sem o campo origem) não quebrem a tela
    const origemSafe = zona.origem || 'custom'; 
    const corSafe = zona.cor_identificacao || '#ccc';

    return (
        <Card variant="outlined" sx={{ mb: 2, borderLeft: `6px solid ${corSafe}` }}>
            <CardContent sx={{ pb: 1 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="h6">{zona.nome}</Typography>
                    <Chip 
                        label={origemSafe.toUpperCase()} 
                        size="small" 
                        color={origemSafe === 'preset' ? 'primary' : 'default'} 
                    />
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
  const { projects, addZonaToProject, addLocalToProject } = useProjectStore();
  
  const project = projects.find(p => p.id === id);
  const [tabValue, setTabValue] = useState(0);
  const [opcoes, setOpcoes] = useState<OpcoesInfluencias | null>(null);
  
  // --- STATES DE CRIAÇÃO ---
  const [viewState, setViewState] = useState<'list' | 'method_select' | 'preset_select' | 'form_custom'>('list');
  const [availablePresets, setAvailablePresets] = useState<PresetZona[]>([]);
  const [selectedPreset, setSelectedPreset] = useState<PresetZona | null>(null);
  
  const [newZona, setNewZona] = useState<Partial<Zona>>({});
  const [newLocal, setNewLocal] = useState<Partial<Local>>({});
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!project) return;
    ProjectService.getOpcoesInfluencias().then(setOpcoes).catch(console.error);
    ProjectService.getPresets(project.tipo_instalacao).then(setAvailablePresets).catch(console.error);
  }, [project]);

  if (!project) return <Container sx={{mt:4}}><Typography>Projeto não encontrado.</Typography></Container>;

  // --- ACTIONS ---

  const handleStartCreateZona = () => {
    if (project.tipo_instalacao.toLowerCase() === 'industrial') {
        setViewState('form_custom');
    } else {
        setViewState('method_select');
    }
    setNewZona({});
    setErrorMsg(null);
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

  const handleSaveZona = async () => {
    try {
      if (!newZona.nome) { setErrorMsg("Nome é obrigatório."); return; }
      
      let finalOrigem = newZona.origem || 'custom';
      
      // Validação de ajuste de preset
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

      const zonaCriada = await ProjectService.createZona(payload as any);
      addZonaToProject(project.id, zonaCriada);
      setViewState('list');
    } catch (error: any) {
        console.error(error);
        setErrorMsg("Erro ao salvar zona.");
    }
  };

  const handleAddLocal = async () => {
    try {
      if (!newLocal.nome || !newLocal.zona_id) { setErrorMsg("Preencha dados obrigatórios."); return; }
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
    } catch (e) { setErrorMsg("Erro ao criar local."); }
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
                    {project.zonas?.map(z => <ZoneCard key={z.id} zona={z} />)}
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
                        {newZona.origem === 'preset' ? 'Revisar Zona (Baseado em Preset)' : 'Nova Zona Personalizada'}
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
                        {/* Adicionar outros campos conforme necessidade */}
                    </Grid>

                    <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
                        <Button variant="outlined" onClick={() => setViewState('list')}>Cancelar</Button>
                        <Button variant="contained" onClick={handleSaveZona}>Salvar Zona</Button>
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
                <Typography variant="h6" gutterBottom>Novo Cômodo</Typography>
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

                <Button variant="contained" fullWidth sx={{ mt: 2 }} onClick={handleAddLocal}>Criar Cômodo</Button>
              </CardContent>
            </Card>
          </Grid>
           <Grid item xs={12} md={8}>
            <Typography variant="h6">Cômodos Cadastrados</Typography>
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
    file_path = "frontend/src/pages/ProjectDetails.tsx"
    full_path = os.path.join(base_dir, file_path)

    print(f"--- Aplicando correção em: {full_path} ---")
    
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(file_content.strip())
        print(f"✅ Arquivo corrigido com sucesso!")
        print(f"👉 Recarregue a página no navegador. O erro deve ter desaparecido.")
    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")

if __name__ == "__main__":
    main()