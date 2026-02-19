// --- ENUMS TÉCNICOS (NBR 5410) ---

export type TipoCircuito = 
  | 'ILUMINACAO' 
  | 'TUG'     // Tomada de Uso Geral
  | 'TUE'     // Tomada de Uso Específico
  | 'DISTRIBUICAO' 
  | 'MOTOR';

export type MetodoInstalacao = 
  | 'A1' | 'A2' | 'B1' | 'B2' | 'C' | 'D' | 'E' | 'F' | 'G';

export type MaterialCondutor = 'COBRE' | 'ALUMINIO';

export type Isolacao = 'PVC' | 'EPR' | 'XLPE';

export type Criticidade = 'NORMAL' | 'ALTA'; 

export type StatusProposta = 
  | 'rascunho'   
  | 'analisada'  
  | 'invalida'   
  | 'aceita'     
  | 'descartada'; 

export type StatusDimensionamento = 'ok' | 'alerta' | 'erro';

// --- ENTIDADES ---

export interface Zona {
  id: string;
  projeto_id: string;
  nome: string;
  descricao?: string;
  
  origem: 'preset' | 'ajustada' | 'custom';
  preset_id?: string;
  
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
  tipo: string; 
  potencia: number;
  unidade: 'W' | 'VA';
  fator_potencia: number;
  origem: 'norma' | 'usuario';
  status?: 'ativo' | 'inativo';
  
  zona_id?: string; 
  circuito_id?: string | null; 
}

// [NOVO] Oficialização do estado de Kanban
export interface PreCircuito {
  id: string;
  nome: string;
  cargas_ids: string[];
  justificativa_sugestao?: string; 
}

export interface PropostaCircuito {
  id: string;
  data_criacao: string;
  status: StatusProposta;
  
  cargas_ids: string[];
  locais_ids: string[];
  zonas_ids: string[];
  
  descricao_intencao: string;
  observacoes_normativas?: string;
  autor: string;
}

export interface Circuito {
  id: string;
  projeto_id: string;
  
  identificador: string; 
  tipo_circuito: TipoCircuito;
  descricao?: string;
  
  proposta_id: string; 
  snapshot_proposta: PropostaCircuito; 
  
  zona_id: string; 
  cargas_ids: string[]; 
  
  metodo_instalacao: MetodoInstalacao;
  sobrescreve_influencias: boolean; 
  
  tensao_nominal: number; 
  circuitos_agrupados: number; 
  fator_agrupamento?: number;
  temperatura_ambiente?: number;
  comprimento_m?: number; 
  
  material_condutor: MaterialCondutor;
  isolacao: Isolacao;
  secao_condutor_mm2?: number; 
  
  corrente_nominal_disjuntor?: number; 
  
  data_criacao: string;
  status: 'rascunho' | 'calculado' | 'erro';
}

// --- RESULTADOS DO MOTOR DE CÁLCULO (Fase 10) ---

export interface VerificacaoNormativa {
  criterio: string;
  status: StatusDimensionamento;
  valor_calculado: number | string;
  limite_normativo?: number | string;
  mensagem: string;
  referencia_nbr: string;
}

export interface MemoriaCalculo {
  passos: string[];
}

export interface ResultadoDimensionamento {
  circuito_id?: string;
  status_global: StatusDimensionamento;
  
  corrente_projeto_ib: number;
  corrente_corrigida_iz?: number;
  disjuntor_nominal_in?: number;
  secao_condutor_mm2?: number;
  queda_tensao_pct?: number;
  
  verificacoes: VerificacaoNormativa[];
  memoria: MemoriaCalculo;
  erros_entrada?: string[];
}

export interface Projeto {
  id: string;
  nome: string;
  tipo_instalacao: string;
  tensao_sistema: string;
  sistema: string;
  esquema_aterramento?: string;
  descricao_aterramento?: string;
  data_criacao: string;
  ultima_modificacao: string;
  
  zonas: Zona[];
  locais: Local[];
  cargas: Carga[];
  pre_circuitos?: PreCircuito[]; // [NOVO] Memória dos rascunhos em andamento
  propostas?: PropostaCircuito[]; 
  circuitos: Circuito[]; 
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