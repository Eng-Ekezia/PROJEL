import { create } from 'zustand';
import { persist } from 'zustand/middleware';
// FIX: Usando 'import type' para satisfazer verbatimModuleSyntax
import type { Projeto, Zona, Local, Carga } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  
  // Project Actions
  createProject: (project: Projeto) => void;
  updateProject: (project: Projeto) => void; // FIX: Adicionado
  deleteProject: (id: string) => void;
  
  // Zona Actions
  addZonaToProject: (projectId: string, zona: Zona) => void;
  updateZonaInProject: (projectId: string, zona: Zona) => void;
  removeZonaFromProject: (projectId: string, zonaId: string) => void;
  
  // Local Actions
  addLocalToProject: (projectId: string, local: Local) => void;
  updateLocalInProject: (projectId: string, local: Local) => void;
  removeLocalFromProject: (projectId: string, localId: string) => void;

  // Carga Actions
  addCargaToProject: (projectId: string, carga: Carga) => void;
  updateCargaInProject: (projectId: string, carga: Carga) => void;
  removeCargaFromProject: (projectId: string, cargaId: string) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set) => ({
      projects: [],
      
      // --- PROJECT IMPLEMENTATION ---
      createProject: (project) => set((state) => ({ 
          projects: [...state.projects, project] 
      })),
      updateProject: (project) => set((state) => ({
          projects: state.projects.map(p => p.id === project.id ? project : p)
      })),
      deleteProject: (id) => set((state) => ({ 
          projects: state.projects.filter(p => p.id !== id) 
      })),
      
      // --- ZONA IMPLEMENTATION ---
      addZonaToProject: (pId, zona) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, zonas: [...p.zonas, zona] } : p)
      })),
      updateZonaInProject: (pId, zona) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { 
            ...p, zonas: p.zonas.map(z => z.id === zona.id ? zona : z) 
        } : p)
      })),
      removeZonaFromProject: (pId, zId) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, zonas: p.zonas.filter(z => z.id !== zId) } : p)
      })),

      // --- LOCAL IMPLEMENTATION ---
      addLocalToProject: (pId, local) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, locais: [...p.locais, local] } : p)
      })),
      updateLocalInProject: (pId, local) => set((state) => ({
         projects: state.projects.map(p => p.id === pId ? {
             ...p, locais: p.locais.map(l => l.id === local.id ? local : l)
         } : p)
      })),
      removeLocalFromProject: (pId, lId) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, locais: p.locais.filter(l => l.id !== lId) } : p)
      })),

      // --- CARGA IMPLEMENTATION ---
      addCargaToProject: (pId, carga) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, cargas: [...p.cargas, carga] } : p)
      })),
      updateCargaInProject: (pId, carga) => set((state) => ({
          projects: state.projects.map(p => p.id === pId ? {
              ...p, cargas: p.cargas.map(c => c.id === carga.id ? carga : c)
          } : p)
      })),
      removeCargaFromProject: (pId, cId) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, cargas: p.cargas.filter(c => c.id !== cId) } : p)
      })),
    }),
    { name: 'projel-storage' }
  )
);