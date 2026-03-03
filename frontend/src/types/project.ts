export interface CategoriaA {
  temp_ambiente: string;
  presenca_agua: string;
  presenca_solidos: string;
}

export interface CategoriaB {
  competencia_pessoas: string;
}

export interface CategoriaC {
  materiais_construcao: string;
  estrutura_edificacao: string;
}

export interface Zona {
  id: string;
  projeto_id: string;
  nome: string;
  descricao?: string;

  // UX Metadata
  origem: 'preset' | 'ajustada' | 'custom';
  autor?: string;
  preset_id?: string;

  // Influences 
  influencias_categoria_a: CategoriaA;
  influencias_categoria_b: CategoriaB;
  influencias_categoria_c: CategoriaC;

  cor_identificacao: string;
  data_criacao: string;
}

export interface Local {
  id: string;
  projeto_id: string;
  zona_id: string;
  nome: string;
  descricao?: string;
  area_m2: number;
  perimetro_m: number;
  pe_direito_m: number;
  perfil_normativo_local: string;
  autor?: string;
  data_criacao: string;
}

export interface Carga {
  id: string;
  projeto_id?: string;
  zona_id?: string;
  nome: string;
  tipo_carga: string;
  potencia_W: number;
  quantidade: number;
  origem: 'normativa' | 'usuario';
  ajustada: boolean;
  justificativa_ajuste?: string;
}

export interface Projeto {
  id: string;
  nome: string;
  tipo_instalacao: string; // 'Residencial' | 'Comercial' | 'Industrial'
  tensao_sistema: string;
  sistema: string;
  esquema_aterramento: string;
  descricao_aterramento?: string;

  descricao_geral?: string;
  criterios_gerais?: string;
  autor?: string;

  data_criacao?: string;
  ultima_modificacao: string;

  zonas: Zona[];
  locais: Local[];
  cargas: Carga[];
}

export interface PresetZona {
  id: string;
  nome: string;
  descricao: string;
  influencias: {
    temp_ambiente: string;
    presenca_agua: string;
    presenca_solidos: string;
    competencia_pessoas: string;
    materiais_construcao: string;
    estrutura_edificacao: string;
  };
  cor: string;
}