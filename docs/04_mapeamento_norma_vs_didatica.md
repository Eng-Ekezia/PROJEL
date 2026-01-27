# Mapeamento NBR 5410 × Estrutura Didática  
## Projeto de Instalações Elétricas – PROJEL

Este documento estabelece o mapeamento explícito entre os
conteúdos da ABNT NBR 5410 e a organização didática da disciplina
Projeto de Instalações Elétricas, bem como sua implementação no PROJEL.

Seu objetivo é:
- garantir aderência normativa
- evitar lacunas conceituais
- permitir rastreabilidade técnica
- servir como documento de defesa acadêmica

---

## 1. Princípio de mapeamento adotado

A NBR 5410 **não é seguida como índice linear**,
mas como um **sistema de decisões normativas interdependentes**.

O mapeamento considera:
- a lógica implícita da norma
- a progressão cognitiva do aluno
- a necessidade de contextualização antes do cálculo

---

## 2. Estrutura geral da NBR 5410 (visão funcional)

| Eixo normativo | Função no projeto |
|---------------|------------------|
| Características da instalação | Definir contexto |
| Influências externas | Definir exigências ambientais |
| Medidas de proteção | Mitigar riscos |
| Esquemas de aterramento | Base da proteção |
| Circuitos | Organização funcional |
| Métodos construtivos | Viabilidade física |
| Dimensionamento | Validação técnica |

Essa lógica orienta toda a disciplina.

---

## 3. Mapeamento detalhado: Norma × Disciplina × PROJEL

### 3.1 Características da instalação
**Norma**  
- Seção 3 – Princípios fundamentais  
- Seção 4 – Proteção para garantir segurança  

**Disciplina**  
- Bloco 1 – Fundamentos do projeto elétrico  
- Bloco 2 – Características da instalação  

**PROJEL**  
- Entidade `ProjetoEletrico`
- Definição de tipo de instalação
- Definição de usuários e criticidade

---

### 3.2 Influências externas
**Norma**  
- Item 4.2.6  
- Anexo C – Influências externas  

**Disciplina**  
- Bloco 2 – Contexto da instalação  
- Aula específica sobre categorias A, B e C  

**PROJEL**  
- Entidade `InfluenciasExternas`
- Wizard de descrição humana do ambiente
- Tradução automática para códigos normativos
- Registro de categoria, código e classe

---

### 3.3 Zonas elétricas (abstração didática)
**Norma**  
- Não explicitamente definida  
- Conceito implícito em influências externas e organização da instalação  

**Disciplina**  
- Bloco 2 – Zonas elétricas e herança de contexto  

**PROJEL**  
- Entidade `ZonaDeInfluencia`
- Herança automática de influências
- Exceções explícitas por circuito

---

### 3.4 Medidas de proteção
**Norma**  
- Seção 4 – Proteção para garantir segurança  
- Proteção contra choques elétricos  
- Proteção contra sobrecorrentes  

**Disciplina**  
- Bloco 3 – Riscos e medidas de proteção  

**PROJEL**  
- Validações condicionadas por influências externas
- Alertas normativos por risco identificado
- Bloqueios para decisões incompatíveis

---

### 3.5 Esquemas de aterramento
**Norma**  
- Seção 5 – Aterramento e condutores de proteção  

**Disciplina**  
- Bloco 3 – Esquemas de aterramento  

**PROJEL**  
- Enum `EsquemaAterramento`
- Impacto do esquema nas exigências de proteção
- Integração com análise de DR

---

### 3.6 Dispositivo diferencial residual (DR)
**Norma**  
- Seção 5  
- Exigências condicionadas ao risco e ambiente  

**Disciplina**  
- Bloco 3 – DR e equipotencialização  

**PROJEL**  
- Verificação automática de exigência de DR
- Alertas e justificativas normativas
- Transparência sob demanda

---

### 3.7 Organização e separação de circuitos
**Norma**  
- Seção 6 – Seleção e instalação dos componentes  

**Disciplina**  
- Bloco 4 – Circuitos e organização funcional  

**PROJEL**  
- Entidade `Circuito`
- Tipos de circuito
- Criticidade
- Reserva técnica
- Associação obrigatória a zona

---

### 3.8 Métodos de instalação e critérios construtivos
**Norma**  
- Seção 6 – Métodos de instalação  
- Tabelas de referência  

**Disciplina**  
- Bloco 6 – Recomendações construtivas  

**PROJEL**  
- Seleção de método de instalação
- Impacto no cálculo
- Alertas por incompatibilidade com influências externas

---

### 3.9 Dimensionamento dos circuitos
**Norma**  
- Seção 6 – Condutores e proteção  
- Anexos normativos de cálculo  

**Disciplina**  
- Bloco 7 – Dimensionamento elétrico  

**PROJEL**  
- Motor de cálculo normativo
- Cálculo de corrente de projeto
- Fatores de correção
- Queda de tensão
- Seleção de dispositivos de proteção
- Referência explícita aos itens normativos

---

## 4. Transparência e rastreabilidade normativa

O PROJEL registra:
- decisões adotadas
- influências consideradas
- regras aplicadas
- justificativas normativas

Isso permite:
- auditoria técnica
- uso didático
- defesa do projeto

---

## 5. Benefícios do mapeamento explícito

Este mapeamento garante que:
- nenhum conteúdo é arbitrário
- nenhuma etapa é “opinião do professor”
- o sistema não ensina nada fora da norma
- o aluno entende a origem das exigências

---

## 6. Consideração final

A disciplina e o PROJEL foram estruturados para
**seguir a lógica da NBR 5410**, não apenas seu texto.

Este documento garante:
- coerência normativa
- integridade pedagógica
- segurança técnica

Qualquer evolução futura do PROJEL
ou da disciplina deve preservar
esse alinhamento explícito com a norma.
