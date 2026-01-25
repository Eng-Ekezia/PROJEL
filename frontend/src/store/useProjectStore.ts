import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { Projeto } from '../types/project';

interface ProjectState {
  // Estado
  projects: Projeto[];
  activeProjectId: string | null;
  
  // Ações (Commands)
  addProject: (project: Projeto) => void;
  updateProject: (id: string, updatedData: Partial<Projeto>) => void;
  deleteProject: (id: string) => void;
  setActiveProject: (id: string | null) => void;
  
  // Seletores (Queries)
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
          activeProjectId: project.id // Seleciona automaticamente ao criar
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
          // Se o projeto deletado estava ativo, remove a seleção
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