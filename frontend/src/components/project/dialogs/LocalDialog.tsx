import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter
} from "@/components/ui/dialog"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select"
import type { Local, Zona } from "@/types/project"

export interface LocalComPerfil extends Local {
  tipo: 'padrao' | 'cozinha' | 'banheiro' | 'servico' | 'externo'; 
}

interface LocalDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: Partial<LocalComPerfil>
  setData: (data: Partial<LocalComPerfil>) => void
  onSave: () => void
  zonas: Zona[]
  isEditing: boolean
}

export function LocalDialog({ open, onOpenChange, data, setData, onSave, zonas, isEditing }: LocalDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
         <DialogHeader>
            <DialogTitle>{isEditing ? "Editar Cômodo" : "Novo Cômodo"}</DialogTitle>
         </DialogHeader>
         <div className="grid gap-4 py-4">
            <div className="grid gap-2">
                <Label>Nome</Label>
                <Input value={data.nome || ''} onChange={(e) => setData({...data, nome: e.target.value})} />
            </div>
            <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                   <Label>Perfil Normativo</Label>
                   <Select value={data.tipo} onValueChange={(v: any) => setData({...data, tipo: v})}>
                     <SelectTrigger><SelectValue /></SelectTrigger>
                     <SelectContent>
                       <SelectItem value="padrao">Padrão</SelectItem>
                       <SelectItem value="cozinha">Cozinha</SelectItem>
                       <SelectItem value="banheiro">Banheiro</SelectItem>
                       <SelectItem value="servico">Serviço</SelectItem>
                       <SelectItem value="externo">Externo</SelectItem>
                     </SelectContent>
                   </Select>
                </div>
                <div className="grid gap-2">
                   <Label>Zona</Label>
                   <Select value={data.zona_id} onValueChange={(v) => setData({...data, zona_id: v})}>
                     <SelectTrigger><SelectValue /></SelectTrigger>
                     <SelectContent>{zonas.map(z => <SelectItem key={z.id} value={z.id}>{z.nome}</SelectItem>)}</SelectContent>
                   </Select>
                </div>
            </div>
            
            {/* NOVO: Grid com 3 colunas para acomodar o Pé-direito */}
            <div className="grid grid-cols-3 gap-3 bg-muted/20 p-3 rounded-md border">
               <div className="grid gap-2">
                   <Label className="text-xs">Área (m²)</Label>
                   <Input type="number" step="0.1" value={data.area_m2} onChange={(e) => setData({...data, area_m2: Number(e.target.value)})} />
               </div>
               <div className="grid gap-2">
                   <Label className="text-xs">Perímetro (m)</Label>
                   <Input type="number" step="0.1" value={data.perimetro_m} onChange={(e) => setData({...data, perimetro_m: Number(e.target.value)})} />
               </div>
               <div className="grid gap-2">
                   <Label className="text-xs">Pé-direito (m)</Label>
                   <Input type="number" step="0.1" value={data.pe_direito_m} onChange={(e) => setData({...data, pe_direito_m: Number(e.target.value)})} />
               </div>
            </div>
         </div>
         <DialogFooter>
             <Button variant="outline" onClick={() => onOpenChange(false)}>Cancelar</Button>
             <Button onClick={onSave}>Salvar</Button>
         </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}