import React, { useState } from 'react';
import { 
  Container, Typography, Button, Card, 
  CardContent, CardActions, Box, Grid, 
  Chip, IconButton
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import BoltIcon from '@mui/icons-material/Bolt';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

// Importação da Navegação
import { useNavigate } from 'react-router-dom';

import { useProjectStore } from '../store/useProjectStore';
import { ProjectDialog } from '../components/ProjectDialog';
import type { Projeto } from '../types/project';

type ProjectFormData = Omit<Projeto, 'id' | 'data_criacao' | 'ultima_modificacao' | 'zonas' | 'locais'>;

const Dashboard: React.FC = () => {
  const { projects, addProject, updateProject, deleteProject } = useProjectStore();
  const navigate = useNavigate(); // Hook para navegar entre páginas
  
  const [openDialog, setOpenDialog] = useState(false);
  const [editingProject, setEditingProject] = useState<Projeto | undefined>(undefined);

  const handleOpenNew = () => {
    setEditingProject(undefined);
    setOpenDialog(true);
  };

  const handleOpenEdit = (project: Projeto, e: React.MouseEvent) => {
    e.stopPropagation(); // Impede que o clique abra o projeto
    setEditingProject(project);
    setOpenDialog(true);
  };

  const handleDelete = (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Impede que o clique abra o projeto
    if (confirm('Tem certeza que deseja excluir este projeto?')) {
      deleteProject(id);
    }
  };

  const handleSave = (data: ProjectFormData) => {
    if (editingProject) {
      updateProject(editingProject.id, data);
    } else {
      const newProject: Projeto = {
        id: crypto.randomUUID(),
        data_criacao: new Date().toISOString(),
        ultima_modificacao: new Date().toISOString(),
        zonas: [], // Inicializa listas vazias
        locais: [],
        ...data
      };
      addProject(newProject);
    }
  };

  // Função para abrir os detalhes
  const handleOpenProject = (id: string) => {
    navigate(`/project/${id}`);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Cabeçalho */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
            <Typography variant="h4" component="h1" fontWeight="bold" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <BoltIcon fontSize="large" color="primary" />
            Meus Projetos
            </Typography>
            <Typography variant="body2" color="text.secondary">
                Gerencie seus dimensionamentos elétricos
            </Typography>
        </Box>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />} 
          onClick={handleOpenNew}
          size="large"
        >
          Novo Projeto
        </Button>
      </Box>

      {projects.length === 0 ? (
        <Box textAlign="center" mt={8} py={8} bgcolor="#f5f5f5" borderRadius={2} border="1px dashed #ccc">
          <BoltIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2, opacity: 0.5 }} />
          <Typography variant="h6" color="text.secondary">Nenhum projeto encontrado.</Typography>
          <Typography color="text.secondary" mb={2}>Clique em "Novo Projeto" para começar seu dimensionamento.</Typography>
          <Button variant="outlined" startIcon={<AddIcon />} onClick={handleOpenNew}>
            Criar Agora
          </Button>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item key={project.id} xs={12} sm={6} md={4}>
              <Card 
                elevation={2} 
                sx={{ 
                    height: '100%', 
                    display: 'flex', 
                    flexDirection: 'column',
                    cursor: 'pointer',
                    transition: '0.2s',
                    '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: 4,
                        borderColor: 'primary.main'
                    },
                    border: '1px solid transparent'
                }}
                onClick={() => handleOpenProject(project.id)}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" gutterBottom noWrap title={project.nome} color="primary.main" fontWeight="bold">
                    {project.nome}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mb: 2 }}>
                    <Chip label={project.tipo_instalacao} size="small" variant="outlined" />
                    <Chip label={project.tensao_sistema} size="small" variant="outlined" />
                  </Box>

                  <Typography variant="caption" display="block" color="text.secondary">
                    Atualizado em: {new Date(project.ultima_modificacao).toLocaleDateString()}
                  </Typography>
                </CardContent>
                
                <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
                  <Box>
                    <IconButton size="small" onClick={(e) => handleOpenEdit(project, e)} title="Editar Configurações">
                        <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={(e) => handleDelete(project.id, e)} title="Excluir">
                        <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Box>
                  <Button size="small" endIcon={<ArrowForwardIcon />}>
                    Abrir
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <ProjectDialog 
        open={openDialog} 
        onClose={() => setOpenDialog(false)} 
        onSave={handleSave}
        initialData={editingProject}
      />
    </Container>
  );
};

export default Dashboard;