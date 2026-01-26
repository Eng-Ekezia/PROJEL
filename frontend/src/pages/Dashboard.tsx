import React, { useState } from 'react';
import { 
  Container, Typography, Button, Card, 
  CardContent, CardActions, Box, Grid2 as Grid,
  Chip
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import BoltIcon from '@mui/icons-material/Bolt';

import { useProjectStore } from '../store/useProjectStore';
import { ProjectDialog } from '../components/ProjectDialog';
import { Projeto } from '../types/project';

const Dashboard: React.FC = () => {
  const { projects, addProject, updateProject, deleteProject } = useProjectStore();
  
  // Estado para controlar o Modal
  const [openDialog, setOpenDialog] = useState(false);
  const [editingProject, setEditingProject] = useState<Projeto | undefined>(undefined);

  const handleOpenNew = () => {
    setEditingProject(undefined);
    setOpenDialog(true);
  };

  const handleOpenEdit = (project: Projeto) => {
    setEditingProject(project);
    setOpenDialog(true);
  };

  const handleDelete = (id: string) => {
    if (confirm('Tem certeza que deseja excluir este projeto?')) {
      deleteProject(id);
    }
  };

  // Callback ao salvar o formulário
  const handleSave = (data: any) => {
    if (editingProject) {
      // Modo Edição
      updateProject(editingProject.id, data);
    } else {
      // Modo Criação
      const newProject: Projeto = {
        id: crypto.randomUUID(), // Gera ID único no navegador
        data_criacao: new Date().toISOString(),
        ultima_modificacao: new Date().toISOString(),
        ...data
      };
      addProject(newProject);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1" fontWeight="bold" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <BoltIcon fontSize="large" color="primary" />
          Meus Projetos
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />} 
          onClick={handleOpenNew}
        >
          Novo Projeto
        </Button>
      </Box>

      {projects.length === 0 ? (
        <Box textAlign="center" mt={8} color="text.secondary">
          <Typography variant="h6">Nenhum projeto encontrado.</Typography>
          <Typography>Clique em "Novo Projeto" para começar seu dimensionamento.</Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid key={project.id} size={{ xs: 12, sm: 6, md: 4 }}>
              <Card elevation={2} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" gutterBottom noWrap title={project.nome}>
                    {project.nome}
                  </Typography>
                  
                  {/* Chips Técnicos (Resumo do Projeto) */}
                  <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mb: 2 }}>
                    <Chip label={project.tipo_instalacao} size="small" color="primary" variant="outlined" />
                    <Chip label={project.esquema_aterramento} size="small" color="secondary" variant="outlined" />
                    <Chip label={project.tensao_sistema} size="small" variant="outlined" />
                  </Box>

                  <Typography variant="caption" display="block" color="text.secondary">
                    Modificado em: {new Date(project.ultima_modificacao).toLocaleDateString()}
                  </Typography>
                </CardContent>
                
                <CardActions sx={{ justifyContent: 'flex-end' }}>
                  <Button 
                    size="small" 
                    startIcon={<EditIcon />} 
                    onClick={() => handleOpenEdit(project)}
                  >
                    Editar
                  </Button>
                  <Button 
                    size="small" 
                    color="error" 
                    startIcon={<DeleteIcon />}
                    onClick={() => handleDelete(project.id)}
                  >
                    Excluir
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Modal de Criação/Edição */}
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