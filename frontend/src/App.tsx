import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from '@/layouts/AppLayout';

// Pages
import Dashboard from './pages/Dashboard';
import ProjectDetails from './pages/ProjectDetails';

function App() {
  return (
    <Router>
      <Routes>
        {/* Rotas que ficam DENTRO do Layout com Sidebar */}
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/project/:id" element={<ProjectDetails />} />
        </Route>

        {/* Rotas soltas (Ex: Login) ficariam fora do AppLayout */}
      </Routes>
    </Router>
  );
}

export default App;