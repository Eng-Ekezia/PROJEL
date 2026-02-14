import { Plus, Settings, Trash2, Thermometer, Droplets, HardHat, Wind, BrickWall, Building } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import type { Zona } from "@/types/project"

interface ZoneTabProps {
  zonas: Zona[]
  onNew: () => void
  onEdit: (zona: Zona) => void
  onDelete: (id: string) => void
}

export function ZoneTab({ zonas, onNew, onEdit, onDelete }: ZoneTabProps) {
  return (
    <div className="mt-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium">Zonas de Influência</h3>
          <p className="text-sm text-muted-foreground">Classificação completa das influências externas.</p>
        </div>
        <Button onClick={onNew}><Plus className="mr-2 h-4 w-4" /> Nova Zona</Button>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
         {zonas.map((zona) => (
            <Card key={zona.id} className="border-l-4" style={{ borderLeftColor: zona.cor_identificacao }}>
              <CardHeader className="pb-2">
                <div className="flex justify-between">
                  <CardTitle className="text-base">{zona.nome}</CardTitle>
                  <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => onEdit(zona)}>
                     <Settings className="h-4 w-4" />
                  </Button>
                </div>
                <CardDescription>{zona.descricao || "Sem descrição"}</CardDescription>
              </CardHeader>
              <CardContent className="pb-2 text-xs">
                <div className="grid grid-cols-2 gap-2">
                  <div className="flex items-center gap-1" title="Temperatura"><Thermometer className="h-3 w-3 text-muted-foreground" /> {zona.temp_ambiente}</div>
                  <div className="flex items-center gap-1" title="Água"><Droplets className="h-3 w-3 text-muted-foreground" /> {zona.presenca_agua}</div>
                  <div className="flex items-center gap-1" title="Sólidos"><Wind className="h-3 w-3 text-muted-foreground" /> {zona.presenca_solidos}</div>
                  <div className="flex items-center gap-1" title="Pessoas"><HardHat className="h-3 w-3 text-muted-foreground" /> {zona.competencia_pessoas}</div>
                  <div className="flex items-center gap-1" title="Materiais"><BrickWall className="h-3 w-3 text-muted-foreground" /> {zona.materiais_construcao}</div>
                  <div className="flex items-center gap-1" title="Estrutura"><Building className="h-3 w-3 text-muted-foreground" /> {zona.estrutura_edificacao}</div>
                </div>
              </CardContent>
              <CardFooter className="pt-2 justify-end">
                <Button variant="ghost" size="sm" className="text-destructive hover:bg-destructive/10" onClick={() => onDelete(zona.id)}>
                    <Trash2 className="h-4 w-4" />
                </Button>
              </CardFooter>
            </Card>
         ))}
      </div>
    </div>
  )
}