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

export type Criticidade = 'NORMAL' | 'ALTA'; // Ex: Equipamentos de suporte à vida ou alto custo

// --- ENTIDADES ---

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
  presenca_solidos: string;   // AE
  competencia_pessoas: string;// BA
  materiais_construcao: string; // CA
  estrutura_edificacao: string; // CB
  
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
  
  // Relação com Circuito (Novo na Fase 08)
  circuito_id?: string | null; // Carga pode ou não ter circuito ainda
}

export interface Circuito {
  id: string;
  projeto_id: string;
  
  // Identificação
  identificador: string; // Ex: "C1", "C2"
  tipo_circuito: TipoCircuito;
  descricao?: string;
  
  // Relacionamentos
  zona_id: string; // Zona dominante (a mais crítica)
  cargas_ids: string[]; // IDs das cargas agrupadas
  
  // Parâmetros de Instalação (Decisão do Usuário)
  metodo_instalacao: MetodoInstalacao;
  sobrescreve_influencias: boolean; // Se true, usuário forçou parâmetros ignorando a Zona
  
  // Parâmetros Elétricos
  tensao_nominal: number; // Ex: 127, 220
  circuitos_agrupados: number; // Para cálculo de fator de agrupamento
  fator_agrupamento?: number;
  temperatura_ambiente?: number;
  
  // Condutores (Decisão ou Resultado)
  material_condutor: MaterialCondutor;
  isolacao: Isolacao;
  secao_condutor_mm2?: number; // Resultado do dimensionamento
  
  // Proteção
  corrente_nominal_disjuntor?: number; // Resultado
  
  data_criacao: string;
  status: 'rascunho' | 'calculado' | 'erro';
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
  circuitos: Circuito[]; // Novo array de circuitos
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