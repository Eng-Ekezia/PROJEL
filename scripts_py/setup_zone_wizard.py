import os

# ==============================================================================
# 1. BASE DE CONHECIMENTO (PERGUNTAS HUMANAS -> CÓDIGOS TÉCNICOS)
# ==============================================================================
# Este arquivo contém a "inteligência" que traduz a realidade para a norma.

wizard_data_content = r'''
export interface WizardOption {
    label: string;
    description: string;
    code: string; // O código NBR que será salvo (ex: AD4)
    icon?: string;
}

export interface WizardQuestion {
    id: string; // Mapeia para o campo do objeto Zona (ex: 'presenca_agua')
    category: 'ambiente' | 'pessoas' | 'estrutura';
    question: string;
    helperText: string;
    options: WizardOption[];
}

export const ZONE_WIZARD_DATA: WizardQuestion[] = [
    // --- AMBIENTE FÍSICO ---
    {
        id: 'temp_ambiente',
        category: 'ambiente',
        question: 'Como é a temperatura média do local?',
        helperText: 'A temperatura afeta a capacidade de condução de corrente dos cabos.',
        options: [
            { code: 'AA4', label: 'Temperada / Normal', description: 'Ambiente interno comum ou externo sombreado (-5°C a +40°C).' },
            { code: 'AA5', label: 'Local Quente', description: 'Casas de máquinas, forros sem ventilação (+5°C a +40°C).' },
            { code: 'AA6', label: 'Muito Quente', description: 'Proximidade de fornos, indústrias (+5°C a +60°C).' },
            { code: 'AA2', label: 'Frio / Câmaras', description: 'Câmaras frigoríficas ou locais muito frios.' }
        ]
    },
    {
        id: 'presenca_agua',
        category: 'ambiente',
        question: 'Qual a presença de água no local?',
        helperText: 'Define a proteção IP necessária para os equipamentos (tomadas, luminárias).',
        options: [
            { code: 'AD1', label: 'Local Seco', description: 'Salas, quartos, escritórios. Risco desprezível.' },
            { code: 'AD2', label: 'Úmido / Gotejamento', description: 'Pode haver condensação ou respingos eventuais (ex: Lavabos).' },
            { code: 'AD3', label: 'Molhado / Aspersão', description: 'Chuva ou respingos frequentes (ex: Banheiros com chuveiro).' },
            { code: 'AD4', label: 'Lavagem com Mangueira', description: 'Garagens, quintais, cozinhas industriais.' },
            { code: 'AD7', label: 'Imersão / Piscinas', description: 'Interior de piscinas ou espelhos d\'água.' }
        ]
    },
    {
        id: 'presenca_solidos',
        category: 'ambiente',
        question: 'O local possui poeira ou resíduos sólidos?',
        helperText: 'Importante para escolha de eletrodutos e vedação de quadros.',
        options: [
            { code: 'AE1', label: 'Limpo / Doméstico', description: 'Poeira normal de ambiente residencial.' },
            { code: 'AE4', label: 'Poeira Leve', description: 'Poeira ou sedimentação de pó.' },
            { code: 'AE6', label: 'Poeira Intensa', description: 'Ambientes industriais, cimento, moinhos.' }
        ]
    },

    // --- PESSOAS E USO ---
    {
        id: 'competencia_pessoas',
        category: 'pessoas',
        question: 'Quem frequenta este local?',
        helperText: 'Determina a proteção contra choques e acessibilidade.',
        options: [
            { code: 'BA1', label: 'Pessoas Comuns', description: 'Uso geral (residencial, comercial). Pessoas não advertidas.' },
            { code: 'BA2', label: 'Crianças', description: 'Creches, escolas infantis, áreas de recreação.' },
            { code: 'BA3', label: 'Pessoas com Deficiência', description: 'Hospitais, asilos, clínicas geriátricas.' },
            { code: 'BA4', label: 'Equipe Advertida', description: 'Áreas de serviço exclusivas para manutenção.' },
            { code: 'BA5', label: 'Profissionais (Eletricistas)', description: 'Subestações, salas elétricas trancadas.' }
        ]
    },

    // --- CONSTRUÇÃO ---
    {
        id: 'materiais_construcao',
        category: 'estrutura',
        question: 'Qual o material predominante da construção?',
        helperText: 'Afeta o risco de incêndio e propagação de chama.',
        options: [
            { code: 'CA1', label: 'Não Combustível', description: 'Alvenaria, concreto, gesso (Maioria dos casos).' },
            { code: 'CA2', label: 'Combustível', description: 'Madeira, dry-wall com isolamento inflamável.' }
        ]
    },
    {
        id: 'estrutura_edificacao',
        category: 'estrutura',
        question: 'Como é a estrutura física?',
        helperText: 'Define flexibilidade da instalação.',
        options: [
            { code: 'CB1', label: 'Estável / Fixa', description: 'Paredes rígidas, risco desprezível de movimento.' },
            { code: 'CB3', label: 'Móvel / Instável', description: 'Estruturas sujeitas a movimentação ou vibração.' }
        ]
    }
];
'''

# ==============================================================================
# 2. COMPONENTE WIZARD (UI DIALOG)
# ==============================================================================
wizard_component_content = r'''
import React, { useState } from 'react';
import { 
    Dialog, DialogTitle, DialogContent, DialogActions, 
    Button, Stepper, Step, StepLabel, Typography, 
    Box, Radio, RadioGroup, FormControlLabel, FormControl, 
    FormLabel, Paper, Grid, Divider
} from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

import { ZONE_WIZARD_DATA, WizardQuestion } from '../data/nbr5410_wizard';
import type { Zona } from '../../types/project';

interface ZoneWizardDialogProps {
    open: boolean;
    onClose: () => void;
    onSave: (zonaData: Partial<Zona>) => void;
}

const STEPS = ['Ambiente Físico', 'Uso e Pessoas', 'Estrutura e Materiais', 'Revisão'];

export const ZoneWizardDialog: React.FC<ZoneWizardDialogProps> = ({ open, onClose, onSave }) => {
    const [activeStep, setActiveStep] = useState(0);
    const [answers, setAnswers] = useState<Partial<Zona>>({
        nome: '',
        // Defaults seguros
        temp_ambiente: 'AA4',
        presenca_agua: 'AD1',
        presenca_solidos: 'AE1',
        competencia_pessoas: 'BA1',
        materiais_construcao: 'CA2',
        estrutura_edificacao: 'CB1'
    });

    // Filtra perguntas da etapa atual
    const getQuestionsForStep = (stepIndex: number): WizardQuestion[] => {
        switch(stepIndex) {
            case 0: return ZONE_WIZARD_DATA.filter(q => q.category === 'ambiente');
            case 1: return ZONE_WIZARD_DATA.filter(q => q.category === 'pessoas');
            case 2: return ZONE_WIZARD_DATA.filter(q => q.category === 'estrutura');
            default: return [];
        }
    };

    const handleChange = (fieldId: string, value: string) => {
        setAnswers(prev => ({ ...prev, [fieldId]: value }));
    };

    const handleNext = () => {
        if (activeStep === STEPS.length - 1) {
            onSave(answers);
            handleClose();
        } else {
            setActiveStep(prev => prev + 1);
        }
    };

    const handleBack = () => setActiveStep(prev => prev - 1);
    
    const handleClose = () => {
        setActiveStep(0);
        setAnswers({ nome: '' }); // Reset parcial
        onClose();
    };

    return (
        <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
            <DialogTitle sx={{ bgcolor: 'primary.main', color: 'white' }}>
                Assistente de Criação de Zona
            </DialogTitle>
            
            <DialogContent sx={{ mt: 2 }}>
                <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
                    {STEPS.map((label) => <Step key={label}><StepLabel>{label}</StepLabel></Step>)}
                </Stepper>

                <Box sx={{ minHeight: '300px' }}>
                    {activeStep < 3 ? (
                        // --- ETAPAS DE PERGUNTAS ---
                        <Box>
                             {/* Nome da Zona (Aparece apenas no passo 0) */}
                            {activeStep === 0 && (
                                <Box mb={4}>
                                    <Typography variant="h6" gutterBottom>1. Identificação</Typography>
                                    <Typography variant="body2" color="text.secondary" paragraph>
                                        Dê um nome descritivo para este grupo de ambientes (ex: "Área de Serviço", "Quartos", "Área Externa").
                                    </Typography>
                                    <input 
                                        type="text" 
                                        placeholder="Nome da Zona (ex: Área Molhada)" 
                                        style={{ width: '100%', padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc' }}
                                        value={answers.nome || ''}
                                        onChange={(e) => handleChange('nome', e.target.value)}
                                        autoFocus
                                    />
                                </Box>
                            )}

                            {getQuestionsForStep(activeStep).map((q) => (
                                <Box key={q.id} sx={{ mb: 4, p: 2, bgcolor: '#f9f9f9', borderRadius: 2 }}>
                                    <FormLabel component="legend" sx={{ color: 'text.primary', fontWeight: 'bold', mb: 1 }}>
                                        {q.question}
                                    </FormLabel>
                                    <Typography variant="caption" color="text.secondary" display="block" mb={2}>
                                        {q.helperText}
                                    </Typography>
                                    
                                    <RadioGroup
                                        value={answers[q.id as keyof Zona] || ''}
                                        onChange={(e) => handleChange(q.id, e.target.value)}
                                    >
                                        <Grid container spacing={2}>
                                            {q.options.map((opt) => (
                                                <Grid item xs={12} sm={6} key={opt.code}>
                                                    <Paper variant="outlined" 
                                                        sx={{ 
                                                            p: 1, 
                                                            borderColor: answers[q.id as keyof Zona] === opt.code ? 'primary.main' : 'divider',
                                                            bgcolor: answers[q.id as keyof Zona] === opt.code ? 'action.selected' : 'background.paper',
                                                            cursor: 'pointer'
                                                        }}
                                                        onClick={() => handleChange(q.id, opt.code)}
                                                    >
                                                        <FormControlLabel 
                                                            value={opt.code} 
                                                            control={<Radio size="small" />} 
                                                            label={
                                                                <Box>
                                                                    <Typography variant="subtitle2" fontWeight="bold">{opt.label}</Typography>
                                                                    <Typography variant="caption" color="text.secondary">{opt.description}</Typography>
                                                                </Box>
                                                            } 
                                                            sx={{ margin: 0, width: '100%', alignItems: 'flex-start' }}
                                                        />
                                                    </Paper>
                                                </Grid>
                                            ))}
                                        </Grid>
                                    </RadioGroup>
                                </Box>
                            ))}
                        </Box>
                    ) : (
                        // --- ETAPA DE REVISÃO (RESUMO TÉCNICO) ---
                        <Box textAlign="center" py={2}>
                            <CheckCircleIcon color="success" sx={{ fontSize: 60, mb: 2 }} />
                            <Typography variant="h5" gutterBottom>Zona Definida!</Typography>
                            <Typography color="text.secondary" paragraph>
                                O sistema traduziu suas respostas para os seguintes parâmetros normativos:
                            </Typography>
                            
                            <Paper variant="outlined" sx={{ maxWidth: 600, mx: 'auto', textAlign: 'left' }}>
                                <Box p={2} display="flex" justifyContent="space-between" bgcolor="#f5f5f5">
                                    <Typography fontWeight="bold">Nome da Zona:</Typography>
                                    <Typography>{answers.nome}</Typography>
                                </Box>
                                <Divider />
                                <Grid container p={2} spacing={2}>
                                    {ZONE_WIZARD_DATA.map(q => {
                                        const selected = q.options.find(o => o.code === answers[q.id as keyof Zona]);
                                        return (
                                            <Grid item xs={6} key={q.id}>
                                                <Typography variant="caption" color="text.secondary">{q.category.toUpperCase()}</Typography>
                                                <Typography variant="subtitle2">{selected?.label}</Typography>
                                                <Typography variant="caption" sx={{ bgcolor: '#eee', px: 0.5, borderRadius: 0.5 }}>
                                                    Código: {selected?.code}
                                                </Typography>
                                            </Grid>
                                        );
                                    })}
                                </Grid>
                            </Paper>
                        </Box>
                    )}
                </Box>
            </DialogContent>
            
            <DialogActions sx={{ p: 3 }}>
                {activeStep > 0 && (
                    <Button onClick={handleBack} startIcon={<NavigateBeforeIcon />}>
                        Voltar
                    </Button>
                )}
                <Box sx={{ flexGrow: 1 }} />
                <Button 
                    variant="contained" 
                    onClick={handleNext}
                    endIcon={activeStep === STEPS.length - 1 ? <CheckCircleIcon /> : <NavigateNextIcon />}
                    disabled={activeStep === 0 && !answers.nome}
                >
                    {activeStep === STEPS.length - 1 ? 'Confirmar e Criar' : 'Próximo'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};
'''

# ==============================================================================
# 3. ATUALIZAR PROJECT DETAILS (INTEGRAR O WIZARD)
# ==============================================================================
# Removemos o formulário antigo e colocamos o botão "Assistente"

project_details_updated = r'''
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Box, Tabs, Tab, Button, 
  Grid, Card, CardContent, TextField, MenuItem, Alert, Divider, 
  Chip, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, Stack
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DeleteIcon from '@mui/icons-material/Delete';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';

import { useProjectStore } from '../store/useProjectStore';
import { ProjectService } from '../api/client';
import type { OpcoesInfluencias } from '../api/client';
import type { Zona, Local, Carga } from '../types/project';
import { ZoneWizardDialog } from '../components/wizards/ZoneWizardDialog'; // Importando Wizard

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
  const { projects, addZonaToProject, addLocalToProject, addCargaToProject, removeCargaFromProject } = useProjectStore();
  
  const project = projects.find(p => p.id === id);
  const [tabValue, setTabValue] = useState(0);
  const [opcoes, setOpcoes] = useState<OpcoesInfluencias | null>(null);
  
  // Forms States
  const [wizardOpen, setWizardOpen] = useState(false); // Estado do Modal Wizard
  const [newLocal, setNewLocal] = useState<Partial<Local>>({});
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // States Tab Cargas
  const [selectedLocalId, setSelectedLocalId] = useState<string>('');
  const [normaData, setNormaData] = useState<any>(null);
  const [newCarga, setNewCarga] = useState<Partial<Carga>>({ quantidade: 1, fator_potencia: 1.0, tipo: 'TUG' });

  useEffect(() => {
    if (!project) return;
    ProjectService.getOpcoesInfluencias().then(setOpcoes).catch(err => console.error("Erro API:", err));
  }, [project]);

  useEffect(() => {
    if (selectedLocalId && project) {
        const local = project.locais?.find(l => l.id === selectedLocalId);
        const zona = project.zonas?.find(z => z.id === local?.zona_id);
        
        if (local && zona) {
            const ehUmida = ["AD2","AD3","AD4","AD5","AD6","AD7","AD8"].includes(zona.presenca_agua) || 
                            /cozinha|serviço|lavanderia|copa/i.test(local.nome);
            ProjectService.calcularNorma(local.area_m2, local.perimetro_m, ehUmida)
                .then(setNormaData)
                .catch(console.error);
        }
    } else {
        setNormaData(null);
    }
  }, [selectedLocalId, project]);

  if (!project) return <Container sx={{mt:4}}><Typography>Projeto não encontrado.</Typography></Container>;

  // --- HANDLER ZONA (VIA WIZARD) ---
  const handleSaveZonaWizard = async (zonaData: Partial<Zona>) => {
      try {
        const zonaCriada = await ProjectService.createZona({
            projeto_id: project.id,
            nome: zonaData.nome!,
            temp_ambiente: zonaData.temp_ambiente || 'AA4',
            presenca_agua: zonaData.presenca_agua || 'AD1',
            presenca_solidos: zonaData.presenca_solidos || 'AE1',
            competencia_pessoas: zonaData.competencia_pessoas || 'BA1',
            materiais_construcao: zonaData.materiais_construcao || 'CA2',
            estrutura_edificacao: zonaData.estrutura_edificacao || 'CB1',
            cor_identificacao: '#ddd'
        } as any);
        addZonaToProject(project.id, zonaCriada);
      } catch (error) {
          console.error(error);
          alert("Erro ao criar zona via assistente.");
      }
  };

  const handleAddLocal = async () => {
    try {
      if (!newLocal.nome || !newLocal.zona_id) { setErrorMsg("Preencha o nome e selecione uma zona."); return; }
      const localCriado = await ProjectService.createLocal({
        projeto_id: project.id,
        zona_id: newLocal.zona_id,
        nome: newLocal.nome,
        area_m2: Number(newLocal.area_m2),
        perimetro_m: Number(newLocal.perimetro_m),
        pe_direito_m: 2.8
      } as any);
      addLocalToProject(project.id, localCriado);
      setNewLocal({}); setErrorMsg(null);
    } catch (error: any) { setErrorMsg(error.response?.data?.detail || "Erro ao criar local."); }
  };

  const handleAddCarga = async () => {
      if (!selectedLocalId || !newCarga.nome || !newCarga.potencia_va) return;
      try {
          const cargaCriada = await ProjectService.createCarga({
              local_id: selectedLocalId,
              nome: newCarga.nome,
              tipo: newCarga.tipo || 'TUG',
              potencia_va: Number(newCarga.potencia_va),
              potencia_w: Number(newCarga.potencia_va) * (newCarga.fator_potencia || 1.0),
              fator_potencia: Number(newCarga.fator_potencia || 1.0),
              quantidade: Number(newCarga.quantidade || 1)
          });
          addCargaToProject(project.id, cargaCriada);
          setNewCarga({ quantidade: 1, fator_potencia: 1.0, tipo: 'TUG' });
      } catch (err) { console.error(err); }
  };

  const handleAplicarNorma = async () => {
      if (!normaData || !selectedLocalId) return;
      if (normaData.norma_iluminacao_va > 0) {
          const ilum = await ProjectService.createCarga({
              local_id: selectedLocalId,
              nome: "Iluminação Geral (Norma)",
              tipo: 'ILUMINACAO',
              potencia_va: normaData.norma_iluminacao_va,
              potencia_w: normaData.norma_iluminacao_va * 1.0,
              fator_potencia: 1.0,
              quantidade: 1
          });
          addCargaToProject(project.id, ilum);
      }
      if (normaData.norma_tugs_quantidade > 0) {
          const tug = await ProjectService.createCarga({
              local_id: selectedLocalId,
              nome: "TUGs (Norma)",
              tipo: 'TUG',
              potencia_va: 100,
              potencia_w: 100 * 0.8,
              fator_potencia: 0.8,
              quantidade: normaData.norma_tugs_quantidade
          });
          addCargaToProject(project.id, tug);
      }
  };

  // Render Helpers
  const cargasDoLocal = project.cargas?.filter(c => c.local_id === selectedLocalId) || [];
  const totalIlumVA = cargasDoLocal.filter(c => c.tipo === 'ILUMINACAO').reduce((acc, c) => acc + (c.potencia_va * c.quantidade), 0);
  const totalTugsQtd = cargasDoLocal.filter(c => c.tipo === 'TUG').reduce((acc, c) => acc + c.quantidade, 0);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} sx={{ mb: 2 }}>Voltar</Button>
      <Typography variant="h4" gutterBottom>{project.nome} <Typography component="span" color="text.secondary">({project.tipo_instalacao})</Typography></Typography>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="1. Ambientes (Zonas)" />
          <Tab label="2. Arquitetura" />
          <Tab label="3. Cargas & Equipamentos" />
        </Tabs>
      </Box>

      {/* ABA 1: ZONAS (REFATORADA - COM WIZARD) */}
      <CustomTabPanel value={tabValue} index={0}>
        <Box textAlign="center" py={4} bgcolor="#f0f7ff" borderRadius={2} border="1px dashed #2196f3" mb={4}>
            <Typography variant="h5" gutterBottom color="primary">Definição de Influências Externas</Typography>
            <Typography color="text.secondary" paragraph sx={{maxWidth: 600, mx: 'auto'}}>
                Crie zonas de influência para agrupar ambientes com características semelhantes (ex: Áreas Molhadas, Áreas Externas). 
                O sistema guiará você pelas definições da NBR 5410.
            </Typography>
            <Button 
                variant="contained" 
                size="large" 
                startIcon={<AddCircleOutlineIcon />}
                onClick={() => setWizardOpen(true)}
            >
                Criar Nova Zona com Assistente
            </Button>
        </Box>

        <Typography variant="h6" gutterBottom>Zonas Definidas no Projeto</Typography>
        <Grid container spacing={3}>
            {project.zonas?.map(z => (
               <Grid item xs={12} sm={6} md={4} key={z.id}>
                   <Card variant="outlined" sx={{ height: '100%', position: 'relative', overflow: 'visible' }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight="bold" gutterBottom>{z.nome}</Typography>
                            <Divider sx={{ my: 1 }} />
                            <Stack spacing={1}>
                                <Box display="flex" justifyContent="space-between">
                                    <Typography variant="body2" color="text.secondary">Ambiente:</Typography>
                                    <Chip label={`${z.temp_ambiente} / ${z.presenca_agua}`} size="small" color="primary" variant="outlined" />
                                </Box>
                                <Box display="flex" justifyContent="space-between">
                                    <Typography variant="body2" color="text.secondary">Uso:</Typography>
                                    <Chip label={z.competencia_pessoas} size="small" color="warning" variant="outlined" />
                                </Box>
                                <Box display="flex" justifyContent="space-between">
                                    <Typography variant="body2" color="text.secondary">Estrutura:</Typography>
                                    <Chip label={`${z.materiais_construcao} / ${z.estrutura_edificacao}`} size="small" variant="outlined" />
                                </Box>
                            </Stack>
                        </CardContent>
                   </Card>
               </Grid>
            ))}
            {(!project.zonas || project.zonas.length === 0) && (
                <Grid item xs={12}>
                    <Typography color="text.secondary" align="center">Nenhuma zona definida ainda.</Typography>
                </Grid>
            )}
        </Grid>
        
        {/* MODAL DO WIZARD */}
        <ZoneWizardDialog 
            open={wizardOpen} 
            onClose={() => setWizardOpen(false)} 
            onSave={handleSaveZonaWizard} 
        />
      </CustomTabPanel>

      {/* ABA 2: LOCAIS (MANTIDA) */}
      <CustomTabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
           <Grid item xs={12} md={4}>
            <Card variant="outlined"><CardContent>
                <Typography variant="h6">Novo Cômodo</Typography>
                {errorMsg && <Alert severity="error">{errorMsg}</Alert>}
                <TextField fullWidth label="Nome" margin="dense" value={newLocal.nome || ''} onChange={e => setNewLocal({...newLocal, nome: e.target.value})} />
                <TextField select fullWidth label="Zona de Influência" margin="dense" value={newLocal.zona_id || ''} onChange={e => setNewLocal({...newLocal, zona_id: e.target.value})}>
                   {project.zonas?.map(z => <MenuItem key={z.id} value={z.id}>{z.nome}</MenuItem>)}
                </TextField>
                <Grid container spacing={1}>
                  <Grid item xs={6}><TextField fullWidth label="Área (m²)" type="number" margin="dense" value={newLocal.area_m2 || ''} onChange={e => setNewLocal({...newLocal, area_m2: Number(e.target.value)})} /></Grid>
                  <Grid item xs={6}><TextField fullWidth label="Perímetro (m)" type="number" margin="dense" value={newLocal.perimetro_m || ''} onChange={e => setNewLocal({...newLocal, perimetro_m: Number(e.target.value)})} /></Grid>
                </Grid>
                <Button variant="contained" fullWidth sx={{ mt: 2 }} onClick={handleAddLocal}>Criar Cômodo</Button>
            </CardContent></Card>
          </Grid>
           <Grid item xs={12} md={8}>
            {project.locais?.map(l => (
               <Card key={l.id} sx={{ mb: 1, p: 1 }}>
                   <Box display="flex" justifyContent="space-between" alignItems="center">
                       <Box>
                           <Typography fontWeight="bold">{l.nome}</Typography>
                           <Typography variant="body2">{l.area_m2}m² • {l.perimetro_m}m</Typography>
                       </Box>
                       <Chip label={project.zonas?.find(z => z.id === l.zona_id)?.nome} size="small" />
                   </Box>
               </Card>
            ))}
          </Grid>
        </Grid>
      </CustomTabPanel>

      {/* ABA 3: CARGAS (MANTIDA) */}
      <CustomTabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
              <Grid item xs={12} md={3}>
                  <Typography variant="h6" gutterBottom>Selecione o Cômodo</Typography>
                  {project.locais && project.locais.length > 0 ? (
                      project.locais.map(l => (
                          <Button key={l.id} variant={selectedLocalId === l.id ? "contained" : "outlined"} fullWidth sx={{ mb: 1, justifyContent: "flex-start" }} onClick={() => setSelectedLocalId(l.id)}>
                              {l.nome}
                          </Button>
                      ))
                  ) : <Typography color="text.secondary">Cadastre cômodos primeiro.</Typography>}
              </Grid>
              <Grid item xs={12} md={9}>
                  {selectedLocalId ? (
                      <>
                        {normaData && (
                            <Paper sx={{ p: 2, mb: 3, bgcolor: '#e3f2fd', border: '1px solid #90caf9' }}>
                                <Box display="flex" justifyContent="space-between" alignItems="center">
                                    <Box>
                                        <Typography variant="subtitle1" fontWeight="bold" color="primary">Diagnóstico NBR 5410</Typography>
                                        <Box display="flex" gap={2} mt={1}>
                                            <Chip icon={totalIlumVA >= normaData.norma_iluminacao_va ? <CheckCircleIcon/> : <WarningIcon/>} label={`Ilum: Min ${normaData.norma_iluminacao_va} VA`} color={totalIlumVA >= normaData.norma_iluminacao_va ? "success" : "warning"} variant="outlined"/>
                                            <Chip icon={totalTugsQtd >= normaData.norma_tugs_quantidade ? <CheckCircleIcon/> : <WarningIcon/>} label={`TUGs: Min ${normaData.norma_tugs_quantidade} pts`} color={totalTugsQtd >= normaData.norma_tugs_quantidade ? "success" : "warning"} variant="outlined"/>
                                        </Box>
                                    </Box>
                                    <Button variant="contained" color="secondary" startIcon={<AutoFixHighIcon/>} onClick={handleAplicarNorma}>Preencher</Button>
                                </Box>
                            </Paper>
                        )}
                        <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
                            <Table size="small">
                                <TableHead sx={{ bgcolor: '#f5f5f5' }}><TableRow><TableCell>Descrição</TableCell><TableCell>Tipo</TableCell><TableCell align="right">Qtd</TableCell><TableCell align="right">VA</TableCell><TableCell align="center">Ações</TableCell></TableRow></TableHead>
                                <TableBody>
                                    {cargasDoLocal.map(c => (
                                        <TableRow key={c.id}>
                                            <TableCell>{c.nome}</TableCell><TableCell><Chip label={c.tipo} size="small" /></TableCell><TableCell align="right">{c.quantidade}</TableCell><TableCell align="right">{c.potencia_va}</TableCell>
                                            <TableCell align="center"><IconButton size="small" color="error" onClick={() => removeCargaFromProject(project.id, c.id)}><DeleteIcon fontSize="small"/></IconButton></TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                        <Paper sx={{ p: 2 }}>
                            <Typography variant="subtitle2" gutterBottom>Adicionar Carga</Typography>
                            <Grid container spacing={2} alignItems="center">
                                <Grid item xs={12} md={3}><TextField fullWidth size="small" label="Descrição" value={newCarga.nome || ''} onChange={e => setNewCarga({...newCarga, nome: e.target.value})} /></Grid>
                                <Grid item xs={6} md={2}><TextField select fullWidth size="small" label="Tipo" value={newCarga.tipo} onChange={e => setNewCarga({...newCarga, tipo: e.target.value as any})}><MenuItem value="ILUMINACAO">Iluminação</MenuItem><MenuItem value="TUG">TUG</MenuItem><MenuItem value="TUE">TUE</MenuItem></TextField></Grid>
                                <Grid item xs={6} md={2}><TextField fullWidth size="small" label="Qtd" type="number" value={newCarga.quantidade} onChange={e => setNewCarga({...newCarga, quantidade: Number(e.target.value)})} /></Grid>
                                <Grid item xs={6} md={2}><TextField fullWidth size="small" label="Potência (VA)" type="number" value={newCarga.potencia_va || ''} onChange={e => setNewCarga({...newCarga, potencia_va: Number(e.target.value)})} /></Grid>
                                <Grid item xs={12} md={3}><Button fullWidth variant="contained" onClick={handleAddCarga}>Adicionar</Button></Grid>
                            </Grid>
                        </Paper>
                      </>
                  ) : <Typography>Selecione um cômodo.</Typography>}
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
    
    # Criar diretórios
    os.makedirs(os.path.join(base_dir, "frontend/src/data"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "frontend/src/components/wizards"), exist_ok=True)
    
    # Escrever arquivos
    files = {
        "frontend/src/data/nbr5410_wizard.ts": wizard_data_content,
        "frontend/src/components/wizards/ZoneWizardDialog.tsx": wizard_component_content,
        "frontend/src/pages/ProjectDetails.tsx": project_details_updated
    }
    
    for path, content in files.items():
        full_path = os.path.join(base_dir, path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Criado/Atualizado: {path}")

    print("\n--- Wizard de Influências Implementado! ---")
    print("O frontend atualizará automaticamente. Teste a criação de Zona na aba 1.")

if __name__ == "__main__":
    main()