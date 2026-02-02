# 📄 `entidade_carga.md`

## Entidade Carga – Definição Normativa e Operacional

**Versão consolidada – fonte oficial do PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Carga** dentro do PROJEL.

Ele existe para garantir que:

* a origem das demandas elétricas seja clara
* a norma não seja diluída em “potências genéricas”
* o aluno compreenda de onde surgem os valores que ele dimensiona
* o sistema nunca trate carga como circuito ou decisão de projeto

Se a entidade Carga estiver mal definida, todo o restante do sistema se degrada.

---

## 2. Definição fundamental

> **Carga é uma demanda elétrica associada a um Local, governada por uma Zona, com origem normativa ou explícita.**

Carga **não é**:

* circuito
* proteção
* equipamento genérico sem contexto
* valor arbitrário “para fechar conta”

---

## 3. Posição hierárquica

A Carga ocupa a seguinte posição obrigatória:

```
Projeto
 └── Zona
     └── Local
         └── Carga
```

Consequências diretas:

* toda Carga pertence a exatamente um Local
* toda Carga herda exatamente uma Zona
* Carga nunca pertence diretamente a um Circuito
* Circuitos agrupam Cargas, não o contrário

---

## 4. Responsabilidades da entidade Carga

A Carga é responsável por:

* representar uma demanda elétrica
* manter sua origem rastreável
* fornecer dados para agrupamento
* fornecer dados para cálculo

A Carga **não**:

* decide agrupamento
* decide proteção
* decide seção
* decide método de instalação
* executa cálculo

Carga não pensa. Ela é pensada.

---

## 5. Atributos obrigatórios da Carga

Toda Carga, independentemente do tipo, deve possuir:

* `id`
* `tipo_carga`
* `potencia_va` ou `potencia_w`
* `origem`
* `local_id`
* `zona_id`
* `descricao`
* `ajustada` (boolean)
* `justificativa_ajuste` (se aplicável)

Zona e Local **nunca são escolhidos pela Carga**.
Eles são herdados.

---

## 6. Classificação das Cargas

O PROJEL reconhece **três tipos de carga**, cada um com regras próprias.

---

### 6.1 Carga de Iluminação (Normativa)

#### Definição

Carga de iluminação representa a **potência mínima exigida pela NBR 5410** para iluminação de um Local.

#### Origem

* sempre normativa
* gerada automaticamente pelo sistema

#### Base normativa

* área do Local
* critérios da NBR 5410

#### Regras obrigatórias

* toda Local possui pelo menos uma carga de iluminação
* valor inicial calculado pelo sistema
* usuário pode ajustar o valor **somente com justificativa**
* ajuste nunca apaga o valor normativo original

#### Atributos específicos

* `criterio_normativo` (ex: área)
* `valor_normativo`
* `valor_ajustado` (se houver)

---

### 6.2 Carga de TUG (Normativa)

#### Definição

Carga de TUG representa **tomadas de uso geral**, conforme regras mínimas da NBR 5410.

#### Origem

* normativa
* gerada automaticamente por Local

#### Base normativa

* perímetro do Local
* tipo de ambiente

#### Regras obrigatórias

* quantidade mínima definida pela norma
* potência atribuída conforme norma
* agrupamento interno permitido apenas para exibição

#### Atributos específicos

* `quantidade`
* `potencia_unitaria`
* `criterio_normativo`

A Carga de TUG pode ser:

* exibida como múltiplas cargas
* ou como carga agregada

Isso é decisão de UX, não de domínio.

---

### 6.3 Carga de TUE (Explícita)

#### Definição

Carga de TUE representa **equipamento de uso específico**, definido pelo projetista.

#### Origem

* sempre explícita
* sempre manual

#### Regras obrigatórias

* nome obrigatório
* potência obrigatória
* finalidade explícita
* nunca gerada automaticamente

Exemplos:

* chuveiro elétrico
* forno elétrico
* motor específico

---

## 7. Herança normativa (regra dura)

### Regra

> **Toda Carga herda automaticamente a Zona do Local ao qual pertence.**

Consequências:

* carga nunca pertence a múltiplas zonas
* carga nunca escolhe zona
* mistura de zonas ocorre apenas em circuitos

Essa regra é **inamovível**.

---

## 8. Ajustes e rastreabilidade

### Ajuste permitido

* apenas quando a norma permitir
* sempre com justificativa textual
* sempre mantendo o valor original

### Ajuste proibido

* apagar valor normativo
* esconder origem
* ajustar sem justificativa

O sistema deve registrar:

* quem ajustou
* quando ajustou
* por quê ajustou

---

## 9. Carga e agrupamento

Carga:

* pode ser sugerida em agrupamentos
* pode participar de múltiplas propostas
* não sabe que está em circuito

Somente após a criação de Circuito:

* a carga passa a estar vinculada a um circuito

---

## 10. Validações obrigatórias da Carga

Antes de avançar no fluxo:

* potência definida
* Local válido
* Zona herdada
* origem definida

Carga inválida bloqueia avanço.

---

## 11. Exibição obrigatória na UI

Toda representação de carga deve exibir claramente:

* tipo da carga
* Local
* Zona
* origem (norma / usuário)
* potência
* indicação de ajuste (se houver)

Zona **nunca pode ficar implícita**.

---

## 12. Erros conceituais proibidos

* Carga sem Local
* Carga sem Zona
* Carga criada direto em Circuito
* Carga normativa sem rastreabilidade
* TUE criada automaticamente
* Carga ajustada sem justificativa

Qualquer um desses invalida o projeto.

---

## 13. Regra final da entidade Carga

> **Carga não é decisão.
> É consequência de contexto.**

Se o PROJEL tratar carga como valor solto, ele trai o propósito didático.

---

**Fim do arquivo `entidade_carga.md`.**
