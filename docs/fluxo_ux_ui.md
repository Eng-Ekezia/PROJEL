# 📄 `fluxo_ux_ui.md`

## Fluxo de UX/UI e Comportamento do Sistema PROJEL

**Versão consolidada – documento normativo interno**

---

## 1. Propósito deste documento

Este documento define **como o usuário interage com o PROJEL**, em que ordem, sob quais restrições e com quais responsabilidades.

Ele existe para garantir que:

* o sistema ensine projeto elétrico, não atalhos
* o fluxo siga o raciocínio da NBR 5410
* a interface não substitua decisões de engenharia

Nenhuma tela, botão ou automação pode violar este fluxo.

---

## 2. Princípio central da UX do PROJEL

> **A interface não facilita o projeto.
> Ela facilita o raciocínio.**

Se o usuário consegue avançar sem pensar, a UX está errada.

---

## 3. Regras gerais de navegação

### 3.1 Ordem obrigatória

O PROJEL impõe uma **ordem rígida de etapas**:

1. Projeto
2. Zonas
3. Locais
4. Cargas
5. Wizard de Agrupamento
6. Propostas de Circuito
7. Circuitos
8. Dimensionamento
9. Resultados

O usuário pode:

* voltar etapas
* revisar decisões

O usuário **não pode**:

* pular etapas
* criar entidades fora de ordem
* calcular sem contexto completo

---

### 3.2 Gate de etapa (bloqueio consciente)

Cada etapa possui um **gate de validação**.

Se o gate não for atendido:

* a próxima etapa fica bloqueada
* o sistema explica **por que**
* o sistema aponta **o que falta**

Nunca existe “seguir mesmo assim”.

---

## 4. Etapa 1 – Tela de Projeto

### Objetivo

Definir o **contexto elétrico global** do empreendimento.

### Decisões coletadas

* tipo de edificação
* sistema elétrico
* tensões
* esquema de aterramento
* diretrizes gerais

### Comportamento da UI

* campos obrigatórios
* sem valores implícitos
* sem sugestões automáticas

### Gate de saída

* todos os campos preenchidos
* coerência básica validada

---

## 5. Etapa 2 – Tela de Zonas

### Objetivo

Definir os **contextos normativos dominantes** do projeto.

### Conceito-chave

> Zona representa **ambiente normativo**, não ambiente físico.

### Funcionalidades

* criação de zonas
* uso de presets (residencial, comercial, etc.)
* edição de influências externas
* rastreabilidade de origem (preset / custom)

### UX obrigatória

* Zona sempre visível nas telas seguintes
* Influências explicadas em linguagem humana
* Códigos normativos ocultos por padrão

### Gate de saída

* pelo menos uma Zona válida e completa

---

## 6. Etapa 3 – Tela de Locais

### Objetivo

Modelar os **ambientes físicos reais** da edificação.

### Conceito-chave

> Local representa o espaço físico onde cargas existem.

### Decisões coletadas

* nome do Local
* tipo de ambiente (didático)
* área
* perímetro
* Zona associada

### Comportamento da UI

* Local **sempre criado dentro de uma Zona**
* Zona exibida explicitamente
* área e perímetro obrigatórios

### Gate de saída

* pelo menos um Local válido
* todos os Locais vinculados a Zonas

---

## 7. Etapa 4 – Tela de Cargas

### Objetivo

Definir todas as **demandas elétricas** do projeto.

### Tipos de carga

* Iluminação (normativa)
* TUG (normativa)
* TUE (explícita)

### Comportamento da UI

#### Iluminação

* gerada automaticamente por Local
* baseada na área
* valor ajustável com justificativa

#### TUG

* geradas automaticamente por Local
* baseadas em perímetro e tipo
* rastreáveis

#### TUE

* inseridas manualmente
* sempre com nome e potência

### Regras visuais

* toda carga mostra:

  * Local
  * Zona herdada
  * origem (norma / usuário)

### Gate de saída

* cargas normativas geradas
* nenhuma carga sem Local

---

## 8. Etapa 5 – Wizard de Agrupamento

### Objetivo

Auxiliar o usuário a **pensar circuitos**, não criá-los.

### Comportamento geral

* lista Locais
* lista cargas por Local
* exibe Zona de cada carga
* sugere agrupamentos possíveis

### Linguagem obrigatória

* “Agrupamento possível”
* “Agrupamento exige atenção”

### Proibições

* criar circuito
* escolher proteção
* escolher seção

### Gate de saída

* pelo menos uma Proposta de Circuito criada
* decisões explícitas do usuário

---

## 9. Etapa 6 – Propostas de Circuito

### Objetivo

Revisar intenções de agrupamento antes de formalizar circuitos.

### Conteúdo exibido

* cargas agrupadas
* Locais envolvidos
* Zonas envolvidas
* alertas normativos

### Comportamento da UI

* permitir editar
* permitir excluir
* não permitir calcular

### Gate de saída

* proposta aceita explicitamente

---

## 10. Etapa 7 – Circuitos

### Objetivo

Formalizar **decisões elétricas completas**.

### Decisões coletadas

* método de instalação
* material do condutor
* tipo de proteção
* parâmetros elétricos

### UX obrigatória

* Zona mais severa destacada
* mistura de zonas sinalizada
* nenhuma decisão implícita

### Gate de saída

* parâmetros completos
* validação estrutural OK

---

## 11. Etapa 8 – Dimensionamento

### Objetivo

Executar cálculos conforme decisões tomadas.

### Comportamento

* cálculo sob demanda
* nenhuma correção automática
* falhas normativas bloqueiam

---

## 12. Etapa 9 – Resultados

### Objetivo

Explicar o projeto, não apenas aprová-lo.

### Conteúdo mínimo

* valores calculados
* limites normativos
* margens
* condicionantes
* alertas

### UX obrigatória

* resultados explicáveis
* referências normativas
* linguagem técnica clara

---

## 13. Modo didático

### Função

Aumentar transparência normativa.

### Ativa

* códigos normativos
* justificativas
* referências à NBR 5410

### Nunca:

* altera resultados
* altera regras

---

## 14. Regra final da UX

> **A melhor interface do PROJEL é aquela que obriga o aluno a justificar suas escolhas.**

Se a interface “some” com o problema, ela falhou.

---

**Fim do arquivo `fluxo_ux_ui.md`.**
