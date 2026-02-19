import { useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { 
  Plus, Lightbulb, Plug, Zap, Trash2, Wand2, Pencil, AlertTriangle 
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table"
import {
  Accordion, AccordionContent, AccordionItem, AccordionTrigger,
} from "@/components/ui/accordion"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from "@/components/ui/alert-dialog"

import { CargaDialog } from "@/components/project/dialogs/CargaDialog"
import { useProjectStore } from "@/store/useProjectStore"
import { NBR5410_WIZARD } from "@/data/nbr5410_wizard"
import type { Carga } from "@/types/project"

export default function CargasPage() {
  const { id } = useParams<{ id: string }>()
  const { projects, addCargaToProject, updateCargaInProject, removeCargaFromProject } = useProjectStore()

  const project = projects.find((p) => p.id === id)

  const [isCargaDialogOpen, setIsCargaDialogOpen] = useState(false)
  const [editingCargaId, setEditingCargaId] = useState<string | null>(null)
  const [cargaFormData, setCargaFormData] = useState<Partial<Carga>>({})

  const [isAutoAlertOpen, setIsAutoAlertOpen] = useState(false)
  const [deleteTargetId, setDeleteTargetId] = useState<string | null>(null)

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  const handleOpenCargaDialog = (carga?: Carga) => {
    if (project.locais.length === 0) {
        toast.error("Você precisa criar Locais antes de adicionar Cargas.")
        return
    }

    if (carga) {
      setEditingCargaId(carga.id)
      setCargaFormData({ ...carga })
    } else {
      setEditingCargaId(null)
      setCargaFormData({
        nome: "", 
        local_id: project.locais[0]?.id || "",
        tipo: "TUG", 
        potencia: 100, 
        unidade: "VA",
        fator_potencia: 0.8, 
        origem: "usuario"
      })
    }
    setIsCargaDialogOpen(true)
  }

  const handleSaveCarga = () => {
    if (!project || !cargaFormData.nome || !cargaFormData.local_id) return

    const cargaId = editingCargaId || crypto.randomUUID()
    const origemFinal = editingCargaId && cargaFormData.origem ? cargaFormData.origem : 'usuario'

    // [NOVO] Resgata a Zona a partir do Local Selecionado
    const localSelecionado = project.locais.find(l => l.id === cargaFormData.local_id)
    const zonaHerdada = localSelecionado?.zona_id || ""

    const payload: Carga = {
      id: cargaId,
      projeto_id: project.id,
      local_id: cargaFormData.local_id,
      zona_id: zonaHerdada, // <--- Herança Injetada Aqui
      nome: cargaFormData.nome,
      tipo: cargaFormData.tipo || "TUG",
      potencia: Number(cargaFormData.potencia),
      unidade: cargaFormData.unidade as 'W' | 'VA',
      fator_potencia: Number(cargaFormData.fator_potencia),
      origem: origemFinal, 
      circuito_id: editingCargaId ? (cargaFormData.circuito_id || null) : null 
    }
    
    if (editingCargaId) {
      updateCargaInProject(project.id, payload)
      toast.success("Carga atualizada com sucesso.")
    } else {
      addCargaToProject(project.id, payload)
      toast.success("Carga adicionada manualmente.")
    }
    
    setIsCargaDialogOpen(false)
  }

  const confirmDelete = () => {
    if (project && deleteTargetId) {
      removeCargaFromProject(project.id, deleteTargetId)
      toast.success("Carga removida.")
    }
    setDeleteTargetId(null)
  }

  const handleAutoCargasConfirm = () => {
    if (!project) return
    setIsAutoAlertOpen(false)

    let contagem = 0
    project.locais.forEach(local => {
        const potIlum = NBR5410_WIZARD.calcularIluminacao(local.area_m2)
        if (potIlum > 0) {
            const cargaIlum: Carga = {
              id: crypto.randomUUID(), 
              projeto_id: project.id, 
              local_id: local.id,
              zona_id: local.zona_id, // <--- Herança Injetada Aqui
              nome: "Iluminação Central", 
              tipo: "Iluminacao", 
              potencia: potIlum,
              unidade: 'VA', 
              fator_potencia: 1.0, 
              origem: 'norma',
              circuito_id: null
            }
            addCargaToProject(project.id, cargaIlum)
            contagem++
        }
        
        const tugs = NBR5410_WIZARD.calcularTUGs(local)
        tugs.forEach(tug => { 
            const cargaTug: Carga = {
                ...tug,
                id: crypto.randomUUID(),
                projeto_id: project.id,
                local_id: local.id,
                zona_id: local.zona_id, // <--- Herança Injetada Aqui
                circuito_id: null
            }
            addCargaToProject(project.id, cargaTug); 
            contagem++ 
        })
    })
    toast.success(`${contagem} cargas sugeridas pela norma foram adicionadas!`)
  }

  const handleOpenAutoWizard = () => {
    if (!project || project.locais.length === 0) {
        toast.error("Adicione locais com dimensões antes de usar o assistente.")
        return
    }
    setIsAutoAlertOpen(true)
  }

  const cargasPorLocal = project.locais.map(local => ({
      local,
      cargas: project.cargas.filter(c => c.local_id === local.id)
  }))

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] gap-4">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Cargas Elétricas</h2>
          <p className="text-muted-foreground">
            Gerenciamento de potência instalada por ambiente.
          </p>
        </div>
        <div className="flex gap-2">
            <Button variant="outline" onClick={handleOpenAutoWizard}>
                <Wand2 className="mr-2 h-4 w-4" /> Assistente NBR 5410
            </Button>
            <Button onClick={() => handleOpenCargaDialog()}>
                <Plus className="mr-2 h-4 w-4" /> Nova Carga
            </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 rounded-md border p-4 bg-background/50">
        {project.cargas.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full py-20 text-muted-foreground">
                <Zap className="h-10 w-10 mb-2 opacity-20" />
                <p>Nenhuma carga cadastrada.</p>
                <p className="text-sm">Adicione manualmente ou use o Assistente.</p>
            </div>
        ) : (
            <Accordion type="multiple" className="w-full space-y-4">
                {cargasPorLocal.map(({ local, cargas }) => (
                    <AccordionItem key={local.id} value={local.id} className="border rounded-lg px-4 bg-card">
                        <AccordionTrigger className="hover:no-underline">
                            <div className="flex items-center gap-4 w-full">
                                <span className="font-medium">{local.nome}</span>
                                <Badge variant="outline" className="text-xs font-normal text-muted-foreground">
                                    {cargas.length} Cargas
                                </Badge>
                                <span className="text-xs text-muted-foreground ml-auto mr-4">
                                    Total: {cargas.reduce((acc, c) => acc + c.potencia, 0)} VA
                                </span>
                            </div>
                        </AccordionTrigger>
                        <AccordionContent>
                            {cargas.length === 0 ? (
                                <p className="text-sm text-muted-foreground py-2 italic">Nenhuma carga neste local.</p>
                            ) : (
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Descrição</TableHead>
                                            <TableHead>Tipo</TableHead>
                                            <TableHead className="text-right">Potência</TableHead>
                                            <TableHead className="w-[100px] text-right">Ações</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {cargas.map((carga) => (
                                            <TableRow key={carga.id}>
                                                <TableCell className="font-medium">
                                                    {carga.nome}
                                                    {carga.origem === 'norma' && (
                                                        <Badge variant="secondary" className="ml-2 text-[10px] h-4 px-1">Norma</Badge>
                                                    )}
                                                </TableCell>
                                                <TableCell>
                                                    {carga.tipo === 'Iluminacao' ? (
                                                        <div className="flex items-center gap-1 text-yellow-600"><Lightbulb className="h-3 w-3" /> Ilum.</div>
                                                    ) : (
                                                        <div className="flex items-center gap-1 text-slate-600"><Plug className="h-3 w-3" /> {carga.tipo}</div>
                                                    )}
                                                </TableCell>
                                                <TableCell className="text-right">
                                                    {carga.potencia} {carga.unidade}
                                                </TableCell>
                                                <TableCell className="text-right">
                                                    <div className="flex justify-end gap-1">
                                                        <Button 
                                                            variant="ghost" 
                                                            size="icon" 
                                                            className="h-8 w-8 text-muted-foreground hover:text-foreground"
                                                            onClick={() => handleOpenCargaDialog(carga)}
                                                        >
                                                            <Pencil className="h-4 w-4" />
                                                        </Button>
                                                        <Button 
                                                            variant="ghost" 
                                                            size="icon" 
                                                            className="h-8 w-8 text-destructive/70 hover:text-destructive"
                                                            onClick={() => setDeleteTargetId(carga.id)}
                                                        >
                                                            <Trash2 className="h-4 w-4" />
                                                        </Button>
                                                    </div>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            )}
                        </AccordionContent>
                    </AccordionItem>
                ))}
            </Accordion>
        )}
      </ScrollArea>

      <CargaDialog
        open={isCargaDialogOpen} 
        onOpenChange={setIsCargaDialogOpen}
        data={cargaFormData} 
        setData={setCargaFormData} 
        onSave={handleSaveCarga}
        locais={project.locais}
      />

      <AlertDialog open={!!deleteTargetId} onOpenChange={(open) => !open && setDeleteTargetId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Excluir Carga</AlertDialogTitle>
            <AlertDialogDescription>
              Esta ação não pode ser desfeita. A carga será removida permanentemente do projeto.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Excluir
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog open={isAutoAlertOpen} onOpenChange={setIsAutoAlertOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
                <Wand2 className="h-5 w-5 text-primary" />
                Assistente NBR 5410
            </AlertDialogTitle>
            <AlertDialogDescription>
              O sistema irá analisar a área e perímetro de <strong>{project.locais.length} locais</strong> e adicionar automaticamente:
              <ul className="list-disc list-inside mt-2 space-y-1">
                  <li>Pontos de iluminação (mínimo normativo)</li>
                  <li>Tomadas de Uso Geral (TUGs)</li>
              </ul>
              <br/>
              <span className="flex items-center gap-2 text-yellow-600 font-medium">
                  <AlertTriangle className="h-4 w-4" />
                  Isso adicionará novas cargas, sem apagar as existentes.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleAutoCargasConfirm}>
              Gerar Cargas
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}