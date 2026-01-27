import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Projeto, Zona, Local, Carga } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  addProject: (project: Projeto) => void;
  updateProject: (id: string, data: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  
  addZonaToProject: (projetoId: string, zona: Zona) => void;
  addLocalToProject: (projetoId: string, local: Local) => void;
  
  // NOVAS AÇÕES (OBRIGATÓRIAS)
  addCargaToProject: (projetoId: string, carga: Carga) => void;
  removeCargaFromProject: (projetoId: string, cargaId: string) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set) => ({
      projects: [],
      
      addProject: (project) => set((state) => ({ 
        projects: [...state.projects, { ...project, zonas: [], locais: [], cargas: [] }] 
      })),

      updateProject: (id, data) => set((state) => ({
        projects: state.projects.map((p) => (p.id === id ? { ...p, ...data, ultima_modificacao: new Date().toISOString() } : p)),
      })),

      deleteProject: (id) => set((state) => ({
        projects: state.projects.filter((p) => p.id !== id),
      })),

      addZonaToProject: (projetoId, zona) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const zonasAtuais = p.zonas || [];
          return { ...p, zonas: [...zonasAtuais, zona], ultima_modificacao: new Date().toISOString() };
        })
      })),

      addLocalToProject: (projetoId, local) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const locaisAtuais = p.locais || [];
          return { ...p, locais: [...locaisAtuais, local], ultima_modificacao: new Date().toISOString() };
        })
      })),

      addCargaToProject: (projetoId, carga) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const cargasAtuais = p.cargas || [];
          return { ...p, cargas: [...cargasAtuais, carga], ultima_modificacao: new Date().toISOString() };
        })
      })),

      removeCargaFromProject: (projetoId, cargaId) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          return { 
            ...p, 
            cargas: (p.cargas || []).filter(c => c.id !== cargaId), 
            ultima_modificacao: new Date().toISOString() 
          };
        })
      })),
    }),
    {
      name: 'projel-storage',
    }
  )
);