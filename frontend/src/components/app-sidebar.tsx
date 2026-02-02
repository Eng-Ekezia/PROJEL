import { Home, Plus, FolderOpen, Settings, Zap } from "lucide-react"
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
} from "@/components/ui/sidebar"
import { useNavigate } from "react-router-dom"

export function AppSidebar() {
  const navigate = useNavigate()

  const items = [
    {
      title: "Meus Projetos",
      url: "/",
      icon: FolderOpen,
    },
    {
      title: "Configurações",
      url: "/settings", // Placeholder
      icon: Settings,
    },
  ]

  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-2">
           <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
             <Zap className="size-5" />
           </div>
           <div className="flex flex-col gap-0.5 leading-none">
             <span className="font-semibold">PROJEL</span>
             <span className="text-xs text-muted-foreground">v0.1.0</span>
           </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Menu</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    onClick={() => navigate(item.url)}
                    tooltip={item.title}
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}