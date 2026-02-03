export interface Zona {
  id: string;
  projeto_id: string;
  nome: string;
  descricao?: string;
  
  // UX Metadata
  origem: 'preset' | 'ajustada' | 'custom';
  preset_id?: string;
  
  // Influencias NBR 5410
  temp_ambiente: string;      // AA
  presenca_agua: string;      // AD
  presenca_solidos: string;   // AE (Novo)
  competencia_pessoas: string;// BA
  materiais_construcao: string; // CA (Novo)
  estrutura_edificacao: string; // CB (Novo)
  
  cor_identificacao: string;
  data_criacao: string;
}

export interface Local {
  id: string;
  projeto_id: string;
  zona_id: string;
  nome: string;
  tipo?: 'padrao' | 'cozinha' | 'banheiro' | 'servico' | 'externo';
  
  area_m2: number;
  perimetro_m: number;
  pe_direito_m: number;
  
  data_criacao: string;
}

export interface Carga {
  id: string;
  projeto_id: string;
  local_id: string;
  nome: string;
  tipo: string; // Ex: 'TUG', 'TUE', 'Iluminacao'
  potencia: number;
  unidade: 'W' | 'VA';
  fator_potencia: number;
  origem: 'norma' | 'usuario'; // Importante para rastreabilidade
  status?: 'ativo' | 'inativo';
}

export interface Projeto {
  id: string;
  nome: string;
  tipo_instalacao: string;
  tensao_sistema: string;
  sistema: string;
  esquema_aterramento?: string;
  data_criacao: string;
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