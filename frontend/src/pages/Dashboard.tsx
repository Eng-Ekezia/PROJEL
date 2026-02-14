import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Plus, Folder, Zap, Settings, Trash2, ArrowRight } from "lucide-react"
import { toast } from "sonner"

// Componentes Shadcn UI
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"

// Componentes do Projeto
import { EditProjectDialog } from "@/components/project/dialogs/EditProjectDialog"

// Store e Tipos
import { useProjectStore } from "../store/useProjectStore"
import type { Projeto } from "@/types/project"

export default function Dashboard() {
  const navigate = useNavigate()
  const { 
    projects, 
    addProject, 
    updateProject, 
    deleteProject 
  } = useProjectStore()

  // --- STATES ---
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [projectToEdit, setProjectToEdit] = useState<Projeto | null>(null)
  const [formData, setFormData] = useState<Partial<Projeto>>({})
  
  // Novo State para Exclusão
  const [projectToDelete, setProjectToDelete] = useState<string | null>(null)

  // --- HANDLERS ---

  const handleCreateProject = () => {
    const nome = prompt("Nome do novo projeto:")
    if (!nome) return

    const newProject = {
      id: crypto.randomUUID(),
      nome,
      tipo_instalacao: "Residencial",
      tensao_sistema: "127/220V",
      sistema: "Monofasico",
      esquema_aterramento: "TN-S",
      data_criacao: new Date().toISOString(),
      ultima_modificacao: new Date().toISOString(),
      zonas: [],
      locais: [],
      cargas: [],
      circuitos: [] 
    } as unknown as Projeto

    addProject(newProject)
    toast.success("Projeto criado com sucesso!")
  }

  const handleEditClick = (e: React.MouseEvent, project: Projeto) => {
    e.stopPropagation()
    setProjectToEdit(project)
    setFormData({ ...project })
    setIsEditOpen(true)
  }

  const handleSaveEdit = () => {
    if (!projectToEdit || !formData.nome) {
        toast.error("Nome é obrigatório")
        return
    }

    const updatedProject = {
        ...projectToEdit,
        ...formData,
        ultima_modificacao: new Date().toISOString()
    } as Projeto

    updateProject(updatedProject)
    setIsEditOpen(false)
    toast.success("Projeto atualizado!")
  }

  // Abre o Dialog de Exclusão
  const handleDeleteClick = (e: React.MouseEvent, id: string) => {
    e.stopPropagation()
    setProjectToDelete(id)
  }

  // Confirma a Exclusão (Ação do botão "Sim, excluir")
  const confirmDelete = () => {
    if (projectToDelete) {
        deleteProject(projectToDelete)
        toast.success("Projeto excluído.")
        setProjectToDelete(null)
    }
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

      {/* Cartões de Resumo */}
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
            <p className="text-xs text-muted-foreground">Soma estimada</p>
          </CardContent>
        </Card>
      </div>

      {/* Tabela de Projetos */}
      <div className="rounded-md border bg-card">
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
                <TableCell colSpan={4} className="h-24 text-center text-muted-foreground">
                  Nenhum projeto encontrado. Clique em "Novo Projeto" para começar.
                </TableCell>
              </TableRow>
            ) : (
              projects.map((project) => (
                <TableRow 
                  key={project.id} 
                  className="cursor-pointer hover:bg-muted/50 group"
                  onClick={() => navigate(`/project/${project.id}`)}
                >
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <div className="h-8 w-8 rounded bg-primary/10 flex items-center justify-center text-primary">
                        <Folder className="h-4 w-4" />
                      </div>
                      <div className="flex flex-col">
                        <span>{project.nome}</span>
                        <span className="text-[10px] text-muted-foreground md:hidden">
                            Atualizado em: {new Date(project.ultima_modificacao).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
                        {project.tipo_instalacao}
                    </span>
                  </TableCell>
                  <TableCell className="text-muted-foreground text-sm">
                    {project.sistema} <span className="text-xs">({project.tensao_sistema})</span>
                  </TableCell>
                  
                  {/* COLUNA DE AÇÕES */}
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                        <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-muted-foreground hover:text-foreground"
                            onClick={(e) => handleEditClick(e, project)}
                            title="Editar Configurações"
                        >
                            <Settings className="h-4 w-4" />
                        </Button>
                        <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10"
                            onClick={(e) => handleDeleteClick(e, project.id)}
                            title="Excluir Projeto"
                        >
                            <Trash2 className="h-4 w-4" />
                        </Button>
                        <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8"
                            onClick={() => navigate(`/project/${project.id}`)}
                        >
                            <ArrowRight className="h-4 w-4" />
                        </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* MODAL DE EDIÇÃO */}
      <EditProjectDialog 
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        data={formData}
        setData={setFormData}
        onSave={handleSaveEdit}
      />

      {/* ALERT DIALOG DE EXCLUSÃO (NOVO) */}
      <AlertDialog open={!!projectToDelete} onOpenChange={(open) => !open && setProjectToDelete(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Tem certeza absoluta?</AlertDialogTitle>
            <AlertDialogDescription>
              Essa ação não pode ser desfeita. Isso excluirá permanentemente o projeto 
              <span className="font-bold text-foreground"> "{projects.find(p => p.id === projectToDelete)?.nome}" </span>
              e todos os seus dados (zonas, cargas, circuitos).
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction 
                onClick={confirmDelete} 
                className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
                Sim, excluir
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}