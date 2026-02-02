# 📄 `entidade_circuito.md`

## Entidade Circuito – Decisão Técnica, Normativa e Responsável

**Versão consolidada – fechamento definitivo do domínio PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Circuito** dentro do PROJEL.

Ele existe para:

* representar a **decisão elétrica formal** do projetista
* ser o **primeiro ponto do sistema onde há responsabilidade técnica**
* concentrar parâmetros elétricos e normativos
* servir como entrada única para o motor de cálculo

Se o Circuito for tratado como “resultado automático”, o PROJEL fracassa.

---

## 2. Definição fundamental

> **Circuito é a decisão consciente de agrupar cargas sob um mesmo conjunto de parâmetros elétricos, assumindo responsabilidade técnica conforme a NBR 5410.**

Circuito **não é**:

* agrupamento automático
* consequência direta das cargas
* simples container de resultados
* entidade neutra

Circuito é **compromisso técnico**.

---

## 3. Posição hierárquica

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
                     └── Resultado de Dimensionamento
```

Regras duras:

* Circuito só nasce de **Proposta de Circuito aceita**
* Circuito nunca nasce vazio
* Circuito nunca nasce automaticamente

---

## 4. Responsabilidades da entidade Circuito

O Circuito é responsável por:

* consolidar cargas agrupadas
* assumir parâmetros elétricos
* herdar e resolver conflitos normativos
* ser avaliado pelo motor de cálculo
* produzir resultados auditáveis

O Circuito **não**:

* cria cargas
* altera cargas
* redefine Zona ou Local
* decide automaticamente soluções

---

## 5. Origem do Circuito

### Regra absoluta

> **Todo Circuito deve ter uma Proposta de Circuito como origem.**

A proposta:

* é congelada
* permanece rastreável
* nunca é apagada

Circuito sem proposta é inválido.

---

## 6. Atributos obrigatórios do Circuito

Todo Circuito deve conter:

* `id`
* `proposta_origem_id`
* `cargas_ids`
* `locais_ids` (derivado)
* `zonas_ids` (derivado)
* `zona_governante`
* `perfil_normativo_aplicavel`
* `descricao_funcional`
* `parametros_eletricos`
* `status`
* `autor`
* `data_criacao`

---

## 7. Zona governante do Circuito

### Regra dura

> **Quando um Circuito envolve cargas de múltiplas Zonas, aplica-se a Zona mais severa.**

Comportamento obrigatório:

* identificação explícita da Zona governante
* alerta ao usuário
* justificativa exibida

Nada de “média normativa”.

---

## 8. Perfil normativo aplicável

O Circuito deve consolidar:

* perfis normativos dos Locais envolvidos

### Regra

> **Se qualquer Local possuir perfil normativo especial, o Circuito herda suas exigências.**

Isso inclui:

* exigência de DR
* restrições de método
* limites adicionais

O Circuito **não escolhe ignorar isso**.

---

## 9. Parâmetros elétricos do Circuito

Esses parâmetros são **decisão do usuário**, nunca automáticos:

* tensão do circuito
* tipo de circuito (iluminação, tomadas, específico)
* método de instalação
* número de condutores carregados
* material do condutor
* tipo de isolação
* fator de agrupamento (quando aplicável)

O sistema:

* valida coerência
* alerta conflitos
* nunca decide por conta própria

---

## 10. Status do Circuito

Estados possíveis:

* `em_definicao`
* `pronto_para_calculo`
* `calculado`
* `reprovado`
* `validado`

Somente circuitos em `pronto_para_calculo` entram no motor.

---

## 11. Circuito e motor de cálculo

O Circuito:

* fornece entradas
* recebe resultados
* não executa cálculo

O motor:

* aplica NBR 5410
* gera resultados
* gera alertas
* pode reprovar o circuito

---

## 12. Exibição obrigatória na UI

Toda visualização de Circuito deve mostrar:

* cargas envolvidas
* Locais e Zonas
* Zona governante
* perfis normativos aplicáveis
* parâmetros elétricos escolhidos
* status atual

Nada pode ficar implícito.

---

## 13. Alterações no Circuito

### Regra

> **Alterar qualquer parâmetro invalida o cálculo anterior.**

Comportamento esperado:

* resultado anterior é marcado como obsoleto
* novo cálculo é exigido
* histórico é mantido

---

## 14. Erros conceituais proibidos

* Circuito criado automaticamente
* Circuito sem proposta
* Circuito sem parâmetros explícitos
* Zona governante implícita
* Perfil normativo ignorado

Qualquer um desses invalida o projeto.

---

## 15. Regra final da entidade Circuito

> **Aqui termina a modelagem.
> Aqui começa a responsabilidade do engenheiro.**

Se o aluno errar aqui, o erro é **dele**, não do sistema.
E isso é exatamente o que um bom sistema didático deve permitir.

---

**Fim do arquivo `entidade_circuito.md`.**
