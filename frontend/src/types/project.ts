import type { EsquemaAterramento, SistemaFases, TensaoSistema, TipoInstalacao } from './enums';

export interface Projeto {
  // Identificadores
  id: string;
  data_criacao: string;
  ultima_modificacao: string;

  // Dados de Engenharia
  nome: string;
  tipo_instalacao: TipoInstalacao;
  tensao_sistema: TensaoSistema;
  sistema: SistemaFases;
  esquema_aterramento: EsquemaAterramento;
  descricao_aterramento?: string;
}