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

  // Circuito Actions (FASE 08)
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
      
      // --- PROJECT IMPLEMENTATION ---
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

      // --- CIRCUITO IMPLEMENTATION (FASE 08) ---
      addCircuitoToProject: (pId, circuito) => {
        const state = get();
        const project = state.projects.find(p => p.id === pId);
        
        if (!project) return;

        // VALIDAÇÃO 1: Identificador Único
        const duplicado = project.circuitos?.some(c => 
            c.identificador.trim().toUpperCase() === circuito.identificador.trim().toUpperCase()
        );

        if (duplicado) {
            toast.error(`Já existe um circuito com o identificador "${circuito.identificador}".`);
            return; 
        }

        set((state) => ({
            projects: state.projects.map(p => p.id === pId ? { 
                ...p, 
                circuitos: [...(p.circuitos || []), circuito] 
            } : p)
        }));
      },
      
      updateCircuitoInProject: (pId, circuito) => {
        const state = get();
        const project = state.projects.find(p => p.id === pId);
        if (!project) return;

        // Validação de Duplicidade (ignorando o próprio ID)
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
                ...p, 
                circuitos: p.circuitos.map(c => c.id === circuito.id ? circuito : c)
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

      // HELPER: Drag-and-Drop com Soft Validation
      setCargaCircuit: (pId, cargaId, circuitoId) => {
        const state = get();
        const project = state.projects.find(p => p.id === pId);
        if (!project) return;

        // Caso 1: Desassociação (Remover do circuito)
        if (circuitoId === null) {
             set((state) => ({
                projects: state.projects.map(p => p.id === pId ? {
                    ...p,
                    cargas: p.cargas.map(c => c.id === cargaId ? { ...c, circuito_id: null } : c)
                } : p)
             }));
             return;
        }

        const circuito = project.circuitos?.find(c => c.id === circuitoId);
        const carga = project.cargas.find(c => c.id === cargaId);

        if (!circuito || !carga) return;

        // --- VERIFICAÇÃO SUAVE (SOFT VALIDATION) ---
        // Alerta sobre boas práticas, mas obedece ao engenheiro.
        
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

        // Se houver aviso, notifica mas NÃO impede
        if (aviso) {
            toast.warning(aviso, {
                duration: 5000, 
                action: {
                    label: "Entendi",
                    onClick: () => console.log("Engenheiro ciente do aviso")
                }
            });
        } else {
            // Feedback positivo discreto
            toast.success("Carga atribuída", { duration: 1500 });
        }

        // --- EXECUÇÃO DA AÇÃO (Soberania do Engenheiro) ---
        set((state) => ({
            projects: state.projects.map(p => p.id === pId ? {
                ...p,
                cargas: p.cargas.map(c => c.id === cargaId ? { ...c, circuito_id: circuitoId } : c)
            } : p)
        }));
      },

    }),
    { name: 'projel-storage' }
  )
);