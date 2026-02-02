# 📄 `architecture.md`

## Arquitetura Conceitual e Técnica do PROJEL

**Versão consolidada – base oficial do projeto**

---

## 1. Propósito deste documento

Este documento define a **arquitetura conceitual e técnica** do PROJEL.

Ele existe para:

* orientar desenvolvimento
* evitar decisões contraditórias
* servir como referência para revisões futuras
* impedir que o sistema se degrade em uma “calculadora bonita”

Nenhum código, tela ou fluxo pode contradizer este documento.

---

## 2. Princípios fundamentais do PROJEL

O PROJEL é regido por três princípios inegociáveis:

### 2.1 Decisão é humana

O sistema **nunca decide** aquilo que é decisão de projeto.

### 2.2 Regra é normativa

A NBR 5410 é tratada como **sistema de restrições e condicionantes**, não como tabela de consulta solta.

### 2.3 Cálculo é mecânico

O motor de cálculo **executa**, **verifica** e **compara**.
Ele **não escolhe** alternativas.

> Se uma decisão não foi explicitamente tomada pelo usuário, ela não pode existir no sistema.

---

## 3. Visão geral da arquitetura

O PROJEL adota uma arquitetura **orientada a domínio**, com separação rígida entre:

* domínio elétrico
* interface
* orquestração
* persistência

A arquitetura existe para **proteger o domínio**, não para facilitar atalhos de implementação.

---

## 4. Camadas do sistema

### 4.1 UI / UX (Frontend)

Responsabilidade:

* coletar decisões explícitas
* impedir avanço sem pré-condições
* tornar contexto normativo visível
* expor consequências das escolhas

A UI **não interpreta norma**, **não calcula** e **não corrige decisões**.

---

### 4.2 API / Orquestração

Responsabilidade:

* receber decisões do frontend
* validar estrutura e completude
* encaminhar ao domínio
* devolver respostas explicáveis

A API **não contém regra elétrica**.

---

### 4.3 Domain Core (núcleo do sistema)

Responsabilidade:

* conter toda a lógica normativa
* definir entidades
* aplicar validações normativas
* executar cálculos

Toda regra elétrica **vive aqui**.

---

### 4.4 Persistência

Responsabilidade:

* armazenar estado
* versionar decisões
* recuperar projetos

Persistência **não valida** e **não decide**.

---

## 5. Hierarquia obrigatória de entidades

O PROJEL possui uma hierarquia rígida. Nenhuma entidade pode “pular” níveis.

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
                     └── Resultado de Dimensionamento
```

Qualquer implementação que permita criar uma entidade fora dessa ordem está errada.

---

## 6. Entidades e seus papéis (visão arquitetural)

### 6.1 Projeto

Define o **contexto elétrico global**:

* sistema elétrico
* tensões
* esquema de aterramento
* diretrizes gerais

Não contém cargas nem circuitos.

---

### 6.2 Zona

Define o **contexto normativo dominante**:

* influências externas (A, B, C)
* severidade
* exigências de proteção

Zona governa tudo que está abaixo dela.

---

### 6.3 Local

Representa o **ambiente físico funcional**:

* área
* perímetro
* uso
* vínculo com Zona

Local é a ponte entre espaço físico e norma.

---

### 6.4 Carga

Representa uma **demanda elétrica**:

* iluminação (normativa)
* TUG (normativa)
* TUE (explícita)

Carga nunca decide, nunca agrupa e nunca calcula.

---

### 6.5 Proposta de Circuito

Representa uma **intenção de agrupamento**:

* ainda sem cálculo
* ainda sem proteção
* ainda sem seção

É um rascunho consciente, não um circuito.

---

### 6.6 Circuito

Representa uma **decisão formal de projeto**:

* parâmetros completos
* pronto para validação e cálculo

Circuito pode ser calculado. Proposta não.

---

### 6.7 Resultado de Dimensionamento

Representa:

* valores calculados
* limites normativos
* margens técnicas
* condicionantes

Resultado **explica**, não apenas informa.

---

## 7. Fluxo normativo obrigatório

Nenhuma etapa pode ser pulada.

1. Definir Projeto
2. Definir Zonas
3. Definir Locais
4. Gerar e revisar Cargas
5. Agrupar cargas (Wizard)
6. Criar Propostas de Circuito
7. Converter em Circuitos
8. Validar contexto normativo
9. Dimensionar
10. Analisar resultados

O sistema deve **bloquear** qualquer tentativa de avanço fora dessa ordem.

---

## 8. Separação interna no Domain Core

O núcleo do domínio deve separar claramente:

* validação estrutural
* validação normativa
* cálculo elétrico

Nenhuma função pode fazer as três coisas ao mesmo tempo.

---

## 9. Tratamento de erros e alertas

* **Erro**: decisão inválida → bloqueio
* **Alerta**: decisão válida com risco → aviso explícito

Nunca mascarar erro como alerta.

---

## 10. Regra final da arquitetura

> O PROJEL deve ser mais rígido que o aluno
> e mais honesto que uma planilha.

Se essa frase continuar verdadeira, a arquitetura está correta.

---

**Fim do arquivo `architecture.md`.**
