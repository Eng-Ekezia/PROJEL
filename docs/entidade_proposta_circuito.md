# 📄 `entidade_proposta_circuito.md`

## Entidade Proposta de Circuito – Definição Normativa e Operacional

**Versão consolidada – fonte oficial do PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Proposta de Circuito** no PROJEL.

Ela existe para:

* separar **intenção** de **decisão**
* impedir criação precoce de circuitos
* forçar revisão consciente antes do cálculo
* tornar explícito o raciocínio de agrupamento

Sem esta entidade, o PROJEL volta a ser uma calculadora com etapas escondidas.

---

## 2. Definição fundamental

> **Proposta de Circuito é um registro explícito de intenção de agrupamento de cargas, ainda sem caráter definitivo.**

Ela **não é**:

* circuito
* entidade calculável
* entidade normativa validada
* compromisso técnico final

Proposta é **rascunho consciente**.

---

## 3. Posição hierárquica

A Proposta de Circuito ocupa a seguinte posição obrigatória:

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
```

Consequências diretas:

* proposta sempre nasce de cargas existentes
* proposta nunca nasce vazia
* circuito só pode nascer de proposta aceita

---

## 4. Responsabilidade da Proposta de Circuito

A Proposta de Circuito é responsável por:

* registrar quais cargas o usuário pretende agrupar
* explicitar Locais envolvidos
* explicitar Zonas envolvidas
* registrar observações e alertas
* permitir revisão antes da decisão final

Ela **não**:

* decide parâmetros elétricos
* executa cálculos
* valida norma
* escolhe proteção ou seção

---

## 5. Atributos obrigatórios

Toda Proposta de Circuito deve conter:

* `id`
* `cargas_ids` (lista não vazia)
* `locais_ids` (derivado das cargas)
* `zonas_ids` (derivado das cargas)
* `descricao_intencao`
* `observacoes_normativas`
* `status` (rascunho | revisada | aceita | descartada)
* `data_criacao`
* `autor`

Nenhum atributo elétrico é permitido nesta entidade.

---

## 6. Criação da Proposta de Circuito

### Origem

A Proposta de Circuito **só pode ser criada** pelo:

* Wizard de Agrupamento

Criação manual fora do wizard é proibida.

---

## 7. Relação com Cargas

### Regra dura

> **Uma Proposta de Circuito deve conter pelo menos uma Carga.**

Regras adicionais:

* uma carga pode aparecer em múltiplas propostas
* propostas concorrentes são permitidas
* exclusividade só ocorre no Circuito definitivo

Isso incentiva comparação e raciocínio, não chute.

---

## 8. Relação com Locais e Zonas

### Derivação obrigatória

* Locais e Zonas **não são escolhidos**
* são sempre derivados das Cargas incluídas

### Comportamento esperado

* se todas as cargas pertencem à mesma Zona → proposta homogênea
* se pertencem a Zonas diferentes → proposta heterogênea

A proposta **não resolve o conflito**, apenas o expõe.

---

## 9. Mistura de Zonas (tratamento)

### Regra

Mistura de Zonas em uma Proposta de Circuito:

* é permitida
* deve gerar alerta explícito
* não bloqueia a proposta

A decisão final é postergada para o Circuito.

---

## 10. Status da Proposta

Estados possíveis:

* `rascunho`

  * criada pelo wizard
  * ainda não revisada

* `revisada`

  * analisada pelo usuário
  * ajustes feitos

* `aceita`

  * pronta para virar Circuito
  * congelada para edição

* `descartada`

  * não será utilizada
  * mantida para rastreabilidade

Circuito **só pode ser criado** a partir de proposta `aceita`.

---

## 11. Proposta e validação normativa

A Proposta de Circuito:

* **não é validada normativamente**
* pode conter conflitos
* pode conter inconsistências

Ela existe exatamente para **permitir que esses conflitos apareçam**.

Validação normativa começa **após** virar Circuito.

---

## 12. Exibição obrigatória na UI

Toda Proposta de Circuito deve exibir:

* lista de cargas
* Locais envolvidos
* Zonas envolvidas
* indicação clara de mistura de zonas
* observações normativas
* status atual

Nenhum parâmetro elétrico deve aparecer.

---

## 13. Conversão para Circuito

### Regra

> **Converter proposta em circuito é uma decisão explícita do usuário.**

No momento da conversão:

* a proposta é congelada
* os dados são copiados
* nasce um Circuito vazio de parâmetros elétricos

Nada é herdado além das cargas.

---

## 14. Erros conceituais proibidos

* Proposta sem carga
* Proposta criada fora do wizard
* Proposta calculável
* Proposta com seção, disjuntor ou método
* Proposta que escolhe zona

Qualquer um destes invalida o modelo.

---

## 15. Regra final da entidade Proposta de Circuito

> **Antes de assumir responsabilidade técnica, o projetista deve poder errar sem consequência.**

A Proposta de Circuito é o espaço seguro do erro consciente.

---

**Fim do arquivo `entidade_proposta_circuito.md`.**
