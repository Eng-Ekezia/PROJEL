import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Projeto } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  activeProjectId: string | null;
  
  // Actions
  addProject: (project: Projeto) => void;
  deleteProject: (id: string) => void;
  setActiveProject: (id: string | null) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set) => ({
      projects: [],
      activeProjectId: null,

      addProject: (project) => 
        set((state) => ({ 
          projects: [...state.projects, project] 
        })),

      deleteProject: (id) => 
        set((state) => ({ 
          projects: state.projects.filter((p) => p.id !== id) 
        })),

      setActiveProject: (id) => 
        set({ activeProjectId: id }),
    }),
    {
      name: 'projel-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);