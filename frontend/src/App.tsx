import { Routes, Route } from "react-router-dom";
import AppLayout from "@/layouts/AppLayout";
import Dashboard from "@/pages/Dashboard";
// REMOVIDO: import ProjectDetails from "@/pages/ProjectDetails";
import OverviewPage from "@/pages/project/OverviewPage"; // NOVA PÁGINA
import ZonesPage from "@/pages/project/ZonesPage";
import LocaisPage from "@/pages/project/LocaisPage";
import CargasPage from "@/pages/project/CargasPage";
import CircuitosPage from "@/pages/project/CircuitosPage";

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        
        <Route path="/project/:id">
          {/* Index agora aponta para o Dashboard do Projeto */}
          <Route index element={<OverviewPage />} />
          
          <Route path="zonas" element={<ZonesPage />} />
          <Route path="locais" element={<LocaisPage />} />
          <Route path="cargas" element={<CargasPage />} />
          <Route path="circuitos" element={<CircuitosPage />} />
        </Route>

        <Route path="*" element={<div className="p-8">Página não encontrada</div>} />
      </Route>
    </Routes>
  );
}

export default App;