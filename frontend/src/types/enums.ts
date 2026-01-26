// Substituindo enum por 'as const' para compatibilidade com erasableSyntaxOnly

export const EsquemaAterramento = {
  TT: "TT",
  TN_S: "TN-S",
  TN_C: "TN-C",
  TN_C_S: "TN-C-S",
  IT: "IT"
} as const;

// Extrai o tipo dos valores (ex: "TT" | "TN-S" | ...)
export type EsquemaAterramento = typeof EsquemaAterramento[keyof typeof EsquemaAterramento];

export const SistemaFases = {
  MONOFASICO: "monofasico",
  BIFASICO: "bifasico",
  TRIFASICO: "trifasico"
} as const;

export type SistemaFases = typeof SistemaFases[keyof typeof SistemaFases];

export const TensaoSistema = {
  V_127_220: "127/220V",
  V_220_380: "220/380V",
  V_380_440: "380/440V",
  OUTRO: "Outro"
} as const;

export type TensaoSistema = typeof TensaoSistema[keyof typeof TensaoSistema];

export const TipoInstalacao = {
  RESIDENCIAL: "Residencial",
  COMERCIAL: "Comercial",
  INDUSTRIAL: "Industrial"
} as const;

export type TipoInstalacao = typeof TipoInstalacao[keyof typeof TipoInstalacao];