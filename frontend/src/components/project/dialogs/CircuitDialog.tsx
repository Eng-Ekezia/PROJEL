import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter
} from "@/components/ui/dialog"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Loader2 } from "lucide-react" 
import type { Circuito, Zona } from "@/types/project"

// URL da API (Idealmente viria de env vars)
const API_URL = "http://localhost:8000/api/v1"; 

interface CircuitDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: Partial<Circuito>
  setData: (data: Partial<Circuito>) => void
  onSave: () => void
  zonas: Zona[]
  isEditing: boolean
}

interface ApiOptions {
    tipos: { codigo: string, descricao: string }[]
    metodos_instalacao: { codigo: string, descricao: string }[]
}

export function CircuitDialog({ open, onOpenChange, data, setData, onSave, zonas, isEditing }: CircuitDialogProps) {
  
  const [options, setOptions] = useState<ApiOptions | null>(null)
  const [loading, setLoading] = useState(false)

  // 1. Fetch da Verdade Normativa (Backend)
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

  // 2. Defaults Inteligentes
  useEffect(() => {
    if (open && !isEditing && !data.identificador) {
        setData({
            ...data,
            tipo_circuito: 'TUG', // Default mais comum mas pode ser ajustado conforme perfil do local/carga
            metodo_instalacao: 'B1',
            tensao_nominal: 127,
            material_condutor: 'COBRE',
            isolacao: 'PVC',
            sobrescreve_influencias: false,
            circuitos_agrupados: 1
        })
    }
  }, [open, isEditing])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px]"> {/* MODAL MAIS LARGO */}
        <DialogHeader>
          <DialogTitle>{isEditing ? "Editar Circuito" : "Novo Circuito"}</DialogTitle>
        </DialogHeader>
        
        {loading ? (
            <div className="flex justify-center py-8"><Loader2 className="h-8 w-8 animate-spin text-muted-foreground"/></div>
        ) : (
            <div className="grid gap-4 py-4">
                {/* Linha 1: Identificação e Zona */}
                <div className="grid grid-cols-2 gap-4">
                    <div className="grid gap-2">
                        <Label>Identificador</Label>
                        <Input 
                            placeholder="Ex: C1, QD-Geral" 
                            value={data.identificador || ''} 
                            onChange={(e) => setData({...data, identificador: e.target.value})} 
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label className="text-destructive-foreground">Zona Governante *</Label>
                        <Select value={data.zona_id} onValueChange={(v) => setData({...data, zona_id: v})}>
                            <SelectTrigger className={!data.zona_id ? "border-red-300" : ""}><SelectValue placeholder="Selecione a Zona" /></SelectTrigger>
                            <SelectContent>
                                {zonas.map(z => <SelectItem key={z.id} value={z.id}>{z.nome}</SelectItem>)}
                            </SelectContent>
                        </Select>
                    </div>
                </div>

                <Separator />

                {/* Linha 2: Elétrica Básica */}
                <div className="grid grid-cols-3 gap-4">
                    <div className="grid gap-2">
                        <Label>Tipo</Label>
                        <Select value={data.tipo_circuito} onValueChange={(v: any) => setData({...data, tipo_circuito: v})}>
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                                {options?.tipos.map(t => (
                                    <SelectItem key={t.codigo} value={t.codigo}>{t.descricao}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="grid gap-2">
                        <Label>Tensão (V)</Label>
                        <Input 
                            type="number" 
                            value={data.tensao_nominal} 
                            onChange={(e) => setData({...data, tensao_nominal: Number(e.target.value)})} 
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label>Agrupamento</Label>
                        <Input 
                            type="number" 
                            min={1}
                            value={data.circuitos_agrupados} 
                            onChange={(e) => setData({...data, circuitos_agrupados: Number(e.target.value)})} 
                        />
                    </div>
                </div>

                {/* Linha 3: Instalação - CORREÇÃO DE LAYOUT */}
                <div className="grid grid-cols-1 gap-4"> 
                    
                    {/* Método ocupa linha inteira agora */}
                    <div className="grid gap-2">
                        <Label>Método de Instalação</Label>
                        <Select value={data.metodo_instalacao} onValueChange={(v: any) => setData({...data, metodo_instalacao: v})}>
                            <SelectTrigger className="w-full">
                                <SelectValue placeholder="Selecione o método normativo..." />
                            </SelectTrigger>
                            <SelectContent className="max-h-[300px]">
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

                    {/* Materiais e Isolação na linha de baixo */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-2">
                            <Label>Material Condutor</Label>
                            <Select value={data.material_condutor} onValueChange={(v: any) => setData({...data, material_condutor: v})}>
                                <SelectTrigger><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="COBRE">Cobre</SelectItem>
                                    <SelectItem value="ALUMINIO">Alumínio</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="grid gap-2">
                            <Label>Isolação</Label>
                            <Select value={data.isolacao} onValueChange={(v: any) => setData({...data, isolacao: v})}>
                                <SelectTrigger><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="PVC">PVC</SelectItem>
                                    <SelectItem value="EPR">EPR</SelectItem>
                                    <SelectItem value="XLPE">XLPE</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>
                </div>

                <div className="flex items-center space-x-2 mt-2">
                    <Checkbox 
                        id="override" 
                        checked={data.sobrescreve_influencias} 
                        onCheckedChange={(c) => setData({...data, sobrescreve_influencias: !!c})}
                    />
                    <Label htmlFor="override" className="text-sm font-normal text-muted-foreground">
                        Sobrescrever influências da Zona (Forçar parâmetros manuais)
                    </Label>
                </div>

            </div>
        )}
        <DialogFooter><Button onClick={onSave} disabled={loading}>Salvar Circuito</Button></DialogFooter>
      </DialogContent>
    </Dialog>
  )
}