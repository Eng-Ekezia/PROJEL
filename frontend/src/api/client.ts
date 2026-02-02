import axios from 'axios';
import type { Projeto, Zona, Local, PresetZona, Carga } from '../types/project';

const api = axios.create({ baseURL: 'http://localhost:8000/api/v1' });

export interface OpcoesInfluencias {
  temperatura: { codigo: string; descricao: string }[];
  agua: { codigo: string; descricao: string }[];
  solidos: { codigo: string; descricao: string }[];
  pessoas: { codigo: string; descricao: string }[];
  materiais: { codigo: string; descricao: string }[];
  estrutura: { codigo: string; descricao: string }[];
}

export interface CargaCreateDTO {
    projeto_id: string; 
    local_id: string;
    nome: string;
    tipo: string;
    quantidade: number;
    potencia: number;
    unidade: 'W' | 'VA';
    fator_potencia: number;
}

export interface CalculoNBRResult {
    norma_iluminacao_va: number;
    norma_tugs_quantidade: number;
}

// DTO para criação de projeto (simplificado)
export interface ProjetoCreateDTO {
  nome: string;
  tipo_instalacao: string;
  tensao_sistema: string;
  sistema: string;
}

export const ProjectService = {
  // --- PROJETO ---
  // Adicionado para satisfazer o Dashboard
  getAll: async () => (await api.get<Projeto[]>('/projetos/')).data,
  create: async (p: ProjetoCreateDTO) => (await api.post<Projeto>('/projetos/', p)).data,
  
  // --- UTILS ---
  getOpcoesInfluencias: async () => (await api.get<OpcoesInfluencias>('/zonas/opcoes-influencias')).data,
  getPresets: async (tipo: string) => (await api.get<PresetZona[]>(`/zonas/presets/${tipo}`)).data,

  // --- ZONA ---
  createZona: async (z: Partial<Zona>) => (await api.post<Zona>('/zonas/', z)).data,
  updateZona: async (id: string, z: Partial<Zona>) => (await api.put<Zona>(`/zonas/${id}`, z)).data,
  deleteZona: async (id: string) => await api.delete(`/zonas/${id}`),

  // --- LOCAL ---
  createLocal: async (l: Omit<Local, 'id' | 'data_criacao'>) => (await api.post<Local>('/locais/', l)).data,
  updateLocal: async (id: string, l: Omit<Local, 'id' | 'data_criacao'>) => (await api.put<Local>(`/locais/${id}`, l)).data,
  deleteLocal: async (id: string) => await api.delete(`/locais/${id}`),

  // --- CARGA ---
  createCarga: async (c: CargaCreateDTO) => (await api.post<Carga>('/cargas/', c)).data,
  updateCarga: async (id: string, c: CargaCreateDTO) => (await api.put<Carga>(`/cargas/${id}`, c)).data,
  deleteCarga: async (id: string) => await api.delete(`/cargas/${id}`),

  calcularMinimoNBR: async (area: number, perim: number, umida: boolean) => 
    (await api.post<CalculoNBRResult>('/cargas/calcular-minimo-nbr', { area, perimetro: perim, eh_cozinha_servico: umida })).data
};