import { Routes, Route } from "react-router-dom";
import AppLayout from "@/layouts/AppLayout";
import Dashboard from "@/pages/Dashboard";
import OverviewPage from "@/pages/project/OverviewPage";
import ZonesPage from "@/pages/project/ZonesPage";
import LocaisPage from "@/pages/project/LocaisPage";
import CargasPage from "@/pages/project/CargasPage";
import PropostasPage from "@/pages/project/PropostasPage"; // [NOVO] Importado
import CircuitosPage from "@/pages/project/CircuitosPage";

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        
        <Route path="/project/:id">
          <Route index element={<OverviewPage />} />
          
          {/* ORDEM OBRIGATÓRIA DA NBR 5410 NO PROJEL */}
          <Route path="zonas" element={<ZonesPage />} />
          <Route path="locais" element={<LocaisPage />} />
          <Route path="cargas" element={<CargasPage />} />
          
          {/* [NOVO] A Área de Rascunho entra aqui antes do compromisso do Circuito */}
          <Route path="propostas" element={<PropostasPage />} />
          
          <Route path="circuitos" element={<CircuitosPage />} />
        </Route>

        <Route path="*" element={<div className="p-8">Página não encontrada</div>} />
      </Route>
    </Routes>
  );
}

export default App;