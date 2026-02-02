/*import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, Typography, Button, Grid, Card, CardContent, CardActions, 
  Dialog, DialogTitle, DialogContent, DialogActions, TextField, 
  IconButton, Box, MenuItem 
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';

import { useProjectStore } from '../store/useProjectStore';
// FIX: Import Type
import type { Projeto } from '../types/project';

// Componente simples de Dialog interno para evitar dependências quebradas
const ProjectDialog: React.FC<{
  open: boolean;
  onClose: () => void;
  onSave: (project: Partial<Projeto>) => void;
  initialData?: Projeto | null;
}> = ({ open, onClose, onSave, initialData }) => {
  const [formData, setFormData] = useState<Partial<Projeto>>(
    initialData || {
      nome: '',
      tipo_instalacao: 'Residencial',
      tensao_sistema: '220/127V',
      sistema: 'Trifásico',
      esquema_aterramento: 'TN-S'
    }
  );

  // Reset form when opening for new project
  React.useEffect(() => {
    if (open) {
        setFormData(initialData || {
            nome: '',
            tipo_instalacao: 'Residencial',
            tensao_sistema: '220/127V',
            sistema: 'Trifásico',
            esquema_aterramento: 'TN-S'
        });
    }
  }, [open, initialData]);

  const handleChange = (field: keyof Projeto, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{initialData ? 'Editar Projeto' : 'Novo Projeto'}</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField label="Nome do Projeto" value={formData.nome} onChange={e => handleChange('nome', e.target.value)} fullWidth />
            
            <TextField select label="Tipo de Instalação" value={formData.tipo_instalacao} onChange={e => handleChange('tipo_instalacao', e.target.value)} fullWidth>
                <MenuItem value="Residencial">Residencial</MenuItem>
                <MenuItem value="Comercial">Comercial</MenuItem>
                <MenuItem value="Industrial">Industrial</MenuItem>
            </TextField>

            <Grid container spacing={2}>
                <Grid item xs={6}>
                    <TextField label="Tensão" value={formData.tensao_sistema} onChange={e => handleChange('tensao_sistema', e.target.value)} fullWidth />
                </Grid>
                <Grid item xs={6}>
                    <TextField label="Sistema" value={formData.sistema} onChange={e => handleChange('sistema', e.target.value)} fullWidth />
                </Grid>
            </Grid>
            
            <TextField label="Aterramento" value={formData.esquema_aterramento} onChange={e => handleChange('esquema_aterramento', e.target.value)} fullWidth />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button variant="contained" onClick={() => onSave(formData)}>Salvar</Button>
      </DialogActions>
    </Dialog>
  );
};

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  // FIX: Destructuring createProject/updateProject correctly
  const { projects, createProject, updateProject, deleteProject } = useProjectStore();
  
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Projeto | null>(null);

  const handleOpenNew = () => {
    setEditingProject(null);
    setDialogOpen(true);
  };

  const handleOpenEdit = (project: Projeto) => {
    setEditingProject(project);
    setDialogOpen(true);
  };

  const handleSave = (data: Partial<Projeto>) => {
    if (editingProject) {
      // Update
      updateProject({ ...editingProject, ...data } as Projeto);
    } else {
      // Create
      const newProject: Projeto = {
        id: crypto.randomUUID(),
        nome: data.nome || 'Novo Projeto',
        tipo_instalacao: data.tipo_instalacao || 'Residencial',
        tensao_sistema: data.tensao_sistema || '220/127V',
        sistema: data.sistema || 'Trifásico',
        esquema_aterramento: data.esquema_aterramento || 'TN-S',
        data_criacao: new Date().toISOString(),
        ultima_modificacao: new Date().toISOString(),
        zonas: [],
        locais: [],
        cargas: []
      };
      createProject(newProject);
    }
    setDialogOpen(false);
  };

  const handleDelete = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Tem certeza que deseja excluir este projeto?')) {
      deleteProject(id);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Meus Projetos
        </Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleOpenNew}>
          Novo Projeto
        </Button>
      </Box>

      <Grid container spacing={3}>
        {projects.map((project) => (
          <Grid item xs={12} sm={6} md={4} key={project.id}>
            <Card 
              variant="outlined" 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                cursor: 'pointer',
                transition: '0.2s',
                '&:hover': { boxShadow: 4 } 
              }}
              onClick={() => navigate(`/project/${project.id}`)}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" gutterBottom>
                  {project.nome}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {project.tipo_instalacao} • {project.sistema}
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Atualizado em: {new Date(project.ultima_modificacao).toLocaleDateString()}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'flex-end' }}>
                <Button size="small" startIcon={<FolderOpenIcon />} onClick={() => navigate(`/project/${project.id}`)}>
                    Abrir
                </Button>
                <IconButton size="small" onClick={(e) => { e.stopPropagation(); handleOpenEdit(project); }}>
                  <EditIcon />
                </IconButton>
                <IconButton size="small" color="error" onClick={(e) => handleDelete(project.id, e)}>
                  <DeleteIcon />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
        
        {projects.length === 0 && (
            <Grid item xs={12}>
                <Box textAlign="center" py={5} sx={{ bgcolor: '#f5f5f5', borderRadius: 2 }}>
                    <Typography variant="h6" color="text.secondary">Nenhum projeto encontrado.</Typography>
                    <Typography variant="body2">Crie seu primeiro projeto elétrico para começar.</Typography>
                </Box>
            </Grid>
        )}
      </Grid>

      <ProjectDialog 
        open={dialogOpen} 
        onClose={() => setDialogOpen(false)} 
        onSave={handleSave} 
        initialData={editingProject} 
      />
    </Container>
  );
};

export default Dashboard;*/

import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { Plus, Folder, Zap } from "lucide-react"

// Componentes Shadcn UI
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table"

// Store e Serviços
import { useProjectStore } from "../store/useProjectStore"
import { ProjectService } from "../api/client"

export default function Dashboard() {
  const navigate = useNavigate()
  const { projects, setProjects, addProject } = useProjectStore()

  // Carrega projetos ao montar
  /*useEffect(() => {
    ProjectService.getAll().then(setProjects).catch(console.error)
  }, [setProjects])*/

  const handleCreateProject = () => {
    const nome = prompt("Nome do novo projeto:")
    if (!nome) return

    const newProject = {
      id: crypto.randomUUID(), // Gera ID local único
      nome,
      tipo_instalacao: "RESIDENCIAL",
      tensao_sistema: "220/127V",
      sistema: "MONOFASICO",
      data_criacao: new Date().toISOString(),
      ultima_modificacao: new Date().toISOString(),
      zonas: [],
      locais: [],
      cargas: []
    } as any; // Cast simples para evitar erro de tipagem estrita no dummy

    addProject(newProject)
    // Feedback visual (opcional)
    // toast("Projeto criado!") 
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Cabeçalho da Página */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Meus Projetos</h1>
          <p className="text-muted-foreground">
            Gerencie seus projetos elétricos e dimensionamentos.
          </p>
        </div>
        <Button onClick={handleCreateProject}>
          <Plus className="mr-2 h-4 w-4" /> Novo Projeto
        </Button>
      </div>

      {/* Cartões de Resumo (Opcional, para dar um visual legal) */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Projetos</CardTitle>
            <Folder className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{projects.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Potência Total</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">-- kVA</div>
            <p className="text-xs text-muted-foreground">Soma de todos os projetos</p>
          </CardContent>
        </Card>
      </div>

      {/* Tabela de Projetos */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Nome do Projeto</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Sistema</TableHead>
              <TableHead className="text-right">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {projects.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  Nenhum projeto encontrado. Crie o primeiro!
                </TableCell>
              </TableRow>
            ) : (
              projects.map((project) => (
                <TableRow 
                  key={project.id} 
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => navigate(`/project/${project.id}`)}
                >
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <div className="h-8 w-8 rounded bg-primary/10 flex items-center justify-center text-primary">
                        <Folder className="h-4 w-4" />
                      </div>
                      {project.nome}
                    </div>
                  </TableCell>
                  <TableCell>{project.tipo_instalacao}</TableCell>
                  <TableCell>{project.sistema} - {project.tensao_sistema}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm">Abrir</Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}