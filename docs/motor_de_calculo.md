# 📄 `motor_de_calculo.md`

## Motor de Cálculo Normativo – Arquitetura, Fluxo e Responsabilidades

**Versão consolidada – núcleo técnico do PROJEL**

---

## 1. Propósito deste documento

Este documento formaliza o **Motor de Cálculo** do PROJEL.

Ele existe para:

* executar **verificações normativas objetivas**
* aplicar a NBR 5410 **sem inferência nem decisão automática**
* produzir Resultados de Dimensionamento rastreáveis
* garantir atendimento **simultâneo** a todos os critérios exigidos

O motor **não projeta**.
Ele **avalia**.

---

## 2. Definição fundamental

> **O Motor de Cálculo é um executor determinístico de critérios normativos, que recebe decisões de projeto e retorna o estado de conformidade frente à NBR 5410.**

O motor **não é**:

* otimizador
* sugeridor
* corretor
* sistema especialista

Ele executa regras. Nada além.

---

## 3. Posição no sistema

```
Circuito (decisão humana)
        ↓
Motor de Cálculo
        ↓
Resultado de Dimensionamento
        ↓
Verificações Normativas
```

Regras duras:

* o motor só aceita Circuitos completos
* o motor nunca altera Circuitos
* o motor nunca persiste decisões

---

## 4. Entradas obrigatórias do Motor

O motor recebe **exclusivamente**:

### 4.1 Circuito

Incluindo:

* cargas consolidadas
* parâmetros elétricos explícitos
* Zona governante
* perfis normativos aplicáveis
* esquema de aterramento
* método de instalação
* comprimento do circuito

Se algo estiver indefinido, o motor **recusa execução**.

---

## 5. Saída obrigatória do Motor

O motor sempre retorna:

* um único `ResultadoDimensionamento`
* contendo **todas** as verificações aplicáveis
* com status global calculado

Nunca retorna “parcial”.

---

## 6. Arquitetura interna do Motor

O Motor é organizado como um **orquestrador de verificações**, não como um pipeline decisório.

### Estrutura conceitual

```
MotorCalculo
 ├── identificar_verificacoes_aplicaveis()
 ├── executar_verificacao_X()
 ├── executar_verificacao_Y()
 ├── executar_verificacao_Z()
 ├── consolidar_resultado()
 └── retornar_resultado()
```

Cada verificação:

* é independente
* não conhece as demais
* não altera entradas

---

## 7. Identificação das verificações aplicáveis

Antes de calcular, o motor:

1. Analisa o Circuito
2. Identifica:

   * tipo de circuito
   * Zona governante
   * perfis normativos dos Locais
   * esquema de aterramento
3. Determina **quais critérios são obrigatórios**

Exemplo:

* Circuito em banheiro com chuveiro → inclui `atuacao_dr`
* Circuito simples de iluminação → exclui critérios não aplicáveis

Nada é inferido sem regra explícita.

---

## 8. Execução das verificações (núcleo)

Cada critério segue o mesmo contrato lógico.

### Contrato de execução de uma verificação

Entrada:

* Circuito
* dados normativos necessários

Processo:

* cálculo conforme fórmula normativa
* identificação do limite normativo
* comparação objetiva

Saída:

* uma `VerificacaoNormativa`

---

## 9. Verificações normativas obrigatórias (escopo inicial)

### 9.1 Capacidade de condução de corrente

Verifica:

* corrente de projeto
* seção do condutor
* método de instalação
* fatores de correção

Resultado:

* atende / não atende

---

### 9.2 Proteção contra sobrecorrente

Verifica:

* coordenação entre condutor e dispositivo de proteção
* critérios de proteção contra sobrecarga

Não escolhe disjuntor.
Avalia o que foi escolhido.

---

### 9.3 Proteção contra curto-circuito

Verifica:

* capacidade térmica do condutor
* tempo de atuação do dispositivo
* corrente de curto presumida (quando disponível)

Resultado explícito. Sem suposição otimista.

---

### 9.4 Queda de tensão

Verifica:

* queda percentual calculada
* limite normativo aplicável
* tipo de circuito

Este critério **não é compensável** por outros.

---

### 9.5 Atuação do DR (quando aplicável)

Verifica:

* exigência normativa
* sensibilidade
* presença ou ausência

Ausência quando exigido → `nao_atende`.

---

## 10. Consolidação do Resultado

Após executar todas as verificações:

1. O motor agrupa as verificações
2. Avalia o status global

### Regra dura

> **Status global = válido somente se TODAS as verificações obrigatórias tiverem status = atende.**

O motor:

* não escolhe “a pior”
* não escolhe “a melhor”
* não prioriza critérios

Todos valem igualmente.

---

## 11. Tratamento de conflitos

O motor:

* **expõe conflitos**
* **não resolve conflitos**

Exemplo:

* atende corrente
* não atende queda de tensão

Resultado:

* conflito explícito
* status global inválido

Cabe ao projetista decidir o que alterar.

---

## 12. Rastreamento normativo

Cada verificação deve:

* citar item da NBR 5410
* indicar capítulo
* conter comentário técnico

O motor nunca retorna resultado sem referência normativa.

---

## 13. Comportamento proibido do Motor

O motor **nunca**:

* ajusta seção automaticamente
* ajusta disjuntor automaticamente
* sugere “melhor opção”
* ignora verificação aplicável
* suaviza falha normativa

Qualquer um desses é falha grave de projeto.

---

## 14. Papel didático do Motor

Didaticamente, o motor deve:

* tornar conflitos visíveis
* forçar revisão consciente
* impedir atalhos cognitivos

Ele não ensina “como passar”.
Ele ensina **por que falhou**.

---

## 15. Regra final do Motor de Cálculo

> **A norma não decide.
> O motor não decide.
> Quem decide é o engenheiro.**

Se o PROJEL mantiver isso, ele cumpre seu papel.

---

**Fim do arquivo `motor_de_calculo.md`.**
