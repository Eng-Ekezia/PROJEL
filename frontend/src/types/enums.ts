// Define os esquemas de aterramento permitidos pela NBR 5410
export enum EsquemaAterramento {
  TT = "TT",
  TN_S = "TN-S",
  TN_C = "TN-C",
  TN_C_S = "TN-C-S",
  IT = "IT"
}

// Define o número de fases do sistema
export enum SistemaFases {
  MONOFASICO = "monofasico",
  BIFASICO = "bifasico",
  TRIFASICO = "trifasico"
}

// Define as tensões nominais padrão
export enum TensaoSistema {
  V_127_220 = "127/220V",
  V_220_380 = "220/380V",
  V_380_440 = "380/440V",
  OUTRO = "Outro"
}

// Define os tipos de instalação para categorização
export enum TipoInstalacao {
  RESIDENCIAL = "Residencial",
  COMERCIAL = "Comercial",
  INDUSTRIAL = "Industrial"
}