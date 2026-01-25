import React from 'react';
import { 
  Container, Typography, Button, Card, 
  CardContent, CardActions, Box, Grid
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { useProjectStore } from '../store/useProjectStore';
import type { Projeto } from '../types/project';

const Dashboard: React.FC = () => {
  const { projects, addProject, deleteProject } = useProjectStore();

  const handleCreateProject = () => {
    const newProject: Projeto = {
      id: crypto.randomUUID(),
      nome: `Projeto NBR 5410 - ${projects.length + 1}`,
      tipo_instalacao: 'Residencial',
      data_criacao: new Date().toISOString(),
      ultima_modificacao: new Date().toISOString(),
    };
    
    addProject(newProject);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1" fontWeight="bold">
          Dimensionamento NBR 5410
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />} 
          onClick={handleCreateProject}
        >
          Novo Projeto
        </Button>
      </Box>

      <Grid container spacing={3}>
        {projects.map((project) => (
          <Grid key={project.id} size={{ xs: 12, sm: 6, md: 4 }}>
            <Card elevation={3}>
              <CardContent>
                <Typography variant="h6" noWrap>{project.nome}</Typography>
                <Typography color="textSecondary">{project.tipo_instalacao}</Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Criado em: {new Date(project.data_criacao).toLocaleDateString()}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small">Editar</Button>
                <Button 
                  size="small" 
                  color="error" 
                  onClick={() => deleteProject(project.id)}
                >
                  Excluir
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Dashboard;