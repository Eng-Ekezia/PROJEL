# 📄 `entidade_zona.md`

## Entidade Zona – Definição Normativa e Operacional

**Versão consolidada – fonte oficial do PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Zona** dentro do PROJEL.

Ele existe para:

* traduzir as **influências externas da NBR 5410** para o modelo computacional
* concentrar o **contexto normativo dominante** do projeto
* governar Locais, Cargas e Circuitos de forma coerente
* impedir decisões normativas fragmentadas ou implícitas

Se Zona estiver mal definida, o projeto perde rastreabilidade normativa.

---

## 2. Definição fundamental

> **Zona representa um contexto normativo homogêneo, definido pelas influências externas da NBR 5410, que governa todos os elementos elétricos nela contidos.**

Zona **não é**:

* ambiente físico
* local arquitetônico
* circuito
* agrupamento de cargas

Zona é **regra**, não espaço.

---

## 3. Posição hierárquica

A Zona ocupa a seguinte posição obrigatória:

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
```

Consequências diretas:

* Zona sempre pertence a exatamente um Projeto
* nenhuma entidade abaixo pode existir sem Zona
* Zona nunca pertence a Circuito
* Circuito apenas herda consequências de Zonas

---

## 4. Responsabilidades da entidade Zona

A Zona é responsável por:

* definir influências externas (categorias A, B e C)
* estabelecer severidade ambiental e de uso
* impor exigências normativas derivadas
* governar decisões posteriores

A Zona **não**:

* calcula
* agrupa
* decide parâmetros elétricos
* cria cargas ou circuitos

Zona governa. Não executa.

---

## 5. Influências externas (núcleo da Zona)

### Base normativa

NBR 5410 – Influências externas:

* Categoria A: meio ambiente
* Categoria B: utilização
* Categoria C: construção da edificação

### Estrutura obrigatória

Cada Zona deve conter:

* influências da categoria A
* influências da categoria B
* influências da categoria C

Zona **nunca pode ser parcial**.

---

## 6. Atributos obrigatórios da Zona

Toda Zona deve conter:

* `id`
* `nome_zona`
* `descricao`
* `influencias_categoria_A`
* `influencias_categoria_B`
* `influencias_categoria_C`
* `origem` (preset | custom | ajustada)
* `projeto_id`
* `data_criacao`
* `autor`

Nenhuma influência pode ser implícita.

---

## 7. Origem da Zona

### Tipos de origem

* `preset`
  Zona criada a partir de modelos pré-definidos (ex: residencial seco).

* `custom`
  Zona criada manualmente pelo usuário.

* `ajustada`
  Zona derivada de um preset, mas modificada.

A origem deve ser:

* registrada
* exibida
* mantida para auditoria

---

## 8. Presets de Zona (regra clara)

Presets:

* **não são verdades normativas**
* são pontos de partida didáticos

Qualquer preset:

* pode ser ajustado
* nunca é aplicado silenciosamente
* mantém rastreabilidade

Preset ajustado ≠ preset original.

---

## 9. Zona e Local (relação)

### Regra dura

> **Todo Local pertence a exatamente uma Zona.**

Consequências:

* Local herda integralmente as influências da Zona
* Local não altera influências
* Local não complementa influências

Se o ambiente muda, cria-se outra Zona.

---

## 10. Zona e Carga (relação)

### Regra dura

> **Toda Carga herda automaticamente a Zona do Local ao qual pertence.**

Carga:

* não escolhe Zona
* não mistura Zonas
* não sobrepõe influências

Mistura só ocorre no Circuito.

---

## 11. Zona e Circuito (relação)

Circuitos:

* podem agrupar cargas de Zonas diferentes
* nesse caso, são governados pela **Zona mais severa**

### Comportamento obrigatório

* detecção explícita de mistura
* alerta normativo
* exigência de confirmação do usuário

Nada é silencioso.

---

## 12. Severidade normativa

### Regra

> **Quando múltiplas Zonas afetam um Circuito, prevalece a condição mais severa.**

Essa severidade deve ser:

* identificável
* justificável
* exibida ao usuário

---

## 13. Validações obrigatórias da Zona

Antes de permitir avanço:

* todas as categorias A, B e C definidas
* nenhuma influência em estado indefinido
* associação válida ao Projeto

Zona inválida bloqueia Locais e tudo abaixo.

---

## 14. Exibição obrigatória na UI

Sempre que relevante, o sistema deve exibir:

* nome da Zona
* origem (preset/custom/ajustada)
* resumo das influências
* impactos normativos principais

Zona **nunca pode ficar oculta**.

---

## 15. Alterações na Zona (impacto)

### Regra

> **Alterar uma Zona invalida todas as entidades abaixo dela.**

Comportamento esperado:

* aviso de impacto
* necessidade de revalidação
* possível invalidação de circuitos

Nada de alteração inocente.

---

## 16. Erros conceituais proibidos

* Zona sem todas as categorias
* Zona criada automaticamente
* Zona inferida a partir de Local
* Zona atribuída diretamente a Circuito
* Zona alterada sem aviso

Qualquer um desses quebra o domínio.

---

## 17. Regra final da entidade Zona

> **Zona é a tradução da norma para o projeto.
> Se a Zona estiver errada, todo o resto é irrelevante.**

---

**Fim do arquivo `entidade_zona.md`.**
