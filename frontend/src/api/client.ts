import axios from 'axios';
import type { Zona, Local, PresetZona } from '../types/project';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

export interface OpcoesInfluencias {
  temperatura: { codigo: string; descricao: string }[];
  agua: { codigo: string; descricao: string }[];
  solidos: { codigo: string; descricao: string }[];
  pessoas: { codigo: string; descricao: string }[];
  materiais: { codigo: string; descricao: string }[];
  estrutura: { codigo: string; descricao: string }[];
}

export const ProjectService = {
  getOpcoesInfluencias: async (): Promise<OpcoesInfluencias> => {
    const response = await api.get<OpcoesInfluencias>('/zonas/opcoes-influencias');
    return response.data;
  },

  getPresets: async (tipoProjeto: string): Promise<PresetZona[]> => {
    const response = await api.get<PresetZona[]>(`/zonas/presets/${tipoProjeto}`);
    return response.data;
  },

  createZona: async (zona: Omit<Zona, 'id' | 'data_criacao'>): Promise<Zona> => {
    const response = await api.post<Zona>('/zonas/', zona);
    return response.data;
  },

  updateZona: async (id: string, zona: Omit<Zona, 'id' | 'data_criacao'>): Promise<Zona> => {
    const response = await api.put<Zona>(`/zonas/${id}`, zona);
    return response.data;
  },

  createLocal: async (local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.post<Local>('/locais/', local);
    return response.data;
  },

  updateLocal: async (id: string, local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.put<Local>(`/locais/${id}`, local);
    return response.data;
  }
};