import { useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { 
  Plus, Settings, Trash2, MapPin, 
  Maximize, ScanLine, ArrowUpFromLine 
} from "lucide-react"

import { Button } from "@/components/ui/button"
// FIX 2: Removido 'CardDescription' que não estava sendo usado
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { LocalDialog, type LocalComPerfil } from "@/components/project/dialogs/LocalDialog"
import { useProjectStore } from "@/store/useProjectStore"
import type { Local } from "@/types/project"

export default function LocaisPage() {
  const { id } = useParams<{ id: string }>()
  const { 
    projects, 
    addLocalToProject, 
    updateLocalInProject, 
    removeLocalFromProject 
  } = useProjectStore()

  const project = projects.find((p) => p.id === id)

  // State Local
  const [isLocalDialogOpen, setIsLocalDialogOpen] = useState(false)
  const [editingLocal, setEditingLocal] = useState<LocalComPerfil | null>(null)
  const [localFormData, setLocalFormData] = useState<Partial<LocalComPerfil>>({})

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  // --- HELPER: Encontrar Zona do Local ---
  const getZona = (zonaId: string) => project.zonas.find(z => z.id === zonaId)

  // --- HANDLERS ---

  const handleOpenLocalDialog = (local?: LocalComPerfil) => {
    // Validação Prévia: Precisa ter Zonas para criar Locais
    if (project.zonas.length === 0) {
        toast.error("Você precisa criar pelo menos uma Zona de Influência antes de adicionar Locais.")
        return
    }

    if (local) {
      setEditingLocal(local)
      setLocalFormData(local)
    } else {
      setEditingLocal(null)
      setLocalFormData({
        nome: "", 
        zona_id: project.zonas[0]?.id || "", // Seleciona a primeira zona por padrão
        tipo: "padrao",
        area_m2: 0, 
        perimetro_m: 0, 
        pe_direito_m: 2.8
      })
    }
    setIsLocalDialogOpen(true)
  }

  const handleSaveLocal = () => {
    if (!project || !localFormData.nome || !localFormData.zona_id) {
      toast.error("Preencha todos os campos obrigatórios.")
      return
    }

    const payload = {
      ...localFormData,
      area_m2: Number(localFormData.area_m2),
      perimetro_m: Number(localFormData.perimetro_m),
      pe_direito_m: Number(localFormData.pe_direito_m),
      projeto_id: project.id,
      id: editingLocal?.id || crypto.randomUUID(),
      data_criacao: editingLocal?.data_criacao || new Date().toISOString()
    } as Local

    if (editingLocal) {
      updateLocalInProject(project.id, payload)
      toast.success("Local atualizado.")
    } else {
      addLocalToProject(project.id, payload)
      toast.success("Local adicionado.")
    }
    setIsLocalDialogOpen(false)
  }

  const handleDeleteLocal = (localId: string) => {
    if (!project) return
    
    // Verifica cargas associadas (Integridade Referencial)
    const cargasNoLocal = project.cargas.filter(c => c.local_id === localId)
    
    if (cargasNoLocal.length > 0) {
        if (!confirm(`Este local possui ${cargasNoLocal.length} cargas associadas. Ao excluir, todas as cargas serão removidas. Deseja continuar?`)) {
            return
        }
    } else {
        if (!confirm("Tem certeza que deseja excluir este local?")) return
    }

    removeLocalFromProject(project.id, localId)
    toast.success("Local removido.")
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Locais e Ambientes</h2>
          <p className="text-muted-foreground">
            Cadastro dos cômodos e áreas físicas do projeto.
          </p>
        </div>
        <Button onClick={() => handleOpenLocalDialog()}>
            <Plus className="mr-2 h-4 w-4" /> Novo Local
        </Button>
      </div>

      {project.locais.length === 0 ? (
         <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed rounded-lg text-muted-foreground">
             <MapPin className="h-10 w-10 mb-2 opacity-20" />
             <p>Nenhum local cadastrado.</p>
             <Button variant="link" onClick={() => handleOpenLocalDialog()}>Adicionar primeiro local</Button>
         </div>
      ) : (
         <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {project.locais.map((local) => {
               const zona = getZona(local.zona_id)
               return (
                 <Card key={local.id} className="flex flex-col">
                   <CardHeader className="pb-2">
                     <div className="flex justify-between items-start">
                        <div className="space-y-1">
                            <CardTitle className="text-base">{local.nome}</CardTitle>
                            {zona && (
                                <Badge variant="outline" style={{ borderColor: zona.cor_identificacao, color: zona.cor_identificacao }}>
                                    {zona.nome}
                                </Badge>
                            )}
                        </div>
                        {/* FIX 1: Garantimos que 'tipo' tenha um fallback para satisfazer LocalComPerfil */}
                        <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 -mt-1 -mr-2" 
                            onClick={() => handleOpenLocalDialog({
                                ...local, 
                                tipo: local.tipo || 'padrao' 
                            })}
                        >
                            <Settings className="h-4 w-4 text-muted-foreground" />
                        </Button>
                     </div>
                   </CardHeader>
                   <CardContent className="pb-2 text-sm flex-1">
                      <div className="grid grid-cols-2 gap-2 mt-2">
                         <div className="flex items-center gap-2 text-muted-foreground" title="Área">
                            <Maximize className="h-4 w-4" />
                            <span>{local.area_m2} m²</span>
                         </div>
                         <div className="flex items-center gap-2 text-muted-foreground" title="Perímetro">
                            <ScanLine className="h-4 w-4" />
                            <span>{local.perimetro_m} m</span>
                         </div>
                         <div className="flex items-center gap-2 text-muted-foreground" title="Pé Direito">
                            <ArrowUpFromLine className="h-4 w-4" />
                            <span>{local.pe_direito_m} m</span>
                         </div>
                      </div>
                   </CardContent>
                   <CardFooter className="pt-2 justify-end border-t bg-muted/20">
                      <Button 
                         variant="ghost" size="sm" 
                         className="text-destructive hover:bg-destructive/10 h-7 px-2"
                         onClick={() => handleDeleteLocal(local.id)}
                      >
                         <Trash2 className="h-3.5 w-3.5 mr-1.5" /> Excluir
                      </Button>
                   </CardFooter>
                 </Card>
               )
            })}
         </div>
      )}

      <LocalDialog
        open={isLocalDialogOpen} 
        onOpenChange={setIsLocalDialogOpen}
        data={localFormData} 
        setData={setLocalFormData} 
        onSave={handleSaveLocal}
        zonas={project.zonas} 
        isEditing={!!editingLocal}
      />
    </div>
  )
}