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
            { code: 'AA2', label: 'Frio / Câmaras', description: 'Câmaras frigoríficas ou locais muito frios.' }
        ]
    },
    {
        id: 'presenca_agua',
        category: 'ambiente',
        question: 'Qual a presença de água no local?',
        helperText: 'Define a proteção IP necessária para os equipamentos (tomadas, luminárias).',
        options: [
            { code: 'AD1', label: 'Local Seco', description: 'Salas, quartos, escritórios. Risco desprezível.' },
            { code: 'AD2', label: 'Úmido / Gotejamento', description: 'Pode haver condensação ou respingos eventuais (ex: Lavabos).' },
            { code: 'AD3', label: 'Molhado / Aspersão', description: 'Chuva ou respingos frequentes (ex: Banheiros com chuveiro).' },
            { code: 'AD4', label: 'Lavagem com Mangueira', description: 'Garagens, quintais, cozinhas industriais.' },
            { code: 'AD7', label: 'Imersão / Piscinas', description: 'Interior de piscinas ou espelhos d\'água.' }
        ]
    },
    {
        id: 'presenca_solidos',
        category: 'ambiente',
        question: 'O local possui poeira ou resíduos sólidos?',
        helperText: 'Importante para escolha de eletrodutos e vedação de quadros.',
        options: [
            { code: 'AE1', label: 'Limpo / Doméstico', description: 'Poeira normal de ambiente residencial.' },
            { code: 'AE4', label: 'Poeira Leve', description: 'Poeira ou sedimentação de pó.' },
            { code: 'AE6', label: 'Poeira Intensa', description: 'Ambientes industriais, cimento, moinhos.' }
        ]
    },

    // --- PESSOAS E USO ---
    {
        id: 'competencia_pessoas',
        category: 'pessoas',
        question: 'Quem frequenta este local?',
        helperText: 'Determina a proteção contra choques e acessibilidade.',
        options: [
            { code: 'BA1', label: 'Pessoas Comuns', description: 'Uso geral (residencial, comercial). Pessoas não advertidas.' },
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
            { code: 'CB1', label: 'Estável / Fixa', description: 'Paredes rígidas, risco desprezível de movimento.' },
            { code: 'CB3', label: 'Móvel / Instável', description: 'Estruturas sujeitas a movimentação ou vibração.' }
        ]
    }
];