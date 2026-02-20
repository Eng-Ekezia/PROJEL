import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { toast } from "sonner"; 
import type { Projeto, Zona, Local, Carga, Circuito, PropostaCircuito, PreCircuito } from '../types/project';

interface ProjectState {
  projects: Projeto[];
  
  setProjects: (projects: Projeto[]) => void;
  addProject: (project: Projeto) => void;
  updateProject: (project: Projeto) => void;
  deleteProject: (id: string) => void;
  
  addZonaToProject: (projectId: string, zona: Zona) => void;
  updateZonaInProject: (projectId: string, zona: Zona) => void;
  removeZonaFromProject: (projectId: string, zonaId: string) => void;
  
  addLocalToProject: (projectId: string, local: Local) => void;
  updateLocalInProject: (projectId: string, local: Local) => void;
  removeLocalFromProject: (projectId: string, localId: string) => void;

  addCargaToProject: (projectId: string, carga: Carga) => void;
  updateCargaInProject: (projectId: string, carga: Carga) => void;
  removeCargaFromProject: (projectId: string, cargaId: string) => void;

  addPropostaToProject: (projectId: string, proposta: PropostaCircuito) => void;
  updatePropostaInProject: (projectId: string, proposta: PropostaCircuito) => void;
  removePropostaFromProject: (projectId: string, propostaId: string) => void;

  // [NOVO] Gestão da Prancheta (Kanban)
  setPreCircuitosInProject: (projectId: string, preCircuitos: PreCircuito[]) => void;

  addCircuitoToProject: (projectId: string, circuito: Circuito) => void;
  updateCircuitoInProject: (projectId: string, circuito: Circuito) => void;
  removeCircuitoFromProject: (projectId: string, circuitoId: string) => void;
  
  converterPropostaEmCircuito: (projectId: string, propostaId: string, dadosCircuito: Partial<Circuito>) => void;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set, get) => ({
      projects: [],
      
      setProjects: (projects) => set({ projects }),
      
      addProject: (project) => set((state) => ({ 
          projects: [...state.projects, { ...project, circuitos: [], propostas: [], pre_circuitos: [] }] 
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

      addLocalToProject: (pId, local) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, locais: [...p.locais, local] } : p)
      })),
      
      updateLocalInProject: (pId, local) => set((state) => ({
         projects: state.projects.map(p => p.id === pId ? {
             ...p, locais: p.locais.map(l => l.id === local.id ? local : l)
         } : p)
      })),
      
      removeLocalFromProject: (pId, lId) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project) return state;

        // 1. Encontra todas as cargas deste local para apagar em cascata
        const cargasIdsToRemove = project.cargas.filter(c => c.local_id === lId).map(c => c.id);

        // 2. Remove local e as suas cargas
        const newLocais = project.locais.filter(l => l.id !== lId);
        const newCargas = project.cargas.filter(c => c.local_id !== lId);

        // 3. Limpa referências nos Pré-Circuitos (Kanban)
        const newPreCircuitos = (project.pre_circuitos || []).map(pc => ({
          ...pc,
          cargas_ids: pc.cargas_ids.filter(id => !cargasIdsToRemove.includes(id))
        }));

        // 4. Limpa referências nos Circuitos e aciona o GARBAGE COLLECTOR
        const circuitosAntes = project.circuitos || [];
        const newCircuitos = circuitosAntes
          .map(circuito => ({
             ...circuito,
             cargas_ids: circuito.cargas_ids.filter(id => !cargasIdsToRemove.includes(id))
          }))
          .filter(circuito => circuito.cargas_ids.length > 0);

        // [NOVO] ALERTA DIDÁTICO
        const circuitosRemovidos = circuitosAntes.filter(cAntes => !newCircuitos.some(cDepois => cDepois.id === cAntes.id));
        if (circuitosRemovidos.length > 0) {
            const nomes = circuitosRemovidos.map(c => c.identificador).join(", ");
            // setTimeout usado para garantir que o toast dispara fora do ciclo principal de renderização do Zustand
            setTimeout(() => toast.info(`Didática NBR 5410: Os circuitos (${nomes}) foram desfeitos automaticamente pois ficaram sem cargas.`), 0);
        }

        return {
          projects: state.projects.map(p => p.id === pId ? { 
              ...p, 
              locais: newLocais,
              cargas: newCargas,
              pre_circuitos: newPreCircuitos,
              circuitos: newCircuitos
          } : p)
        };
      }),

      // --- CARGA IMPLEMENTATION ---
      addCargaToProject: (pId, carga) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project) return state;

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

      removeCargaFromProject: (pId, cId) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project) return state;

        // 1. Remove a carga
        const newCargas = project.cargas.filter(c => c.id !== cId);

        // 2. Limpa dos Pré-Circuitos
        const newPreCircuitos = (project.pre_circuitos || []).map(pc => ({
          ...pc,
          cargas_ids: pc.cargas_ids.filter(id => id !== cId)
        }));

        // 3. Limpa dos Circuitos Definitivos e aciona o GARBAGE COLLECTOR
        const circuitosAntes = project.circuitos || [];
        const newCircuitos = circuitosAntes
          .map(circuito => ({
             ...circuito,
             cargas_ids: circuito.cargas_ids.filter(id => id !== cId)
          }))
          .filter(circuito => circuito.cargas_ids.length > 0);

        // [NOVO] ALERTA DIDÁTICO
        const circuitosRemovidos = circuitosAntes.filter(cAntes => !newCircuitos.some(cDepois => cDepois.id === cAntes.id));
        if (circuitosRemovidos.length > 0) {
            const nomes = circuitosRemovidos.map(c => c.identificador).join(", ");
            setTimeout(() => toast.info(`Didática NBR 5410: O circuito ${nomes} foi desfeito automaticamente pois a sua única carga foi apagada.`), 0);
        }

        return {
          projects: state.projects.map(p => p.id === pId ? { 
              ...p, 
              cargas: newCargas, 
              pre_circuitos: newPreCircuitos,
              circuitos: newCircuitos 
          } : p)
        };
      }),

      // --- PROPOSTA DE CIRCUITO IMPLEMENTATION ---
      addPropostaToProject: (pId, proposta) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project) return state;
        const propostasAtuais = project.propostas || [];
        return {
          projects: state.projects.map(p => p.id === pId ? { 
            ...p, propostas: [...propostasAtuais, proposta] 
          } : p)
        };
      }),

      updatePropostaInProject: (pId, proposta) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project || !project.propostas) return state;
        return {
          projects: state.projects.map(p => p.id === pId ? {
              ...p, propostas: p.propostas!.map(prop => prop.id === proposta.id ? proposta : prop)
          } : p)
        };
      }),

      removePropostaFromProject: (pId, propostaId) => set((state) => {
        const project = state.projects.find(p => p.id === pId);
        if (!project || !project.propostas) return state;
        return {
          projects: state.projects.map(p => p.id === pId ? { 
            ...p, propostas: p.propostas!.filter(prop => prop.id !== propostaId) 
          } : p)
        };
      }),

      // [NOVO] Implementação da Prancheta
      setPreCircuitosInProject: (pId, preCircuitos) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { ...p, pre_circuitos: preCircuitos } : p)
      })),

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
      
      // Ao deletar o circuito, ele simplesmente deixa de existir. As cargas voltam a ficar "órfãs" de circuito_id naturalmente.
      // E a proposta original continua salva na lista de propostas com o status "aceita" (ou poderíamos reverter o status, 
      // mas mantê-la como histórico é mais seguro).
      removeCircuitoFromProject: (pId, cId) => set((state) => ({
        projects: state.projects.map(p => p.id === pId ? { 
            ...p, 
            circuitos: p.circuitos.filter(c => c.id !== cId)
        } : p)
      })),

      converterPropostaEmCircuito: (pId, propostaId, dadosCircuito) => {
        set((state) => {
          const project = state.projects.find(p => p.id === pId);
          if (!project || !project.propostas) return state;

          const propostaIndex = project.propostas.findIndex(p => p.id === propostaId);
          if (propostaIndex === -1) return state;

          const proposta = project.propostas[propostaIndex];

          // 1. Validação estrita do Identificador
          const idPadronizado = dadosCircuito.identificador?.trim().toUpperCase();
          if (!idPadronizado) {
              toast.error("O identificador do circuito é obrigatório.");
              return state;
          }

          const duplicado = project.circuitos?.some(c => c.identificador === idPadronizado);
          
          if (duplicado) {
            toast.error(`O identificador "${idPadronizado}" já está em uso neste projeto.`);
            return state; 
          }

          const novoCircuito = {
            ...dadosCircuito,
            id: crypto.randomUUID(),
            identificador: idPadronizado,
            projeto_id: pId,
            proposta_id: proposta.id,
            cargas_ids: [...proposta.cargas_ids], 
            snapshot_proposta: JSON.parse(JSON.stringify(proposta)), 
            status: 'rascunho', 
            data_criacao: new Date().toISOString()
          } as Circuito;

          toast.success(`Circuito ${idPadronizado} formalizado com sucesso!`);

          return {
            projects: state.projects.map(p => {
              if (p.id !== pId) return p;
              
              const propostasAtualizadas = [...(p.propostas || [])];
              propostasAtualizadas[propostaIndex] = { ...proposta, status: 'aceita' };

              return {
                ...p,
                propostas: propostasAtualizadas,
                circuitos: [...(p.circuitos || []), novoCircuito]
              };
            })
          };
        });
      },

    }),
    { name: 'projel-storage' }
  )
);