import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Projeto } from '../types/project'; // ADICIONADO 'type'

interface ProjectState {
  projects: Projeto[];
  activeProjectId: string | null;
  
  addProject: (project: Projeto) => void;
  updateProject: (id: string, updatedData: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  setActiveProject: (id: string | null) => void;
  getActiveProject: () => Projeto | undefined;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set, get) => ({
      projects: [],
      activeProjectId: null,

      addProject: (project) => 
        set((state) => ({ 
          projects: [...state.projects, project],
          activeProjectId: project.id
        })),

      updateProject: (id, updatedData) =>
        set((state) => ({
          projects: state.projects.map((p) => 
            p.id === id 
              ? { ...p, ...updatedData, ultima_modificacao: new Date().toISOString() } 
              : p
          )
        })),

      deleteProject: (id) => 
        set((state) => ({ 
          projects: state.projects.filter((p) => p.id !== id),
          activeProjectId: state.activeProjectId === id ? null : state.activeProjectId
        })),

      setActiveProject: (id) => 
        set({ activeProjectId: id }),

      getActiveProject: () => {
        const state = get();
        return state.projects.find((p) => p.id === state.activeProjectId);
      }
    }),
    {
      name: 'projel-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);