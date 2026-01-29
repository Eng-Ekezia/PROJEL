import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Projeto, Zona, Local, Carga } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  addProject: (project: Projeto) => void;
  updateProject: (id: string, data: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  
  // ZONAS
  addZonaToProject: (projetoId: string, zona: Zona) => void;
  updateZonaInProject: (projetoId: string, zonaId: string, zona: Zona) => void;
  removeZonaFromProject: (projetoId: string, zonaId: string) => void;

  // LOCAIS
  addLocalToProject: (projetoId: string, local: Local) => void;
  updateLocalInProject: (projetoId: string, localId: string, local: Local) => void;
  removeLocalFromProject: (projetoId: string, localId: string) => void;
  
  // CARGAS
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

      // --- ZONAS ---
      addZonaToProject: (projetoId, zona) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const zonasAtuais = p.zonas || [];
          return { ...p, zonas: [...zonasAtuais, zona], ultima_modificacao: new Date().toISOString() };
        })
      })),

      updateZonaInProject: (projetoId, zonaId, zonaAtualizada) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          return {
             ...p,
             zonas: p.zonas.map(z => z.id === zonaId ? zonaAtualizada : z),
             ultima_modificacao: new Date().toISOString()
          };
        })
      })),

      removeZonaFromProject: (projetoId, zonaId) => set((state) => ({
        projects: state.projects.map(p => {
            if (p.id !== projetoId) return p;
            return {
                ...p,
                zonas: p.zonas.filter(z => z.id !== zonaId),
                ultima_modificacao: new Date().toISOString()
            };
        })
      })),

      // --- LOCAIS ---
      addLocalToProject: (projetoId, local) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          const locaisAtuais = p.locais || [];
          return { ...p, locais: [...locaisAtuais, local], ultima_modificacao: new Date().toISOString() };
        })
      })),

      updateLocalInProject: (projetoId, localId, localAtualizado) => set((state) => ({
        projects: state.projects.map(p => {
          if (p.id !== projetoId) return p;
          return {
             ...p,
             locais: (p.locais || []).map(l => l.id === localId ? localAtualizado : l),
             ultima_modificacao: new Date().toISOString()
          };
        })
      })),

      removeLocalFromProject: (projetoId, localId) => set((state) => ({
        projects: state.projects.map(p => {
            if (p.id !== projetoId) return p;
            return {
                ...p,
                locais: (p.locais || []).filter(l => l.id !== localId),
                ultima_modificacao: new Date().toISOString()
            };
        })
      })),

      // --- CARGAS ---
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