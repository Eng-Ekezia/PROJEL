# 📄 `entidade_local.md`

## Entidade Local – Definição Normativa, Física e Operacional

**Versão consolidada (com suporte ao Capítulo 9 da NBR 5410)**

---

## 1. Propósito deste documento

Este documento formaliza a entidade **Local** dentro do PROJEL.

Ele existe para:

* representar os **ambientes físicos reais** da edificação
* servir de base para a **geração de cargas normativas**
* ativar **requisitos normativos complementares** quando aplicável
* manter rastreabilidade espacial e normativa
* impedir que cargas e circuitos existam fora de contexto físico

---

## 2. Definição fundamental

> **Local representa um ambiente físico funcional da edificação, pertencente a uma Zona normativa, podendo estar sujeito a requisitos normativos complementares conforme a NBR 5410.**

Local **não é**:

* Zona normativa
* Circuito
* Planta gráfica
* Elemento geométrico CAD

Local é **ambiente físico com qualificação normativa explícita**.

---

## 3. Posição hierárquica

```
Projeto
 └── Zona
     └── Local
         └── Carga
             └── Proposta de Circuito
                 └── Circuito
```

Regras duras:

* Local sempre pertence a exatamente uma Zona
* Local nunca governa influências externas
* Requisitos especiais não substituem Zona

---

## 4. Responsabilidades da entidade Local

O Local é responsável por:

* descrever o ambiente físico
* fornecer área e perímetro
* agrupar cargas por ambiente
* **ativar requisitos normativos complementares, quando aplicável**

O Local **não**:

* redefine influências externas
* toma decisões elétricas
* executa cálculos
* escolhe soluções de proteção

---

## 5. Atributos obrigatórios do Local

Todo Local deve conter:

* `id`
* `nome_local`
* `tipo_ambiente` (didático, não normativo)
* `area_m2`
* `perimetro_m`
* `zona_id`
* `projeto_id`
* `perfil_normativo_local`
* `descricao`
* `data_criacao`
* `autor`

---

## 6. Perfil Normativo do Local (Capítulo 9)

### Definição

`perfil_normativo_local` identifica se o Local está sujeito a **requisitos normativos complementares**, conforme o Capítulo 9 da NBR 5410.

### Natureza do atributo

* decisão **explícita do usuário**
* enum controlado
* valor padrão: `padrao`
* **não altera Zona**
* **não altera influências externas**

---

### Valores típicos (exemplos)

* `padrao`
* `banheiro_chuveiro`
* `piscina`
* `sauna`
* `local_condutivo`
* `area_externa_especial`
* `outro_especial`

A lista é extensível, mas **sempre controlada**.

---

## 7. Relação com a Zona

### Regra dura

> **O perfil normativo do Local não substitui nem altera a Zona.**

Consequências:

* Zona continua governando influências A, B e C
* Perfil normativo apenas **acrescenta restrições**
* Em caso de conflito, aplica-se a condição mais restritiva

---

## 8. Ativação de regras do Capítulo 9

No Domain Core, o `perfil_normativo_local`:

* ativa verificações adicionais
* impõe exigências obrigatórias
* gera alertas e bloqueios específicos
* referencia explicitamente o Capítulo 9 da NBR 5410

Nada é aplicado implicitamente.

---

## 9. Exibição obrigatória na UI

Sempre que um Local possuir perfil diferente de `padrao`, a UI deve:

* exibir o perfil claramente
* indicar que há requisitos adicionais
* informar o capítulo normativo aplicável

Exemplo de mensagem aceitável:

> “Este Local possui perfil normativo *banheiro com chuveiro*.
> Requisitos adicionais conforme Capítulo 9 da NBR 5410 serão aplicados.”

---

## 10. Validações obrigatórias

Antes de avançar:

* área > 0
* perímetro > 0
* Zona associada
* perfil normativo definido (mesmo que `padrao`)

---

## 11. Alterações no Local

Alterar:

* área
* perímetro
* Zona
* perfil normativo

implica:

* invalidação de cargas
* revalidação normativa
* aviso explícito ao usuário

---

## 12. Erros conceituais proibidos

* Perfil normativo inferido automaticamente
* Perfil normativo oculto do usuário
* Perfil normativo tratado como Zona
* Regra do Cap. 9 aplicada sem perfil explícito

Qualquer um desses invalida o modelo.

---

## 13. Regra final da entidade Local

> **Local descreve o espaço físico.
> O perfil normativo descreve exceções da norma.
> Zona descreve o contexto dominante.**

Misturar isso é erro conceitual.

---

**Fim do arquivo `entidade_local.md` (versão atualizada).**
