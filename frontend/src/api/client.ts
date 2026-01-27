import axios from 'axios';
import type { Zona, Local, Carga } from '../types/project';

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

  createZona: async (zona: Omit<Zona, 'id' | 'data_criacao'>): Promise<Zona> => {
    const response = await api.post<Zona>('/zonas/', zona);
    return response.data;
  },

  createLocal: async (local: Omit<Local, 'id' | 'data_criacao'>): Promise<Local> => {
    const response = await api.post<Local>('/locais/', local);
    return response.data;
  },

  // --- NOVOS MÉTODOS DE CARGA ---
  
  createCarga: async (carga: Omit<Carga, 'id' | 'data_criacao'>): Promise<Carga> => {
    const response = await api.post<Carga>('/cargas/', carga);
    return response.data;
  },

  calcularNorma: async (area: number, perimetro: number, eh_cozinha_servico: boolean) => {
    const response = await api.post('/cargas/calcular-minimo-nbr', {
        area,
        perimetro,
        eh_cozinha_servico
    });
    return response.data;
  }
};