# PROJEL

### Projeto Elétrico Didático conforme NBR 5410

---

## 1. O que é o PROJEL

O **PROJEL** é uma aplicação web de apoio ao ensino e à prática de **projetos elétricos de baixa tensão**, desenvolvida com foco explícito na **NBR 5410** e no **raciocínio de engenharia**, não na automação cega de cálculos.

O sistema foi concebido para:

* substituir planilhas didáticas frágeis
* expor decisões de projeto de forma rastreável
* ensinar o *porquê* das escolhas, não apenas o *como calcular*

O PROJEL **não é** um CAD, **não é** um dimensionador automático e **não é** um gerador de projetos finais.

---

## 2. Princípios fundamentais

O PROJEL é regido por três princípios inegociáveis:

> **Decisão é humana**
> **Regra é normativa**
> **Cálculo é mecânico**

Se qualquer parte do sistema violar isso, o projeto está conceitualmente errado.

---

## 3. Público-alvo

* Estudantes de Engenharia Civil
* Estudantes de Engenharia de Energia
* Docentes de Instalações Elétricas
* Projetistas em formação

O sistema assume **nível técnico**, não simplifica linguagem para leigos.

---

## 4. O que o PROJEL faz

✔ Modela o contexto normativo do projeto
✔ Explicita influências externas conforme a NBR 5410
✔ Gera cargas normativas de iluminação e TUG
✔ Permite inclusão consciente de TUE
✔ Auxilia o agrupamento de cargas em circuitos
✔ Executa dimensionamento elétrico com rastreabilidade
✔ Explica resultados e alertas normativos

---

## 5. O que o PROJEL não faz

✘ Não cria circuitos automaticamente
✘ Não escolhe seção de condutor
✘ Não escolhe disjuntor
✘ Não corrige decisões erradas
✘ Não esconde conflitos normativos
✘ Não substitui o engenheiro

Se o aluno “apertar um botão e sair com o projeto pronto”, algo deu errado.

---

## 6. Arquitetura conceitual (visão geral)

O PROJEL é orientado a **domínio**, não a interface.

### Hierarquia obrigatória de entidades

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
                     └── Resultado de Dimensionamento
```

Nenhuma entidade pode existir fora dessa ordem.

---

## 7. Fluxo normativo do sistema

O usuário é conduzido pelo **mesmo raciocínio de um projeto real**:

1. Definição do Projeto
2. Definição das Zonas (influências externas)
3. Definição dos Locais (ambientes físicos)
4. Geração e revisão das Cargas
5. Wizard de Agrupamento de Cargas
6. Criação de Propostas de Circuito
7. Conversão em Circuitos
8. Dimensionamento
9. Análise de Resultados

O sistema **bloqueia** qualquer tentativa de pular etapas.

---

## 8. Entidades centrais (resumo)

### Projeto

Define o contexto elétrico global.

### Zona

Define o contexto normativo dominante (influências externas).

### Local

Representa o ambiente físico funcional.

### Carga

Representa a demanda elétrica (Iluminação, TUG ou TUE).

### Proposta de Circuito

Registro de intenção de agrupamento (ainda sem decisão técnica).

### Circuito

Decisão formal de projeto, pronta para cálculo.

### Resultado

Explicação técnica do que foi calculado e por quê.

---

## 9. Wizard de Agrupamento (ponto crítico)

O wizard:

* lista Locais
* lista Cargas por Local
* mostra Zonas herdadas
* sugere agrupamentos possíveis

O wizard **não**:

* cria circuitos
* escolhe parâmetros
* valida projeto

Ele apenas pergunta:

> “Essas cargas podem formar um circuito?”

---

## 10. Tratamento de Zonas

* Toda Carga pertence a **uma única Zona**
* Circuitos podem agrupar cargas de Zonas diferentes
* Nesse caso, o circuito é governado pela **Zona mais severa**
* O sistema **sempre alerta**, nunca silencia

---

## 11. Motor de cálculo

O motor de cálculo:

* executa fórmulas
* aplica fatores
* verifica limites
* gera alertas e bloqueios

Ele **não decide** alternativas.

---

## 12. Resultados e relatórios

Resultados nunca são apenas “OK”.

Todo resultado apresenta:

* valor calculado
* limite normativo
* margem técnica
* condicionantes
* referências à norma

Erro também ensina.

---

## 13. Stack tecnológica (referência)

* Frontend: React + TypeScript + Vite
* UI: Material UI
* Backend: Python 3.11 + FastAPI
* Domínio: orientado a regras normativas
* Persistência: SQLite (didático)
* Deploy: free tier

A stack é **meio**, não fim.

---

## 14. Licença e uso

O PROJEL é concebido como:

* software livre
* uso acadêmico prioritário
* foco didático

Ele não substitui responsabilidade técnica profissional.

---

## 15. Regra final (a mais importante)

> **Se o aluno consegue usar o PROJEL sem pensar, o PROJEL falhou.**

Este README existe para impedir isso.

---

**PROJEL**
*Projeto Elétrico não é cálculo. É decisão.*
