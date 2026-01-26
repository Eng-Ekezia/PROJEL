import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Projeto, Zona, Local } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  addProject: (project: Projeto) => void;
  updateProject: (id: string, data: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  
  // Actions da Fase 06
  addZonaToProject: (projetoId: string, zona: Zona) => void;
  addLocalToProject: (projetoId: string, local: Local) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set) => ({
      projects: [],
      
      addProject: (project) => set((state) => ({ 
        projects: [...state.projects, { ...project, zonas: [], locais: [] }] 
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
    }),
    {
      name: 'projel-storage',
    }
  )
);