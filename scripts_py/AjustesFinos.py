import os

# ==============================================================================
# SCRIPT DE CORREÇÃO EMERGENCIAL: RESTAURAÇÃO DE FUNCIONALIDADES
# ==============================================================================
# 1. Restaura BatchCargasDialog (Entrada em lote/planilha).
# 2. Expande formulário de Zonas para exibir TODAS as influências (AA, AD, AE, BA, CA, CB).
# ==============================================================================

files_content = {
    "frontend/src/pages/ProjectDetails.tsx": r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Chip, 
  Paper, IconButton, Dialog, DialogTitle, DialogContent, DialogActions,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Tooltip
} from '@mui/material';

// Icons
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import ScienceIcon from '@mui/icons-material/Science';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import PlaylistAddIcon from '@mui/icons-material/PlaylistAdd'; // Icone do Lote

// Stores & API
import { useProjectStore } from '../store/useProjectStore';
import { ProjectService } from '../api/client';
import type { OpcoesInfluencias, CargaCreateDTO } from '../api/client';
import type { Zona, Local, PresetZona, Carga } from '../types/project';

// --- HELPERS ---
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

// --- DIALOGS ---

// 1. DIALOG DE LOTE (RESTAURADO)
const BatchCargasDialog: React.FC<{ 
    open: boolean, 
    onClose: () => void, 
    locais: Local[], 
    projetoId: string,
    onSave: (cargas: CargaCreateDTO[]) => Promise<void>
}> = ({ open, onClose, locais, projetoId, onSave }) => {
    // Estado local para linhas da tabela
    const [rows, setRows] = useState<CargaCreateDTO[]>([
        { projeto_id: projetoId, local_id: '', nome: 'Iluminação', tipo: 'ILUMINACAO', quantidade: 1, potencia: 100, unidade: 'VA', fator_potencia: 1.0 }
    ]);

    const handleChange = (index: number, field: keyof CargaCreateDTO, value: any) => {
        const newRows = [...rows];
        newRows[index] = { ...newRows[index], [field]: value };
        setRows(newRows);
    };

    const addRow = () => {
        setRows([...rows, { projeto_id: projetoId, local_id: '', nome: '', tipo: 'TUG', quantidade: 1, potencia: 100, unidade: 'VA', fator_potencia: 1.0 }]);
    };

    const removeRow = (index: number) => {
        const newRows = rows.filter((_, i) => i !== index);
        setRows(newRows);
    };

    const handleSave = async () => {
        // Filtra linhas vazias (sem local ou nome)
        const validRows = rows.filter(r => r.local_id && r.nome);
        await onSave(validRows);
        onClose();
        // Reset básico
        setRows([{ projeto_id: projetoId, local_id: '', nome: '', tipo: 'TUG', quantidade: 1, potencia: 100, unidade: 'VA', fator_potencia: 1.0 }]);
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
            <DialogTitle>Entrada de Cargas em Lote (Modo Planilha)</DialogTitle>
            <DialogContent>
                <TableContainer component={Paper} variant="outlined" sx={{ mt: 1 }}>
                    <Table size="small">
                        <TableHead>
                            <TableRow sx={{ bgcolor: '#eee' }}>
                                <TableCell width="20%">Local</TableCell>
                                <TableCell width="25%">Descrição</TableCell>
                                <TableCell width="15%">Tipo</TableCell>
                                <TableCell width="10%">Qtd</TableCell>
                                <TableCell width="10%">Potência</TableCell>
                                <TableCell width="10%">Unid.</TableCell>
                                <TableCell width="5%"></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows.map((row, idx) => (
                                <TableRow key={idx}>
                                    <TableCell>
                                        <TextField select fullWidth size="small" variant="standard" value={row.local_id} onChange={e => handleChange(idx, 'local_id', e.target.value)}>
                                            {locais.map(l => <MenuItem key={l.id} value={l.id}>{l.nome}</MenuItem>)}
                                        </TextField>
                                    </TableCell>
                                    <TableCell>
                                        <TextField fullWidth size="small" variant="standard" value={row.nome} onChange={e => handleChange(idx, 'nome', e.target.value)} />
                                    </TableCell>
                                    <TableCell>
                                        <TextField select fullWidth size="small" variant="standard" value={row.tipo} onChange={e => handleChange(idx, 'tipo', e.target.value)}>
                                            <MenuItem value="ILUMINACAO">Ilum.</MenuItem>
                                            <MenuItem value="TUG">TUG</MenuItem>
                                            <MenuItem value="TUE">TUE</MenuItem>
                                        </TextField>
                                    </TableCell>
                                    <TableCell>
                                        <TextField type="number" fullWidth size="small" variant="standard" value={row.quantidade} onChange={e => handleChange(idx, 'quantidade', Number(e.target.value))} />
                                    </TableCell>
                                    <TableCell>
                                        <TextField type="number" fullWidth size="small" variant="standard" value={row.potencia} onChange={e => handleChange(idx, 'potencia', Number(e.target.value))} />
                                    </TableCell>
                                    <TableCell>
                                        <TextField select fullWidth size="small" variant="standard" value={row.unidade} onChange={e => handleChange(idx, 'unidade', e.target.value)}>
                                            <MenuItem value="W">W</MenuItem>
                                            <MenuItem value="VA">VA</MenuItem>
                                        </TextField>
                                    </TableCell>
                                    <TableCell>
                                        <IconButton size="small" color="error" onClick={() => removeRow(idx)} disabled={rows.length === 1}><DeleteIcon /></IconButton>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                <Button startIcon={<AddCircleOutlineIcon />} onClick={addRow} sx={{ mt: 2 }}>Adicionar Linha</Button>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancelar</Button>
                <Button variant="contained" onClick={handleSave} color="primary">Processar Lote</Button>
            </DialogActions>
        </Dialog>
    );
};

// 2. DIALOG INDIVIDUAL (Carga Única)
const CargaDialog: React.FC<{
    open: boolean,
    onClose: () => void,
    initialData?: Carga | null,
    locais: Local[],
    projetoId: string,
    onSave: (carga: CargaCreateDTO) => Promise<void>
}> = ({ open, onClose, initialData, locais, projetoId, onSave }) => {
    const [form, setForm] = useState<CargaCreateDTO>({
        projeto_id: projetoId, local_id: '', nome: '', tipo: 'TUG',
        quantidade: 1, potencia: 100, unidade: 'VA', fator_potencia: 1.0
    });

    useEffect(() => {
        if (initialData) {
            setForm({
                projeto_id: projetoId,
                local_id: initialData.local_id,
                nome: initialData.nome,
                tipo: initialData.tipo,
                quantidade: initialData.quantidade,
                potencia: initialData.potencia_va > 0 ? initialData.potencia_va : initialData.potencia_w,
                unidade: initialData.potencia_va > 0 ? 'VA' : 'W',
                fator_potencia: initialData.fator_potencia
            });
        } else {
            setForm({ projeto_id: projetoId, local_id: '', nome: '', tipo: 'TUG', quantidade: 1, potencia: 100, unidade: 'VA', fator_potencia: 1.0 });
        }
    }, [initialData, open, projetoId]);

    const handleSubmit = async () => {
        await onSave(form);
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
            <DialogTitle>{initialData ? 'Editar Carga' : 'Nova Carga'}</DialogTitle>
            <DialogContent>
                <Grid container spacing={2} sx={{ mt: 1 }}>
                     <Grid item xs={12}>
                        <TextField select fullWidth label="Local" value={form.local_id} onChange={e => setForm({...form, local_id: e.target.value})}>
                            {locais.map(l => <MenuItem key={l.id} value={l.id}>{l.nome}</MenuItem>)}
                        </TextField>
                     </Grid>
                     <Grid item xs={12}>
                        <TextField fullWidth label="Descrição" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
                     </Grid>
                     <Grid item xs={6}>
                        <TextField select fullWidth label="Tipo" value={form.tipo} onChange={e => setForm({...form, tipo: e.target.value})}>
                            <MenuItem value="ILUMINACAO">Iluminação</MenuItem>
                            <MenuItem value="TUG">TUG</MenuItem>
                            <MenuItem value="TUE">TUE</MenuItem>
                        </TextField>
                     </Grid>
                     <Grid item xs={6}>
                        <TextField type="number" fullWidth label="Quantidade" value={form.quantidade} onChange={e => setForm({...form, quantidade: Number(e.target.value)})} />
                     </Grid>
                     <Grid item xs={6}>
                        <TextField type="number" fullWidth label="Potência" value={form.potencia} onChange={e => setForm({...form, potencia: Number(e.target.value)})} />
                     </Grid>
                     <Grid item xs={6}>
                        <TextField select fullWidth label="Unidade" value={form.unidade} onChange={e => setForm({...form, unidade: e.target.value as any})}>
                            <MenuItem value="W">Watts (W)</MenuItem>
                            <MenuItem value="VA">VA</MenuItem>
                        </TextField>
                     </Grid>
                     <Grid item xs={6}>
                        <TextField type="number" fullWidth label="Fator Potência" value={form.fator_potencia} onChange={e => setForm({...form, fator_potencia: Number(e.target.value)})} />
                     </Grid>
                </Grid>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancelar</Button>
                <Button variant="contained" onClick={handleSubmit}>Salvar</Button>
            </DialogActions>
        </Dialog>
    );
};

// --- COMPONENTE PRINCIPAL ---
const ProjectDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { 
      projects, 
      addZonaToProject, updateZonaInProject, removeZonaFromProject, 
      addLocalToProject, updateLocalInProject, removeLocalFromProject, 
      addCargaToProject, updateCargaInProject, removeCargaFromProject 
  } = useProjectStore();
  
  const project = projects.find(p => p.id === id);
  const [tabValue, setTabValue] = useState(0);
  const [opcoes, setOpcoes] = useState<OpcoesInfluencias | null>(null);
  const [availablePresets, setAvailablePresets] = useState<PresetZona[]>([]);
  
  // UX States
  const [viewState, setViewState] = useState<'list' | 'method_select' | 'preset_select' | 'form_custom'>('list');
  const [editingZonaId, setEditingZonaId] = useState<string | null>(null);
  const [editingLocalId, setEditingLocalId] = useState<string | null>(null);
  
  const [cargaDialogOpen, setCargaDialogOpen] = useState(false);
  const [batchDialogOpen, setBatchDialogOpen] = useState(false); // RESTAURADO
  const [editingCarga, setEditingCarga] = useState<Carga | null>(null);
  
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  
  // Forms
  const [newZona, setNewZona] = useState<Partial<Zona>>({});
  const [newLocal, setNewLocal] = useState<Partial<Local>>({});

  useEffect(() => {
    if (!project) return;
    ProjectService.getOpcoesInfluencias().then(setOpcoes).catch(console.error);
    ProjectService.getPresets(project.tipo_instalacao).then(setAvailablePresets).catch(console.error);
  }, [project]);

  if (!project) return <Container sx={{mt:4}}><Typography>Projeto não encontrado.</Typography></Container>;

  // --- ACTIONS ZONA ---
  const handleEditZona = (z: Zona) => {
      setEditingZonaId(z.id);
      setNewZona(z);
      setViewState('form_custom');
  };

  const handleSelectPreset = (preset: PresetZona) => {
    setNewZona({
        nome: preset.nome, descricao: preset.descricao, origem: 'preset', preset_id: preset.id, cor_identificacao: preset.cor 
    });
    setViewState('form_custom'); 
  };

  const handleSaveZona = async () => {
    if (!newZona.nome) { setErrorMsg("Nome obrigatório"); return; }
    try {
        if (editingZonaId) {
            const updated = await ProjectService.updateZona(editingZonaId, { ...newZona, projeto_id: project.id });
            updateZonaInProject(project.id, updated);
        } else {
            const created = await ProjectService.createZona({ ...newZona, projeto_id: project.id });
            addZonaToProject(project.id, created);
        }
        setViewState('list'); setNewZona({}); setEditingZonaId(null);
    } catch (e) { setErrorMsg("Erro ao salvar zona"); }
  };

  const handleDeleteZona = async (zId: string) => {
    if (confirm("Excluir zona? Locais vinculados ficarão sem zona.")) {
        await ProjectService.deleteZona(zId);
        removeZonaFromProject(project.id, zId);
    }
  };

  // --- ACTIONS LOCAL ---
  const handleEditLocal = (l: Local) => {
      setEditingLocalId(l.id);
      setNewLocal(l);
      window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSaveLocal = async () => {
    if (!newLocal.nome || !newLocal.zona_id) { setErrorMsg("Nome e Zona obrigatórios"); return; }
    try {
        const payload = {
            projeto_id: project.id,
            zona_id: newLocal.zona_id,
            nome: newLocal.nome,
            area_m2: Number(newLocal.area_m2),
            perimetro_m: Number(newLocal.perimetro_m),
            pe_direito_m: 2.8
        };
        if (editingLocalId) {
             const updated = await ProjectService.updateLocal(editingLocalId, payload);
             updateLocalInProject(project.id, updated);
        } else {
             const created = await ProjectService.createLocal(payload);
             addLocalToProject(project.id, created);
        }
        setNewLocal({}); setEditingLocalId(null);
    } catch (e) { setErrorMsg("Erro ao salvar local"); }
  };

  const handleDeleteLocal = async (lId: string) => {
      if (confirm("Excluir local e todas as suas cargas?")) {
          await ProjectService.deleteLocal(lId);
          removeLocalFromProject(project.id, lId);
      }
  };

  const handleAutoCargas = async (local: Local) => {
      const isWet = project.zonas?.find(z => z.id === local.zona_id)?.presenca_agua !== 'AD1';
      const result = await ProjectService.calcularMinimoNBR(local.area_m2, local.perimetro_m, isWet || false);
      if (confirm(`Gerar Cargas Sugeridas NBR?\n\nIluminação: ${result.norma_iluminacao_va} VA\nTUGs: ${result.norma_tugs_quantidade} pontos`)) {
          const c1 = await ProjectService.createCarga({ projeto_id: project.id, local_id: local.id, nome: 'Iluminação Centro', tipo: 'ILUMINACAO', quantidade: 1, potencia: result.norma_iluminacao_va, unidade: 'VA', fator_potencia: 1.0 });
          addCargaToProject(project.id, c1);
          const c2 = await ProjectService.createCarga({ projeto_id: project.id, local_id: local.id, nome: 'TUGs Gerais', tipo: 'TUG', quantidade: result.norma_tugs_quantidade, potencia: 100, unidade: 'VA', fator_potencia: 0.8 });
          addCargaToProject(project.id, c2);
          alert("Cargas criadas na aba 'Cargas'.");
      }
  };

  // --- ACTIONS CARGA ---
  const handleOpenCargaDialog = (carga?: Carga) => {
      setEditingCarga(carga || null);
      setCargaDialogOpen(true);
  };

  const handleSaveCarga = async (dto: CargaCreateDTO) => {
      if (editingCarga) {
          const updated = await ProjectService.updateCarga(editingCarga.id, dto);
          updateCargaInProject(project.id, updated);
      } else {
          const created = await ProjectService.createCarga(dto);
          addCargaToProject(project.id, created);
      }
  };
  
  const handleBatchSave = async (cargas: CargaCreateDTO[]) => {
      // Simples loop. Em produção idealmente seria um endpoint /batch
      for (const c of cargas) {
          const created = await ProjectService.createCarga(c);
          addCargaToProject(project.id, created);
      }
  };

  const handleDeleteCarga = async (cId: string) => {
      if (confirm("Excluir carga?")) {
          await ProjectService.deleteCarga(cId);
          removeCargaFromProject(project.id, cId);
      }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} sx={{ mb: 2 }}>Dashboard</Button>
      <Typography variant="h4" gutterBottom>{project.nome}</Typography>
      
      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tab label="1. Ambientes (Zonas)" />
        <Tab label="2. Arquitetura (Cômodos)" />
        <Tab label="3. Cargas & Equipamentos" />
      </Tabs>

      {/* ABA 1: ZONAS */}
      <CustomTabPanel value={tabValue} index={0}>
        {viewState === 'list' && (
            <Box>
                {project.zonas?.map(z => (
                     <Card key={z.id} variant="outlined" sx={{ mb: 2, borderLeft: `6px solid ${z.cor_identificacao}` }}>
                        <CardContent sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Box>
                                <Typography variant="h6">{z.nome} <Chip size="small" label={z.origem} /></Typography>
                                <Typography variant="body2" color="text.secondary">{z.descricao}</Typography>
                                {/* Exibe influencias compactas */}
                                <Box mt={1} display="flex" gap={1} flexWrap="wrap">
                                    <Chip label={z.temp_ambiente} size="small" variant="outlined" />
                                    <Chip label={z.presenca_agua} size="small" variant="outlined" />
                                    <Chip label={z.competencia_pessoas} size="small" variant="outlined" />
                                </Box>
                            </Box>
                            <Box>
                                <IconButton color="primary" onClick={() => handleEditZona(z)}><EditIcon /></IconButton>
                                <IconButton color="error" onClick={() => handleDeleteZona(z.id)}><DeleteIcon /></IconButton>
                            </Box>
                        </CardContent>
                     </Card>
                ))}
                <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={() => { setEditingZonaId(null); setViewState('method_select'); }}>Nova Zona</Button>
            </Box>
        )}
        {viewState === 'method_select' && (
             <Grid container spacing={2} justifyContent="center" sx={{ mt: 2 }}>
                <Grid item xs={5}>
                    <Paper sx={{ p: 3, textAlign: 'center', cursor: 'pointer', bgcolor: '#f0f4ff' }} onClick={() => setViewState('preset_select')}>
                        <ScienceIcon fontSize="large" color="primary" /> <Typography variant="h6">Usar Preset</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={5}>
                    <Paper sx={{ p: 3, textAlign: 'center', cursor: 'pointer' }} onClick={() => { setNewZona({origem: 'custom'}); setViewState('form_custom'); }}>
                        <SettingsIcon fontSize="large" color="secondary" /> <Typography variant="h6">Personalizado</Typography>
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
                <Grid item xs={12}><Button onClick={() => setViewState('method_select')}>Voltar</Button></Grid>
            </Grid>
         )}
         
         {/* FORMULÁRIO DE ZONA (AGORA COMPLETO) */}
         {viewState === 'form_custom' && (
             <Card sx={{ maxWidth: 800, mx: 'auto', mt: 2 }}>
                 <CardContent>
                     <Typography variant="h6">{editingZonaId ? 'Editar Zona' : 'Nova Zona'}</Typography>
                     {errorMsg && <Alert severity="error">{errorMsg}</Alert>}
                     
                     <TextField fullWidth margin="normal" label="Nome" value={newZona.nome || ''} onChange={e => setNewZona({...newZona, nome: e.target.value})} />
                     <TextField fullWidth margin="dense" label="Descrição" value={newZona.descricao || ''} onChange={e => setNewZona({...newZona, descricao: e.target.value})} />

                     {(newZona.origem === 'custom' || editingZonaId) && (
                        <Grid container spacing={2} sx={{ mt: 2 }}>
                            <Grid item xs={6}>
                                <TextField select fullWidth label="Temperatura (AA)" value={newZona.temp_ambiente || ''} onChange={e => setNewZona({...newZona, temp_ambiente: e.target.value})}>
                                    {opcoes?.temperatura.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.codigo} - {op.descricao}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <TextField select fullWidth label="Água (AD)" value={newZona.presenca_agua || ''} onChange={e => setNewZona({...newZona, presenca_agua: e.target.value})}>
                                    {opcoes?.agua.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.codigo} - {op.descricao}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <TextField select fullWidth label="Sólidos (AE)" value={newZona.presenca_solidos || ''} onChange={e => setNewZona({...newZona, presenca_solidos: e.target.value})}>
                                    {opcoes?.solidos.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.codigo} - {op.descricao}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <TextField select fullWidth label="Pessoas (BA)" value={newZona.competencia_pessoas || ''} onChange={e => setNewZona({...newZona, competencia_pessoas: e.target.value})}>
                                    {opcoes?.pessoas.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.codigo} - {op.descricao}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <TextField select fullWidth label="Materiais (CA)" value={newZona.materiais_construcao || ''} onChange={e => setNewZona({...newZona, materiais_construcao: e.target.value})}>
                                    {opcoes?.materiais.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.codigo} - {op.descricao}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <TextField select fullWidth label="Estrutura (CB)" value={newZona.estrutura_edificacao || ''} onChange={e => setNewZona({...newZona, estrutura_edificacao: e.target.value})}>
                                    {opcoes?.estrutura.map(op => <MenuItem key={op.codigo} value={op.codigo}>{op.codigo} - {op.descricao}</MenuItem>)}
                                </TextField>
                            </Grid>
                        </Grid>
                     )}
                     
                     <Box mt={3} display="flex" justifyContent="flex-end" gap={2}>
                        <Button onClick={() => { setViewState('list'); setEditingZonaId(null); }}>Cancelar</Button>
                        <Button variant="contained" onClick={handleSaveZona}>Salvar</Button>
                     </Box>
                 </CardContent>
             </Card>
         )}
      </CustomTabPanel>

      {/* ABA 2: ARQUITETURA */}
      <CustomTabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
                <Card variant="outlined" sx={{ border: editingLocalId ? '2px solid #1976d2' : '1px solid #ddd' }}>
                    <CardContent>
                        <Typography variant="subtitle1" color={editingLocalId ? 'primary' : 'textPrimary'}>
                            {editingLocalId ? '✏️ Editando Cômodo' : 'Novo Cômodo'}
                        </Typography>
                        {errorMsg && <Alert severity="error">{errorMsg}</Alert>}
                        <TextField fullWidth size="small" margin="dense" label="Nome" value={newLocal.nome || ''} onChange={e => setNewLocal({...newLocal, nome: e.target.value})} />
                        <TextField select fullWidth size="small" margin="dense" label="Zona" value={newLocal.zona_id || ''} onChange={e => setNewLocal({...newLocal, zona_id: e.target.value})}>
                            {project.zonas?.map(z => <MenuItem key={z.id} value={z.id}>{z.nome}</MenuItem>)}
                        </TextField>
                        <Grid container spacing={1}>
                            <Grid item xs={6}><TextField fullWidth size="small" margin="dense" type="number" label="Area" value={newLocal.area_m2 || ''} onChange={e => setNewLocal({...newLocal, area_m2: Number(e.target.value)})} /></Grid>
                            <Grid item xs={6}><TextField fullWidth size="small" margin="dense" type="number" label="Perim" value={newLocal.perimetro_m || ''} onChange={e => setNewLocal({...newLocal, perimetro_m: Number(e.target.value)})} /></Grid>
                        </Grid>
                        <Box mt={2} display="flex" gap={1}>
                            {editingLocalId && <Button fullWidth variant="outlined" onClick={() => { setEditingLocalId(null); setNewLocal({}); }}>Cancelar</Button>}
                            <Button fullWidth variant="contained" onClick={handleSaveLocal}>{editingLocalId ? 'Atualizar' : 'Adicionar'}</Button>
                        </Box>
                    </CardContent>
                </Card>
            </Grid>
            <Grid item xs={12} md={8}>
                {project.locais?.map(local => (
                    <Card key={local.id} sx={{ mb: 2, bgcolor: editingLocalId === local.id ? '#e3f2fd' : 'white' }}>
                        <CardContent>
                            <Box display="flex" justifyContent="space-between" alignItems="center">
                                <Box>
                                    <Typography variant="h6">{local.nome}</Typography>
                                    <Typography variant="caption" color="text.secondary">Zona: {project.zonas?.find(z => z.id === local.zona_id)?.nome} | {local.area_m2}m²</Typography>
                                </Box>
                                <Box>
                                    <Tooltip title="Gerar Cargas"><IconButton color="primary" onClick={() => handleAutoCargas(local)}><AutoFixHighIcon /></IconButton></Tooltip>
                                    <IconButton color="default" onClick={() => handleEditLocal(local)}><EditIcon /></IconButton>
                                    <IconButton color="error" onClick={() => handleDeleteLocal(local.id)}><DeleteIcon /></IconButton>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                ))}
            </Grid>
        </Grid>
      </CustomTabPanel>

      {/* ABA 3: CARGAS */}
      <CustomTabPanel value={tabValue} index={2}>
         <Box display="flex" justifyContent="flex-end" mb={2} gap={2}>
             <Button variant="outlined" startIcon={<PlaylistAddIcon />} onClick={() => setBatchDialogOpen(true)}>Adicionar em Lote</Button>
             <Button variant="contained" startIcon={<AddCircleOutlineIcon />} onClick={() => handleOpenCargaDialog()}>Nova Carga</Button>
         </Box>
         
         <TableContainer component={Paper} variant="outlined">
             <Table>
                 <TableHead>
                     <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                         <TableCell>Local</TableCell>
                         <TableCell>Descrição</TableCell>
                         <TableCell>Tipo</TableCell>
                         <TableCell>Qtd</TableCell>
                         <TableCell>Potência (Unit)</TableCell>
                         <TableCell>Potência Total (W)</TableCell>
                         <TableCell align="right">Ações</TableCell>
                     </TableRow>
                 </TableHead>
                 <TableBody>
                     {project.cargas?.map(c => (
                         <TableRow key={c.id}>
                             <TableCell>{project.locais?.find(l => l.id === c.local_id)?.nome || '?'}</TableCell>
                             <TableCell>{c.nome}</TableCell>
                             <TableCell><Chip label={c.tipo} size="small" /></TableCell>
                             <TableCell>{c.quantidade}</TableCell>
                             <TableCell>{c.potencia_w} W / {c.potencia_va} VA</TableCell>
                             <TableCell sx={{ fontWeight: 'bold' }}>{(c.quantidade * c.potencia_w).toFixed(0)} W</TableCell>
                             <TableCell align="right">
                                 <IconButton size="small" onClick={() => handleOpenCargaDialog(c)}><EditIcon /></IconButton>
                                 <IconButton size="small" color="error" onClick={() => handleDeleteCarga(c.id)}><DeleteIcon /></IconButton>
                             </TableCell>
                         </TableRow>
                     ))}
                 </TableBody>
             </Table>
         </TableContainer>

         <CargaDialog 
            open={cargaDialogOpen} 
            onClose={() => setCargaDialogOpen(false)} 
            initialData={editingCarga}
            locais={project.locais} 
            projetoId={project.id} 
            onSave={handleSaveCarga}
         />

         <BatchCargasDialog
             open={batchDialogOpen}
             onClose={() => setBatchDialogOpen(false)}
             locais={project.locais}
             projetoId={project.id}
             onSave={handleBatchSave}
         />
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