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
import type { Zona } from "@/types/project"

interface ZoneDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: Partial<Zona>
  setData: (data: Partial<Zona>) => void
  onSave: () => void
  isEditing: boolean
}

export function ZoneDialog({ open, onOpenChange, data, setData, onSave, isEditing }: ZoneDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>{isEditing ? "Editar Zona" : "Nova Zona"}</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label>Nome</Label>
            <Input 
              value={data.nome || ''} 
              onChange={(e) => setData({...data, nome: e.target.value})} 
            />
          </div>
          
          <Separator className="my-2" />
          <h4 className="text-sm font-medium">Influências Externas (NBR 5410)</h4>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="grid gap-2">
              <Label>Temperatura (AA)</Label>
              <Select value={data.temp_ambiente} onValueChange={(v) => setData({...data, temp_ambiente: v})}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="AA1">AA1 (25°C)</SelectItem><SelectItem value="AA2">AA2 (30°C)</SelectItem></SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>Água (AD)</Label>
              <Select value={data.presenca_agua} onValueChange={(v) => setData({...data, presenca_agua: v})}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="AD1">AD1 (Seco)</SelectItem><SelectItem value="AD2">AD2 (Gotas)</SelectItem></SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>Sólidos (AE)</Label>
              <Select value={data.presenca_solidos} onValueChange={(v) => setData({...data, presenca_solidos: v})}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="AE1">AE1 (Desprezível)</SelectItem><SelectItem value="AE2">AE2 (Pequenos)</SelectItem></SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>Pessoas (BA)</Label>
              <Select value={data.competencia_pessoas} onValueChange={(v) => setData({...data, competencia_pessoas: v})}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="BA1">BA1 (Comuns)</SelectItem><SelectItem value="BA4">BA4 (Instruídas)</SelectItem></SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>Materiais (CA)</Label>
              <Select value={data.materiais_construcao} onValueChange={(v) => setData({...data, materiais_construcao: v})}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="CA1">CA1 (Não Combustível)</SelectItem><SelectItem value="CA2">CA2 (Combustível)</SelectItem></SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>Estrutura (CB)</Label>
              <Select value={data.estrutura_edificacao} onValueChange={(v) => setData({...data, estrutura_edificacao: v})}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="CB1">CB1 (Desprezível)</SelectItem><SelectItem value="CB2">CB2 (Móvel)</SelectItem></SelectContent>
              </Select>
            </div>
          </div>
        </div>
        <DialogFooter><Button onClick={onSave}>Salvar</Button></DialogFooter>
      </DialogContent>
    </Dialog>
  )
}