import { Routes, Route } from "react-router-dom";
import AppLayout from "@/layouts/AppLayout";
import Dashboard from "@/pages/Dashboard";
import ProjectDetails from "@/pages/ProjectDetails";
import ZonesPage from "@/pages/project/ZonesPage";
import LocaisPage from "@/pages/project/LocaisPage";
import CargasPage from "@/pages/project/CargasPage";
import CircuitosPage from "@/pages/project/CircuitosPage"; // Importação Final

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        
        <Route path="/project/:id">
          {/* A rota index ainda aponta para o antigo ProjectDetails (Overview) 
              Fase 09 não exigiu refatorar o Dashboard interno, apenas a navegação */}
          <Route index element={<ProjectDetails />} />
          
          <Route path="zonas" element={<ZonesPage />} />
          <Route path="locais" element={<LocaisPage />} />
          <Route path="cargas" element={<CargasPage />} />
          
          {/* Rota Finalizada */}
          <Route path="circuitos" element={<CircuitosPage />} />
        </Route>

        <Route path="*" element={<div className="p-8">Página não encontrada</div>} />
      </Route>
    </Routes>
  );
}

export default App;