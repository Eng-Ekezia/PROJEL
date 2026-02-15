import {
  FolderOpen,
  Settings,
  Zap,
  LayoutDashboard,
  Map,
  MapPin,
  Lightbulb,
  Activity,
  ArrowLeft
} from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
  SidebarRail,
} from "@/components/ui/sidebar"
import { useLocation, useNavigate, matchPath } from "react-router-dom"

export function AppSidebar() {
  const navigate = useNavigate()
  const location = useLocation()

  // 1. Detecção de Contexto: Verifica se a URL corresponde a um projeto
  // Utiliza matchPath para ser robusto e capturar o ID corretamente
  const projectMatch = matchPath("/project/:id/*", location.pathname)
  const projectId = projectMatch?.params.id

  // 2. Definição dos Menus

  // Menu Global (App Home)
  const mainNav = [
    {
      title: "Meus Projetos",
      url: "/",
      icon: FolderOpen,
    },
    {
      title: "Configurações",
      url: "/settings",
      icon: Settings,
    },
  ]

  // Menu de Ferramentas do Projeto
  // Segue estritamente a hierarquia do architecture.md: Projeto > Zona > Local > Carga > Circuito
  const projectNav = projectId ? [
    {
      title: "Visão Geral",
      url: `/project/${projectId}`,
      icon: LayoutDashboard,
    },
    {
      title: "Zonas",
      url: `/project/${projectId}/zonas`,
      icon: Map,
    },
    {
      title: "Locais",
      url: `/project/${projectId}/locais`,
      icon: MapPin,
    },
    {
      title: "Cargas",
      url: `/project/${projectId}/cargas`,
      icon: Lightbulb,
    },
    {
      title: "Circuitos",
      url: `/project/${projectId}/circuitos`,
      icon: Activity,
    },
  ] : []

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-2 text-sidebar-accent-foreground">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Zap className="size-5" />
          </div>
          <div className="flex flex-col gap-0.5 leading-none">
            <span className="font-semibold">PROJEL</span>
            <span className="text-xs text-muted-foreground">v0.8.0</span>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        {/* Renderização Condicional baseada na presença do projectId */}
        {projectId ? (
          <SidebarGroup>
            <SidebarGroupLabel>Projeto Atual</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {projectNav.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      onClick={() => navigate(item.url)}
                      tooltip={item.title}
                      isActive={location.pathname === item.url} // Highlight da rota ativa
                    >
                      <item.icon />
                      <span>{item.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ) : (
          <SidebarGroup>
            <SidebarGroupLabel>Principal</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {mainNav.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      onClick={() => navigate(item.url)}
                      tooltip={item.title}
                      isActive={location.pathname === item.url}
                    >
                      <item.icon />
                      <span>{item.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        )}
      </SidebarContent>

      <SidebarFooter>
        {projectId && (
           <SidebarMenu>
             <SidebarMenuItem>
               <SidebarMenuButton
                 onClick={() => navigate("/")}
                 tooltip="Voltar aos Projetos"
                 className="text-muted-foreground hover:text-foreground"
               >
                 <ArrowLeft />
                 <span>Trocar de Projeto</span>
               </SidebarMenuButton>
             </SidebarMenuItem>
           </SidebarMenu>
        )}
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}