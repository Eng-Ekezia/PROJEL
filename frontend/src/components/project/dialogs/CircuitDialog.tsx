import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { Loader2, AlertTriangle, Info, Zap, CheckCircle2 } from "lucide-react" 

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription
} from "@/components/ui/dialog"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"

import type { Circuito, Zona, PropostaCircuito } from "@/types/project"
import { useProjectStore } from "@/store/useProjectStore"

const API_URL = "http://localhost:8000/api/v1"; 

interface ApiOptions {
    tipos: { codigo: string, descricao: string }[]
    metodos_instalacao: { codigo: string, descricao: string }[]
}

export interface CircuitDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  zonas: Zona[]
  propostaContext?: PropostaCircuito | null
  onSuccess?: () => void
  
  data?: any
  setData?: any
  onSave?: any
  isEditing?: boolean
}

export function CircuitDialog({ 
    open, onOpenChange, zonas, propostaContext, isEditing, onSuccess 
}: CircuitDialogProps) {
  
  const { id: projectId } = useParams<{ id: string }>()
  const { converterPropostaEmCircuito, projects } = useProjectStore()
  const project = projects.find(p => p.id === projectId)

  const [options, setOptions] = useState<ApiOptions | null>(null)
  const [loading, setLoading] = useState(false)

  // [NOVO] Estado para rastrear os campos com erro de validação
  const [fieldErrors, setFieldErrors] = useState<{ identificador?: boolean; zona_id?: boolean }>({})

  const [formData, setFormData] = useState<Partial<Circuito>>({
      identificador: '',
      tipo_circuito: 'TUG',
      tensao_nominal: 220,
      circuitos_agrupados: 1,
      metodo_instalacao: 'B1',
      material_condutor: 'COBRE',
      isolacao: 'PVC',
      sobrescreve_influencias: false,
      zona_id: ''
  })

  useEffect(() => {
    if (open && !options) {
        setLoading(true)
        fetch(`${API_URL}/circuitos/opcoes`)
            .then(res => res.json())
            .then(data => {
                setOptions(data)
                setLoading(false)
            })
            .catch(err => {
                console.error("Erro ao buscar normas:", err)
                setLoading(false)
            })
    }
  }, [open])

  useEffect(() => {
    if (open && propostaContext) {
        const multiplasZonas = propostaContext.zonas_ids.length > 1;
        setFormData({
            identificador: '', 
            tipo_circuito: 'TUG', 
            tensao_nominal: 220,
            circuitos_agrupados: 1,
            metodo_instalacao: 'B1',
            material_condutor: 'COBRE',
            isolacao: 'PVC',
            sobrescreve_influencias: false,
            zona_id: !multiplasZonas && propostaContext.zonas_ids.length > 0 ? propostaContext.zonas_ids[0] : ''
        })
        setFieldErrors({}) // Reseta erros ao abrir
    }
  }, [open, propostaContext])

  const handleFormalizar = () => {
      if (!projectId || !propostaContext || !project) return;

      let hasError = false;
      const newErrors = { identificador: false, zona_id: false };

      const idPadronizado = formData.identificador?.trim().toUpperCase();

      // Validação Identificador
      if (!idPadronizado) {
          toast.error("O identificador do circuito é obrigatório (Ex: C1).")
          newErrors.identificador = true;
          hasError = true;
      } else {
          const duplicado = project.circuitos?.some(c => c.identificador === idPadronizado);
          if (duplicado) {
              toast.error(`O identificador "${idPadronizado}" já está em uso neste projeto.`);
              newErrors.identificador = true;
              hasError = true;
          }
      }

      // Validação Zona
      if (!formData.zona_id) {
          toast.error("Você deve declarar explicitamente a Zona Governante do circuito.")
          newErrors.zona_id = true;
          hasError = true;
      }

      if (hasError) {
          setFieldErrors(newErrors);
          return;
      }

      converterPropostaEmCircuito(projectId, propostaContext.id, formData as Circuito)
      
      if (onSuccess) onSuccess(); 
      onOpenChange(false)
  }

  if (!propostaContext && !isEditing) return null; 

  const multiplasZonas = propostaContext ? propostaContext.zonas_ids.length > 1 : false;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[750px] overflow-hidden flex flex-col max-h-[90vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-xl">
             <Zap className="h-5 w-5 text-primary" /> Formalizar Circuito
          </DialogTitle>
          <DialogDescription>
            Defina os parâmetros elétricos e normativos definitivos para este agrupamento.
          </DialogDescription>
        </DialogHeader>
        
        {loading ? (
            <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin text-muted-foreground"/></div>
        ) : (
            <div className="grid gap-6 py-2 overflow-y-auto pr-2">
                
                {propostaContext && (
                    <div className="bg-muted/30 border rounded-lg p-4 space-y-3">
                        <div className="flex items-center justify-between">
                            <h4 className="text-sm font-semibold flex items-center gap-2">
                                <Info className="h-4 w-4" /> Origem: {propostaContext.descricao_intencao}
                            </h4>
                            <Badge variant="secondary">{propostaContext.cargas_ids.length} Cargas Envolvidas</Badge>
                        </div>
                        {propostaContext.observacoes_normativas && (
                            <p className="text-xs text-muted-foreground border-l-2 border-primary/50 pl-2">
                                {propostaContext.observacoes_normativas}
                            </p>
                        )}
                    </div>
                )}

                <div className="grid grid-cols-2 gap-5 bg-card p-4 rounded-lg border shadow-sm">
                    <div className="grid gap-2">
                        <Label className="font-bold">Identificador do Circuito *</Label>
                        <Input 
                            placeholder="Ex: C1, QD-Geral" 
                            className={`focus-visible:ring-primary transition-colors ${fieldErrors.identificador ? 'border-red-500 ring-1 ring-red-500 bg-red-50 dark:bg-red-950/20' : 'border-primary/50'}`}
                            value={formData.identificador || ''} 
                            onChange={(e) => {
                                setFormData({...formData, identificador: e.target.value})
                                if (fieldErrors.identificador) setFieldErrors(prev => ({...prev, identificador: false}))
                            }} 
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label className="font-bold flex items-center gap-2">
                            Zona Governante *
                            {multiplasZonas && <AlertTriangle className="h-4 w-4 text-yellow-500" />}
                        </Label>
                        <Select 
                            value={formData.zona_id} 
                            onValueChange={(v) => {
                                setFormData({...formData, zona_id: v})
                                if (fieldErrors.zona_id) setFieldErrors(prev => ({...prev, zona_id: false}))
                            }}
                        >
                            <SelectTrigger className={`transition-colors ${fieldErrors.zona_id ? "border-red-500 ring-1 ring-red-500 bg-red-50 dark:bg-red-950/20" : (!formData.zona_id ? "border-red-300 ring-1 ring-red-200" : "")}`}>
                                <SelectValue placeholder="Determine a Zona (Condição Pior)" />
                            </SelectTrigger>
                            <SelectContent>
                                {zonas.map(z => (
                                    <SelectItem key={z.id} value={z.id}>
                                        {z.nome} {propostaContext?.zonas_ids.includes(z.id) ? "(Envolvida)" : ""}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        {multiplasZonas && (
                            <span className="text-[10px] text-yellow-600 font-medium leading-tight">
                                Atenção: As cargas pertencem a zonas diferentes. Segundo a NBR 5410, você deve eleger a zona com influências externas mais severas para governar o circuito.
                            </span>
                        )}
                    </div>
                </div>

                <Separator />

                <div className="grid grid-cols-3 gap-4">
                    <div className="grid gap-2">
                        <Label>Tipo de Circuito</Label>
                        <Select value={formData.tipo_circuito} onValueChange={(v: any) => setFormData({...formData, tipo_circuito: v})}>
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                                {options?.tipos.map(t => (
                                    <SelectItem key={t.codigo} value={t.codigo}>{t.descricao}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="grid gap-2">
                        <Label>Tensão Nominal (V)</Label>
                        <Input 
                            type="number" 
                            value={formData.tensao_nominal} 
                            onChange={(e) => setFormData({...formData, tensao_nominal: Number(e.target.value)})} 
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label>Fator de Agrupamento</Label>
                        <Input 
                            type="number" 
                            min={1}
                            placeholder="Circuitos no mesmo duto"
                            value={formData.circuitos_agrupados} 
                            onChange={(e) => setFormData({...formData, circuitos_agrupados: Number(e.target.value)})} 
                        />
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-4 bg-muted/10 p-4 rounded-lg border"> 
                    <div className="grid gap-2">
                        <Label>Método de Instalação (Tabelas 36-39)</Label>
                        <Select value={formData.metodo_instalacao} onValueChange={(v: any) => setFormData({...formData, metodo_instalacao: v})}>
                            <SelectTrigger className="w-full bg-background">
                                <SelectValue placeholder="Selecione o método normativo..." />
                            </SelectTrigger>
                            <SelectContent className="max-h-[250px]">
                                {options?.metodos_instalacao.map((metodo) => (
                                    <SelectItem key={metodo.codigo} value={metodo.codigo}>
                                        <span className="font-bold mr-2">{metodo.codigo}</span> 
                                        <span className="text-muted-foreground text-xs">
                                            {metodo.descricao.split('-')[1] || metodo.descricao}
                                        </span>
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-2">
                            <Label>Material Condutor</Label>
                            <Select value={formData.material_condutor} onValueChange={(v: any) => setFormData({...formData, material_condutor: v})}>
                                <SelectTrigger className="bg-background"><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="COBRE">Cobre</SelectItem>
                                    <SelectItem value="ALUMINIO">Alumínio</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="grid gap-2">
                            <Label>Isolação</Label>
                            <Select value={formData.isolacao} onValueChange={(v: any) => setFormData({...formData, isolacao: v})}>
                                <SelectTrigger className="bg-background"><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="PVC">PVC</SelectItem>
                                    <SelectItem value="EPR">EPR</SelectItem>
                                    <SelectItem value="XLPE">XLPE</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>
                </div>

                <div className="flex items-center space-x-2 pt-2 pb-4">
                    <Checkbox 
                        id="override" 
                        checked={formData.sobrescreve_influencias} 
                        onCheckedChange={(c) => setFormData({...formData, sobrescreve_influencias: !!c})}
                    />
                    <Label htmlFor="override" className="text-sm font-normal text-muted-foreground cursor-pointer">
                        Sobrescrever matriz de influências da Zona (Assumir responsabilidade manual)
                    </Label>
                </div>

            </div>
        )}
        <DialogFooter className="border-t pt-4">
            <Button variant="outline" onClick={() => onOpenChange(false)}>Cancelar</Button>
            <Button onClick={handleFormalizar} disabled={loading} className="gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Criar Circuito Definitivo
            </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}