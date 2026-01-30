## Princípio-mestre de UX (grave isso)

👉 **O usuário não escolhe códigos. Ele descreve o local.**
👉 **O sistema traduz isso para códigos normativos.**

Se você pedir para alguém selecionar “AC3” ou “BB2”, você perdeu. Mesmo sendo engenheiro.

---

## Arquitetura de UX em 3 camadas (a única que funciona)

### Camada 1 – Descrição humana do ambiente (entrada principal)

Isso é o que o usuário realmente sabe responder.

Formato ideal:

* cards ou blocos
* linguagem natural
* exemplos explícitos

Exemplos de perguntas:

* “O local está sujeito à presença de água?”

  * Nunca
  * Ocasionalmente (limpeza, respingos)
  * Frequentemente (chuveiro, lavagem)
  * Permanentemente

* “Quem utiliza o local?”

  * Pessoas leigas
  * Pessoas instruídas
  * Pessoas qualificadas (técnicos)

* “Há partes metálicas acessíveis?”

  * Não
  * Sim, poucas
  * Sim, várias

Nada de norma aqui. Só realidade.

---

### Camada 2 – Tradução automática para influências normativas (invisível)

Aqui o sistema trabalha, o usuário não.

Exemplo:

* “Presença frequente de água”
  → Categoria A
  → Código AC
  → Classe 3

Isso acontece:

* em tempo real
* sem o usuário perceber
* com rastreabilidade total

O backend recebe **apenas o resultado normativo**, não a resposta textual.

---

### Camada 3 – Transparência técnica sob demanda (opcional)

Para quem quiser ver.

Um painel tipo:

> Influências normativas identificadas para este local
> • AC3 – Presença frequente de água
> • BB3 – Baixa resistência do corpo humano
> • CE2 – Equipotencialização necessária

Isso **não é editável diretamente**, só explicável.

---

## Componentes de UI que funcionam (testados na vida real)

### 1. Wizard curto e progressivo

Nunca tudo numa tela.

Fluxo ideal:

1. Ambiente
2. Pessoas e uso
3. Construção
4. Revisão técnica

Cada etapa com 2–4 perguntas no máximo.

---

### 2. Cards com exemplos visuais (sem exagero)

Exemplo de card:

**Presença de água**

> ☐ Nunca
> ☐ Ocasional (lavagem, limpeza)
> ☐ Frequente (chuveiro, torneiras)
> ☐ Permanente

Texto pequeno abaixo:

> Ex.: banheiros, áreas externas, cozinhas

Isso evita erro sem “dar aula”.

---

### 3. Validação imediata, mas silenciosa

Nada de popup agressivo.

Exemplo:

* Usuário marca “frequente presença de água”
* Sistema:

  * marca internamente AC3
  * prepara exigência de DR
  * não interrompe o fluxo

Alertas só aparecem **na revisão**.

---

### 4. Tela de revisão técnica (momento de maturidade)

Antes de salvar:

> **Resumo técnico do ambiente**
>
> O sistema identificou condições que exigem atenção especial:
>
> * Presença frequente de água
> * Usuários leigos
> * Estrutura metálica acessível
>
> Isso implicará:
>
> * Uso obrigatório de DR
> * Restrições de método de instalação

Sem botão “ok, ok, segue”.
Botão claro: **“Confirmar contexto”**.

Isso muda o comportamento do usuário.

---

## UX específica para ensino (seu diferencial)

Inclua um modo:

* “Mostrar justificativa normativa”

Quando ativado:

* aparece o código (AC3, BB2…)
* aparece o item da norma
* aparece o porquê da exigência

Quando desativado:

* some tudo

Isso atende:

* aluno curioso
* professor exigente
* sem poluir o uso normal

---

## Erros de UX que você deve evitar a todo custo

* Checkbox com código normativo
* Dropdown gigante com “AC1, AC2, AC3…”
* Campo “outros”
* Texto longo da norma colado na tela
* Tornar obrigatório preencher tudo manualmente

Esses erros matam a adesão.
