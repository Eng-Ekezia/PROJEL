import { Plus, Settings, Trash2, Maximize, Ruler } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import type { Local, Zona } from "@/types/project"
import type { LocalComPerfil } from "../dialogs/LocalDialog"

interface LocalTabProps {
  locais: Local[]
  zonas: Zona[]
  onNew: () => void
  onEdit: (local: LocalComPerfil) => void
  onDelete: (id: string) => void
}

export function LocalTab({ locais, zonas, onNew, onEdit, onDelete }: LocalTabProps) {
  const getZonaInfo = (zonaId: string) => zonas.find(z => z.id === zonaId)

  return (
    <div className="mt-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium">Cômodos e Áreas</h3>
          <p className="text-sm text-muted-foreground">Definição física e perfil normativo.</p>
        </div>
        <Button onClick={onNew} disabled={zonas.length === 0}>
            <Plus className="mr-2 h-4 w-4" /> Novo Cômodo
        </Button>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {locais.map((local) => {
          const zona = getZonaInfo(local.zona_id)
          return (
            <Card key={local.id}>
              <CardHeader className="pb-2">
                <div className="flex justify-between">
                  <div>
                    <CardTitle className="text-base">{local.nome}</CardTitle>
                    <div className="flex items-center gap-1 mt-1 text-xs text-muted-foreground">
                       <span className="w-2 h-2 rounded-full" style={{ backgroundColor: zona?.cor_identificacao || '#ccc' }} />
                       {zona?.nome}
                    </div>
                  </div>
                  <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => onEdit(local as LocalComPerfil)}>
                    <Settings className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="pb-2">
                 <div className="grid grid-cols-2 gap-2 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2"><Maximize className="h-3.5 w-3.5" /> {local.area_m2} m²</div>
                    <div className="flex items-center gap-2"><Ruler className="h-3.5 w-3.5" /> {local.perimetro_m} m</div>
                 </div>
              </CardContent>
              <CardFooter className="pt-2 justify-end">
                <Button variant="ghost" size="sm" className="text-destructive hover:bg-destructive/10" onClick={() => onDelete(local.id)}>
                    <Trash2 className="h-4 w-4" />
                </Button>
              </CardFooter>
            </Card>
          )
        })}
      </div>
    </div>
  )
}