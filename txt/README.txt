# PROJEL

**PROJEL** é um sistema web de apoio ao projeto elétrico conforme a
**ABNT NBR 5410**, desenvolvido com foco em raciocínio de engenharia,
contexto normativo e excelência didática.

O objetivo do PROJEL é substituir planilhas genéricas por um ambiente
que force decisões explícitas, valide contexto e torne o projeto
eletricamente defensável.

---

## 🎯 Objetivo do Projeto

- Apoiar disciplinas de Instalações Elétricas
- Reforçar o raciocínio de projeto, não apenas o cálculo
- Traduzir a NBR 5410 em decisões claras e auditáveis
- Servir como base para projetos acadêmicos reais

Público-alvo:
- Engenharia Civil
- Engenharia de Energia

---

## 🧠 Princípios do PROJEL

- Engenharia antes de interface
- Contexto antes de circuito
- Norma como regra explícita
- Usuário descreve a realidade, sistema traduz para a norma
- Transparência técnica sem poluição cognitiva

---

## 🏗️ Arquitetura

O PROJEL é estruturado em camadas bem definidas:

- **Frontend (React)**  
  Interface e experiência do usuário

- **Backend (FastAPI)**  
  Orquestração e contratos

- **Domain Core (Python)**  
  Lógica de engenharia e norma

- **Persistência (SQLite)**  
  Armazenamento didático

Detalhes completos estão disponíveis em:
[`docs/architecture.md`](docs/architecture.md)

---

## 🔁 Fluxo de uso

1. Definição do projeto elétrico
2. Criação de zonas de influência
3. Definição dos circuitos
4. Validação de contexto normativo
5. Dimensionamento elétrico
6. Análise de resultados e ajustes

O sistema é iterativo e orientado a decisões explícitas.

---

## 🧪 Status do Projeto

🚧 Em desenvolvimento ativo  
Fase atual: **Domínio e regras normativas**

Este projeto é utilizado como base didática e evolui de forma incremental.

---

## 🛠️ Stack Tecnológica

- Python 3.11
- Pydantic
- FastAPI
- React + TypeScript
- SQLite
- Deploy em serviços free-tier

---

## 📄 Licença

Este projeto é distribuído sob licença **MIT**.

---

## 👤 Autor

Desenvolvido por **Ezequiel Lima**  
Professor e pesquisador na área de Engenharia Elétrica.

---

## ⚠️ Aviso

O PROJEL é uma ferramenta de apoio ao projeto elétrico.
Ele **não substitui o engenheiro responsável** nem dispensa
a análise crítica e o julgamento técnico.
````
