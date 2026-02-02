# 📄 `entidade_resultado_dimensionamento.md`

## Entidade Resultado de Dimensionamento – Avaliação Normativa Explícita

**Versão consolidada – núcleo didático do PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Resultado de Dimensionamento** no PROJEL.

Ela existe para:

* representar o **estado normativo** de um circuito
* tornar explícitas **todas as verificações exigidas pela NBR 5410**
* impedir conclusões simplistas do tipo “passou / não passou”
* expor conflitos técnicos de forma didática e rastreável

Resultado **não é solução**.
Resultado é **diagnóstico normativo**.

---

## 2. Definição fundamental

> **Resultado de Dimensionamento é o conjunto estruturado de verificações normativas aplicadas a um Circuito, com seus respectivos valores calculados, limites normativos e status.**

Resultado **não é**:

* decisão de projeto
* escolha automática de condutor
* escolha automática de proteção
* entidade que “corrige” erro do usuário

Resultado **mostra**. Quem decide é o projetista.

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
                         └── Verificacoes Normativas
```

Regras duras:

* Resultado sempre pertence a exatamente um Circuito
* Circuito pode ter múltiplos Resultados (histórico)
* Resultado nunca altera o Circuito

---

## 4. Responsabilidades da entidade Resultado

O Resultado é responsável por:

* armazenar todas as verificações aplicáveis
* registrar valores calculados
* registrar limites normativos
* indicar atendimento ou não atendimento
* consolidar o status global do circuito

O Resultado **não**:

* escolhe parâmetros
* altera entradas
* propõe soluções
* decide validade por conveniência

---

## 5. Estrutura conceitual do Resultado

### Estrutura geral

```
ResultadoDimensionamento
 ├── id
 ├── circuito_id
 ├── data_execucao
 ├── verificacoes[]
 ├── status_global
 ├── observacoes
 └── referencia_normativa_geral
```

---

## 6. Conceito central: Verificação Normativa

### Definição

> **Verificação Normativa é a aplicação objetiva de um critério da NBR 5410 a um Circuito específico.**

Cada verificação é **independente** das demais.

---

### Entidade: VerificacaoNormativa

#### Atributos obrigatórios

* `criterio`
* `valor_calculado`
* `limite_normativo`
* `status`
* `referencia_normativa`
* `comentario_tecnico`

Nenhum desses campos é opcional.

---

## 7. Enum: Critério de Verificação

Critérios iniciais obrigatórios no PROJEL:

* `capacidade_conducao_corrente`
* `queda_tensao`
* `protecao_sobrecorrente`
* `protecao_curto_circuito`
* `atuacao_dr` (quando aplicável)
* `medidas_adicionais` (quando perfil normativo exigir)

Essa lista:

* é explícita
* é extensível
* nunca é inferida

---

## 8. Enum: Status da Verificação

Estados possíveis e exclusivos:

* `atende`
* `nao_atende`
* `atende_com_restricao`

Definições:

* **atende**: cumpre integralmente a norma
* **nao_atende**: viola requisito normativo
* **atende_com_restricao**: atende, mas com limitação relevante

Não existe “quase atende”.

---

## 9. Status global do Resultado

### Regra dura do domínio

> **Um Circuito só é considerado válido se TODAS as verificações obrigatórias tiverem status = atende.**

Consequências:

* qualquer `nao_atende` → circuito inválido
* qualquer `atende_com_restricao` → alerta obrigatório
* o sistema nunca “compensa” falhas

---

## 10. Referência normativa

Cada verificação deve conter:

* item ou subitem da NBR 5410
* capítulo aplicável
* texto resumido do requisito

Exemplo aceitável:

> “NBR 5410 – Cap. 6.2.5.3 – Limite de queda de tensão”

Nada genérico. Nada implícito.

---

## 11. Histórico de resultados

* Resultados não são sobrescritos
* Cada execução gera um novo Resultado
* Resultados antigos são marcados como obsoletos, não apagados

Isso reforça:

* rastreabilidade
* aprendizado por comparação

---

## 12. Exibição obrigatória na UI

O Resultado deve ser exibido como:

* lista de verificações
* cada verificação com:

  * valor calculado
  * limite
  * status visual claro
* status global destacado

O aluno deve enxergar **o conflito**, não apenas o erro.

---

## 13. Erros conceituais proibidos

* Resultado com “OK” genérico
* Resultado sem verificação explícita
* Resultado que sugere solução automática
* Resultado que ignora critério aplicável

Qualquer um desses destrói o caráter didático.

---

## 14. Regra final da entidade Resultado de Dimensionamento

> **A norma não diz “qual escolher”.
> Ela diz “o que verificar”.**

O Resultado existe para tornar isso explícito.

---

**Fim do arquivo `entidade_resultado_dimensionamento.md`.**
