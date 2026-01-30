# PROJEL

## Comportamento do Sistema, UX/UI e Fluxo de Projeto

---

## 1. Princípios gerais de UX do PROJEL

O PROJEL **não é uma calculadora** e **não é um CAD**.
Ele é um **ambiente de raciocínio de projeto elétrico**.

Princípios inegociáveis:

* o usuário **descreve a realidade**
* o sistema **traduz isso para a norma**
* o sistema **explica o resultado**, não só mostra
* nenhum campo existe sem justificativa técnica
* erro normativo é tratado como **decisão inválida**, não como “bug”

A interface evita:

* tabelas gigantes
* jargão normativo direto
* telas carregadas

A interface privilegia:

* fluxo progressivo
* decisões explícitas
* feedback imediato

---

## 2. Fluxo geral do projeto (visão macro)

O PROJEL opera sempre no mesmo macrofluxo:

1. Definição do projeto
2. Definição das zonas de influência
3. Definição dos circuitos
4. Validação de contexto
5. Dimensionamento
6. Análise de resultados
7. Ajustes iterativos

O usuário **nunca “pula” etapas**, mas pode **voltar** a qualquer uma.

---

## 3. Tela 1 – Projeto Elétrico

### Objetivo da tela

Definir o **contexto global** da instalação.

### Campos apresentados

* Nome do projeto
* Tipo de instalação (residencial, comercial, industrial)
* Sistema elétrico (mono, bi, trifásico)
* Tensão do sistema (ex: 127/220 V)
* Esquema de aterramento (TT, TN-S, etc.)
* Campo opcional: descrição do aterramento

### UX

* linguagem simples
* exemplos abaixo dos campos
* sem referência direta à norma

### Comportamento

* nenhum cálculo ocorre aqui
* decisões feitas aqui **afetam todas as etapas seguintes**
* alterações posteriores geram aviso:

  > “Esta alteração pode invalidar dimensionamentos já realizados”

---

## 4. Tela 2 – Zonas de Influência

### Objetivo da tela

Modelar o **ambiente físico e humano** da instalação.

O usuário não cria circuitos aqui.
Ele cria **contextos normativos reutilizáveis**.

---

### 4.1 Criação de uma Zona

#### Campos

* Nome da zona (ex: “Área molhada”, “Garagem”, “Apartamentos tipo”)
* Tipo da zona (residencial, técnica, externa, etc.)
* Descrição opcional

---

### 4.2 Wizard de Influências Externas (UX central do PROJEL)

O usuário **não escolhe códigos AC, BA, CB**.
Ele responde perguntas humanas.

#### Etapa A – Ambiente físico

Perguntas típicas:

* Há presença frequente de água?
* Existe poeira ou sujidade significativa?
* Há solicitações mecânicas relevantes?
* O local está exposto ao tempo?

#### Etapa B – Uso e pessoas

Perguntas típicas:

* Quem utiliza o local?
* Pessoas leigas têm acesso?
* Uma falha elétrica pode causar riscos relevantes?
* A interrupção do fornecimento causa prejuízo significativo?

#### Etapa C – Construção

Perguntas típicas:

* Existem partes metálicas acessíveis?
* A estrutura permite equipotencialização?
* Há compartimentação relevante?

---

### 4.3 Tradução normativa (invisível por padrão)

Internamente, o sistema:

* converte respostas em influências A/B/C
* atribui códigos e classes
* registra tudo no modelo de domínio

O usuário **não vê isso** por padrão.

---

### 4.4 Transparência técnica (sob demanda)

Um botão:

> “Mostrar justificativa normativa”

Exibe:

* códigos identificados (ex: AC3, BA2)
* descrição técnica
* impacto esperado no projeto

Modo professor pode deixar isso sempre visível.

---

## 5. Tela 3 – Circuitos

### Objetivo da tela

Definir os circuitos **sem repetir contexto**.

Cada circuito:

* pertence a **uma zona**
* herda suas influências externas

---

### 5.1 Criação de circuito

Campos principais:

* Identificador do circuito (C1, TUG-01)
* Tipo de circuito (iluminação, TUG, TUE)
* Zona associada
* Comprimento
* Método de instalação
* Material do condutor
* Isolação
* Temperatura ambiente
* Número de circuitos agrupados
* Potência **ou** corrente (mutuamente exclusivo)
* Criticidade (normal, importante, essencial)

---

### 5.2 Herança de influências (UX clara)

A interface mostra:

> “Este circuito herda as influências da zona ‘Área molhada’”

Um checkbox opcional:

> “Este circuito possui influências diferentes da zona”

Se marcado:

* o wizard de influências reaparece
* o sistema exige justificativa
* a exceção fica registrada

Exceção nunca é silenciosa.

---

## 6. Validação de contexto (antes do cálculo)

Antes de dimensionar, o sistema valida:

* toda zona possui influências A, B e C
* todo circuito pertence a uma zona
* não há circuitos com dados incompletos
* não há conflitos grosseiros de entrada

Se algo falhar:

* cálculo é bloqueado
* mensagem clara explica o motivo

Exemplo:

> “A zona ‘Garagem’ não possui influência da categoria B (uso).”

---

## 7. Tela 4 – Dimensionamento

### Comportamento

* cálculo ocorre **por circuito**
* mas sempre considerando:

  * zona
  * projeto
  * influências
  * criticidade

Nenhum cálculo é “cego”.

---

### Resultados apresentados por circuito

Cada circuito exibe:

* Corrente de projeto
* Seção do condutor
* Dispositivo de proteção sugerido
* Queda de tensão percentual
* Status visual:

  * verde: conforme
  * amarelo: limite
  * vermelho: não conforme

---

### Alertas normativos

Exemplos:

* “Exigência de DR devido à presença de água”
* “Método de instalação não recomendado para este ambiente”
* “Queda de tensão próxima ao limite normativo”

Alertas:

* não travam o sistema
* orientam decisões
* ficam registrados

---

## 8. Transparência dos cálculos (modo didático)

O usuário pode expandir um circuito e ver:

* fórmula aplicada
* fatores de correção
* origem normativa
* justificativa textual

Aluno vê.
Professor decide quando mostrar.

---

## 9. Iteração e ajustes

O sistema é **iterativo por natureza**.

Qualquer alteração em:

* projeto
* zona
* circuito

gera:

* aviso de impacto
* necessidade de recalcular

Nada é “automaticamente aceito”.

---

## 10. Relatórios (visão futura próxima)

O PROJEL gera:

* resumo do projeto
* lista de zonas e influências
* tabela de circuitos dimensionados
* alertas normativos
* referências à NBR 5410

Relatório:

* técnico
* enxuto
* defensável

---

## 11. O que o PROJEL NÃO faz (intencionalmente)

* não desenha
* não gera planta
* não “adivinha” dados
* não esconde decisões normativas

Ele **apoia** o projetista.
Não substitui o cérebro dele.

---

## Encerramento técnico

Este documento descreve:

* comportamento esperado
* UX coerente com engenharia
* fluxo alinhado à NBR 5410
* decisões pedagógicas conscientes

Com isso:

* o frontend pode ser implementado sem improviso
* o backend sabe o que esperar
* um assistente de vibecoding tem **referência clara**

Se quiser, o próximo passo natural é:

* transformar isso em **mapa de telas**
* ou escrever **histórias de usuário técnicas**
* ou alinhar isso com **estrutura de componentes React**

Você escolhe.
