# Wireframes Textuais de UX  
## PROJEL – Fluxos, Telas e Decisões Visíveis

Este documento descreve, em formato textual estruturado, as telas,
fluxos e comportamentos da interface do PROJEL.

O objetivo é:
- alinhar UX, domínio e didática
- evitar decisões implícitas
- permitir implementação fiel sem improviso

Não é um layout visual.
É um **contrato de comportamento da interface**.

---

## 1. Tela Inicial – Lista de Projetos

### Objetivo
Permitir criar, acessar e gerenciar projetos elétricos.

### Elementos
- Título: “Projetos Elétricos”
- Botão primário: “Novo Projeto”
- Lista de projetos existentes
  - nome
  - tipo (Residencial | Comercial | Industrial)
  - data da última modificação

### Ações
- Criar projeto
- Abrir projeto
- Duplicar projeto (opcional)
- Excluir projeto (com confirmação)

---

## 2. Tela – Criação de Projeto

### Objetivo
Definir o **contexto global** da instalação.

### Campos
- Nome do projeto (texto)
- Tipo de projeto (select)
  - Residencial
  - Comercial
  - Industrial
- Sistema elétrico (select)
  - Monofásico
  - Bifásico
  - Trifásico
- Tensão nominal (select ou campo numérico)
- Esquema de aterramento (select)
  - TT
  - TN-S
  - TN-C-S
  - IT
- Campo opcional: descrição do aterramento

### Mensagem fixa (UX importante)
> “As decisões tomadas aqui afetam todo o projeto.”

### Ações
- Salvar e continuar
- Cancelar

---

## 3. Tela – Visão Geral do Projeto (Dashboard)

### Objetivo
Servir como mapa mental do projeto.

### Seções
- Resumo do projeto
- Zonas de influência
- Circuitos
- Status geral

### Indicadores visuais
- Zonas definidas: ✔ / ⚠ / ✖
- Circuitos definidos: ✔ / ⚠ / ✖
- Pronto para dimensionamento: Sim / Não

---

## 4. Tela – Zonas de Influência (Lista)

### Objetivo
Gerenciar zonas elétricas.

### Elementos
- Lista de zonas
  - nome
  - origem (Preset | Ajustada | Custom)
  - resumo das influências
- Botão: “Nova Zona”

### Ações por zona
- Editar
- Visualizar influências
- Excluir (se não vinculada a circuito)

---

## 5. Tela – Criação de Zona (Escolha de Método)

### Objetivo
Definir como a zona será criada.

### Pergunta central
> “Como você deseja definir esta zona?”

### Opções
- Usar preset recomendado
- Ajustar um preset existente
- Criar zona personalizada

### Comportamento
- As opções disponíveis dependem do tipo de projeto
- Industrial não exibe presets fechados

---

## 6. Tela – Criação de Zona por Preset

### Objetivo
Criar zona rapidamente com consciência.

### Elementos
- Lista de presets aplicáveis
  - nome
  - descrição curta
- Painel lateral (opcional):
  - “Ver detalhes normativos”

### Ação
- Selecionar preset
- Confirmar criação

### Mensagem informativa
> “Você poderá ajustar esta zona posteriormente.”

---

## 7. Tela – Wizard de Zona Personalizada

### Objetivo
Construir a zona por descrição humana.

### Etapas do wizard

#### Etapa 1 – Ambiente físico
- Presença de água?
- Poeira significativa?
- Solicitações mecânicas?
- Exposição ao tempo?

#### Etapa 2 – Uso e pessoas
- Quem utiliza o local?
- Acesso do público?
- Consequência de falha elétrica?

#### Etapa 3 – Construção
- Estrutura metálica acessível?
- Possibilidade de equipotencialização?

### Comportamento UX
- Perguntas condicionais
- Etapas exibem progresso
- Não permite avançar sem resposta

---

## 8. Tela – Resumo da Zona

### Objetivo
Validar entendimento antes de salvar.

### Elementos
- Nome da zona
- Lista resumida de influências
- Origem da zona
- Impactos normativos esperados

### Ações
- Confirmar
- Voltar e ajustar

---

## 9. Tela – Circuitos (Lista)

### Objetivo
Gerenciar circuitos do projeto.

### Elementos
- Lista de circuitos
  - identificação
  - tipo
  - zona associada
  - status normativo
- Botão: “Novo Circuito”

---

## 10. Tela – Criação de Circuito

### Objetivo
Definir o circuito sem repetir contexto.

### Campos
- Identificador do circuito
- Tipo de circuito
- Zona associada
- Comprimento
- Método de instalação
- Material do condutor
- Isolação
- Temperatura ambiente
- Agrupamento
- Potência ou corrente (exclusivo)
- Criticidade

### Mensagem automática
> “Este circuito herda as influências da zona selecionada.”

### Opção avançada
- Checkbox: “Sobrescrever influências da zona”
  - Exige justificativa
  - Abre wizard reduzido

---

## 11. Tela – Validação Pré-Dimensionamento

### Objetivo
Impedir cálculo sem contexto válido.

### Verificações exibidas
- Zonas completas?
- Circuitos completos?
- Conflitos normativos?

### Estados
- ✔ Pronto para dimensionar
- ✖ Ajustes necessários (lista explícita)

---

## 12. Tela – Dimensionamento

### Objetivo
Executar e analisar cálculos.

### Elementos por circuito
- Corrente de projeto
- Seção do condutor
- Dispositivo de proteção
- Queda de tensão
- Status visual (verde / amarelo / vermelho)

### Ações
- Expandir detalhes
- Ver justificativa normativa

---

## 13. Tela – Detalhes do Cálculo (Modo Didático)

### Objetivo
Expor o raciocínio sem poluir a tela principal.

### Conteúdo
- Fórmulas utilizadas
- Fatores de correção
- Origem normativa
- Texto explicativo

---

## 14. Tela – Relatório

### Objetivo
Consolidar o projeto.

### Conteúdo
- Resumo do projeto
- Zonas e influências
- Circuitos dimensionados
- Alertas normativos
- Referências à NBR 5410

### Ações
- Exportar relatório
- Revisar projeto

---

## 15. Estados globais de UX

### Erros
- Mensagens claras
- Referência ao problema, não ao usuário

### Alertas
- Decisões no limite normativo
- Recomendações, não bloqueios

### Bloqueios
- Decisões inválidas
- Justificativa explícita

---

## Consideração final

Estes wireframes definem:
- o que o usuário vê
- quando decide
- o que o sistema valida
- o que é explicitado ou ocultado

Qualquer implementação do PROJEL
deve respeitar este fluxo,
sob pena de comprometer o objetivo didático e técnico.
