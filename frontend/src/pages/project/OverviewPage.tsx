import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { toast } from "sonner" 
import { 
  Zap, Map, MapPin, Activity, Settings, 
  ArrowRight, CheckCircle2, AlertTriangle 
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { useProjectStore } from "@/store/useProjectStore"

// Importação do Modal
import { EditProjectDialog } from "@/components/project/dialogs/EditProjectDialog"
import type { Projeto } from "@/types/project"

export default function OverviewPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { projects, updateProject } = useProjectStore()
  
  // State para controlar o modal
  const [isEditOpen, setIsEditOpen] = useState(false)
  
  // State para os dados do formulário de edição
  const [projectFormData, setProjectFormData] = useState<Partial<Projeto>>({})

  const project = projects.find((p) => p.id === id)

  // Sincroniza o formulário com os dados do projeto ao carregar ou abrir modal
  useEffect(() => {
    if (project) {
        // Inicializa com todos os dados existentes para não perder arrays (locais, zonas...)
        setProjectFormData({ ...project })
    }
  }, [project, isEditOpen])

  if (!project) return <div className="p-8">Projeto não encontrado.</div>

  // --- HANDLERS ---
  const handleSaveProject = () => {
      if (projectFormData && project) {
          // CORREÇÃO CRÍTICA:
          // A store espera UM objeto Projeto completo, não (id, data).
          // Fazemos o merge para garantir que arrays (cargas, zonas) sejam preservados.
          const updatedProject = { ...project, ...projectFormData } as Projeto
          
          updateProject(updatedProject)
          
          toast.success("Configurações do projeto atualizadas.")
          setIsEditOpen(false)
      }
  }

  // --- CÁLCULOS DE RESUMO (KPIs) ---
  const totalArea = project.locais.reduce((acc, l) => acc + l.area_m2, 0)
  const totalCargas = project.cargas.length
  const totalPotenciaVA = project.cargas.reduce((acc, c) => acc + c.potencia, 0)
  const cargasSemCircuito = project.cargas.filter(c => !c.circuito_id).length
  const totalCircuitos = project.circuitos?.length || 0

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* HEADER DO PROJETO */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
             <h1 className="text-3xl font-bold tracking-tight">{project.nome}</h1>
             <Badge variant="outline" className="uppercase text-xs tracking-wider">
                {project.tipo_instalacao}
             </Badge>
          </div>
          <p className="text-muted-foreground mt-1">
             Configurado para <strong className="font-mono text-foreground">{project.tensao_sistema}</strong> • Sistema {project.sistema}
          </p>
        </div>
        
        <Button variant="outline" onClick={() => setIsEditOpen(true)}>
           <Settings className="mr-2 h-4 w-4" /> Configurações Globais
        </Button>
      </div>

      <Separator />

      {/* CARDS DE STATUS (KPIs) */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Potência Total Est.</CardTitle>
            <Zap className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalPotenciaVA} VA</div>
            <p className="text-xs text-muted-foreground">
              Soma de todas as cargas ativas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Área Construída</CardTitle>
            <Map className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalArea.toFixed(2)} m²</div>
            <p className="text-xs text-muted-foreground">
              {project.locais.length} locais definidos
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Circuitos</CardTitle>
            <Activity className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalCircuitos}</div>
            <p className="text-xs text-muted-foreground">
              {cargasSemCircuito > 0 
                ? `${cargasSemCircuito} cargas sem circuito` 
                : "Todas cargas alocadas"}
            </p>
          </CardContent>
        </Card>

        <Card className={cargasSemCircuito > 0 ? "border-orange-200 bg-orange-50 dark:bg-orange-950/20" : "border-green-200 bg-green-50 dark:bg-green-950/20"}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saúde do Projeto</CardTitle>
            {cargasSemCircuito > 0 ? <AlertTriangle className="h-4 w-4 text-orange-500" /> : <CheckCircle2 className="h-4 w-4 text-green-500" />}
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold">
                {cargasSemCircuito > 0 ? "Atenção Necessária" : "Pronto p/ Cálculo"}
            </div>
            <p className="text-xs text-muted-foreground">
               {cargasSemCircuito > 0 ? "Finalize a distribuição" : "Avance para a Fase 10"}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* PROXIMOS PASSOS */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Ficha Técnica</CardTitle>
            <CardDescription>Parâmetros globais utilizados no dimensionamento.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
             <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                    <span className="text-sm font-medium text-muted-foreground">Sistema de Tensão</span>
                    <p className="font-mono">{project.tensao_sistema}</p>
                </div>
                <div className="space-y-1">
                    <span className="text-sm font-medium text-muted-foreground">Esquema de Aterramento</span>
                    <p className="font-mono">{project.esquema_aterramento || "Não definido"}</p>
                </div>
                <div className="space-y-1">
                    <span className="text-sm font-medium text-muted-foreground">Tipo de Fornecimento</span>
                    <p>{project.sistema}</p>
                </div>
                <div className="space-y-1">
                    <span className="text-sm font-medium text-muted-foreground">Data de Criação</span>
                    <p>{new Date(project.data_criacao).toLocaleDateString()}</p>
                </div>
             </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Fluxo de Trabalho</CardTitle>
            <CardDescription>Navegue pelas etapas do projeto.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-2">
             <Button 
                variant="ghost" 
                className="justify-between h-auto py-3 border border-transparent hover:border-border hover:bg-muted"
                onClick={() => navigate(`/project/${project.id}/zonas`)}
             >
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 text-blue-600 rounded-lg dark:bg-blue-900/40"><Map className="h-4 w-4" /></div>
                    <div className="text-left">
                        <div className="font-medium">1. Zonas e Influências</div>
                        <div className="text-xs text-muted-foreground">{project.zonas.length} zonas definidas</div>
                    </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
             </Button>

             <Button 
                variant="ghost" 
                className="justify-between h-auto py-3 border border-transparent hover:border-border hover:bg-muted"
                onClick={() => navigate(`/project/${project.id}/locais`)}
             >
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-indigo-100 text-indigo-600 rounded-lg dark:bg-indigo-900/40"><MapPin className="h-4 w-4" /></div>
                    <div className="text-left">
                        <div className="font-medium">2. Locais e Cargas</div>
                        <div className="text-xs text-muted-foreground">{project.locais.length} locais, {totalCargas} cargas</div>
                    </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
             </Button>

             <Button 
                variant="ghost" 
                className="justify-between h-auto py-3 border border-transparent hover:border-border hover:bg-muted"
                onClick={() => navigate(`/project/${project.id}/circuitos`)}
             >
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-emerald-100 text-emerald-600 rounded-lg dark:bg-emerald-900/40"><Activity className="h-4 w-4" /></div>
                    <div className="text-left">
                        <div className="font-medium">3. Circuitos</div>
                        <div className="text-xs text-muted-foreground">{totalCircuitos} circuitos criados</div>
                    </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
             </Button>
          </CardContent>
        </Card>
      </div>

      {/* COMPONENTE REUTILIZADO */}
      <EditProjectDialog 
        open={isEditOpen} 
        onOpenChange={setIsEditOpen}
        data={projectFormData}      
        setData={setProjectFormData} 
        onSave={handleSaveProject}   
      />
    </div>
  )
}