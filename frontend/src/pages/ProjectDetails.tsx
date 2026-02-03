import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { 
  ArrowLeft, Plus, Settings, Trash2, 
  Thermometer, Droplets, HardHat, 
  Ruler, Maximize, Home, Utensils, Bath, Waves, 
  Wind, BrickWall, Building, Zap, Lightbulb, Plug
} from "lucide-react"

import { NBR5410_WIZARD } from "../data/nbr5410_wizard"

// Shadcn UI Components
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"

// Store & Types
import { useProjectStore } from "../store/useProjectStore"
import type { Zona, Local, Carga } from "../types/project"

// Extensões de tipo para UI
interface LocalComPerfil extends Local {
  tipo: 'padrao' | 'cozinha' | 'banheiro' | 'servico' | 'externo'; 
}

export default function ProjectDetails() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { 
    projects, 
    addZonaToProject, updateZonaInProject, removeZonaFromProject,
    addLocalToProject, updateLocalInProject, removeLocalFromProject,
    addCargaToProject, removeCargaFromProject 
  } = useProjectStore()
  
  const project = projects.find((p) => p.id === id)

  // --- STATE ---
  const [activeTab, setActiveTab] = useState("zonas")
  
  // Dialog States
  const [isZoneDialogOpen, setIsZoneDialogOpen] = useState(false)
  const [editingZona, setEditingZona] = useState<Zona | null>(null)
  const [zonaFormData, setZonaFormData] = useState<Partial<Zona>>({})

  const [isLocalDialogOpen, setIsLocalDialogOpen] = useState(false)
  const [editingLocal, setEditingLocal] = useState<LocalComPerfil | null>(null)
  const [localFormData, setLocalFormData] = useState<Partial<LocalComPerfil>>({})

  // Carga Manual State (Novo)
  const [isCargaDialogOpen, setIsCargaDialogOpen] = useState(false)
  const [cargaFormData, setCargaFormData] = useState<Partial<Carga>>({})

  // --- HANDLERS: ZONA ---
  const handleOpenZoneDialog = (zona?: Zona) => {
    if (zona) {
      setEditingZona(zona)
      setZonaFormData(zona)
    } else {
      setEditingZona(null)
      setZonaFormData({
        nome: "", descricao: "", 
        temp_ambiente: "AA1", presenca_agua: "AD1", presenca_solidos: "AE1",
        competencia_pessoas: "BA1", materiais_construcao: "CA1", estrutura_edificacao: "CB1",
        origem: "custom", cor_identificacao: "#3b82f6"
      })
    }
    setIsZoneDialogOpen(true)
  }

  const handleSaveZona = () => {
    if (!project || !zonaFormData.nome) {
      toast.error("Nome é obrigatório")
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
      toast.success("Zona atualizada")
    } else {
      addZonaToProject(project.id, payload)
      toast.success("Zona criada")
    }
    setIsZoneDialogOpen(false)
  }

  const handleDeleteZona = (zonaId: string) => {
    if (!project) return
    const locais = project.locais.filter(l => l.zona_id === zonaId)
    if (locais.length > 0) {
      toast.error(`Impossível excluir: Existem ${locais.length} locais nesta zona.`)
      return
    }
    if (confirm("Excluir esta zona?")) {
      removeZonaFromProject(project.id, zonaId)
      toast.success("Zona removida")
    }
  }

  // --- HANDLERS: LOCAL ---
  const handleOpenLocalDialog = (local?: Local) => {
    if (local) {
      const localTyped = local as LocalComPerfil
      setEditingLocal(localTyped)
      setLocalFormData(localTyped)
    } else {
      setEditingLocal(null)
      setLocalFormData({
        nome: "", zona_id: project?.zonas[0]?.id || "", tipo: "padrao",
        area_m2: 0, perimetro_m: 0, pe_direito_m: 2.8
      })
    }
    setIsLocalDialogOpen(true)
  }

  const handleSaveLocal = () => {
    if (!project || !localFormData.nome || !localFormData.zona_id || !localFormData.tipo) {
      toast.error("Preencha todos os campos obrigatórios")
      return
    }
    const payload = {
      ...localFormData,
      area_m2: Number(localFormData.area_m2),
      perimetro_m: Number(localFormData.perimetro_m),
      pe_direito_m: Number(localFormData.pe_direito_m),
      projeto_id: project.id,
      id: editingLocal?.id || crypto.randomUUID(),
      data_criacao: editingLocal?.data_criacao || new Date().toISOString()
    } as Local

    if (editingLocal) {
      updateLocalInProject(project.id, payload)
      toast.success("Local atualizado")
    } else {
      addLocalToProject(project.id, payload)
      toast.success("Local adicionado")
    }
    setIsLocalDialogOpen(false)
  }

  const handleDeleteLocal = (localId: string) => {
    if (!project) return
    if (confirm("Excluir local e todas as cargas associadas?")) {
      removeLocalFromProject(project.id, localId)
      toast.success("Local removido")
    }
  }

  // --- HANDLERS: CARGA (NOVO) ---
  const handleOpenCargaDialog = () => {
    setCargaFormData({
      nome: "",
      local_id: project?.locais[0]?.id || "",
      tipo: "TUG",
      potencia: 100,
      unidade: "VA",
      fator_potencia: 0.8,
      origem: "usuario"
    })
    setIsCargaDialogOpen(true)
  }

  const handleSaveCarga = () => {
    if (!project || !cargaFormData.nome || !cargaFormData.local_id) return
    
    const payload: Carga = {
      id: crypto.randomUUID(),
      projeto_id: project.id,
      local_id: cargaFormData.local_id!,
      nome: cargaFormData.nome!,
      tipo: cargaFormData.tipo || "TUG",
      potencia: Number(cargaFormData.potencia),
      unidade: cargaFormData.unidade as 'W' | 'VA',
      fator_potencia: Number(cargaFormData.fator_potencia),
      origem: "usuario"
    }

    addCargaToProject(project.id, payload)
    toast.success("Carga adicionada manualmente")
    setIsCargaDialogOpen(false)
  }

  const handleDeleteCarga = (cargaId: string) => {
    if(!project) return
    removeCargaFromProject(project.id, cargaId)
    toast.success("Carga removida")
  }

  const handleAutoCargas = () => {
        if (!project) return;

        const confirmacao = confirm(
            `Deseja gerar automaticamente a previsão de cargas para todos os ${project.locais.length} locais conforme NBR 5410?\n\nIsso adicionará TUGs baseadas no perímetro e tipo de cômodo.`
        );

        if (!confirmacao) return;

        let contagem = 0;

        project.locais.forEach(local => {
            // 1. Gera Iluminação (Regra de Área)
            const potIlum = NBR5410_WIZARD.calcularIluminacao(local.area_m2);
            const cargaIlum: Carga = {
            id: crypto.randomUUID(),
            projeto_id: project.id,
            local_id: local.id,
            nome: "Iluminação Central",
            tipo: "Iluminacao",
            potencia: potIlum,
            unidade: 'VA',
            fator_potencia: 1.0,
            origem: 'norma'
            };
            addCargaToProject(project.id, cargaIlum);
            contagem++;

            // 2. Gera TUGs (Regra de Perímetro/Perfil)
            const tugs = NBR5410_WIZARD.calcularTUGs(local);
            tugs.forEach(tug => {
            addCargaToProject(project.id, tug);
            contagem++;
            });
        });

        toast.success(`${contagem} cargas sugeridas pela norma foram adicionadas!`);
    };

  // --- HELPERS ---
  const getZonaInfo = (zonaId: string) => project?.zonas.find(z => z.id === zonaId)
  const getLocalInfo = (localId: string) => project?.locais.find(l => l.id === localId)

  if (!project) return null

  return (
    <div className="flex flex-col gap-6 pb-20">
      {/* HEADER */}
      <div className="flex items-center gap-4 border-b pb-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/")}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{project.nome}</h1>
          <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
            <Badge variant="outline">{project.tipo_instalacao}</Badge>
            <Separator orientation="vertical" className="h-4" />
            <span>{project.sistema} ({project.tensao_sistema})</span>
            <Separator orientation="vertical" className="h-4" />
            <Badge variant="secondary">At: {project.esquema_aterramento || "ND"}</Badge>
          </div>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
          <TabsTrigger value="zonas">1. Ambientes</TabsTrigger>
          <TabsTrigger value="locais">2. Arquitetura</TabsTrigger>
          <TabsTrigger value="cargas">3. Cargas</TabsTrigger>
        </TabsList>

        {/* --- ABA ZONAS --- */}
        <TabsContent value="zonas" className="mt-6 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-medium">Zonas de Influência</h3>
              <p className="text-sm text-muted-foreground">Classificação completa das influências externas.</p>
            </div>
            <Button onClick={() => handleOpenZoneDialog()}><Plus className="mr-2 h-4 w-4" /> Nova Zona</Button>
          </div>
          
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
             {project.zonas.map((zona) => (
                <Card key={zona.id} className="border-l-4" style={{ borderLeftColor: zona.cor_identificacao }}>
                  <CardHeader className="pb-2">
                    <div className="flex justify-between">
                      <CardTitle className="text-base">{zona.nome}</CardTitle>
                      <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => { setEditingZona(zona); setZonaFormData(zona); setIsZoneDialogOpen(true); }}>
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
                    <Button variant="ghost" size="sm" className="text-destructive hover:bg-destructive/10" onClick={() => handleDeleteZona(zona.id)}><Trash2 className="h-4 w-4" /></Button>
                  </CardFooter>
                </Card>
             ))}
          </div>
        </TabsContent>

        {/* --- ABA LOCAIS --- */}
        <TabsContent value="locais" className="mt-6 space-y-4">
           {/* (Mesmo código da Etapa B, mantido por brevidade e consistência) */}
           <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-medium">Cômodos e Áreas</h3>
              <p className="text-sm text-muted-foreground">Definição física e perfil normativo.</p>
            </div>
            <Button onClick={() => handleOpenLocalDialog()} disabled={project.zonas.length === 0}><Plus className="mr-2 h-4 w-4" /> Novo Cômodo</Button>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {project.locais.map((local) => {
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
                      <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => { setEditingLocal(local as LocalComPerfil); setLocalFormData(local as LocalComPerfil); setIsLocalDialogOpen(true); }}><Settings className="h-4 w-4" /></Button>
                    </div>
                  </CardHeader>
                  <CardContent className="pb-2">
                     <div className="grid grid-cols-2 gap-2 text-sm text-muted-foreground">
                        <div className="flex items-center gap-2"><Maximize className="h-3.5 w-3.5" /> {local.area_m2} m²</div>
                        <div className="flex items-center gap-2"><Ruler className="h-3.5 w-3.5" /> {local.perimetro_m} m</div>
                     </div>
                  </CardContent>
                  <CardFooter className="pt-2 justify-end">
                    <Button variant="ghost" size="sm" className="text-destructive hover:bg-destructive/10" onClick={() => handleDeleteLocal(local.id)}><Trash2 className="h-4 w-4" /></Button>
                  </CardFooter>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* --- ABA CARGAS (NOVA) --- */}
        <TabsContent value="cargas" className="mt-6 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-medium">Previsão de Cargas</h3>
              <p className="text-sm text-muted-foreground">Cargas definidas manual ou normativamente.</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleAutoCargas} disabled={project.locais.length === 0}>
                <Zap className="mr-2 h-4 w-4 text-yellow-500" />
                Sugestão NBR 5410
               </Button>
              <Button onClick={handleOpenCargaDialog} disabled={project.locais.length === 0}>
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
                {project.cargas.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                      Nenhuma carga cadastrada. Use "Adicionar Carga" ou a Sugestão NBR.
                    </TableCell>
                  </TableRow>
                ) : (
                  project.cargas.map((carga) => {
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
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => handleDeleteCarga(carga.id)}>
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
        </TabsContent>
      </Tabs>

      {/* DIALOG ZONA (ATUALIZADO) */}
      <Dialog open={isZoneDialogOpen} onOpenChange={setIsZoneDialogOpen}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader><DialogTitle>{editingZona ? "Editar Zona" : "Nova Zona"}</DialogTitle></DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label>Nome</Label>
              <Input value={zonaFormData.nome} onChange={(e) => setZonaFormData({...zonaFormData, nome: e.target.value})} />
            </div>
            
            <Separator className="my-2" />
            <h4 className="text-sm font-medium">Influências Externas (NBR 5410)</h4>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label>Temperatura (AA)</Label>
                <Select value={zonaFormData.temp_ambiente} onValueChange={(v) => setZonaFormData({...zonaFormData, temp_ambiente: v})}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent><SelectItem value="AA1">AA1 (25°C)</SelectItem><SelectItem value="AA2">AA2 (30°C)</SelectItem></SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label>Água (AD)</Label>
                <Select value={zonaFormData.presenca_agua} onValueChange={(v) => setZonaFormData({...zonaFormData, presenca_agua: v})}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent><SelectItem value="AD1">AD1 (Seco)</SelectItem><SelectItem value="AD2">AD2 (Gotas)</SelectItem></SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label>Sólidos (AE)</Label>
                <Select value={zonaFormData.presenca_solidos} onValueChange={(v) => setZonaFormData({...zonaFormData, presenca_solidos: v})}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent><SelectItem value="AE1">AE1 (Desprezível)</SelectItem><SelectItem value="AE2">AE2 (Pequenos)</SelectItem></SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label>Pessoas (BA)</Label>
                <Select value={zonaFormData.competencia_pessoas} onValueChange={(v) => setZonaFormData({...zonaFormData, competencia_pessoas: v})}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent><SelectItem value="BA1">BA1 (Comuns)</SelectItem><SelectItem value="BA4">BA4 (Instruídas)</SelectItem></SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label>Materiais (CA)</Label>
                <Select value={zonaFormData.materiais_construcao} onValueChange={(v) => setZonaFormData({...zonaFormData, materiais_construcao: v})}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent><SelectItem value="CA1">CA1 (Não Combustível)</SelectItem><SelectItem value="CA2">CA2 (Combustível)</SelectItem></SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label>Estrutura (CB)</Label>
                <Select value={zonaFormData.estrutura_edificacao} onValueChange={(v) => setZonaFormData({...zonaFormData, estrutura_edificacao: v})}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent><SelectItem value="CB1">CB1 (Desprezível)</SelectItem><SelectItem value="CB2">CB2 (Móvel)</SelectItem></SelectContent>
                </Select>
              </div>
            </div>
          </div>
          <DialogFooter><Button onClick={handleSaveZona}>Salvar</Button></DialogFooter>
        </DialogContent>
      </Dialog>

      {/* DIALOG LOCAL */}
      <Dialog open={isLocalDialogOpen} onOpenChange={setIsLocalDialogOpen}>
        <DialogContent>
           <DialogHeader><DialogTitle>Editar Local</DialogTitle></DialogHeader>
           <div className="grid gap-4 py-4">
              <div className="grid gap-2"><Label>Nome</Label><Input value={localFormData.nome} onChange={(e) => setLocalFormData({...localFormData, nome: e.target.value})} /></div>
              <div className="grid gap-2">
                 <Label>Perfil Normativo</Label>
                 <Select value={localFormData.tipo} onValueChange={(v:any) => setLocalFormData({...localFormData, tipo: v})}>
                   <SelectTrigger><SelectValue /></SelectTrigger>
                   <SelectContent>
                     <SelectItem value="padrao">Padrão</SelectItem><SelectItem value="cozinha">Cozinha</SelectItem>
                     <SelectItem value="banheiro">Banheiro</SelectItem><SelectItem value="servico">Serviço</SelectItem>
                     <SelectItem value="externo">Externo</SelectItem>
                   </SelectContent>
                 </Select>
              </div>
              <div className="grid gap-2">
                 <Label>Zona</Label>
                 <Select value={localFormData.zona_id} onValueChange={(v) => setLocalFormData({...localFormData, zona_id: v})}>
                   <SelectTrigger><SelectValue /></SelectTrigger>
                   <SelectContent>{project.zonas.map(z => <SelectItem key={z.id} value={z.id}>{z.nome}</SelectItem>)}</SelectContent>
                 </Select>
              </div>
              <div className="grid grid-cols-2 gap-2">
                 <div className="grid gap-2"><Label>Área (m²)</Label><Input type="number" value={localFormData.area_m2} onChange={(e) => setLocalFormData({...localFormData, area_m2: Number(e.target.value)})} /></div>
                 <div className="grid gap-2"><Label>Perímetro (m)</Label><Input type="number" value={localFormData.perimetro_m} onChange={(e) => setLocalFormData({...localFormData, perimetro_m: Number(e.target.value)})} /></div>
              </div>
           </div>
           <DialogFooter><Button onClick={handleSaveLocal}>Salvar</Button></DialogFooter>
        </DialogContent>
      </Dialog>

      {/* DIALOG CARGA MANUAL */}
      <Dialog open={isCargaDialogOpen} onOpenChange={setIsCargaDialogOpen}>
        <DialogContent>
          <DialogHeader><DialogTitle>Nova Carga Manual</DialogTitle></DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label>Nome da Carga</Label>
              <Input placeholder="Ex: Ar Condicionado" value={cargaFormData.nome} onChange={(e) => setCargaFormData({...cargaFormData, nome: e.target.value})} />
            </div>
            <div className="grid gap-2">
              <Label>Local</Label>
              <Select value={cargaFormData.local_id} onValueChange={(v) => setCargaFormData({...cargaFormData, local_id: v})}>
                <SelectTrigger><SelectValue placeholder="Selecione o local" /></SelectTrigger>
                <SelectContent>
                  {project.locais.map(l => <SelectItem key={l.id} value={l.id}>{l.nome}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-4">
               <div className="grid gap-2">
                  <Label>Tipo</Label>
                  <Select value={cargaFormData.tipo} onValueChange={(v) => setCargaFormData({...cargaFormData, tipo: v})}>
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
                     <Input type="number" value={cargaFormData.potencia} onChange={(e) => setCargaFormData({...cargaFormData, potencia: Number(e.target.value)})} />
                     <Select value={cargaFormData.unidade} onValueChange={(v:any) => setCargaFormData({...cargaFormData, unidade: v})}>
                        <SelectTrigger className="w-[80px]"><SelectValue /></SelectTrigger>
                        <SelectContent><SelectItem value="W">W</SelectItem><SelectItem value="VA">VA</SelectItem></SelectContent>
                     </Select>
                  </div>
               </div>
            </div>
          </div>
          <DialogFooter><Button onClick={handleSaveCarga}>Salvar Carga</Button></DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}