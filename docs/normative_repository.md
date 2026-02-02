## 📄 `normative_repository.md`

### Repositório Normativo – NBR 5410 no PROJEL

---

## 1. Propósito do Repositório Normativo

Este documento define o **papel, escopo e regras de uso** do repositório normativo do PROJEL.

O repositório normativo existe para:

* concentrar **TODOS os dados normativos**
* eliminar números mágicos do código
* garantir rastreabilidade normativa
* permitir evolução da norma sem reescrita do motor

Sem esse repositório, o PROJEL perde:

* auditabilidade
* confiabilidade didática
* coerência normativa

---

## 2. Princípio fundamental

> **O código não conhece a norma.
> Ele apenas a executa.**

Toda constante normativa deve existir **exclusivamente** no repositório.

---

## 3. O que pertence ao repositório normativo

Pertencem ao repositório:

* tabelas de capacidade de condução
* fatores de correção
* limites normativos
* códigos de influências externas
* critérios condicionais (Cap. 9)
* constantes físicas normativas
* referências formais à NBR 5410

---

## 4. O que NÃO pertence ao repositório

Não pertencem ao repositório:

* fórmulas de cálculo (lógica)
* decisões de projeto
* heurísticas
* fluxos de UX
* validações condicionais

Esses pertencem ao **Motor de Cálculo**.

---

## 5. Estrutura geral do repositório

O repositório normativo é implementado como um arquivo declarativo:

```
NBR5410.json
```

Ele é:

* lido no startup
* imutável em runtime
* versionado junto ao código
* referenciado por chave, nunca por valor direto

---

## 6. Versionamento normativo

Cada versão do arquivo deve declarar:

* norma
* ano
* status
* observações

Exemplo:

* NBR 5410:2005
* NBR 5410:202X (futura)

O motor **nunca mistura versões**.

---

## 7. Integração com o domínio

| Entidade         | Uso do repositório              |
| ---------------- | ------------------------------- |
| Zona             | códigos de influências externas |
| Local            | perfis normativos (Cap. 9)      |
| Circuito         | limites e critérios             |
| Motor de cálculo | tabelas e fatores               |
| Resultado        | referência normativa            |

---

## 8. Regra dura de integridade

> **Se um valor aparece no resultado e não existe no repositório normativo, o sistema está errado.**

Não é aviso. É falha conceitual.

---

## 9. Papel didático

O repositório permite:

* mostrar de onde o número vem
* citar a tabela normativa
* comparar versões futuras
* ensinar leitura de norma

Sem isso, o aluno só “confia no software”.

---

## 10. Regra final

> **O repositório normativo é a própria norma, estruturada.
> O PROJEL apenas a percorre.**

---

**Fim do arquivo `normative_repository.md`.**