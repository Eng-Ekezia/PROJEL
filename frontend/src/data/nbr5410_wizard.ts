import type { Local, Carga } from "../types/project";

// ============================================================================
// PARTE A: WIZARD DE ZONAS (Classificação de Influências)
// ============================================================================

export interface WizardOption {
    label: string;
    description: string;
    code: string; // O código NBR que será salvo (ex: AD4)
    icon?: string;
}

export interface WizardQuestion {
    id: string; // Mapeia para o campo do objeto Zona (ex: 'presenca_agua')
    category: 'ambiente' | 'pessoas' | 'estrutura';
    question: string;
    helperText: string;
    options: WizardOption[];
}

export const ZONE_WIZARD_DATA: WizardQuestion[] = [
    // --- AMBIENTE FÍSICO ---
    {
        id: 'temp_ambiente',
        category: 'ambiente',
        question: 'Como é a temperatura média do local?',
        helperText: 'A temperatura afeta a capacidade de condução de corrente dos cabos.',
        options: [
            { code: 'AA4', label: 'Temperada / Normal', description: 'Ambiente interno comum ou externo sombreado (-5°C a +40°C).' },
            { code: 'AA5', label: 'Local Quente', description: 'Casas de máquinas, forros sem ventilação (+5°C a +40°C).' },
            { code: 'AA6', label: 'Muito Quente', description: 'Proximidade de fornos, indústrias (+5°C a +60°C).' },
            { code: 'AA2', label: 'Frio / Câmaras', description: 'Câmaras frigoríficas ou locais climatizados rigorosos.' }
        ]
    },
    {
        id: 'presenca_agua',
        category: 'ambiente',
        question: 'Qual o nível de contato com água?',
        helperText: 'Define a proteção IP necessária para equipamentos.',
        options: [
            { code: 'AD1', label: 'Seco (Desprezível)', description: 'Salas, quartos, locais sem risco de água.' },
            { code: 'AD2', label: 'Gotejamento (Úmido)', description: 'Cozinhas, áreas de serviço, banheiros (fora do box).' },
            { code: 'AD3', label: 'Aspersão (Molhado)', description: 'Áreas externas expostas à chuva, lavanderias pesadas.' },
            { code: 'AD4', label: 'Projeções de Água', description: 'Locais lavados com mangueira, lava-jatos.' },
            { code: 'AD7', label: 'Submersão (Alagável)', description: 'Piscinas, reservatórios, áreas inundáveis.' }
        ]
    },
    {
        id: 'presenca_solidos',
        category: 'ambiente',
        question: 'Existe poeira ou corpos estranhos?',
        helperText: 'Define proteção contra entrada de objetos (IP).',
        options: [
            { code: 'AE1', label: 'Desprezível', description: 'Ambiente doméstico padrão.' },
            { code: 'AE2', label: 'Pequenos Objetos', description: 'Oficinas com limalha, locais com insetos pequenos.' },
            { code: 'AE3', label: 'Poeira', description: 'Marcenarias, indústrias de cimento, obras.' }
        ]
    },

    // --- PESSOAS E UTILIZAÇÃO ---
    {
        id: 'competencia_pessoas',
        category: 'pessoas',
        question: 'Quem frequenta o local?',
        helperText: 'Define a proteção contra choque elétrico necessária.',
        options: [
            { code: 'BA1', label: 'Pessoas Comuns', description: 'Residências, escritórios. Pessoas não advertidas.' },
            { code: 'BA2', label: 'Crianças', description: 'Creches, escolas infantis, áreas de recreação.' },
            { code: 'BA3', label: 'Pessoas com Deficiência', description: 'Hospitais, asilos, clínicas geriátricas.' },
            { code: 'BA4', label: 'Equipe Advertida', description: 'Áreas de serviço exclusivas para manutenção.' },
            { code: 'BA5', label: 'Profissionais (Eletricistas)', description: 'Subestações, salas elétricas trancadas.' }
        ]
    },

    // --- CONSTRUÇÃO ---
    {
        id: 'materiais_construcao',
        category: 'estrutura',
        question: 'Qual o material predominante da construção?',
        helperText: 'Afeta o risco de incêndio e propagação de chama.',
        options: [
            { code: 'CA1', label: 'Não Combustível', description: 'Alvenaria, concreto, gesso (Maioria dos casos).' },
            { code: 'CA2', label: 'Combustível', description: 'Madeira, dry-wall com isolamento inflamável.' }
        ]
    },
    {
        id: 'estrutura_edificacao',
        category: 'estrutura',
        question: 'Como é a estrutura física?',
        helperText: 'Define flexibilidade da instalação.',
        options: [
            { code: 'CB1', label: 'Estável / Fixa', description: 'Paredes rígidas, alvenaria convencional.' },
            { code: 'CB2', label: 'Móvel / Flexível', description: 'Estruturas sujeitas a vibração ou movimento.' }
        ]
    }
];

// ============================================================================
// PARTE B: WIZARD DE CARGAS (Capítulo 9 - NBR 5410)
// ============================================================================

export const NBR5410_WIZARD = {
  
  /**
   * Calcula a potência mínima de iluminação baseada na área (m²)
   * Regra: 100VA para os primeiros 6m² + 60VA para cada 4m² inteiros excedentes.
   */
  calcularIluminacao: (area: number): number => {
    if (area <= 6) return 100;
    const excedente = area - 6;
    const inteiros = Math.floor(excedente / 4);
    return 100 + (inteiros * 60);
  },

  /**
   * Calcula a quantidade e potência de TUGs baseada no Perímetro e Tipo de Local.
   * Regras aplicadas:
   * - Cozinhas/Serviço: 1 tomada a cada 3,5m. 3 primeiras de 600VA.
   * - Banheiros: Pelo menos 1 de 600VA.
   * - Demais (Quartos/Salas): 1 tomada a cada 5m.
   */
  calcularTUGs: (local: Local): Carga[] => {
    // Cast seguro para acessar o tipo, garantindo fallback para 'padrao'
    const perfil = (local as any).tipo || 'padrao';
    const perimetro = Number(local.perimetro_m) || 0;
    
    if (perimetro <= 0) return [];

    let quantidade = 0;
    let regraEspecial = false; // Define se usa regra de 600VA (Cozinha/Copa/Serviço)
    let regraBanheiro = false;

    // 1. Definição da Quantidade por Perímetro
    switch (perfil) {
      case 'cozinha':
      case 'servico':
        // Regra: Uma tomada a cada 3.5m (fração conta como inteira)
        quantidade = Math.ceil(perimetro / 3.5);
        // Mínimo de 2 tomadas para cozinhas (boa prática, norma pede acima da bancada)
        if (quantidade < 2) quantidade = 2;
        regraEspecial = true;
        break;
      
      case 'banheiro':
        // Regra: Pelo menos 1 tomada junto ao lavatório
        quantidade = 1;
        regraBanheiro = true;
        break;

      case 'externo':
      case 'padrao':
      default:
        // Regra: Uma tomada a cada 5m (fração conta como inteira)
        quantidade = Math.ceil(perimetro / 5);
        if (quantidade < 1) quantidade = 1;
        break;
    }

    const cargasSugeridas: Carga[] = [];
    const basePayload = {
        projeto_id: local.projeto_id,
        local_id: local.id,
        tipo: 'TUG',
        unidade: 'VA' as const,
        fator_potencia: 0.8,
        origem: 'norma' as const
    };

    // 2. Distribuição de Potências
    if (regraEspecial) {
      // Regra: As 3 primeiras tomadas são de 600VA, as demais de 100VA
      const qtd600 = Math.min(3, quantidade);
      const qtd100 = quantidade - qtd600;

      if (qtd600 > 0) {
        cargasSugeridas.push({
          ...basePayload,
          id: crypto.randomUUID(),
          nome: `TUG ${perfil.toUpperCase()} (Prioritária - 600VA)`,
          potencia: 600 * qtd600, // Agrupamos a potência para simplificar a lista inicial
          fator_potencia: 1.0 // Cargas resistivas puras tendem a FP 1
        });
      }
      if (qtd100 > 0) {
        cargasSugeridas.push({
          ...basePayload,
          id: crypto.randomUUID(),
          nome: `TUG ${perfil.toUpperCase()} (Adicional - 100VA)`,
          potencia: 100 * qtd100,
        });
      }
    } 
    else if (regraBanheiro) {
        // Regra: Mínimo 600VA
        cargasSugeridas.push({
            ...basePayload,
            id: crypto.randomUUID(),
            nome: `TUG LAVATÓRIO`,
            potencia: 600,
            fator_potencia: 1.0
        });
    }
    else {
      // Regra Padrão (Quartos/Salas): Tudo 100VA
      cargasSugeridas.push({
        ...basePayload,
        id: crypto.randomUUID(),
        nome: `TUG ${perfil === 'padrao' ? 'Geral' : perfil.toUpperCase()}`,
        potencia: quantidade * 100,
      });
    }

    return cargasSugeridas;
  }
};