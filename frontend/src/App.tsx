import { Routes, Route } from "react-router-dom";
import AppLayout from "@/layouts/AppLayout";
import Dashboard from "@/pages/Dashboard";
import ProjectDetails from "@/pages/ProjectDetails";
import ZonesPage from "@/pages/project/ZonesPage";
import LocaisPage from "@/pages/project/LocaisPage";
import CargasPage from "@/pages/project/CargasPage"; // Importação Nova

// Componente temporário final
const TempPage = ({ title }: { title: string }) => (
  <div className="flex flex-col gap-4 p-4">
    <div className="rounded-lg border border-dashed p-8 text-center">
      <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      <p className="text-muted-foreground">Em construção...</p>
    </div>
  </div>
);

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        
        <Route path="/project/:id">
          <Route index element={<ProjectDetails />} />
          <Route path="zonas" element={<ZonesPage />} />
          <Route path="locais" element={<LocaisPage />} />
          
          {/* Rota Atualizada */}
          <Route path="cargas" element={<CargasPage />} />
          
          <Route path="circuitos" element={<TempPage title="Dimensionamento de Circuitos" />} />
        </Route>

        <Route path="*" element={<div className="p-8">Página não encontrada</div>} />
      </Route>
    </Routes>
  );
}

export default App;