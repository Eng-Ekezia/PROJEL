import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter
} from "@/components/ui/dialog"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select"
import type { Carga, Local } from "@/types/project"

interface CargaDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: Partial<Carga>
  setData: (data: Partial<Carga>) => void
  onSave: () => void
  locais: Local[]
}

export function CargaDialog({ open, onOpenChange, data, setData, onSave, locais }: CargaDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader><DialogTitle>Nova Carga Manual</DialogTitle></DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label>Nome da Carga</Label>
            <Input placeholder="Ex: Ar Condicionado" value={data.nome || ''} onChange={(e) => setData({...data, nome: e.target.value})} />
          </div>
          <div className="grid gap-2">
            <Label>Local</Label>
            <Select value={data.local_id} onValueChange={(v) => setData({...data, local_id: v})}>
              <SelectTrigger><SelectValue placeholder="Selecione o local" /></SelectTrigger>
              <SelectContent>
                {locais.map(l => <SelectItem key={l.id} value={l.id}>{l.nome}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-2 gap-4">
             <div className="grid gap-2">
                <Label>Tipo</Label>
                <Select value={data.tipo} onValueChange={(v) => setData({...data, tipo: v})}>
                   <SelectTrigger><SelectValue /></SelectTrigger>
                   <SelectContent>
                      <SelectItem value="TUG">TUG</SelectItem>
                      <SelectItem value="TUE">TUE</SelectItem>
                      <SelectItem value="Iluminacao">Iluminação</SelectItem>
                      <SelectItem value="Motor">Motor</SelectItem>
                   </SelectContent>
                </Select>
             </div>
             <div className="grid gap-2">
                <Label>Potência</Label>
                <div className="flex gap-2">
                   <Input type="number" value={data.potencia} onChange={(e) => setData({...data, potencia: Number(e.target.value)})} />
                   <Select value={data.unidade} onValueChange={(v:any) => setData({...data, unidade: v})}>
                      <SelectTrigger className="w-[80px]"><SelectValue /></SelectTrigger>
                      <SelectContent><SelectItem value="W">W</SelectItem><SelectItem value="VA">VA</SelectItem></SelectContent>
                   </Select>
                </div>
             </div>
          </div>
        </div>
        <DialogFooter><Button onClick={onSave}>Salvar Carga</Button></DialogFooter>
      </DialogContent>
    </Dialog>
  )
}