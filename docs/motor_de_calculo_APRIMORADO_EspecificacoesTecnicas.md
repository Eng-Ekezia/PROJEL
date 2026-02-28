# 📘 Especificação Técnica – Motor NBR Contextualizado (PROJEL)

---

# 1. Visão Geral da Arquitetura

```
domain_core/
 ├── engine/
 │    ├── dimensionador_projeto.py
 │    ├── contexto_instalacao.py
 │    ├── influencias_externas.py
 │    ├── regras_zona.py
 │    ├── calculo_corrente.py
 │    ├── selecao_condutor.py
 │    ├── selecao_disjuntor.py
 │    ├── calculo_queda_tensao.py
 │    ├── validacoes_normativas.py
 │    └── resultado_builder.py
```

Princípio central:

O motor é **100% desacoplado da API** e **100% dependente do domínio e do repositório normativo**.

Não conhece HTTP.
Não conhece banco.
Não conhece frontend.

---

# 2. Arquivo: `dimensionador_projeto.py`

## Responsabilidade

Orquestrar o dimensionamento completo de um Projeto.

Ele coordena:

* Iteração por circuitos
* Construção de contexto
* Aplicação das regras normativas
* Consolidação dos resultados

## O que faz

* Recebe objeto `Projeto`
* Percorre `locais → zonas → circuitos`
* Instancia `ContextoInstalacao`
* Chama os módulos de cálculo
* Produz lista de `ResultadoDimensionamento`

## O que NÃO faz

* Não executa cálculos matemáticos diretamente
* Não consulta tabela normativa diretamente
* Não valida regras específicas
* Não formata saída para API
* Não persiste dados

## Dependências

* contexto_instalacao
* regras_zona
* calculo_corrente
* selecao_condutor
* calculo_queda_tensao
* selecao_disjuntor
* validacoes_normativas
* resultado_builder

---

# 3. Arquivo: `contexto_instalacao.py`

## Responsabilidade

Consolidar todas as variáveis ambientais e estruturais que influenciam o dimensionamento.

## Estrutura

Classe:

```
ContextoInstalacao:
    projeto
    local
    zona
    circuito
    influencias_externas
    restricoes_normativas
```

## O que faz

* Recebe entidades estruturais
* Extrai tipo de zona
* Extrai tipo de instalação
* Identifica fatores ambientais
* Constrói objeto de restrições técnicas

## O que NÃO faz

* Não realiza cálculo elétrico
* Não consulta tabela normativa diretamente
* Não valida conformidade final

## Dependências

* influencias_externas
* regras_zona

---

# 4. Arquivo: `influencias_externas.py`

## Responsabilidade

Mapear características ambientais da Zona em impactos técnicos.

## O que faz

Traduz:

* Zona úmida
* Área externa
* Temperatura elevada
* Ambiente agressivo
* Presença de público

Em:

* Fatores de correção térmica
* Exigência de DR
* Limite de queda de tensão
* Grau mínimo de proteção IP
* Restrições de método de instalação

## O que NÃO faz

* Não executa cálculo de corrente
* Não seleciona seção
* Não decide disjuntor
* Não valida norma final

## Dependência

* normative_repository (indiretamente via regras_zona)

---

# 5. Arquivo: `regras_zona.py`

## Responsabilidade

Converter influências externas em restrições normativas aplicáveis.

## O que faz

* Consulta repositório normativo
* Determina:

  * fator de correção térmica
  * limite máximo de queda de tensão
  * exigência obrigatória de DR
  * exigência de grau IP
* Retorna objeto `RestricoesNormativas`

## O que NÃO faz

* Não realiza cálculo elétrico
* Não seleciona componentes
* Não valida projeto completo

## Dependência

* normative_repository

---

# 6. Arquivo: `calculo_corrente.py`

## Responsabilidade

Calcular corrente elétrica da carga ou do circuito.

## O que faz

* Implementa fórmulas para:

  * Monofásico
  * Bifásico
  * Trifásico
* Aplica fator de potência
* Retorna corrente calculada

## O que NÃO faz

* Não aplica fator de correção térmica
* Não decide seção
* Não consulta norma
* Não valida conformidade

---

# 7. Arquivo: `selecao_condutor.py`

## Responsabilidade

Selecionar seção mínima do condutor.

## O que faz

* Recebe:

  * corrente calculada
  * método de instalação
  * fatores de correção
* Consulta tabela NBR
* Aplica fatores ambientais
* Retorna seção recomendada

## O que NÃO faz

* Não calcula corrente
* Não valida queda de tensão
* Não seleciona disjuntor
* Não valida conformidade final

## Dependência

* normative_repository

---

# 8. Arquivo: `calculo_queda_tensao.py`

## Responsabilidade

Calcular queda percentual de tensão.

## O que faz

* Utiliza:

  * comprimento do circuito
  * resistividade
  * seção escolhida
  * corrente
* Retorna percentual de queda

## O que NÃO faz

* Não seleciona seção
* Não valida limite permitido
* Não altera escolha de condutor

---

# 9. Arquivo: `selecao_disjuntor.py`

## Responsabilidade

Selecionar dispositivo de proteção adequado.

## O que faz

* Recebe corrente calculada
* Consulta curvas disponíveis
* Verifica coordenação com seção
* Aplica exigências (ex: DR obrigatório)
* Retorna disjuntor recomendado

## O que NÃO faz

* Não calcula corrente
* Não valida queda de tensão
* Não valida conformidade global

---

# 10. Arquivo: `validacoes_normativas.py`

## Responsabilidade

Realizar validação final de conformidade normativa.

## O que faz

* Verifica:

  * queda ≤ limite
  * seção ≥ mínima normativa
  * disjuntor compatível
  * exigências ambientais atendidas
* Retorna:

  * atende_norma (bool)
  * lista de inconformidades

## O que NÃO faz

* Não altera resultados
* Não recalcula seção
* Não decide componentes

---

# 11. Arquivo: `resultado_builder.py`

## Responsabilidade

Construir objeto final `ResultadoDimensionamento`.

## O que faz

* Consolida:

  * corrente
  * seção
  * disjuntor
  * queda
  * fatores aplicados
  * inconformidades
* Retorna objeto estruturado

## O que NÃO faz

* Não executa cálculos
* Não consulta norma
* Não valida regras

---

# 12. Fluxo de Dependência

Dependência unidirecional:

```
dimensionador_projeto
    ↓
contexto_instalacao
    ↓
regras_zona
    ↓
influencias_externas
    ↓
normative_repository
```

Módulos matemáticos:

```
calculo_corrente
selecao_condutor
calculo_queda_tensao
selecao_disjuntor
```

Validação final:

```
validacoes_normativas
```

Construção final:

```
resultado_builder
```

Nenhum módulo inferior conhece o superior.

---

# 13. Regras Arquiteturais Obrigatórias

1. Nenhum módulo pode acessar diretamente dados da API.
2. Nenhum módulo pode alterar entidades estruturais.
3. normative_repository é a única fonte normativa.
4. Influências externas devem impactar explicitamente fatores de cálculo.
5. Resultado final deve registrar quais influências foram aplicadas.

---

# 14. Limites Explícitos do Motor

O motor NÃO:

* Persiste resultados
* Faz cache
* Gera relatórios PDF
* Controla estado do projeto
* Realiza autenticação
* Conhece usuário

Ele apenas dimensiona sob contexto normativo.

---

# 15. Benefício Arquitetural

* Alta testabilidade
* Auditoria acadêmica possível
* Evolução normativa isolada
* Separação clara entre ambiente e cálculo
