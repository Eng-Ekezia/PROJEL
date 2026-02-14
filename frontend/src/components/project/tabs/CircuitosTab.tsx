import { useState } from "react"
import { useDraggable, useDroppable } from '@dnd-kit/core';
import { Plus, Settings, Trash2, ArrowRight, Zap, AlertTriangle, GripVertical } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import { toast } from "sonner"
// import { cn } from "@/lib/utils" // Opcional se usar shadcn utils

import type { Circuito, Carga, Zona } from "@/types/project"

// --- SUB-COMPONENTES DND ---

// 1. Carga Draggable (Arrastável)
function DraggableCarga({ carga, isSelected, onToggle }: { carga: Carga, isSelected: boolean, onToggle: (id: string) => void }) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: carga.id,
    data: { type: 'carga', carga }
  });

  const style = transform ? {
    transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
    zIndex: 999,
  } : undefined;

  return (
    <div 
      ref={setNodeRef} 
      style={style} 
      className={`flex items-start gap-3 p-3 rounded-md border bg-card transition-colors ${isSelected ? 'border-primary bg-accent' : ''} ${isDragging ? 'opacity-50 ring-2 ring-primary shadow-lg' : 'hover:border-primary/50'}`}
    >
        <div className="flex items-center h-5">
             <Checkbox 
                checked={isSelected}
                onCheckedChange={() => onToggle(carga.id)}
             />
        </div>
        
        {/* Grip Handle para arrastar (PONTO 2 RESOLVIDO: DnD explícito) */}
        <div {...listeners} {...attributes} className="cursor-grab active:cursor-grabbing text-muted-foreground hover:text-foreground mt-0.5" title="Arrastar para um circuito">
            <GripVertical className="h-4 w-4" />
        </div>

        <div className="flex-1 min-w-0 select-none">
            <div className="font-medium text-sm truncate">{carga.nome}</div>
            <div className="text-xs text-muted-foreground flex gap-2">
                <span>{carga.tipo}</span>
                <span>•</span>
                {/* PONTO 3 RESOLVIDO: Força Number() para evitar NaN */}
                <span>{Number(carga.potencia || 0)} {carga.unidade}</span>
            </div>
        </div>
    </div>
  );
}

// 2. Circuito Droppable (Alvo)
function DroppableCircuito({ children, circuitoId }: { children: React.ReactNode, circuitoId: string }) {
  const { setNodeRef, isOver } = useDroppable({
    id: circuitoId,
  });

  return (
    <Card 
      ref={setNodeRef} 
      className={`flex flex-col transition-all ${isOver ? 'ring-2 ring-primary bg-primary/5 scale-[1.01]' : ''}`}
    >
      {children}
    </Card>
  );
}

// --- COMPONENTE PRINCIPAL ---

interface CircuitosTabProps {
  circuitos: Circuito[]
  cargas: Carga[]
  zonas: Zona[]
  onNewCircuito: () => void
  onEditCircuito: (c: Circuito) => void
  onDeleteCircuito: (id: string) => void
  onAssignCargas: (circuitoId: string, cargasIds: string[]) => void
  onUnassignCarga: (cargaId: string) => void
}

export function CircuitosTab({ 
    circuitos, cargas, zonas,
    onNewCircuito, onEditCircuito, onDeleteCircuito,
    onAssignCargas, onUnassignCarga
}: CircuitosTabProps) {
  
  const [selectedCargas, setSelectedCargas] = useState<string[]>([])
  const cargasSoltas = cargas.filter(c => !c.circuito_id)
  
  const handleToggleSelect = (id: string) => {
    if (selectedCargas.includes(id)) {
        setSelectedCargas(prev => prev.filter(c => c !== id))
    } else {
        setSelectedCargas(prev => [...prev, id])
    }
  }

  const handleAssignTo = (circuitoId: string) => {
    if (selectedCargas.length === 0) {
        toast.error("Selecione pelo menos uma carga da lista à esquerda ou arraste uma carga.")
        return
    }
    onAssignCargas(circuitoId, selectedCargas)
    setSelectedCargas([])
    toast.success(`${selectedCargas.length} cargas movidas.`)
  }

  const getZonaInfo = (id: string) => zonas.find(z => z.id === id)

  // PONTO 3 RESOLVIDO: Lógica de soma segura
  const getCircuitTotals = (circuitoId: string) => {
    const cargasDoCircuito = cargas.filter(c => c.circuito_id === circuitoId)
    const potTotal = cargasDoCircuito.reduce((acc, c) => acc + Number(c.potencia || 0), 0)
    return { count: cargasDoCircuito.length, potTotal }
  }

  return (
    <div className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-200px)]">
      
      {/* COLUNA ESQUERDA: Cargas Soltas */}
      <div className="lg:col-span-4 flex flex-col gap-4 h-full">
        <div className="flex justify-between items-center">
            <h3 className="font-medium flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-orange-500" />
                Cargas sem Circuito ({cargasSoltas.length})
            </h3>
            <span className="text-xs text-muted-foreground">Arraste ou Selecione</span>
        </div>
        
        <Card className="flex-1 overflow-hidden border-dashed bg-muted/20">
            <ScrollArea className="h-full p-4">
                {cargasSoltas.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-40 text-muted-foreground text-sm">
                        <Zap className="h-8 w-8 mb-2 opacity-20" />
                        Tudo organizado!
                    </div>
                ) : (
                    <div className="space-y-2">
                        {cargasSoltas.map(carga => (
                            <DraggableCarga 
                                key={carga.id} 
                                carga={carga} 
                                isSelected={selectedCargas.includes(carga.id)}
                                onToggle={handleToggleSelect}
                            />
                        ))}
                    </div>
                )}
            </ScrollArea>
        </Card>
      </div>

      {/* COLUNA DIREITA: Circuitos (Droppables) */}
      <div className="lg:col-span-8 flex flex-col gap-4 h-full">
         <div className="flex justify-between items-center">
            <h3 className="font-medium">Quadro de Circuitos</h3>
            <Button onClick={onNewCircuito}><Plus className="mr-2 h-4 w-4" /> Novo Circuito</Button>
         </div>

         <ScrollArea className="flex-1 pr-4">
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-2">
                {circuitos.length === 0 && (
                     <div className="col-span-2 flex flex-col items-center justify-center h-40 border rounded-lg bg-muted/10 text-muted-foreground">
                        <p>Nenhum circuito criado.</p>
                        <Button variant="link" onClick={onNewCircuito}>Criar o primeiro</Button>
                     </div>
                )}

                {circuitos.map(circuito => {
                    const stats = getCircuitTotals(circuito.id)
                    const zona = getZonaInfo(circuito.zona_id)
                    const cargasDoCircuito = cargas.filter(c => c.circuito_id === circuito.id)

                    return (
                        <DroppableCircuito key={circuito.id} circuitoId={circuito.id}>
                            <CardHeader className="pb-2 bg-muted/30 rounded-t-lg">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <CardTitle className="text-base flex items-center gap-2">
                                            {circuito.identificador}
                                            <Badge variant="outline" className="text-xs font-normal">{circuito.tipo_circuito}</Badge>
                                        </CardTitle>
                                        <div className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                                            <div className={`w-2 h-2 rounded-full ${!zona ? 'bg-red-500 animate-pulse' : ''}`} style={{background: zona?.cor_identificacao || '#ccc'}} />
                                            {zona?.nome || <span className="text-red-500 font-bold">Zona Inválida</span>}
                                        </div>
                                    </div>
                                    <div className="flex gap-1">
                                        <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => onEditCircuito(circuito)}>
                                            <Settings className="h-3.5 w-3.5" />
                                        </Button>
                                        <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => onDeleteCircuito(circuito.id)}>
                                            <Trash2 className="h-3.5 w-3.5" />
                                        </Button>
                                    </div>
                                </div>
                            </CardHeader>
                            
                            <CardContent className="flex-1 py-3">
                                <div className="grid grid-cols-2 gap-2 mb-3 text-xs">
                                    <div className="bg-background p-1.5 rounded border text-center">
                                        <div className="font-bold">{stats.count}</div>
                                        <div className="text-muted-foreground">Cargas</div>
                                    </div>
                                    <div className="bg-background p-1.5 rounded border text-center">
                                        {/* Display Seguro */}
                                        <div className="font-bold">~{stats.potTotal}</div>
                                        <div className="text-muted-foreground">VA/W</div>
                                    </div>
                                </div>

                                <div className="space-y-1">
                                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Cargas Associadas</p>
                                    {cargasDoCircuito.length === 0 ? (
                                        <div className="text-xs italic text-muted-foreground py-2 text-center border border-dashed rounded">
                                            Arraste cargas aqui
                                        </div>
                                    ) : (
                                        <div className="flex flex-wrap gap-1">
                                            {cargasDoCircuito.slice(0, 8).map(c => (
                                                <Badge key={c.id} variant="secondary" className="text-[10px] px-1 h-5 flex gap-1 cursor-default group hover:bg-destructive/10">
                                                    {c.nome}
                                                    <span className="cursor-pointer text-muted-foreground hover:text-destructive" onClick={() => onUnassignCarga(c.id)}>×</span>
                                                </Badge>
                                            ))}
                                            {cargasDoCircuito.length > 8 && <Badge variant="outline" className="text-[10px] h-5">+{cargasDoCircuito.length - 8}</Badge>}
                                        </div>
                                    )}
                                </div>
                            </CardContent>

                            <CardFooter className="pt-2 pb-3 border-t bg-muted/10 rounded-b-lg">
                                <Button 
                                    className="w-full h-8 text-xs" 
                                    variant={selectedCargas.length > 0 ? "default" : "secondary"}
                                    disabled={selectedCargas.length === 0}
                                    onClick={() => handleAssignTo(circuito.id)}
                                >
                                    <ArrowRight className="mr-2 h-3 w-3" />
                                    {selectedCargas.length > 0 ? `Mover Selecionadas (${selectedCargas.length})` : "Selecione cargas"}
                                </Button>
                            </CardFooter>
                        </DroppableCircuito>
                    )
                })}
            </div>
         </ScrollArea>
      </div>
    </div>
  )
}