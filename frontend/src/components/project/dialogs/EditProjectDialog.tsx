//import { useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter
} from "@/components/ui/dialog"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea" // <--- IMPORT CORRETO

import type { Projeto } from "@/types/project"

interface EditProjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: Partial<Projeto>
  setData: (data: Partial<Projeto>) => void
  onSave: () => void
}

export function EditProjectDialog({ open, onOpenChange, data, setData, onSave }: EditProjectDialogProps) {
  
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Editar Configurações do Projeto</DialogTitle>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
            {/* Nome */}
            <div className="grid gap-2">
                <Label>Nome do Projeto</Label>
                <Input 
                    value={data.nome || ''} 
                    onChange={(e) => setData({...data, nome: e.target.value})} 
                />
            </div>

            {/* Linha 1: Instalação e Sistema */}
            <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                    <Label>Tipo de Instalação</Label>
                    <Select value={data.tipo_instalacao} onValueChange={(v) => setData({...data, tipo_instalacao: v})}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="Residencial">Residencial</SelectItem>
                            <SelectItem value="Comercial">Comercial</SelectItem>
                            <SelectItem value="Industrial">Industrial</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                <div className="grid gap-2">
                    <Label>Sistema</Label>
                    <Select value={data.sistema} onValueChange={(v) => setData({...data, sistema: v})}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="Monofasico">Monofásico</SelectItem>
                            <SelectItem value="Bifasico">Bifásico</SelectItem>
                            <SelectItem value="Trifasico">Trifásico</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>

            {/* Linha 2: Tensão e Aterramento */}
            <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                    <Label>Tensão Nominal</Label>
                    <Select value={data.tensao_sistema} onValueChange={(v) => setData({...data, tensao_sistema: v})}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="127/220V">127/220V</SelectItem>
                            <SelectItem value="220/380V">220/380V</SelectItem>
                            <SelectItem value="380/440V">380/440V</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                <div className="grid gap-2">
                    <Label>Esquema de Aterramento</Label>
                    <Select value={data.esquema_aterramento} onValueChange={(v) => setData({...data, esquema_aterramento: v})}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            <SelectItem value="TN-S">TN-S (Recomendado)</SelectItem>
                            <SelectItem value="TN-C">TN-C</SelectItem>
                            <SelectItem value="TN-C-S">TN-C-S</SelectItem>
                            <SelectItem value="TT">TT</SelectItem>
                            <SelectItem value="IT">IT</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>

            {/* Descrição Aterramento - CORREÇÃO AQUI */}
             <div className="grid gap-2">
                <Label>Detalhes do Aterramento (Opcional)</Label>
                <Textarea 
                    value={data.descricao_aterramento || ''} 
                    onChange={(e) => setData({...data, descricao_aterramento: e.target.value})}
                    placeholder="Ex: Malha com 3 hastes cobreadas de 2,40m..."
                    className="min-h-[80px]"
                />
            </div>

        </div>
        <DialogFooter>
            <Button variant="outline" onClick={() => onOpenChange(false)}>Cancelar</Button>
            <Button onClick={onSave}>Salvar Alterações</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}