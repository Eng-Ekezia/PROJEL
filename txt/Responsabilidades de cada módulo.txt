## Visão geral (uma frase que manda em tudo)

> **O PROJEL separa contexto, decisão e cálculo.**
> Cada camada existe para fazer **uma coisa só**, e fazer bem.

Se alguma camada começa a “ajudar demais”, ela está errada.

---

## 1. `domain_core`

### 🧠 Responsabilidade: **engenharia pura**

Essa é a parte mais importante do sistema.
Ela **não sabe** que existe web, banco, usuário ou VSCode.

### O que ela FAZ

* define o vocabulário técnico (enums)
* define as estruturas normativas (schemas)
* aplica regras de herança e consistência
* valida decisões de projeto
* executa cálculos normativos

### O que ela NÃO FAZ

* não renderiza tela
* não recebe request HTTP
* não salva em banco
* não decide fluxo de UX

Se amanhã você quiser:

* CLI
* desktop app
* integração com CAD
* API pública

👉 **o domínio continua igual**.

Isso é arquitetura madura.

---

### Subpartes do `domain_core`

#### `enums/`

📌 **Responsabilidade**: vocabulário fechado

* nomes oficiais
* categorias normativas
* tipos aceitos
* impede string solta

Se algo vira enum aqui, é porque **não pode variar livremente**.

---

#### `schemas/`

📌 **Responsabilidade**: estrutura e sanidade dos dados

* define o que é um projeto
* define o que é uma zona
* define o que é um circuito
* valida inconsistências óbvias

Aqui não existe cálculo, só **coerência**.

---

#### `rules/`

📌 **Responsabilidade**: decisões lógicas de projeto

* herança de influências
* exceções explícitas
* validações normativas prévias
* bloqueios conceituais

Essas regras dizem:

> “Isso faz sentido como projeto?”

Antes de perguntar:

> “Quanto dá a corrente?”

---

#### `calculations/` (quando entrar)

📌 **Responsabilidade**: matemática normativa

* corrente de projeto
* capacidade de condução
* fatores de correção
* queda de tensão
* seleção de proteção

Aqui não se decide **se** algo é aceitável.
Só se calcula **assumindo que é**.

---

## 2. Backend (FastAPI)

### 🧩 Responsabilidade: **orquestração**

O backend **não é engenheiro**.
Ele é um **maître** educado.

### O que ele FAZ

* recebe dados do frontend
* valida formato (schema)
* chama o domínio
* devolve resultados
* traduz exceções em mensagens HTTP

### O que ele NÃO FAZ

* não interpreta norma
* não decide regra
* não altera resultado
* não “conserta” entrada errada

Se o backend começar a ter lógica elétrica, o projeto apodrece.

---

## 3. Frontend (React)

### 🧭 Responsabilidade: **tradução humana**

O frontend é onde o PROJEL vira **usável**.

### O que ele FAZ

* guia o usuário no fluxo correto
* coleta decisões humanas
* explica resultados
* organiza complexidade
* evita erro por UX ruim

Ele **ensina sem dar aula**.

---

### O que o frontend NÃO FAZ

* não calcula
* não aplica norma
* não decide exceção
* não “corrige” engenharia

Ele só pergunta:

> “Você quis dizer isso mesmo?”

---

## 4. UX (camada conceitual, não técnica)

UX no PROJEL **não é estética**, é **método**.

### Responsabilidade

* transformar norma em perguntas humanas
* evitar repetição (zonas)
* tornar exceções conscientes
* mostrar consequências de decisões

UX ruim ensina errado.
UX boa **forma projetista**.

---

## 5. Persistência (SQLite, futuramente)

### Responsabilidade: **memória, não inteligência**

O banco:

* guarda projetos
* guarda zonas
* guarda circuitos
* guarda resultados

Ele **não sabe**:

* se algo está certo
* se algo é normativo
* se algo faz sentido

Se o banco “entende” engenharia, algo deu muito errado.

---

## 6. Testes

### Responsabilidade: **não deixar o sistema mentir**

* testes do domínio garantem engenharia
* testes do backend garantem integração
* testes de casos reais garantem didática

Aqui o objetivo não é cobertura bonita.
É evitar que o PROJEL ensine bobagem.

---

## 7. O PROJEL como um todo

O sistema, como entidade única, tem uma missão clara:

> **Forçar decisões explícitas, contextualizar a norma e tornar o projeto elétrico defensável.**

Ele não:

* acelera projeto mal feito
* esconde erro
* transforma chute em cálculo

E isso é exatamente o que o torna valioso em sala de aula.