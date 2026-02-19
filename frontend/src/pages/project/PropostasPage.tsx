import { useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { 
  CheckSquare, Square, AlertTriangle, ListChecks, GripVertical, 
  ArrowDownToLine, Zap, Plus, Trash2, CheckCircle2, Wand2, MapPin
} from "lucide-react"

// DnD Kit
import { 
  DndContext, DragOverlay, useDraggable, useDroppable, 
  type DragEndEvent, type DragStartEvent, useSensor, useSensors, PointerSensor 
} from '@dnd-kit/core'

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"

import { useProjectStore } from "@/store/useProjectStore"
import type { Carga, PropostaCircuito } from "@/types/project"
import { CircuitDialog } from "@/components/project/dialogs/CircuitDialog"

interface PreCircuito {
  id: string;
  nome: string;
  cargas_ids: string[];
  justificativa_sugestao?: string; 
}

function DraggableCarga({ carga, localNome, zonaNome, zonaCor, isSelected, onToggleSelect }: { carga: Carga, localNome: string, zonaNome: string, zonaCor?: string, isSelected: boolean, onToggleSelect: (id: string) => void }) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({ id: carga.id, data: { carga } })

  return (
    <div 
      ref={setNodeRef} 
      className={`group flex items-center justify-between p-2 mb-2 border rounded-md transition-all bg-card shadow-sm
        ${isDragging ? 'opacity-30 grayscale' : ''} 
        ${isSelected ? 'border-primary bg-primary/5 ring-1 ring-primary/20' : 'hover:border-primary/50'}`}
    >
      <div className="flex items-center gap-2 overflow-hidden flex-1 pr-2">
        <div {...listeners} {...attributes} className="cursor-grab active:cursor-grabbing p-1 text-muted-foreground hover:text-foreground shrink-0">
          <GripVertical className="h-4 w-4" />
        </div>
        <div className="cursor-pointer flex items-start gap-2 w-full overflow-hidden" onClick={() => onToggleSelect(carga.id)}>
          {isSelected ? <CheckSquare className="w-4 h-4 text-primary mt-0.5 shrink-0" /> : <Square className="w-4 h-4 text-muted-foreground mt-0.5 shrink-0" />}
          <div className="flex flex-col min-w-0 w-full">
            <p className="font-medium text-sm leading-tight truncate">{carga.nome}</p>
            <div className="flex flex-wrap gap-1 mt-1.5">
               <Badge variant="secondary" className="text-[9px] px-1 py-0 h-4 font-medium flex items-center gap-0.5 rounded-sm bg-muted/60 text-muted-foreground">
                  <MapPin className="w-2.5 h-2.5"/>
                  <span className="truncate max-w-[100px]">{localNome}</span>
               </Badge>
               {zonaNome !== 'Zona N/A' && (
                 <Badge 
                    variant="outline" 
                    className="text-[9px] px-1 py-0 h-4 font-semibold rounded-sm bg-background/50" 
                    style={{ borderColor: zonaCor || 'inherit', color: zonaCor || 'inherit' }}
                 >
                    <span className="truncate max-w-[100px]">{zonaNome}</span>
                 </Badge>
               )}
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-col items-end gap-1 shrink-0 ml-2">
        <Badge variant="outline">{carga.potencia} {carga.unidade}</Badge>
        <span className="text-[9px] font-mono text-muted-foreground">{carga.tipo}</span>
      </div>
    </div>
  )
}

function DroppableContainer({ id, children, isOver, isSelectionMode, onDropSelected, className }: { id: string, children: React.ReactNode, isOver: boolean, isSelectionMode: boolean, onDropSelected: () => void, className?: string }) {
  const { setNodeRef } = useDroppable({ id })
  const activeStyle = isOver ? "border-primary bg-primary/5" : "border-border hover:border-primary/30"

  return (
    <div ref={setNodeRef} className={`relative transition-colors duration-200 ease-in-out ${activeStyle} ${className}`}>
      {isSelectionMode && (
        <div 
          onClick={onDropSelected}
          className="absolute inset-0 bg-background/90 z-20 flex flex-col items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-200 rounded-lg cursor-pointer border-2 border-primary"
        >
          <ArrowDownToLine className="h-8 w-8 text-primary mb-2 animate-bounce" />
          <span className="font-bold text-primary">Mover Selecionadas para cá</span>
        </div>
      )}
      {children}
    </div>
  )
}

function validarPropostaLocal(cargas: Carga[]): { alertas: string[], ok: boolean } {
  if (cargas.length === 0) return { alertas: [], ok: true }
  const alertas: string[] = []
  
  const temTUE = cargas.some(c => ['TUE', 'MOTOR'].includes(c.tipo?.toUpperCase()))
  if (temTUE && cargas.length > 1) {
    alertas.push("Atenção: Equipamentos de Uso Específico (TUE/Motor) geralmente exigem circuitos independentes.")
  }
  
  const zonasIds = new Set(cargas.map(c => c.zona_id).filter(Boolean))
  if (zonasIds.size > 1) {
    alertas.push("Zonas misturadas detetadas. O circuito herdará a zona de pior condição.")
  }

  return { alertas, ok: alertas.length === 0 }
}

export default function PropostasPage() {
  const { id } = useParams<{ id: string }>()
  const { projects, addPropostaToProject } = useProjectStore()

  const project = projects.find((p) => p.id === id)

  const [selectedCargaIds, setSelectedCargaIds] = useState<string[]>([])
  const [preCircuitos, setPreCircuitos] = useState<PreCircuito[]>([])
  const [activeDragItem, setActiveDragItem] = useState<Carga | null>(null)
  const [activeDropId, setActiveDropId] = useState<string | null>(null)
  const [isAssistantLoading, setIsAssistantLoading] = useState(false)
  
  const [propostaParaConverter, setPropostaParaConverter] = useState<PropostaCircuito | null>(null)
  const [preCircuitoEmConversao, setPreCircuitoEmConversao] = useState<string | null>(null)

  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 8 } }))

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  // [CORREÇÃO AQUI]: A fonte da verdade agora verifica diretamente a coleção de circuitos do projeto
  const cargasEmCircuitosDefinitivos = project.circuitos?.flatMap(c => c.cargas_ids) || []
  const cargasEmPreCircuitos = preCircuitos.flatMap(pc => pc.cargas_ids)
  
  const cargasLivres = project.cargas.filter(c => 
      !cargasEmCircuitosDefinitivos.includes(c.id) && 
      !cargasEmPreCircuitos.includes(c.id)
  )

  const handleDragStart = (e: DragStartEvent) => {
    if (e.active.data.current) setActiveDragItem(e.active.data.current.carga as Carga)
  }

  const handleDragOver = (e: DragEndEvent) => {
      setActiveDropId(e.over ? String(e.over.id) : null)
  }

  const handleDragEnd = (e: DragEndEvent) => {
    const { active, over } = e
    setActiveDragItem(null)
    setActiveDropId(null)
    if (!over) return

    const cargaId = active.id as string
    const targetId = over.id as string

    setPreCircuitos(prev => prev.map(pc => ({
        ...pc, cargas_ids: pc.cargas_ids.filter(id => id !== cargaId)
    })))

    if (targetId !== 'pool') {
        setPreCircuitos(prev => prev.map(pc => 
            pc.id === targetId ? { ...pc, cargas_ids: [...pc.cargas_ids, cargaId] } : pc
        ))
    }
  }

  const moverSelecionadasPara = (targetId: string) => {
    if (selectedCargaIds.length === 0) return

    setPreCircuitos(prev => prev.map(pc => ({
        ...pc, cargas_ids: pc.cargas_ids.filter(id => !selectedCargaIds.includes(id))
    })))

    if (targetId !== 'pool') {
        setPreCircuitos(prev => prev.map(pc => 
            pc.id === targetId ? { ...pc, cargas_ids: [...pc.cargas_ids, ...selectedCargaIds] } : pc
        ))
    }
    
    toast.success(`${selectedCargaIds.length} cargas movidas.`)
    setSelectedCargaIds([])
  }

  const adicionarPreCircuito = () => {
      setPreCircuitos(prev => [
          ...prev, 
          { id: crypto.randomUUID(), nome: `Pré-Circuito ${prev.length + 1}`, cargas_ids: [] }
      ])
  }

  const deletarPreCircuito = (id: string) => {
      setPreCircuitos(prev => prev.filter(pc => pc.id !== id))
      toast.success("Pré-circuito removido. Cargas voltaram para a lista.")
  }

  const atualizarNomePreCircuito = (id: string, novoNome: string) => {
      setPreCircuitos(prev => prev.map(pc => pc.id === id ? { ...pc, nome: novoNome } : pc))
  }

  const simularAssistente = () => {
    if (cargasLivres.length === 0) {
      toast.error("Não há cargas livres para o Assistente analisar.")
      return
    }
    setIsAssistantLoading(true)
    setTimeout(() => {
      const novasSugestoes: PreCircuito[] = []
      
      const tues = cargasLivres.filter(c => ['TUE', 'MOTOR'].includes(c.tipo?.toUpperCase()))
      tues.forEach((tue) => {
        novasSugestoes.push({
          id: crypto.randomUUID(),
          nome: `Circuito Específico - ${tue.nome}`,
          cargas_ids: [tue.id],
          justificativa_sugestao: `NBR 5410 exige circuito exclusivo para equipamentos de uso específico.`
        })
      })

      const iluminacao = cargasLivres.filter(c => c.tipo?.toUpperCase() === 'ILUMINACAO')
      if (iluminacao.length > 0) {
        novasSugestoes.push({
          id: crypto.randomUUID(),
          nome: `Iluminação Geral`,
          cargas_ids: iluminacao.map(i => i.id),
          justificativa_sugestao: `Recomendação: Agrupar pontos de iluminação separados das tomadas.`
        })
      }

      if (novasSugestoes.length === 0) {
        toast.info("Nenhum padrão óbvio encontrado. Agrupe as tomadas manualmente.")
      } else {
        setPreCircuitos(prev => [...novasSugestoes, ...prev])
        toast.success(`${novasSugestoes.length} agrupamentos sugeridos!`)
      }
      
      setIsAssistantLoading(false)
    }, 800)
  }

  const handlePrepararConversao = (pc: PreCircuito) => {
    if (pc.cargas_ids.length === 0) {
        toast.error("O pré-circuito está vazio.")
        return
    }

    const cargasDoPc = project.cargas.filter(c => pc.cargas_ids.includes(c.id))
    const validacao = validarPropostaLocal(cargasDoPc)
    const observacoes = [pc.justificativa_sugestao, ...validacao.alertas].filter(Boolean).join(" | ")

    const novaProposta: PropostaCircuito = {
      id: crypto.randomUUID(), 
      data_criacao: new Date().toISOString(),
      status: 'analisada',
      cargas_ids: pc.cargas_ids,
      locais_ids: [...new Set(cargasDoPc.map(c => c.local_id))],
      zonas_ids: [...new Set(cargasDoPc.map(c => c.zona_id).filter(Boolean) as string[])],
      descricao_intencao: pc.nome,
      observacoes_normativas: observacoes || "Agrupamento manual válido.",
      autor: pc.justificativa_sugestao ? "Assistente NBR5410" : "Projetista"
    }

    addPropostaToProject(project.id, novaProposta)
    setPropostaParaConverter(novaProposta)
    setPreCircuitoEmConversao(pc.id) 
  }

  const isSelectionActive = selectedCargaIds.length > 0;
  const isSelectionInPool = cargasLivres.some(c => selectedCargaIds.includes(c.id));

  return (
    <DndContext sensors={sensors} onDragStart={handleDragStart} onDragOver={handleDragOver} onDragEnd={handleDragEnd}>
      <div className="flex flex-col h-[calc(100vh-8rem)] gap-4">
        
        <div className="flex justify-between items-center shrink-0">
          <div>
            <h2 className="text-2xl font-bold tracking-tight">Rascunhos (Pré-Circuitos)</h2>
            <p className="text-muted-foreground">Arraste as cargas ou use o assistente normativo para organizar ideias.</p>
          </div>
          <div className="flex gap-3">
            <Button 
              onClick={simularAssistente} 
              variant="secondary" 
              className="gap-2 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border-indigo-200 dark:bg-indigo-900/30 dark:text-indigo-300 dark:border-indigo-800"
              disabled={isAssistantLoading || cargasLivres.length === 0}
            >
                <Wand2 className={`w-4 h-4 ${isAssistantLoading ? 'animate-spin' : ''}`} /> 
                {isAssistantLoading ? 'Analisando...' : 'Assistente NBR 5410'}
            </Button>
            <Button onClick={adicionarPreCircuito} variant="outline" className="gap-2">
                <Plus className="w-4 h-4" /> Novo Pré-Circuito
            </Button>
          </div>
        </div>

        <div className="flex gap-6 flex-1 min-h-0">
          
          <Card className="w-1/3 min-w-[320px] flex flex-col shrink-0">
            <CardHeader className="pb-3 shrink-0">
              <CardTitle className="text-lg flex items-center justify-between">
                <div className="flex items-center gap-2"><ListChecks className="w-5 h-5" /> Cargas Livres</div>
                <Badge variant="secondary">{cargasLivres.length}</Badge>
              </CardTitle>
            </CardHeader>
            <DroppableContainer 
                id="pool" 
                isOver={activeDropId === 'pool'} 
                isSelectionMode={isSelectionActive && !isSelectionInPool} 
                onDropSelected={() => moverSelecionadasPara('pool')}
                className="flex-1 m-3 rounded-md border-2 border-dashed overflow-hidden bg-muted/5"
            >
                <ScrollArea className="h-full p-3">
                {cargasLivres.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full opacity-50 space-y-2 mt-10">
                        <CheckCircle2 className="w-8 h-8 text-muted-foreground" />
                        <p className="text-sm text-center text-muted-foreground italic">Todas as cargas foram agrupadas.</p>
                    </div>
                ) : (
                    <div className="space-y-1">
                    {cargasLivres.map(carga => {
                        const local = project.locais.find(l => l.id === carga.local_id)
                        const zona = project.zonas.find(z => z.id === carga.zona_id)
                        return (
                            <DraggableCarga 
                                key={carga.id} 
                                carga={carga} 
                                localNome={local?.nome || 'Local N/A'}
                                zonaNome={zona?.nome || 'Zona N/A'}
                                zonaCor={zona?.cor_identificacao}
                                isSelected={selectedCargaIds.includes(carga.id)}
                                onToggleSelect={(id) => setSelectedCargaIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id])}
                            />
                        )
                    })}
                    </div>
                )}
                </ScrollArea>
            </DroppableContainer>
          </Card>

          <ScrollArea className="flex-1 bg-muted/5 rounded-lg border p-4">
              {preCircuitos.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-muted-foreground opacity-60">
                    <p className="mb-2">Nenhum pré-circuito criado.</p>
                    <p className="text-sm">Clique em "Novo Pré-Circuito" ou use o "Assistente NBR 5410".</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                    {preCircuitos.map(pc => {
                        const cargasDoPc = project.cargas.filter(c => pc.cargas_ids.includes(c.id))
                        const potenciaTotal = cargasDoPc.reduce((acc, c) => acc + c.potencia, 0)
                        const validacao = validarPropostaLocal(cargasDoPc)
                        const hasSelectionHere = pc.cargas_ids.some(id => selectedCargaIds.includes(id));

                        return (
                            <DroppableContainer 
                                key={pc.id} 
                                id={pc.id} 
                                isOver={activeDropId === pc.id}
                                isSelectionMode={isSelectionActive && !hasSelectionHere}
                                onDropSelected={() => moverSelecionadasPara(pc.id)}
                                className={`bg-card border-2 rounded-xl shadow-sm flex flex-col min-h-[300px] ${pc.justificativa_sugestao ? 'border-indigo-200 shadow-indigo-100 dark:border-indigo-800 dark:shadow-none' : ''}`}
                            >
                                <div className="p-3 border-b bg-muted/30 flex items-center justify-between gap-2 rounded-t-xl">
                                    <div className="flex-1 flex flex-col gap-1">
                                      <Input 
                                        value={pc.nome} 
                                        onChange={(e) => atualizarNomePreCircuito(pc.id, e.target.value)}
                                        className="h-8 font-semibold bg-transparent border-transparent hover:border-border focus:bg-background"
                                      />
                                      {pc.justificativa_sugestao && (
                                          <span className="text-[10px] text-indigo-600 dark:text-indigo-400 px-3 flex items-center gap-1">
                                              <Wand2 className="w-3 h-3"/> Sugestão: {pc.justificativa_sugestao}
                                          </span>
                                      )}
                                    </div>
                                    <div className="flex items-center gap-2">
                                      <Badge variant="outline">{potenciaTotal} VA</Badge>
                                      <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => deletarPreCircuito(pc.id)}>
                                          <Trash2 className="h-4 w-4" />
                                      </Button>
                                    </div>
                                </div>
                                
                                <ScrollArea className="flex-1 p-3">
                                    {pc.cargas_ids.length === 0 ? (
                                        <div className="h-full flex items-center justify-center text-muted-foreground text-sm opacity-50 py-10">
                                            Arraste cargas para cá
                                        </div>
                                    ) : (
                                        <div className="space-y-1">
                                            {pc.cargas_ids.map(cId => {
                                                const carga = project.cargas.find(c => c.id === cId)
                                                if (!carga) return null
                                                const local = project.locais.find(l => l.id === carga.local_id)
                                                const zona = project.zonas.find(z => z.id === carga.zona_id)
                                                return (
                                                  <DraggableCarga 
                                                      key={carga.id} 
                                                      carga={carga} 
                                                      localNome={local?.nome || 'Local N/A'}
                                                      zonaNome={zona?.nome || 'Zona N/A'}
                                                      zonaCor={zona?.cor_identificacao}
                                                      isSelected={selectedCargaIds.includes(carga.id)}
                                                      onToggleSelect={(id) => setSelectedCargaIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id])}
                                                  />
                                                )
                                            })}
                                        </div>
                                    )}
                                </ScrollArea>

                                <div className="p-3 bg-muted/10 border-t rounded-b-xl flex flex-col gap-2">
                                    {validacao.ok && pc.cargas_ids.length > 0 && (
                                      <div className="text-[10px] font-semibold text-green-700 bg-green-500/10 p-1.5 rounded border border-green-500/20 flex items-center gap-1">
                                          <CheckCircle2 className="h-3 w-3" /> NBR 5410: Agrupamento aceitável
                                      </div>
                                    )}
                                    {!validacao.ok && (
                                      <div className="text-[10px] text-yellow-700 bg-yellow-500/10 p-2 rounded border border-yellow-500/20 leading-tight">
                                          <p className="font-bold flex items-center gap-1 mb-1"><AlertTriangle className="h-3 w-3"/> Alertas NBR</p>
                                          {validacao.alertas.map((a, i) => <p key={i}>• {a}</p>)}
                                      </div>
                                    )}

                                    <Button 
                                      className="w-full gap-2" 
                                      disabled={pc.cargas_ids.length === 0}
                                      onClick={() => handlePrepararConversao(pc)}
                                    >
                                        <Zap className="h-4 w-4" /> Converter em Circuito
                                    </Button>
                                </div>
                            </DroppableContainer>
                        )
                    })}
                </div>
              )}
          </ScrollArea>
        </div>

        <DragOverlay>
          {activeDragItem ? (
            <div className="opacity-90 w-[280px]">
              <Card className="p-2 shadow-xl border-primary bg-background flex items-center gap-3">
                <GripVertical className="h-4 w-4 text-primary" />
                <div className="flex flex-col">
                  <span className="font-bold text-sm truncate">{activeDragItem.nome}</span>
                  <span className="text-xs text-muted-foreground">{activeDragItem.potencia} {activeDragItem.unidade}</span>
                </div>
              </Card>
            </div>
          ) : null}
        </DragOverlay>

        <CircuitDialog 
          open={!!propostaParaConverter}
          onOpenChange={(open) => {
              if (!open) {
                  setPropostaParaConverter(null)
                  setPreCircuitoEmConversao(null)
              }
          }}
          zonas={project.zonas}
          propostaContext={propostaParaConverter}
          onSuccess={() => {
              if (preCircuitoEmConversao) deletarPreCircuito(preCircuitoEmConversao)
          }}
        />

      </div>
    </DndContext>
  )
}