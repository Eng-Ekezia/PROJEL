import { Outlet } from "react-router-dom"
import { SidebarProvider, SidebarTrigger, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Separator } from "@/components/ui/separator"
import { Toaster } from "@/components/ui/sonner"

export default function AppLayout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <div className="flex items-center gap-2 text-sm font-medium">
            <span className="text-muted-foreground">Área de Trabalho</span>
          </div>
        </header>
        
        {/* Aqui é onde as páginas (Dashboard, ProjectDetails) serão renderizadas */}
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <Outlet /> 
        </div>
      </SidebarInset>
      <Toaster /> {/* Notificações Toast globais */}
    </SidebarProvider>
  )
}