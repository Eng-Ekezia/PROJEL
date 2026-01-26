export interface Zona {
  id: string;
  projeto_id: string;
  nome: string;
  descricao?: string;
  temp_ambiente: string;
  presenca_agua: string;
  presenca_solidos: string;
  competencia_pessoas: string;
  materiais_construcao: string;
  estrutura_edificacao: string;
  cor_identificacao: string;
  data_criacao: string;
}

export interface Local {
  id: string;
  projeto_id: string;
  zona_id: string;
  nome: string;
  area_m2: number;
  perimetro_m: number;
  pe_direito_m: number;
  data_criacao: string;
}

export interface Projeto {
  id: string;
  nome: string;
  tipo_instalacao: string;
  tensao_sistema: string;
  sistema: string;
  esquema_aterramento: string;
  descricao_aterramento?: string;
  data_criacao: string;
  ultima_modificacao: string;
  
  // Listas de entidades filhas
  zonas: Zona[];
  locais: Local[];
}