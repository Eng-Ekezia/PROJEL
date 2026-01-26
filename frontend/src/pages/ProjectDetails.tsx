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