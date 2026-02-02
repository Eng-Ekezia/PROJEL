# 📄 `entidade_projeto.md`

## Entidade Projeto – Definição Normativa e Operacional

**Versão consolidada – fonte oficial do PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Projeto** dentro do PROJEL.

Ele existe para:

* definir o **contexto elétrico global** do empreendimento
* estabelecer limites e diretrizes que governam todo o restante do sistema
* impedir decisões implícitas ou contraditórias nas etapas seguintes

Nenhuma entidade pode existir fora de um Projeto.
Nenhuma decisão pode contrariar o Projeto sem alerta explícito.

---

## 2. Definição fundamental

> **Projeto representa o contexto elétrico global de uma edificação ou instalação, conforme a NBR 5410, antes de qualquer decisão de detalhamento.**

Projeto **não é**:

* conjunto de circuitos
* conjunto de cargas
* cálculo
* resultado

Projeto é **enquadramento**, não execução.

---

## 3. Posição hierárquica

O Projeto é a **raiz absoluta** da hierarquia do PROJEL:

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
                     └── Resultado de Dimensionamento
```

Consequências diretas:

* nenhuma Zona existe sem Projeto
* nenhuma decisão elétrica pode contradizer o Projeto
* alterações no Projeto impactam todo o restante

---

## 4. Responsabilidades da entidade Projeto

O Projeto é responsável por:

* definir o tipo de edificação
* definir o sistema elétrico adotado
* definir níveis de tensão
* definir esquema de aterramento
* estabelecer diretrizes gerais de projeto

O Projeto **não**:

* define cargas
* define circuitos
* executa cálculos
* valida detalhes normativos específicos

Projeto governa. Não executa.

---

## 5. Atributos obrigatórios do Projeto

Todo Projeto deve conter, no mínimo:

* `id`
* `nome_projeto`
* `tipo_empreendimento`
* `descricao_geral`
* `sistema_eletrico`
* `tensoes_nominais`
* `esquema_aterramento`
* `criterios_gerais`
* `data_criacao`
* `autor`

Nenhum desses atributos pode ser implícito ou inferido.

---

## 6. Detalhamento dos atributos

### 6.1 Nome e identificação

* `nome_projeto`
  Identificação clara do projeto.

* `descricao_geral`
  Texto livre descrevendo escopo, premissas e limites.

---

### 6.2 Tipo de empreendimento

* `tipo_empreendimento` (enum didático)

  * residencial
  * comercial
  * industrial
  * misto
  * outro

Este atributo:

* orienta presets
* **não impõe** regras normativas automáticas

---

### 6.3 Sistema elétrico

* `sistema_eletrico`

  * monofásico
  * bifásico
  * trifásico

O sistema:

* governa tensões possíveis
* governa limites de corrente
* governa critérios de balanceamento

---

### 6.4 Tensões nominais

* `tensoes_nominais`

  * tensão fase-fase
  * tensão fase-neutro (se aplicável)

Essas tensões:

* são usadas em cálculos
* não podem ser alteradas sem impacto global

---

### 6.5 Esquema de aterramento

* `esquema_aterramento`

  * TN
  * TT
  * IT
  * variantes (TN-S, TN-C, etc.)

Este atributo:

* influencia medidas de proteção
* influencia exigências de DR
* governa verificações posteriores

---

### 6.6 Critérios gerais

* `criterios_gerais`
  Texto livre para registrar:

  * critérios adotados
  * limitações assumidas
  * decisões institucionais

Este campo é **didaticamente crítico**.

---

## 7. Projeto e Zonas (relação)

### Regra dura

> **Todas as Zonas pertencem a exatamente um Projeto.**

O Projeto:

* não herda nada das Zonas
* apenas as governa

Alterar o Projeto:

* invalida Zonas
* invalida Locais
* exige revalidação completa

---

## 8. Validações obrigatórias do Projeto

Antes de permitir avanço:

* todos os campos obrigatórios preenchidos
* coerência básica entre sistema e tensões
* esquema de aterramento definido

Projeto inválido **bloqueia todo o sistema**.

---

## 9. Alterações no Projeto (impacto)

### Regra

> **Alterar o Projeto após etapas posteriores exige confirmação explícita.**

Comportamento esperado:

* aviso de impacto global
* possível invalidação de decisões
* revalidação obrigatória

Nada de alteração silenciosa.

---

## 10. Exibição obrigatória na UI

Sempre que relevante, o sistema deve exibir:

* nome do Projeto
* sistema elétrico
* tensões
* esquema de aterramento

O usuário nunca deve “esquecer” em que contexto está projetando.

---

## 11. Erros conceituais proibidos

* Projeto criado automaticamente
* Sistema elétrico inferido
* Esquema de aterramento assumido
* Projeto alterado sem aviso
* Decisão normativa fora do Projeto

Qualquer um desses invalida a integridade do sistema.

---

## 12. Regra final da entidade Projeto

> **Projeto não resolve problemas.
> Ele define em que universo os problemas existem.**

Se o PROJEL respeitar isso, o domínio permanece íntegro.

---

**Fim do arquivo `entidade_projeto.md`.**
