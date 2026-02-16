import { useState, useMemo, useEffect } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { 
  Plus, Settings, Trash2, Zap, Activity, AlertCircle, GripVertical, 
  ArrowDownToLine, LayoutGrid, Table as TableIcon 
} from "lucide-react"

// DnD Kit
import { 
  DndContext, 
  DragOverlay, 
  useDraggable, 
  useDroppable, 
  type DragEndEvent, 
  type DragStartEvent,
  useSensor, 
  useSensors, 
  PointerSensor 
} from '@dnd-kit/core'

// UI Components
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
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

// Project Components
import { CircuitDialog } from "@/components/project/dialogs/CircuitDialog"
import { useProjectStore } from "@/store/useProjectStore"
import type { Carga, Circuito, Zona } from "@/types/project"

// --- SUB-COMPONENTES DE VISUALIZAÇÃO ---

// 1. Item Arrastável (Carga no Quadro)
function DraggableCarga({ 
  carga, 
  isSelected, 
  onToggleSelect, 
  showCheckbox 
}: { 
  carga: Carga, 
  isSelected?: boolean, 
  onToggleSelect?: (id: string) => void,
  showCheckbox?: boolean
}) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
    id: carga.id,
    data: { carga }
  })

  if (isDragging) {
    return (
      <div ref={setNodeRef} className="opacity-30 border-2 border-dashed border-primary/50 bg-background p-2 mb-2 rounded grayscale" style={{ height: '50px' }}>
      </div>
    )
  }

  return (
    <div 
      ref={setNodeRef} 
      className={`group flex items-center gap-3 p-2 mb-2 text-sm bg-card border rounded shadow-sm hover:border-primary/50 transition-all ${isSelected ? 'border-primary bg-primary/5 ring-1 ring-primary/20' : ''}`}
    >
      <div 
        {...listeners} 
        {...attributes} 
        className="cursor-grab active:cursor-grabbing p-1 text-muted-foreground hover:text-foreground"
      >
        <GripVertical className="h-4 w-4" />
      </div>

      {showCheckbox && onToggleSelect && (
        <Checkbox 
          checked={isSelected} 
          onCheckedChange={() => onToggleSelect(carga.id)}
          className="data-[state=checked]:bg-primary"
        />
      )}

      <div className="flex flex-col truncate flex-1">
         <span className="truncate font-medium leading-none">{carga.nome}</span>
         <span className="text-[10px] text-muted-foreground flex gap-1 mt-1">
           {carga.tipo} • <strong className="font-mono">{carga.potencia} {carga.unidade}</strong>
         </span>
      </div>
    </div>
  )
}

// 2. Container Soltável (Circuito no Quadro)
function DroppableContainer({ 
  id, 
  children, 
  className,
  isOver
}: { 
  id: string, 
  children: React.ReactNode, 
  className?: string,
  isOver?: boolean
}) {
  const { setNodeRef } = useDroppable({ id })
  
  const activeStyle = isOver 
    ? "border-primary bg-primary/5" 
    : "border-border hover:border-primary/30"

  return (
    <div 
        ref={setNodeRef} 
        className={`${className} border transition-colors duration-200 ease-in-out ${activeStyle}`}
    >
      {children}
    </div>
  )
}

// 3. Tabela Editável (Modo Planilha - COMPLETA)
function CircuitosTable({ 
    circuitos, 
    zonas,
    onUpdate, 
    onDelete 
}: { 
  circuitos: Circuito[], 
  zonas: Zona[],
  onUpdate: (circuito: Circuito) => void,
  onDelete: (id: string) => void
}) {
  if (circuitos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 border rounded-lg bg-muted/10 text-muted-foreground">
        <p>Nenhum circuito para exibir na tabela.</p>
      </div>
    )
  }

  return (
    <div className="border rounded-md overflow-hidden">
      <div className="overflow-x-auto">
        <Table className="min-w-[1000px]"> {/* Garante largura mínima para não esmagar colunas */}
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">ID</TableHead>
              <TableHead className="w-[140px]">Zona</TableHead>
              <TableHead className="w-[130px]">Tipo</TableHead>
              <TableHead className="w-[180px]">Método Inst.</TableHead>
              <TableHead className="w-[80px]">Tens.(V)</TableHead>
              <TableHead className="w-[80px]">Comp.(m)</TableHead>
              <TableHead className="w-[80px]">Temp.(°C)</TableHead>
              <TableHead className="w-[80px]">Agrup.</TableHead>
              <TableHead className="text-right w-[60px]">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {circuitos.map((circuito) => (
              <TableRow key={circuito.id}>
                {/* ID / NOME */}
                <TableCell>
                  <Input 
                    defaultValue={circuito.identificador} 
                    className="h-8 px-2"
                    onBlur={(e) => {
                      if (e.target.value !== circuito.identificador) {
                        onUpdate({ ...circuito, identificador: e.target.value })
                      }
                    }}
                  />
                </TableCell>

                {/* ZONA (Critical Link) */}
                <TableCell>
                  <Select 
                    defaultValue={circuito.zona_id} 
                    onValueChange={(val) => onUpdate({ ...circuito, zona_id: val })}
                  >
                    <SelectTrigger className="h-8 px-2">
                      <SelectValue placeholder="Selecione" />
                    </SelectTrigger>
                    <SelectContent>
                      {zonas.map(z => (
                          <SelectItem key={z.id} value={z.id}>{z.nome}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </TableCell>

                {/* TIPO */}
                <TableCell>
                  <Select 
                    defaultValue={circuito.tipo_circuito} 
                    onValueChange={(val) => onUpdate({ ...circuito, tipo_circuito: val as any })}
                  >
                    <SelectTrigger className="h-8 px-2">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ILUMINACAO">Iluminação</SelectItem>
                      <SelectItem value="TUG">TUG</SelectItem>
                      <SelectItem value="TUE">TUE</SelectItem>
                      <SelectItem value="MOTOR">Motor</SelectItem>
                      <SelectItem value="DISTRIBUICAO">Distribuição</SelectItem>
                    </SelectContent>
                  </Select>
                </TableCell>

                {/* MÉTODO */}
                <TableCell>
                  <Select 
                    defaultValue={circuito.metodo_instalacao}
                    onValueChange={(val) => onUpdate({ ...circuito, metodo_instalacao: val as any })}
                  >
                    <SelectTrigger className="h-8 px-2 text-xs">
                        <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="A1">A1 (Parede Isolada)</SelectItem>
                        <SelectItem value="B1">B1 (Eletroduto Emb.)</SelectItem>
                        <SelectItem value="C">C (Direto Parede)</SelectItem>
                        <SelectItem value="F">F (Ao Ar Livre)</SelectItem>
                    </SelectContent>
                  </Select>
                </TableCell>

                {/* TENSÃO */}
                <TableCell>
                  <Input 
                    type="number"
                    defaultValue={circuito.tensao_nominal}
                    className="h-8 px-2"
                    onBlur={(e) => {
                      const val = Number(e.target.value)
                      if (val !== circuito.tensao_nominal) onUpdate({ ...circuito, tensao_nominal: val })
                    }}
                  />
                </TableCell>

                {/* COMPRIMENTO (Opcional no início, crítico depois) */}
                <TableCell>
                  <Input 
                    type="number"
                    placeholder="0"
                    defaultValue={circuito.comprimento_m || 0}
                    className="h-8 px-2"
                    onBlur={(e) => {
                      const val = Number(e.target.value)
                      if (val !== circuito.comprimento_m) onUpdate({ ...circuito, comprimento_m: val })
                    }}
                  />
                </TableCell>

                {/* TEMPERATURA */}
                <TableCell>
                  <Input 
                    type="number"
                    placeholder="30"
                    defaultValue={circuito.temperatura_ambiente || 30}
                    className="h-8 px-2"
                    onBlur={(e) => {
                      const val = Number(e.target.value)
                      if (val !== circuito.temperatura_ambiente) onUpdate({ ...circuito, temperatura_ambiente: val })
                    }}
                  />
                </TableCell>

                {/* AGRUPAMENTO */}
                <TableCell>
                  <Input 
                        type="number"
                        defaultValue={circuito.circuitos_agrupados}
                        className="h-8 px-2"
                        onBlur={(e) => {
                          const val = Number(e.target.value)
                          if (val !== circuito.circuitos_agrupados) {
                            onUpdate({ ...circuito, circuitos_agrupados: val })
                          }
                        }}
                      />
                </TableCell>

                {/* AÇÕES */}
                <TableCell className="text-right">
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    className="h-8 w-8 text-destructive/70 hover:text-destructive"
                    onClick={() => onDelete(circuito.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}

// --- PÁGINA PRINCIPAL ---

export default function CircuitosPage() {
  const { id } = useParams<{ id: string }>()
  const { 
    projects, 
    addCircuitoToProject, 
    updateCircuitoInProject,
    removeCircuitoFromProject,
    setCargaCircuit 
  } = useProjectStore()

  const project = projects.find((p) => p.id === id)

  // --- STATES ---
  const [viewMode, setViewMode] = useState<"board" | "table">("board")
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingCircuito, setEditingCircuito] = useState<Circuito | null>(null)
  const [formData, setFormData] = useState<Partial<Circuito>>({})
  const [deleteTargetId, setDeleteTargetId] = useState<string | null>(null)
  
  // State DnD
  const [activeDragItem, setActiveDragItem] = useState<Carga | null>(null)
  const [activeDropId, setActiveDropId] = useState<string | null>(null) 

  // State Seleção em Massa
  const [selectedCargas, setSelectedCargas] = useState<string[]>([])

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: { distance: 8 },
    })
  )

  // --- EFFECT: Feedback de Seleção via Sonner ---
  useEffect(() => {
    if (selectedCargas.length > 0) {
        toast.message(`${selectedCargas.length} cargas selecionadas`, {
            id: 'bulk-selection-feedback', 
            description: "Arraste ou passe o mouse sobre um circuito.",
            duration: Infinity, 
            action: {
                label: "Cancelar",
                onClick: () => setSelectedCargas([])
            },
        })
    } else {
        toast.dismiss('bulk-selection-feedback')
    }
  }, [selectedCargas.length])

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  // --- DATA ---
  const cargasSemCircuito = useMemo(() => 
    project.cargas.filter(c => !c.circuito_id), 
  [project.cargas])

  const circuitos = project.circuitos || []

  // --- HANDLERS DND ---
  const handleDragStart = (event: DragStartEvent) => {
    if (event.active.data.current) {
        setActiveDragItem(event.active.data.current.carga as Carga)
    }
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    setActiveDragItem(null)
    setActiveDropId(null)

    if (!over) return

    const cargaId = active.id as string
    const targetId = over.id as string

    if (active.data.current?.carga?.circuito_id === targetId) return
    
    const finalTarget = targetId === 'unassigned' ? null : targetId
    setCargaCircuit(project.id, cargaId, finalTarget)
  }

  const handleDragOver = (event: DragEndEvent) => {
      const { over } = event
      setActiveDropId(over ? String(over.id) : null)
  }

  // --- HANDLERS SELEÇÃO EM MASSA ---
  const toggleSelectCarga = (cargaId: string) => {
    setSelectedCargas(prev => 
      prev.includes(cargaId) 
        ? prev.filter(id => id !== cargaId) 
        : [...prev, cargaId]
    )
  }

  const toggleSelectAll = () => {
    if (selectedCargas.length === cargasSemCircuito.length) {
      setSelectedCargas([])
    } else {
      setSelectedCargas(cargasSemCircuito.map(c => c.id))
    }
  }

  const handleMoveSelectedToCircuit = (circuitoId: string) => {
      if (selectedCargas.length === 0) return

      let count = 0
      selectedCargas.forEach(cargaId => {
          setCargaCircuit(project.id, cargaId, circuitoId)
          count++
      })
      toast.success(`${count} cargas movidas.`)
      setSelectedCargas([])
  }

  // --- HANDLERS CRUD ---
  const handleOpenDialog = (circuito?: Circuito) => {
    if (project.zonas.length === 0) {
        toast.error("Crie Zonas antes de definir Circuitos.")
        return
    }

    if (circuito) {
        setEditingCircuito(circuito)
        setFormData(circuito)
    } else {
        setEditingCircuito(null)
        setFormData({ 
            projeto_id: project.id,
            zona_id: project.zonas[0]?.id,
            tipo_circuito: 'ILUMINACAO',
            metodo_instalacao: 'B1',
            tensao_nominal: 220,
            circuitos_agrupados: 1,
            temperatura_ambiente: 30, // Defaults normativos
            comprimento_m: 0
        })
    }
    setIsDialogOpen(true)
  }

  const handleSave = () => {
    if (!project || !formData.identificador || !formData.zona_id) {
        toast.error("Identificador e Zona são obrigatórios.")
        return
    }

    const payload = {
        ...formData,
        id: editingCircuito?.id || crypto.randomUUID(),
        projeto_id: project.id,
        tensao_nominal: Number(formData.tensao_nominal),
        circuitos_agrupados: Number(formData.circuitos_agrupados),
        temperatura_ambiente: Number(formData.temperatura_ambiente || 30),
        comprimento_m: Number(formData.comprimento_m || 0),
        data_criacao: editingCircuito?.data_criacao || new Date().toISOString(),
        status: 'rascunho',
        cargas_ids: [] 
    } as Circuito

    if (editingCircuito) {
        updateCircuitoInProject(project.id, payload)
        toast.success("Circuito atualizado.")
    } else {
        addCircuitoToProject(project.id, payload)
        toast.success("Circuito criado.")
    }
    setIsDialogOpen(false)
  }

  const handleTableUpdate = (updatedCircuito: Circuito) => {
      updateCircuitoInProject(project.id, updatedCircuito)
      toast.success("Atualizado", { duration: 1000 })
  }

  const handleDeleteRequest = (id: string) => setDeleteTargetId(id)
  
  const confirmDelete = () => {
      if (deleteTargetId) {
          removeCircuitoFromProject(project.id, deleteTargetId)
          toast.success("Circuito excluído e cargas liberadas.")
          setDeleteTargetId(null)
      }
  }

  return (
    <DndContext 
      sensors={sensors} 
      onDragStart={handleDragStart} 
      onDragOver={handleDragOver}
      onDragEnd={handleDragEnd}
    >
      <div className="flex flex-col h-[calc(100vh-8rem)] gap-4 relative">
        
        {/* HEADER & TOGGLE VIEW */}
        <div className="flex justify-between items-center shrink-0">
          <div className="flex items-center gap-6">
             <div>
                <h2 className="text-2xl font-bold tracking-tight">Quadros e Circuitos</h2>
                <p className="text-muted-foreground">Distribuição e dimensionamento.</p>
             </div>
             
             {/* View Toggle */}
             <div className="h-9 bg-muted rounded-lg p-1 flex items-center">
                <button 
                    onClick={() => setViewMode("board")}
                    className={`flex items-center gap-2 px-3 py-1 text-sm font-medium rounded-md transition-all ${viewMode === 'board' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                >
                    <LayoutGrid className="h-4 w-4" /> Quadro
                </button>
                <button 
                    onClick={() => setViewMode("table")}
                    className={`flex items-center gap-2 px-3 py-1 text-sm font-medium rounded-md transition-all ${viewMode === 'table' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                >
                    <TableIcon className="h-4 w-4" /> Planilha
                </button>
             </div>
          </div>

          <Button onClick={() => handleOpenDialog()}>
              <Plus className="mr-2 h-4 w-4" /> Novo Circuito
          </Button>
        </div>

        {/* --- VIEW: BOARD (DND) --- */}
        {viewMode === "board" && (
            <div className="flex flex-1 gap-6 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
                {/* COLUNA 1: CARGAS SEM CIRCUITO */}
                <div className="w-1/3 flex flex-col gap-2 min-w-[300px]">
                    <div className="flex items-center justify-between pr-2">
                    <h3 className="font-semibold text-sm text-muted-foreground flex items-center gap-2">
                        <AlertCircle className="h-4 w-4" />
                        Sem Circuito ({cargasSemCircuito.length})
                    </h3>
                    {cargasSemCircuito.length > 0 && (
                        <div className="flex items-center gap-2">
                            <label className="text-xs text-muted-foreground cursor-pointer select-none" htmlFor="select-all">
                                Todos
                            </label>
                            <Checkbox 
                                id="select-all"
                                checked={cargasSemCircuito.length > 0 && selectedCargas.length === cargasSemCircuito.length}
                                onCheckedChange={toggleSelectAll}
                            />
                        </div>
                    )}
                    </div>
                    
                    <DroppableContainer 
                        id="unassigned" 
                        className="flex-1 bg-muted/30 border-dashed rounded-lg p-3 overflow-hidden"
                        isOver={activeDropId === "unassigned"}
                    >
                        <ScrollArea className="h-full pr-3">
                            {cargasSemCircuito.length === 0 ? (
                                <div className="text-center text-sm text-muted-foreground mt-10">
                                    Todas as cargas alocadas.
                                </div>
                            ) : (
                                cargasSemCircuito.map(carga => (
                                    <DraggableCarga 
                                    key={carga.id} 
                                    carga={carga} 
                                    showCheckbox={true}
                                    isSelected={selectedCargas.includes(carga.id)}
                                    onToggleSelect={toggleSelectCarga}
                                    />
                                ))
                            )}
                        </ScrollArea>
                    </DroppableContainer>
                </div>

                {/* COLUNA 2: LISTA DE CIRCUITOS */}
                <div className="flex-1 flex flex-col gap-2">
                    <h3 className="font-semibold text-sm text-muted-foreground flex items-center gap-2">
                        <Activity className="h-4 w-4" />
                        Quadro de Distribuição ({circuitos.length})
                    </h3>
                    
                    <ScrollArea className="flex-1 pr-4 -mr-4">
                        {circuitos.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-40 border rounded-lg bg-card text-muted-foreground">
                                <Zap className="h-8 w-8 mb-2 opacity-20" />
                                <p>Nenhum circuito criado.</p>
                                <Button variant="link" onClick={() => handleOpenDialog()}>Criar Primeiro Circuito</Button>
                            </div>
                        ) : (
                            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                                {circuitos.map(circuito => {
                                    const cargasDoCircuito = project.cargas.filter(c => c.circuito_id === circuito.id)
                                    const potenciaTotal = cargasDoCircuito.reduce((acc, c) => acc + c.potencia, 0)
                                    const isSelectionMode = selectedCargas.length > 0;

                                    return (
                                        <DroppableContainer 
                                            key={circuito.id} 
                                            id={circuito.id}
                                            className="h-full rounded-lg relative group"
                                            isOver={activeDropId === circuito.id}
                                        >
                                            <Card className="h-full flex flex-col border-0 shadow-none bg-transparent">
                                                {/* OVERLAY DE AÇÃO EM MASSA (Contextual) */}
                                                {isSelectionMode && (
                                                    <div className="absolute inset-0 bg-background/90 z-20 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg cursor-pointer border-2 border-primary"
                                                        onClick={() => handleMoveSelectedToCircuit(circuito.id)}
                                                    >
                                                        <ArrowDownToLine className="h-8 w-8 text-primary mb-2 animate-bounce" />
                                                        <span className="font-bold text-primary">Mover para cá</span>
                                                        <span className="text-xs text-muted-foreground">{selectedCargas.length} itens</span>
                                                    </div>
                                                )}

                                                <CardHeader className="pb-2 flex flex-row items-center justify-between space-y-0">
                                                    <div className="flex flex-col">
                                                        <CardTitle className="text-base font-bold flex items-center gap-2">
                                                            {circuito.identificador}
                                                            <Badge variant="secondary" className="text-[10px] font-normal h-5">
                                                                {circuito.tipo_circuito}
                                                            </Badge>
                                                        </CardTitle>
                                                        <span className="text-xs text-muted-foreground mt-1">
                                                            {potenciaTotal} VA • {circuito.tensao_nominal}V
                                                        </span>
                                                    </div>
                                                    <div className="flex -mr-2">
                                                        <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => handleOpenDialog(circuito)}>
                                                            <Settings className="h-3.5 w-3.5" />
                                                        </Button>
                                                        <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => handleDeleteRequest(circuito.id)}>
                                                            <Trash2 className="h-3.5 w-3.5" />
                                                        </Button>
                                                    </div>
                                                </CardHeader>
                                                
                                                <CardContent className="flex-1 pb-2 bg-muted/10 mx-1 mb-1 rounded-md mt-1 pt-2">
                                                    {cargasDoCircuito.length === 0 ? (
                                                        <div className="text-xs text-center text-muted-foreground py-6 border-2 border-dashed rounded opacity-50">
                                                            Arraste cargas aqui
                                                        </div>
                                                    ) : (
                                                        <div className="space-y-1">
                                                            {cargasDoCircuito.map(carga => (
                                                                <DraggableCarga key={carga.id} carga={carga} />
                                                            ))}
                                                        </div>
                                                    )}
                                                </CardContent>
                                            </Card>
                                        </DroppableContainer>
                                    )
                                })}
                            </div>
                        )}
                    </ScrollArea>
                </div>
            </div>
        )}

        {/* --- VIEW: TABLE (SPREADSHEET) --- */}
        {viewMode === "table" && (
             <div className="flex-1 overflow-auto bg-card rounded-lg border p-4 animate-in fade-in slide-in-from-bottom-2 duration-200">
                <div className="mb-4 flex items-center gap-2 text-sm text-muted-foreground bg-blue-50/50 p-2 rounded border border-blue-100 dark:bg-blue-900/10 dark:border-blue-800">
                    <AlertCircle className="h-4 w-4 text-blue-500" />
                    Edição rápida: As alterações são salvas automaticamente ao sair do campo.
                </div>
                
                <CircuitosTable 
                    circuitos={circuitos} 
                    zonas={project.zonas} // Passando as zonas para o Dropdown
                    onUpdate={handleTableUpdate}
                    onDelete={handleDeleteRequest}
                />
            </div>
        )}

        {/* DRAG OVERLAY (VISUAL FEEDBACK) */}
        <DragOverlay>
            {activeDragItem ? (
                <div className="opacity-90 w-[280px]">
                    <Card className="p-2 shadow-xl border-primary bg-background flex items-center gap-3">
                        <GripVertical className="h-4 w-4 text-primary" />
                        <div className="flex flex-col">
                             <span className="font-bold text-sm">{activeDragItem.nome}</span>
                             <span className="text-xs text-muted-foreground">{activeDragItem.potencia} {activeDragItem.unidade}</span>
                        </div>
                    </Card>
                </div>
            ) : null}
        </DragOverlay>

        {/* DIALOG FORM */}
        <CircuitDialog 
             open={isDialogOpen} 
             onOpenChange={setIsDialogOpen}
             data={formData}
             setData={setFormData}
             onSave={handleSave}
             zonas={project.zonas}
             isEditing={!!editingCircuito}
        />

        {/* DIALOG DELETE ALERT */}
        <AlertDialog open={!!deleteTargetId} onOpenChange={(open) => !open && setDeleteTargetId(null)}>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Excluir Circuito</AlertDialogTitle>
                    <AlertDialogDescription>
                        Tem certeza? Todas as cargas vinculadas a este circuito voltarão para a lista de "Sem Circuito".
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction onClick={confirmDelete} className="bg-destructive hover:bg-destructive/90 text-destructive-foreground">
                        Excluir
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>

      </div>
    </DndContext>
  )
}