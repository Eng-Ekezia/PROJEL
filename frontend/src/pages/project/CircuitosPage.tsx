import { useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { Trash2, AlertCircle, Zap, Activity } from "lucide-react"

// UI Components
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
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

import { useProjectStore } from "@/store/useProjectStore"
import type { Circuito, Zona, Carga } from "@/types/project"

// --- COMPONENTE DE TABELA (O Coração da Página) ---
function CircuitosTable({ 
    circuitos, 
    zonas,
    todasCargas,
    onUpdate, 
    onDelete 
}: { 
  circuitos: Circuito[], 
  zonas: Zona[],
  todasCargas: Carga[],
  onUpdate: (circuito: Circuito) => void,
  onDelete: (id: string) => void
}) {
  if (circuitos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 border rounded-lg bg-muted/10 text-muted-foreground">
        <Zap className="h-10 w-10 mb-2 opacity-20" />
        <p>Nenhum circuito formalizado.</p>
        <p className="text-sm">Vá para a aba "Rascunhos (Propostas)" para criar seus circuitos.</p>
      </div>
    )
  }

  return (
    <div className="border rounded-md overflow-hidden bg-card shadow-sm">
      <div className="overflow-x-auto">
        <Table className="min-w-[1200px]">
          <TableHeader className="bg-muted/50">
            <TableRow>
              <TableHead className="w-[120px] font-bold">Identificador</TableHead>
              <TableHead className="w-[150px]">Zona Gov.</TableHead>
              <TableHead className="w-[130px]">Tipo</TableHead>
              <TableHead className="w-[120px]">Cargas / Pot.</TableHead> {/* Read-only info */}
              <TableHead className="w-[180px]">Método Inst.</TableHead>
              <TableHead className="w-[80px]">Tens.(V)</TableHead>
              <TableHead className="w-[90px]">Comp.(m)</TableHead>
              <TableHead className="w-[90px]">Temp.(°C)</TableHead>
              <TableHead className="w-[80px]">Agrup.</TableHead>
              <TableHead className="text-right w-[60px]">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {circuitos.map((circuito) => {
              // Calcula dados em tempo real das cargas herdadas
              const cargasDoCircuito = todasCargas.filter(c => circuito.cargas_ids?.includes(c.id))
              const potenciaTotal = cargasDoCircuito.reduce((acc, c) => acc + c.potencia, 0)

              return (
                <TableRow key={circuito.id} className="group">
                  {/* IDENTIFICADOR */}
                  <TableCell>
                    <Input 
                      defaultValue={circuito.identificador} 
                      className="h-8 px-2 font-bold focus-visible:ring-primary"
                      onBlur={(e) => {
                        const val = e.target.value.trim().toUpperCase()
                        if (val && val !== circuito.identificador) {
                          onUpdate({ ...circuito, identificador: val })
                        }
                      }}
                    />
                  </TableCell>

                  {/* ZONA */}
                  <TableCell>
                    <Select 
                      value={circuito.zona_id} 
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
                      value={circuito.tipo_circuito} 
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

                  {/* INFO DAS CARGAS (Read-Only) */}
                  <TableCell>
                    <div className="flex flex-col gap-0.5">
                      <span className="text-xs font-medium">{cargasDoCircuito.length} itens</span>
                      <Badge variant="outline" className="w-fit text-[10px] px-1 h-4">{potenciaTotal} VA</Badge>
                    </div>
                  </TableCell>

                  {/* MÉTODO */}
                  <TableCell>
                    <Select 
                      value={circuito.metodo_instalacao}
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
                        if (val > 0 && val !== circuito.tensao_nominal) onUpdate({ ...circuito, tensao_nominal: val })
                      }}
                    />
                  </TableCell>

                  {/* COMPRIMENTO */}
                  <TableCell>
                    <Input 
                      type="number"
                      placeholder="0"
                      defaultValue={circuito.comprimento_m || 0}
                      className="h-8 px-2"
                      onBlur={(e) => {
                        const val = Number(e.target.value)
                        if (val >= 0 && val !== circuito.comprimento_m) onUpdate({ ...circuito, comprimento_m: val })
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
                        if (val > 0 && val !== circuito.temperatura_ambiente) onUpdate({ ...circuito, temperatura_ambiente: val })
                      }}
                    />
                  </TableCell>

                  {/* AGRUPAMENTO */}
                  <TableCell>
                    <Input 
                          type="number"
                          min={1}
                          defaultValue={circuito.circuitos_agrupados}
                          className="h-8 px-2"
                          onBlur={(e) => {
                            const val = Number(e.target.value)
                            if (val > 0 && val !== circuito.circuitos_agrupados) {
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
                      className="h-8 w-8 text-destructive/70 hover:text-destructive hover:bg-destructive/10"
                      onClick={() => onDelete(circuito.id)}
                      title="Desfazer circuito e liberar cargas"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              )
            })}
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
    updateCircuitoInProject,
    removeCircuitoFromProject
  } = useProjectStore()

  const project = projects.find((p) => p.id === id)

  const [deleteTargetId, setDeleteTargetId] = useState<string | null>(null)

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  const circuitos = project.circuitos || []

  // --- HANDLERS ---
  const handleTableUpdate = (updatedCircuito: Circuito) => {
      // Validação rápida de unicidade
      const duplicado = circuitos.some(c => 
          c.id !== updatedCircuito.id && 
          c.identificador === updatedCircuito.identificador
      )
      
      if (duplicado) {
          toast.error(`O identificador "${updatedCircuito.identificador}" já existe.`)
          return
      }

      updateCircuitoInProject(project.id, updatedCircuito)
      toast.success("Parâmetro atualizado e salvo.", { duration: 1500 })
  }

  const handleDeleteRequest = (id: string) => setDeleteTargetId(id)
  
  const confirmDelete = () => {
      if (deleteTargetId) {
          removeCircuitoFromProject(project.id, deleteTargetId)
          toast.success("Circuito excluído. Suas cargas voltaram para os Rascunhos.")
          setDeleteTargetId(null)
      }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] gap-4">
      
      {/* HEADER */}
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
              <Activity className="h-6 w-6 text-primary" />
              Quadros e Circuitos (Definitivos)
          </h2>
          <p className="text-muted-foreground">
              Ajuste fino de parâmetros elétricos e de instalação para o dimensionamento.
          </p>
        </div>
      </div>

      {/* TABLE VIEW */}
      <div className="flex-1 overflow-auto animate-in fade-in duration-300 flex flex-col gap-4">
        
        <div className="flex items-center gap-2 text-sm text-muted-foreground bg-blue-50/50 p-3 rounded-lg border border-blue-100 dark:bg-blue-900/10 dark:border-blue-800 shrink-0">
            <AlertCircle className="h-5 w-5 text-blue-500 shrink-0" />
            <p>
                <strong>Modo Planilha Ativo:</strong> As edições nos parâmetros elétricos são salvas automaticamente ao sair do campo. Para agrupar ou desagrupar cargas, utilize a área de <em>Rascunhos</em>.
            </p>
        </div>
        
        <CircuitosTable 
            circuitos={circuitos} 
            zonas={project.zonas} 
            todasCargas={project.cargas}
            onUpdate={handleTableUpdate}
            onDelete={handleDeleteRequest}
        />
      </div>

      {/* DIALOG DELETE ALERT */}
      <AlertDialog open={!!deleteTargetId} onOpenChange={(open) => !open && setDeleteTargetId(null)}>
          <AlertDialogContent>
              <AlertDialogHeader>
                  <AlertDialogTitle>Desfazer Circuito Definitivo?</AlertDialogTitle>
                  <AlertDialogDescription>
                      Tem certeza? O agrupamento será desfeito e todas as cargas vinculadas a este circuito voltarão imediatamente para a lista de "Cargas Livres" nos Rascunhos. Esta ação não pode ser desfeita.
                  </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                  <AlertDialogCancel>Cancelar</AlertDialogCancel>
                  <AlertDialogAction onClick={confirmDelete} className="bg-destructive hover:bg-destructive/90 text-destructive-foreground">
                      Sim, desfazer circuito
                  </AlertDialogAction>
              </AlertDialogFooter>
          </AlertDialogContent>
      </AlertDialog>

    </div>
  )
}