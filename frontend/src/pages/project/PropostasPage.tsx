import { useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { 
  CheckSquare, Square, AlertTriangle, Zap, CheckCircle2, Save, ListChecks, Info
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { useProjectStore } from "@/store/useProjectStore"
import type { PropostaCircuito } from "@/types/project"

export default function PropostasPage() {
  const { id } = useParams<{ id: string }>()
  const { projects, addPropostaToProject, aceitarProposta } = useProjectStore()

  const project = projects.find((p) => p.id === id)

  // --- STATES ---
  const [selectedCargaIds, setSelectedCargaIds] = useState<string[]>([])
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [analiseResult, setAnaliseResult] = useState<any>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [descricaoIntencao, setDescricaoIntencao] = useState("")

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  const cargasDisponiveis = project.cargas.filter(c => !c.circuito_id)
  const propostas = project.propostas || []

  // --- HANDLERS ---
  const toggleCargaSelection = (cargaId: string) => {
    setSelectedCargaIds(prev => 
      prev.includes(cargaId) ? prev.filter(ident => ident !== cargaId) : [...prev, cargaId]
    )
    setAnaliseResult(null) 
  }

  const handleAnalisarAgrupamento = async () => {
    if (selectedCargaIds.length === 0) {
      toast.error("Selecione pelo menos uma carga para analisar.")
      return
    }

    setIsAnalyzing(true)
    try {
      const payload = {
        cargas_selecionadas: project.cargas.filter(c => selectedCargaIds.includes(c.id)),
        zonas_do_projeto: project.zonas
      }

      const response = await fetch('http://localhost:8000/api/v1/propostas/analisar-rascunho', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) throw new Error("Erro na análise do backend")
      
      const data = await response.json()
      setAnaliseResult(data)
      toast.success("Análise concluída.")
    } catch (error) {
      console.error(error)
      toast.error("Falha ao comunicar com o motor de cálculo.")
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleSalvarProposta = () => {
    if (!analiseResult || !analiseResult.is_valida) return
    if (!descricaoIntencao.trim()) {
      toast.error("Forneça uma descrição/intenção para este rascunho.")
      return
    }

    const novaProposta: PropostaCircuito = {
      id: crypto.randomUUID(),
      data_criacao: new Date().toISOString(),
      status: 'rascunho',
      cargas_ids: selectedCargaIds,
      locais_ids: analiseResult.locais_envolvidos_ids,
      zonas_ids: analiseResult.zonas_envolvidas_ids,
      descricao_intencao: descricaoIntencao,
      observacoes_normativas: analiseResult.alertas_normativos.join(" | "),
      autor: "Usuário Atual" 
    }

    addPropostaToProject(project.id, novaProposta)
    toast.success("Proposta guardada com sucesso!")
    
    setSelectedCargaIds([])
    setAnaliseResult(null)
    setDescricaoIntencao("")
  }

  const handleAceitarProposta = (propostaId: string) => {
    aceitarProposta(project.id, propostaId)
    toast.success("Proposta Aceite! Pronta para virar Circuito.")
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] gap-4">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Área de Rascunho (Propostas)</h2>
          <p className="text-muted-foreground">
            Selecione as cargas, analise os impactos normativos e consolide suas intenções.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1 min-h-0">
        
        <Card className="flex flex-col">
          <CardHeader className="pb-3 shrink-0">
            <CardTitle className="text-lg flex items-center gap-2">
              <ListChecks className="w-5 h-5" /> Cargas Disponíveis
            </CardTitle>
            <CardDescription>Cargas que ainda não possuem circuito definitivo.</CardDescription>
          </CardHeader>
          <CardContent className="flex-1 overflow-auto">
            {cargasDisponiveis.length === 0 ? (
              <p className="text-sm text-muted-foreground italic">Todas as cargas já estão em circuitos ou o projeto não possui cargas.</p>
            ) : (
              <div className="space-y-2">
                {cargasDisponiveis.map(carga => {
                  const isSelected = selectedCargaIds.includes(carga.id)
                  const local = project.locais.find(l => l.id === carga.local_id)
                  return (
                    <div 
                      key={carga.id} 
                      className={`flex items-center justify-between p-3 border rounded-md cursor-pointer transition-colors ${isSelected ? 'bg-primary/5 border-primary/30' : 'hover:bg-muted/50'}`}
                      onClick={() => toggleCargaSelection(carga.id)}
                    >
                      <div className="flex items-center gap-3">
                        {isSelected ? <CheckSquare className="w-5 h-5 text-primary" /> : <Square className="w-5 h-5 text-muted-foreground" />}
                        <div>
                          <p className="font-medium text-sm">{carga.nome}</p>
                          <p className="text-xs text-muted-foreground">{local?.nome} • {carga.tipo}</p>
                        </div>
                      </div>
                      <Badge variant="outline">{carga.potencia} {carga.unidade}</Badge>
                    </div>
                  )
                })}
              </div>
            )}
          </CardContent>
          <CardFooter className="pt-3 border-t">
            <Button 
              className="w-full" 
              onClick={handleAnalisarAgrupamento} 
              disabled={selectedCargaIds.length === 0 || isAnalyzing}
            >
              {isAnalyzing ? "Analisando..." : "1. Analisar Agrupamento"}
            </Button>
          </CardFooter>
        </Card>

        <div className="flex flex-col gap-4 overflow-hidden">
          <Card className={`shrink-0 transition-all ${analiseResult ? 'border-primary' : ''}`}>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center gap-2">
                <Zap className="w-5 h-5" /> Impacto do Agrupamento
              </CardTitle>
              {!analiseResult && <CardDescription>Aguardando análise...</CardDescription>}
            </CardHeader>
            {analiseResult && (
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 p-4 bg-muted/30 rounded-lg">
                  <div>
                    <p className="text-xs text-muted-foreground uppercase font-semibold">Locais Envolvidos</p>
                    <p className="text-lg font-medium">{analiseResult.locais_envolvidos_ids.length}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground uppercase font-semibold">Potência Total</p>
                    <p className="text-lg font-medium text-primary">{analiseResult.potencia_total_va} VA</p>
                  </div>
                </div>

                {analiseResult.alertas_normativos.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm font-semibold flex items-center gap-2 text-yellow-600">
                      <AlertTriangle className="w-4 h-4" /> Alertas da NBR 5410
                    </p>
                    <ul className="text-sm space-y-2 text-muted-foreground bg-yellow-500/10 p-3 rounded-md border border-yellow-500/20">
                      {analiseResult.alertas_normativos.map((alerta: string, idx: number) => (
                        <li key={idx} className="flex gap-2">
                          <span className="shrink-0 mt-0.5">•</span>
                          <span>{alerta}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="space-y-3 pt-2">
                  <Label>Qual a intenção deste agrupamento? (Obrigatório)</Label>
                  <Textarea 
                    placeholder="Ex: Circuito para atender iluminação geral da área social..." 
                    value={descricaoIntencao}
                    onChange={(e) => setDescricaoIntencao(e.target.value)}
                  />
                  <Button className="w-full gap-2" onClick={handleSalvarProposta}>
                    <Save className="w-4 h-4" /> 2. Guardar como Rascunho
                  </Button>
                </div>
              </CardContent>
            )}
          </Card>

          <Card className="flex-1 flex flex-col min-h-0">
            <CardHeader className="pb-3 shrink-0 border-b">
              <CardTitle className="text-lg">Propostas Guardadas</CardTitle>
            </CardHeader>
            <ScrollArea className="flex-1 p-4">
              {propostas.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-muted-foreground opacity-50 py-8">
                  <Info className="w-8 h-8 mb-2" />
                  <p>Nenhuma proposta registada.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {propostas.map(prop => (
                    <div key={prop.id} className="p-4 border rounded-lg bg-card shadow-sm space-y-3">
                      <div className="flex justify-between items-start">
                        <div>
                          <Badge variant={prop.status === 'aceita' ? 'default' : 'secondary'} className="mb-2">
                            {prop.status.toUpperCase()}
                          </Badge>
                          <p className="font-medium text-sm">{prop.descricao_intencao}</p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {prop.cargas_ids.length} Cargas agrupadas
                          </p>
                        </div>
                        {prop.status === 'rascunho' && (
                          <Button size="sm" variant="outline" onClick={() => handleAceitarProposta(prop.id)}>
                            <CheckCircle2 className="w-4 h-4 mr-2 text-green-600" /> Aceitar
                          </Button>
                        )}
                      </div>
                      {prop.observacoes_normativas && (
                        <p className="text-xs text-yellow-600/80 bg-yellow-500/5 p-2 rounded border border-yellow-500/10">
                          {prop.observacoes_normativas}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </Card>
          
        </div>
      </div>
    </div>
  )
}