Certo. Seguimos **sem atalhos**.

Abaixo está o **arquivo completo**, consolidado e definitivo. Este documento é o que impede o PROJEL de virar uma colcha de retalhos quando o código crescer ou quando outra pessoa encostar no projeto.

---

# 📄 `responsabilidades.md`

## Divisão de Responsabilidades do PROJEL

**Versão consolidada – contrato interno do sistema**

---

## 1. Propósito deste documento

Este documento define **quem faz o quê** dentro do PROJEL, em nível conceitual e técnico.

Ele existe para:

* impedir sobreposição de responsabilidades
* evitar decisões implícitas
* preservar o caráter didático do sistema
* garantir aderência à NBR 5410

Se uma camada ou entidade assumir responsabilidade que não lhe cabe, o sistema está errado por definição.

---

## 2. Princípio fundamental

> **Cada decisão de projeto deve ter exatamente um responsável.**

Se ninguém é responsável, o sistema decide sozinho.
Se mais de um é responsável, o sistema vira ambíguo.

---

## 3. Usuário (Aluno / Projetista)

### Responsabilidade principal

Tomar **todas as decisões de projeto elétrico**.

### Decide explicitamente

* parâmetros do projeto
* definição de zonas
* definição de locais
* aceitação ou ajuste de cargas normativas
* inclusão de TUEs
* agrupamento de cargas
* conversão de propostas em circuitos
* parâmetros elétricos dos circuitos

### Não faz

* cálculos normativos
* validações automáticas
* interpretação implícita da norma

O usuário **pensa**.
O sistema **responde às decisões**.

---

## 4. UI / UX (Frontend)

### Responsabilidade principal

Guiar o raciocínio do usuário **sem substituir decisões**.

### Faz

* coleta dados
* apresenta contexto
* bloqueia etapas incompletas
* diferencia erro de alerta
* exibe consequências das escolhas

### Pode

* sugerir presets
* sugerir agrupamentos
* destacar conflitos
* exigir justificativas

### Não pode

* criar entidades automaticamente
* assumir valores padrão sem confirmação
* esconder zona, local ou origem de carga
* corrigir decisões erradas
* “simplificar” a norma

UX **orienta**, não **resolve**.

---

## 5. API / Camada de Orquestração

### Responsabilidade principal

Intermediar comunicação entre UI e domínio.

### Faz

* valida estrutura de dados
* valida completude
* aplica contratos
* encaminha chamadas ao domínio

### Não faz

* cálculos
* validação normativa
* interpretação da norma

A API **não sabe engenharia elétrica**.

---

## 6. Domain Core (Núcleo do Domínio)

### Responsabilidade principal

Concentrar **toda a lógica normativa e elétrica** do sistema.

### Faz

* define entidades
* valida regras normativas
* aplica restrições da NBR 5410
* executa cálculos
* gera resultados explicáveis

### Não faz

* interface
* persistência
* decisões de projeto

O domínio **julga decisões**, não as cria.

---

## 7. Entidade: Projeto

### Responsabilidade

Definir o **contexto elétrico global**.

### Contém

* tipo de empreendimento
* sistema elétrico
* tensões
* esquema de aterramento
* diretrizes gerais

### Não contém

* cargas
* circuitos
* cálculos

Projeto governa, mas não detalha.

---

## 8. Entidade: Zona

### Responsabilidade

Definir o **contexto normativo dominante**.

### Contém

* influências externas (A, B, C)
* severidade
* origem (preset / custom)

### Governa

* Locais
* Cargas
* Circuitos (indiretamente)

### Não faz

* cálculos
* decisões de agrupamento
* decisões elétricas

Zona manda. O resto obedece ou justifica exceção.

---

## 9. Entidade: Local

### Responsabilidade

Representar o **ambiente físico funcional**.

### Contém

* área
* perímetro
* uso
* vínculo com Zona

### Serve para

* gerar cargas normativas
* agrupar cargas por ambiente
* manter rastreabilidade espacial

### Não faz

* validação normativa
* decisões elétricas
* agrupamento em circuitos

Local é ponte, não juiz.

---

## 10. Entidade: Carga

### Responsabilidade

Representar uma **demanda elétrica individual**.

### Tipos

* Iluminação (normativa)
* TUG (normativa)
* TUE (explícita)

### Contém

* potência
* origem (norma / usuário)
* Local
* Zona herdada

### Não faz

* agrupamento
* cálculo
* decisão
* validação

Carga não pensa. Ela existe.

---

## 11. Wizard de Agrupamento

### Responsabilidade

Auxiliar o usuário a **pensar agrupamentos de cargas**.

### Faz

* lista Locais
* lista Cargas
* exibe Zonas
* sugere combinações possíveis
* alerta sobre conflitos

### Não faz

* criar circuitos
* validar norma
* dimensionar
* corrigir escolhas

Wizard pergunta. Nunca responde.

---

## 12. Entidade: Proposta de Circuito

### Responsabilidade

Registrar uma **intenção consciente de agrupamento**.

### Contém

* cargas agrupadas
* Locais envolvidos
* Zonas envolvidas
* observações

### Não contém

* parâmetros elétricos
* proteção
* seção
* cálculo

Proposta não é circuito.

---

## 13. Entidade: Circuito

### Responsabilidade

Formalizar uma **decisão elétrica completa**.

### Contém

* cargas agrupadas
* parâmetros elétricos
* método de instalação
* proteção

### Pode

* misturar zonas (com alerta)
* assumir zona mais severa

### Não faz

* cálculo
* validação normativa isolada

Circuito decide. O domínio valida.

---

## 14. Motor de Cálculo

### Responsabilidade

Executar **cálculos normativos**.

### Faz

* cálculo de corrente
* aplicação de fatores
* verificação de limites
* geração de resultados

### Não faz

* escolha de parâmetros
* correção de decisões
* flexibilização normativa

Motor calcula. Não opina.

---

## 15. Validação Normativa

### Responsabilidade

Verificar **aceitabilidade das decisões**.

### Atua

* antes do cálculo
* depois do cálculo
* sempre que o contexto muda

### Resultado

* erro (bloqueio)
* alerta (condicionado)
* aprovação técnica

---

## 16. Resultados e Relatórios

### Responsabilidade

Explicar tecnicamente o projeto.

### Devem conter

* valores
* limites
* margens
* condicionantes
* exceções

Resultado ensina tanto quanto erro.

---

## 17. Regra final de integridade

> **Se uma decisão aparece no sistema sem um responsável humano identificado, o PROJEL falhou.**

Este documento é o guardião dessa regra.

---

**Fim do arquivo `responsabilidades.md`.**
