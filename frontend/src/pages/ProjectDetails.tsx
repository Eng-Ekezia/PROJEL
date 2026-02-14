import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { toast } from "sonner"
import { DndContext, type DragEndEvent, useSensor, useSensors, PointerSensor } from '@dnd-kit/core';

import { NBR5410_WIZARD } from "../data/nbr5410_wizard"

// UI Components
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"

// Sub-components (Refatoração Fase 08)
import { ZoneTab } from "@/components/project/tabs/ZoneTab"
import { LocalTab } from "@/components/project/tabs/LocalTab"
import { CargaTab } from "@/components/project/tabs/CargaTab"
import { CircuitosTab } from "@/components/project/tabs/CircuitosTab"

import { ZoneDialog } from "@/components/project/dialogs/ZoneDialog"
import { LocalDialog, type LocalComPerfil } from "@/components/project/dialogs/LocalDialog"
import { CargaDialog } from "@/components/project/dialogs/CargaDialog"
import { CircuitDialog } from "@/components/project/dialogs/CircuitDialog"

// Store & Types
import { useProjectStore } from "../store/useProjectStore"
import type { Zona, Local, Carga, Circuito } from "../types/project"

export default function ProjectDetails() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { 
    projects, 
    addZonaToProject, updateZonaInProject, removeZonaFromProject,
    addLocalToProject, updateLocalInProject, removeLocalFromProject,
    addCargaToProject, removeCargaFromProject,
    // Actions de Circuito
    addCircuitoToProject, updateCircuitoInProject, removeCircuitoFromProject, setCargaCircuit
  } = useProjectStore()
  
  const project = projects.find((p) => p.id === id)

  // --- STATE ---
  const [activeTab, setActiveTab] = useState("zonas")
  
  // Dialog States
  const [isZoneDialogOpen, setIsZoneDialogOpen] = useState(false)
  const [editingZona, setEditingZona] = useState<Zona | null>(null)
  const [zonaFormData, setZonaFormData] = useState<Partial<Zona>>({})

  const [isLocalDialogOpen, setIsLocalDialogOpen] = useState(false)
  const [editingLocal, setEditingLocal] = useState<LocalComPerfil | null>(null)
  const [localFormData, setLocalFormData] = useState<Partial<LocalComPerfil>>({})

  const [isCargaDialogOpen, setIsCargaDialogOpen] = useState(false)
  const [cargaFormData, setCargaFormData] = useState<Partial<Carga>>({})

  // Estado para Circuitos
  const [isCircuitoDialogOpen, setIsCircuitoDialogOpen] = useState(false)
  const [editingCircuito, setEditingCircuito] = useState<Circuito | null>(null)
  const [circuitoFormData, setCircuitoFormData] = useState<Partial<Circuito>>({})

  // Sensores para o DnD (Melhora a UX do clique vs arraste)
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // Só ativa o drag se mover 8px (permite clicar no checkbox sem arrastar)
      },
    })
  );

  // --- HANDLERS: ZONA ---
  const handleOpenZoneDialog = (zona?: Zona) => {
    if (zona) {
      setEditingZona(zona)
      setZonaFormData(zona)
    } else {
      setEditingZona(null)
      setZonaFormData({
        nome: "", descricao: "", 
        temp_ambiente: "AA1", presenca_agua: "AD1", presenca_solidos: "AE1",
        competencia_pessoas: "BA1", materiais_construcao: "CA1", estrutura_edificacao: "CB1",
        origem: "custom", cor_identificacao: "#3b82f6"
      })
    }
    setIsZoneDialogOpen(true)
  }

  const handleSaveZona = () => {
    if (!project || !zonaFormData.nome) {
      toast.error("Nome é obrigatório")
      return
    }
    const payload = {
      ...zonaFormData,
      projeto_id: project.id,
      id: editingZona?.id || crypto.randomUUID(),
      data_criacao: editingZona?.data_criacao || new Date().toISOString()
    } as Zona

    if (editingZona) {
      updateZonaInProject(project.id, payload)
      toast.success("Zona atualizada")
    } else {
      addZonaToProject(project.id, payload)
      toast.success("Zona criada")
    }
    setIsZoneDialogOpen(false)
  }

  const handleDeleteZona = (zonaId: string) => {
    if (!project) return
    const locais = project.locais.filter(l => l.zona_id === zonaId)
    if (locais.length > 0) {
      toast.error(`Impossível excluir: Existem ${locais.length} locais nesta zona.`)
      return
    }
    if (confirm("Excluir esta zona?")) {
      removeZonaFromProject(project.id, zonaId)
      toast.success("Zona removida")
    }
  }

  // --- HANDLERS: LOCAL ---
  const handleOpenLocalDialog = (local?: LocalComPerfil) => {
    if (local) {
      setEditingLocal(local)
      setLocalFormData(local)
    } else {
      setEditingLocal(null)
      setLocalFormData({
        nome: "", zona_id: project?.zonas[0]?.id || "", tipo: "padrao",
        area_m2: 0, perimetro_m: 0, pe_direito_m: 2.8
      })
    }
    setIsLocalDialogOpen(true)
  }

  const handleSaveLocal = () => {
    if (!project || !localFormData.nome || !localFormData.zona_id || !localFormData.tipo) {
      toast.error("Preencha todos os campos obrigatórios")
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
      toast.success("Local atualizado")
    } else {
      addLocalToProject(project.id, payload)
      toast.success("Local adicionado")
    }
    setIsLocalDialogOpen(false)
  }

  const handleDeleteLocal = (localId: string) => {
    if (!project) return
    if (confirm("Excluir local e todas as cargas associadas?")) {
      removeLocalFromProject(project.id, localId)
      toast.success("Local removido")
    }
  }

  // --- HANDLERS: CARGA ---
  const handleOpenCargaDialog = () => {
    setCargaFormData({
      nome: "", local_id: project?.locais[0]?.id || "",
      tipo: "TUG", potencia: 100, unidade: "VA",
      fator_potencia: 0.8, origem: "usuario"
    })
    setIsCargaDialogOpen(true)
  }

  const handleSaveCarga = () => {
    if (!project || !cargaFormData.nome || !cargaFormData.local_id) return
    const payload: Carga = {
      id: crypto.randomUUID(),
      projeto_id: project.id,
      local_id: cargaFormData.local_id!,
      nome: cargaFormData.nome!,
      tipo: cargaFormData.tipo || "TUG",
      potencia: Number(cargaFormData.potencia),
      unidade: cargaFormData.unidade as 'W' | 'VA',
      fator_potencia: Number(cargaFormData.fator_potencia),
      origem: "usuario"
    }
    addCargaToProject(project.id, payload)
    toast.success("Carga adicionada manualmente")
    setIsCargaDialogOpen(false)
  }

  const handleDeleteCarga = (cargaId: string) => {
    if(!project) return
    removeCargaFromProject(project.id, cargaId)
    toast.success("Carga removida")
  }

  const handleAutoCargas = () => {
    if (!project) return
    const confirmacao = confirm(`Gerar automaticamente a previsão de cargas para ${project.locais.length} locais conforme NBR 5410?`)
    if (!confirmacao) return

    let contagem = 0
    project.locais.forEach(local => {
        const potIlum = NBR5410_WIZARD.calcularIluminacao(local.area_m2)
        const cargaIlum: Carga = {
          id: crypto.randomUUID(), projeto_id: project.id, local_id: local.id,
          nome: "Iluminação Central", tipo: "Iluminacao", potencia: potIlum,
          unidade: 'VA', fator_potencia: 1.0, origem: 'norma'
        }
        addCargaToProject(project.id, cargaIlum)
        contagem++
        
        const tugs = NBR5410_WIZARD.calcularTUGs(local)
        tugs.forEach(tug => { addCargaToProject(project.id, tug); contagem++ })
    })
    toast.success(`${contagem} cargas sugeridas pela norma foram adicionadas!`)
  }

  // --- HANDLERS: CIRCUITO ---
  const handleOpenCircuitoDialog = (circuito?: Circuito) => {
    if (circuito) {
        setEditingCircuito(circuito)
        setCircuitoFormData(circuito)
    } else {
        setEditingCircuito(null)
        setCircuitoFormData({ projeto_id: project?.id }) // IDs gerados no save
    }
    setIsCircuitoDialogOpen(true)
  }

  const handleSaveCircuito = () => {
    if (!project || !circuitoFormData.identificador) {
        toast.error("Identificador é obrigatório (Ex: C1)")
        return
    }

    // Validação de Zona Obrigatória (Regra de Negócio: entidade_circuito.md)
    if (!circuitoFormData.zona_id) {
        toast.error("ERRO NORMATIVO: O Circuito deve pertencer a uma Zona de Influência.")
        return
    }
    
    // Tratamento seguro dos Enums com fallback e conversão numérica
    const payload = {
        ...circuitoFormData,
        id: editingCircuito?.id || crypto.randomUUID(),
        projeto_id: project.id,
        // Garante que campos numéricos sejam Number
        tensao_nominal: Number(circuitoFormData.tensao_nominal),
        circuitos_agrupados: Number(circuitoFormData.circuitos_agrupados),
        data_criacao: editingCircuito?.data_criacao || new Date().toISOString(),
        status: 'rascunho',
        cargas_ids: [] // Gerenciado via filtro (Source of Truth no ID da Carga)
    } as Circuito

    if (editingCircuito) {
        updateCircuitoInProject(project.id, payload)
        toast.success("Circuito atualizado")
    } else {
        addCircuitoToProject(project.id, payload)
        toast.success("Circuito criado")
    }
    setIsCircuitoDialogOpen(false)
  }

  const handleDeleteCircuito = (circuitoId: string) => {
     if(!project) return
     if(confirm("Excluir circuito? As cargas voltarão para a lista de 'Sem Circuito'.")){
        removeCircuitoFromProject(project.id, circuitoId)
        toast.success("Circuito removido")
     }
  }

  const handleAssignCargas = (circuitoId: string, cargasIds: string[]) => {
    if (!project) return
    cargasIds.forEach(cargaId => {
        setCargaCircuit(project.id, cargaId, circuitoId)
    })
  }

  const handleUnassignCarga = (cargaId: string) => {
    if (!project) return
    setCargaCircuit(project.id, cargaId, null)
    toast.info("Carga removida do circuito")
  }

  // Handler do Drag-and-Drop
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const cargaId = active.id as string;
      const circuitoId = over.id as string;
      
      // Chama a store para associar
      if (project) {
        setCargaCircuit(project.id, cargaId, circuitoId);
        toast.success("Carga movida com sucesso!");
      }
    }
  };

  if (!project) return null

  return (
    <div className="flex flex-col gap-6 pb-20">
      {/* HEADER */}
      <div className="flex items-center gap-4 border-b pb-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/")}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{project.nome}</h1>
          <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
            <Badge variant="outline">{project.tipo_instalacao}</Badge>
            <Separator orientation="vertical" className="h-4" />
            <span>{project.sistema} ({project.tensao_sistema})</span>
            <Separator orientation="vertical" className="h-4" />
            <Badge variant="secondary">At: {project.esquema_aterramento || "ND"}</Badge>
          </div>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4 lg:w-[600px]">
          <TabsTrigger value="zonas">1. Ambientes</TabsTrigger>
          <TabsTrigger value="locais">2. Arquitetura</TabsTrigger>
          <TabsTrigger value="cargas">3. Cargas</TabsTrigger>
          <TabsTrigger value="circuitos">4. Circuitos</TabsTrigger>
        </TabsList>

        <TabsContent value="zonas">
          <ZoneTab 
            zonas={project.zonas} 
            onNew={() => handleOpenZoneDialog()} 
            onEdit={handleOpenZoneDialog} 
            onDelete={handleDeleteZona} 
          />
        </TabsContent>

        <TabsContent value="locais">
          <LocalTab 
            locais={project.locais} 
            zonas={project.zonas}
            onNew={() => handleOpenLocalDialog()} 
            onEdit={handleOpenLocalDialog} 
            onDelete={handleDeleteLocal} 
          />
        </TabsContent>

        <TabsContent value="cargas">
          <CargaTab 
            cargas={project.cargas} 
            locais={project.locais}
            zonas={project.zonas}
            onNew={handleOpenCargaDialog}
            onAutoCargas={handleAutoCargas}
            onDelete={handleDeleteCarga}
          />
        </TabsContent>

        <TabsContent value="circuitos">
            <DndContext sensors={sensors} onDragEnd={handleDragEnd}>
                <CircuitosTab 
                    circuitos={project.circuitos || []}
                    cargas={project.cargas}
                    zonas={project.zonas}
                    onNewCircuito={() => handleOpenCircuitoDialog()}
                    onEditCircuito={handleOpenCircuitoDialog}
                    onDeleteCircuito={handleDeleteCircuito}
                    onAssignCargas={handleAssignCargas}
                    onUnassignCarga={handleUnassignCarga}
                />
            </DndContext>
        </TabsContent>
      </Tabs>

      {/* DIALOGS */}
      <ZoneDialog 
        open={isZoneDialogOpen} onOpenChange={setIsZoneDialogOpen}
        data={zonaFormData} setData={setZonaFormData} onSave={handleSaveZona}
        isEditing={!!editingZona}
      />
      <LocalDialog
        open={isLocalDialogOpen} onOpenChange={setIsLocalDialogOpen}
        data={localFormData} setData={setLocalFormData} onSave={handleSaveLocal}
        zonas={project.zonas} isEditing={!!editingLocal}
      />
      <CargaDialog
        open={isCargaDialogOpen} onOpenChange={setIsCargaDialogOpen}
        data={cargaFormData} setData={setCargaFormData} onSave={handleSaveCarga}
        locais={project.locais}
      />
      
      {/* DIALOG DE CIRCUITO */}
      <CircuitDialog 
        open={isCircuitoDialogOpen} onOpenChange={setIsCircuitoDialogOpen}
        data={circuitoFormData} setData={setCircuitoFormData} onSave={handleSaveCircuito}
        zonas={project.zonas} isEditing={!!editingCircuito}
      />
    </div>
  )
}