import { EsquemaAterramento, SistemaFases, TensaoSistema, TipoInstalacao } from './enums';

export interface Projeto {
  // Identificadores e Metadados (Controle de Aplicação)
  id: string;
  data_criacao: string;
  ultima_modificacao: string;

  // Dados de Engenharia (Domínio NBR 5410)
  nome: string;
  tipo_instalacao: TipoInstalacao;
  tensao_sistema: TensaoSistema;
  sistema: SistemaFases;
  esquema_aterramento: EsquemaAterramento;
  descricao_aterramento?: string; // Campo opcional para notas técnicas
}