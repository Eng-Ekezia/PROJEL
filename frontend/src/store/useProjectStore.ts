import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { toast } from "sonner"; 
import type { Projeto, Zona, Local, Carga, Circuito } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  
  // Project Actions
  setProjects: (projects: Projeto[]) => void;
  addProject: (project: Projeto) => void;
  updateProject: (project: Projeto) => void;
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

  // Circuito Actions
  addCircuitoToProject: (projectId: string, circuito: Circuito) => void;
  updateCircuitoInProject: (projectId: string, circuito: Circuito) => void;
  removeCircuitoFromProject: (projectId: string, circuitoId: string) => void;
  
  // Helpers de Associação
  setCargaCircuit: (projectId: string, cargaId: string, circuitoId: string | null) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set, get) => ({
      projects: [],
      
      setProjects: (projects) => set({ projects }),
      
      addProject: (project) => set((state) => ({ 
          projects: [...state.projects, { ...project, circuitos: [] }] 
      })),

      updateProject: (project) => set((state) => ({
          projects: state.projects.map(p => p.id === project.id ? project : p)
      })),
      
      deleteProject: (id) => set((state) => ({ 
          projects: state.projects.filter(p => p.id !== id) 
      })),
      
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

      // --- CARGA IMPLEMENTATION (Refatorada Fase 10) ---
      addCargaToProject: (pId, carga) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project) return state;

        // Garantia de Integridade: Injeção de zona_id herdada
        const finalCarga = { ...carga };
        if (!finalCarga.zona_id) {
            const local = project.locais.find(l => l.id === finalCarga.local_id);
            if (local) finalCarga.zona_id = local.zona_id;
        }

        return {
          projects: state.projects.map(p => p.id === pId ? { ...p, cargas: [...p.cargas, finalCarga] } : p)
        };
      }),

      updateCargaInProject: (pId, carga) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project) return state;

        // Garantia de Integridade: Injeção de zona_id herdada ao atualizar
        const finalCarga = { ...carga };
        if (!finalCarga.zona_id) {
            const local = project.locais.find(l => l.id === finalCarga.local_id);
            if (local) finalCarga.zona_id = local.zona_id;
        }

        return {
          projects: state.projects.map(p => p.id === pId ? {
              ...p, cargas: p.cargas.map(c => c.id === finalCarga.id ? finalCarga : c)
          } : p)
        };
      }),

      removeCargaFromProject: (pId, cId) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, cargas: p.cargas.filter(c => c.id !== cId) } : p)
      })),

      // --- CIRCUITO IMPLEMENTATION ---
      addCircuitoToProject: (pId, circuito) => {
        const state = get();
        const project = state.projects.find(p => p.id === pId);
        if (!project) return;

        const duplicado = project.circuitos?.some(c => 
            c.identificador.trim().toUpperCase() === circuito.identificador.trim().toUpperCase()
        );

        if (duplicado) {
            toast.error(`Já existe um circuito com o identificador "${circuito.identificador}".`);
            return; 
        }

        set((state) => ({
            projects: state.projects.map(p => p.id === pId ? { 
                ...p, circuitos: [...(p.circuitos || []), circuito] 
            } : p)
        }));
      },
      
      updateCircuitoInProject: (pId, circuito) => {
        const state = get();
        const project = state.projects.find(p => p.id === pId);
        if (!project) return;

        const duplicado = project.circuitos?.some(c => 
            c.id !== circuito.id && 
            c.identificador.trim().toUpperCase() === circuito.identificador.trim().toUpperCase()
        );

        if (duplicado) {
            toast.error(`Já existe outro circuito com o ID "${circuito.identificador}".`);
            return;
        }

        set((state) => ({
            projects: state.projects.map(p => p.id === pId ? {
                ...p, circuitos: p.circuitos.map(c => c.id === circuito.id ? circuito : c)
            } : p)
        }));
      },
      
      removeCircuitoFromProject: (pId, cId) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { 
            ...p, 
            circuitos: p.circuitos.filter(c => c.id !== cId),
            cargas: p.cargas.map(carga => 
              carga.circuito_id === cId ? { ...carga, circuito_id: null } : carga
            )
        } : p)
      })),

      setCargaCircuit: (pId, cargaId, circuitoId) => {
        const state = get();
        const project = state.projects.find(p => p.id === pId);
        if (!project) return;

        if (circuitoId === null) {
             set((state) => ({
                projects: state.projects.map(p => p.id === pId ? {
                    ...p, cargas: p.cargas.map(c => c.id === cargaId ? { ...c, circuito_id: null } : c)
                } : p)
             }));
             return;
        }

        const circuito = project.circuitos?.find(c => c.id === circuitoId);
        const carga = project.cargas.find(c => c.id === cargaId);

        if (!circuito || !carga) return;

        const tipoCircuito = circuito.tipo_circuito.toLowerCase();
        const tipoCarga = carga.tipo.toLowerCase();
        let aviso = null;

        const isIluminacao = tipoCircuito.includes('iluminacao');
        const isTug = tipoCircuito.includes('tomadas') && !tipoCircuito.includes('especifico');
        const isTue = tipoCircuito.includes('especifico');

        if (isIluminacao && tipoCarga !== 'iluminacao') {
            aviso = "Atenção: Misturar tomadas em circuito de iluminação requer cuidados (ver NBR 5410 9.5.3).";
        } else if (isTug && tipoCarga !== 'tug') {
             aviso = "Nota: Carga não classificada como TUG em circuito de TUG.";
        } else if (isTue && tipoCarga !== 'tue' && tipoCarga !== 'motor') {
             aviso = "Nota: Circuito TUE geralmente atende cargas específicas.";
        }

        if (aviso) {
            toast.warning(aviso, { duration: 5000 });
        } else {
            toast.success("Carga atribuída", { duration: 1500 });
        }

        set((state) => ({
            projects: state.projects.map(p => p.id === pId ? {
                ...p, cargas: p.cargas.map(c => c.id === cargaId ? { ...c, circuito_id: circuitoId } : c)
            } : p)
        }));
      },

    }),
    { name: 'projel-storage' }
  )
);