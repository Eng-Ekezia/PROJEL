import { useState } from "react"
import { useParams } from "react-router-dom"
import { toast } from "sonner"
import { Plus, Settings, Trash2, Thermometer, Droplets, HardHat, Wind, BrickWall, Building } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { ZoneDialog } from "@/components/project/dialogs/ZoneDialog" // Reutilizamos o Dialog existente
import { useProjectStore } from "@/store/useProjectStore"
import type { Zona } from "@/types/project"

export default function ZonesPage() {
  const { id } = useParams<{ id: string }>()
  const { 
    projects, 
    addZonaToProject, 
    updateZonaInProject, 
    removeZonaFromProject 
  } = useProjectStore()

  // Busca o projeto pelo ID da URL (Contexto Global)
  const project = projects.find((p) => p.id === id)

  // State Local da Página
  const [isZoneDialogOpen, setIsZoneDialogOpen] = useState(false)
  const [editingZona, setEditingZona] = useState<Zona | null>(null)
  const [zonaFormData, setZonaFormData] = useState<Partial<Zona>>({})

  if (!project) {
    return <div className="p-8">Projeto não encontrado.</div>
  }

  // --- HANDLERS (Migrados de ProjectDetails) ---

  const handleOpenZoneDialog = (zona?: Zona) => {
    if (zona) {
      setEditingZona(zona)
      setZonaFormData(zona)
    } else {
      setEditingZona(null)
      // Valores Default alinhados com a NBR 5410 (Ambiente Normal)
      setZonaFormData({
        nome: "", 
        descricao: "", 
        temp_ambiente: "AA1", 
        presenca_agua: "AD1", 
        presenca_solidos: "AE1",
        competencia_pessoas: "BA1", 
        materiais_construcao: "CA1", 
        estrutura_edificacao: "CB1",
        origem: "custom", 
        cor_identificacao: "#3b82f6" // Azul padrão
      })
    }
    setIsZoneDialogOpen(true)
  }

  const handleSaveZona = () => {
    if (!project || !zonaFormData.nome) {
      toast.error("O nome da zona é obrigatório.")
      return
    }

    const payload = {
      ...zonaFormData,
      projeto_id: project.id,
      id: editingZona?.id || crypto.randomUUID(),
      data_criacao: editingZona?.data_criacao || new Date().toISOString()
    } as Zona

    if (editingZona) {
      updateZonaInProject(project.id, payload)
      toast.success("Zona atualizada com sucesso.")
    } else {
      addZonaToProject(project.id, payload)
      toast.success("Zona criada com sucesso.")
    }
    setIsZoneDialogOpen(false)
  }

  const handleDeleteZona = (zonaId: string) => {
    if (!project) return
    
    // Validação de Integridade: Não apagar Zona se houver locais vinculados
    const locaisNaZona = project.locais.filter(l => l.zona_id === zonaId)
    if (locaisNaZona.length > 0) {
      toast.error(`Bloqueado: Existem ${locaisNaZona.length} locais dependentes desta zona.`)
      return
    }

    if (confirm("Tem certeza que deseja excluir esta zona?")) {
      removeZonaFromProject(project.id, zonaId)
      toast.success("Zona removida.")
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Zonas de Influência</h2>
          <p className="text-muted-foreground">
            Defina as características ambientais e normativas (NBR 5410) para agrupar seus locais.
          </p>
        </div>
        <Button onClick={() => handleOpenZoneDialog()}>
            <Plus className="mr-2 h-4 w-4" /> Nova Zona
        </Button>
      </div>
      
      {/* GRID DE CARDS (Visualização) */}
      {project.zonas.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed rounded-lg text-muted-foreground">
              <p>Nenhuma zona definida.</p>
              <Button variant="link" onClick={() => handleOpenZoneDialog()}>Criar a primeira zona</Button>
          </div>
      ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
             {project.zonas.map((zona) => (
                <Card key={zona.id} className="border-l-4 shadow-sm hover:shadow-md transition-shadow" style={{ borderLeftColor: zona.cor_identificacao }}>
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-base font-semibold truncate pr-2">{zona.nome}</CardTitle>
                      <Button variant="ghost" size="icon" className="h-8 w-8 -mt-1 -mr-2" onClick={() => handleOpenZoneDialog(zona)}>
                         <Settings className="h-4 w-4 text-muted-foreground" />
                      </Button>
                    </div>
                    <CardDescription className="line-clamp-2 min-h-[40px]">
                        {zona.descricao || "Sem descrição definida."}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pb-2 text-xs">
                    <div className="grid grid-cols-2 gap-y-2 gap-x-1">
                      <div className="flex items-center gap-1" title={`Temperatura: ${zona.temp_ambiente}`}>
                          <Thermometer className="h-3 w-3 text-muted-foreground" /> 
                          <span className="font-mono text-muted-foreground">{zona.temp_ambiente}</span>
                      </div>
                      <div className="flex items-center gap-1" title={`Água: ${zona.presenca_agua}`}>
                          <Droplets className="h-3 w-3 text-muted-foreground" /> 
                          <span className="font-mono text-muted-foreground">{zona.presenca_agua}</span>
                      </div>
                      <div className="flex items-center gap-1" title={`Sólidos: ${zona.presenca_solidos}`}>
                          <Wind className="h-3 w-3 text-muted-foreground" /> 
                          <span className="font-mono text-muted-foreground">{zona.presenca_solidos}</span>
                      </div>
                      <div className="flex items-center gap-1" title={`Pessoas: ${zona.competencia_pessoas}`}>
                          <HardHat className="h-3 w-3 text-muted-foreground" /> 
                          <span className="font-mono text-muted-foreground">{zona.competencia_pessoas}</span>
                      </div>
                      <div className="flex items-center gap-1" title={`Materiais: ${zona.materiais_construcao}`}>
                          <BrickWall className="h-3 w-3 text-muted-foreground" /> 
                          <span className="font-mono text-muted-foreground">{zona.materiais_construcao}</span>
                      </div>
                      <div className="flex items-center gap-1" title={`Estrutura: ${zona.estrutura_edificacao}`}>
                          <Building className="h-3 w-3 text-muted-foreground" /> 
                          <span className="font-mono text-muted-foreground">{zona.estrutura_edificacao}</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="pt-2 justify-end border-t bg-muted/20">
                    <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-destructive hover:bg-destructive/10 hover:text-destructive h-7 px-2" 
                        onClick={() => handleDeleteZona(zona.id)}
                    >
                        <Trash2 className="h-3.5 w-3.5 mr-1.5" /> Excluir
                    </Button>
                  </CardFooter>
                </Card>
             ))}
          </div>
      )}

      {/* DIALOG COMPARTILHADO */}
      <ZoneDialog 
        open={isZoneDialogOpen} 
        onOpenChange={setIsZoneDialogOpen}
        data={zonaFormData} 
        setData={setZonaFormData} 
        onSave={handleSaveZona}
        isEditing={!!editingZona}
      />
    </div>
  )
}