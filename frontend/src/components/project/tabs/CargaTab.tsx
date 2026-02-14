import { Plus, Zap, Lightbulb, Plug, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import type { Carga, Local, Zona } from "@/types/project"

interface CargaTabProps {
  cargas: Carga[]
  locais: Local[]
  zonas: Zona[]
  onNew: () => void
  onAutoCargas: () => void
  onDelete: (id: string) => void
}

export function CargaTab({ cargas, locais, zonas, onNew, onAutoCargas, onDelete }: CargaTabProps) {
  const getLocalInfo = (localId: string) => locais.find(l => l.id === localId)
  const getZonaInfo = (zonaId: string) => zonas.find(z => z.id === zonaId)

  return (
    <div className="mt-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium">Previsão de Cargas</h3>
          <p className="text-sm text-muted-foreground">Cargas definidas manual ou normativamente.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={onAutoCargas} disabled={locais.length === 0}>
            <Zap className="mr-2 h-4 w-4 text-yellow-500" />
            Sugestão NBR 5410
           </Button>
          <Button onClick={onNew} disabled={locais.length === 0}>
            <Plus className="mr-2 h-4 w-4" /> Adicionar Carga
          </Button>
        </div>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Carga</TableHead>
              <TableHead>Local / Zona</TableHead>
              <TableHead>Potência</TableHead>
              <TableHead>Origem</TableHead>
              <TableHead className="text-right">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {cargas.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                  Nenhuma carga cadastrada. Use "Adicionar Carga" ou a Sugestão NBR.
                </TableCell>
              </TableRow>
            ) : (
              cargas.map((carga) => {
                const local = getLocalInfo(carga.local_id)
                const zona = local ? getZonaInfo(local.zona_id) : null
                return (
                  <TableRow key={carga.id}>
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        {carga.tipo === 'Iluminacao' ? <Lightbulb className="h-4 w-4 text-yellow-500" /> : <Plug className="h-4 w-4 text-blue-500" />}
                        {carga.nome}
                        <span className="text-xs text-muted-foreground border px-1 rounded">{carga.tipo}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-col">
                        <span>{local?.nome || 'Local Inválido'}</span>
                        <span className="text-xs text-muted-foreground" style={{ color: zona?.cor_identificacao }}>{zona?.nome}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="font-mono">{carga.potencia} {carga.unidade}</div>
                      <div className="text-xs text-muted-foreground">FP: {carga.fator_potencia}</div>
                    </TableCell>
                    <TableCell>
                      <Badge variant={carga.origem === 'norma' ? 'secondary' : 'outline'}>{carga.origem}</Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => onDelete(carga.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                )
              })
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}