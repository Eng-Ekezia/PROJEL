---
description: Realinhamento do PROJEL a sua filosofia
---

# ⚙️ WORKFLOW DE EXECUÇÃO: PROJEL - FASE 10

**Diretrizes de Operação para o Agente**

## 📜 Regras de Engajamento (Invioláveis)

1. **Verificação Dupla Documental:** Nenhuma fase começa ou termina sem ler os arquivos `.md` e `.yaml` relevantes da pasta `./docs`.
2. **Isolamento de Branch:** Cada Fase (1 a 5) terá sua própria branch partindo da `main`. Formato: `feat/phase-X-nome-da-fase`.
3. **Commits Atômicos:** Cada *microtask* concluída gera um e apenas um commit. A mensagem deve ser clara (ex: `refactor(domain): remove defaults ocultos de Zona`).
4. **Zero Assunção / Human-in-the-Loop:** Ao final de cada fase, o agente **para** a execução, gera um script/roteiro de teste manual para o usuário e aguarda a string de aprovação (`[APPROVE]`).
5. **Merge Condicionado:** O merge para a `main` só ocorre após a aprovação do usuário.

---

## 🚀 O WORKFLOW PASSO A PASSO

### 🏗️ FASE 1: Fundação Normativa e Repositório

**Branch:** `feat/phase-1-repositorio-normativo`

* **[PRE-CHECK DOCUMENTAL]** Ler `normative_repository.md`, `regras_normativas_5410.yaml` e `NBR5410.yaml`.
* **Microtask 1.1:** Criar `normative_repository.py` com parser YAML/JSON e métodos de consulta estritos.
* *Commit:* `feat(engine): implementa parser estrito do repositorio normativo NBR5410`


* **Microtask 1.2:** Remover `RHO_COBRE`, `RHO_ALUMINIO`, default de `fator_potencia` (em `calculo_corrente.py` e `calculo_queda_tensao.py`) e `limite_queda_tensao` (em `ContextoInstalacao`).
* *Commit:* `refactor(engine): remove hardcodes matematicos e defaults indevidos`


* **Microtask 1.3:** Criar `ZonaResolver` no backend para receber intenções e consultar o repositório.
* *Commit:* `feat(engine): cria servico ZonaResolver para traducao didatica`


* **[POST-CHECK DOCUMENTAL]** Verificar se sobrou algum número mágico no código do motor.
* 🧪 **Roteiro de Teste para o Usuário:**
1. Fornecer ao usuário um script Python curto que importa o `normative_repository` e imprime a resistividade do cobre e o limite de queda para iluminação puxados diretamente do YAML.
2. Fornecer payload de teste para o `ZonaResolver`.


* 🛑 **AGUARDAR APROVAÇÃO DO USUÁRIO.** Após aprovação: Merge para `main`.

---

### 🧱 FASE 2: Contratos Pydantic e TypeScript

**Branch:** `feat/phase-2-contratos-dominio`

* **[PRE-CHECK DOCUMENTAL]** Ler `entidade_zona.md`, `entidade_local.md`, `entidade_carga.md` e `ux_backend_contratos.md`.
* **Microtask 2.1 (Projeto):** Adicionar `descricao_geral`, `criterios_gerais`, `autor` e `data_criacao` no front e back.
* *Commit:* `feat(domain): adiciona campos de auditoria e criterios em Projeto`


* **Microtask 2.2 (Zona):** Remover *defaults* cegos. Adicionar `autor`, `origem` e estruturar influências em Categorias A, B e C.
* *Commit:* `refactor(domain): remove defaults cegos e estrutura influencias de Zona`


* **Microtask 2.3 (Local):** Adicionar `perfil_normativo_local` (Enum Capítulo 9), `descricao`, `autor` e sincronizar `tipo_ambiente`.
* *Commit:* `feat(domain): implementa perfil_normativo_local para regras do Cap 9`


* **Microtask 2.4 (Carga):** Tornar IDs obrigatórios, adicionar `origem`, `ajustada`, `justificativa_ajuste`. Remover `circuito_id` do Frontend.
* *Commit:* `refactor(domain): trava rastreabilidade e justificativa de ajustes em Carga`


* **Microtask 2.5 (Circuito):** Tornar `proposta_id` obrigatório. Adicionar arrays de locais, zonas, `zona_governante` e `perfil_normativo_aplicavel`. Corrigir status.
* *Commit:* `refactor(domain): corrige heranca de zonas e perfis no Circuito`


* **[POST-CHECK DOCUMENTAL]** Analisar schemas para garantir ausência de `Optional` em relacionamentos parentais.
* 🧪 **Roteiro de Teste para o Usuário:**
1. Tentar criar uma `Zona` via API enviando um payload vazio (deve falhar e retornar 422, provando que não há defaults).
2. Tentar criar uma `Carga` sem `zona_id` (deve falhar).


* 🛑 **AGUARDAR APROVAÇÃO DO USUÁRIO.** Após aprovação: Merge para `main`.

---

### 🧠 FASE 3: Engenharia de Zonas (Presets e Wizard)

**Branch:** `feat/phase-3-wizard-zonas`

* **[PRE-CHECK DOCUMENTAL]** Ler `UX-GUIDE.md` e `ux_presets_zonas.md`.
* **Microtask 3.1:** Implementar fluxo de perguntas do Wizard no Frontend mapeando para Códigos (AD, BA, etc) via dicionário JSON. O usuário não deve ver códigos.
* *Commit:* `feat(ux): implementa perguntas textuais do wizard de zonas`


* **Microtask 3.2:** Implementar os Presets Residenciais e Comerciais documentados. Bloquear presets para a tag "Industrial".
* *Commit:* `feat(ux): adiciona presets oficiais e bloqueia uso em projetos industriais`


* **Microtask 3.3:** Integrar Frontend com a API usando o contrato estrito (`origem: PRESET` ou respostas do Wizard).
* *Commit:* `feat(api): integra front e back no fluxo de criacao de zona`


* **[POST-CHECK DOCUMENTAL]** Validar se o UX continua "escondendo a norma" na entrada e exibindo-a apenas na validação.
* 🧪 **Roteiro de Teste para o Usuário:**
1. Testar a criação via Preset `RES_MOLHADA` na UI. Verificar se a API retorna a estrutura correta.
2. Selecionar Projeto Industrial e verificar se os botões de Presets ficam desabilitados.


* 🛑 **AGUARDAR APROVAÇÃO DO USUÁRIO.** Após aprovação: Merge para `main`.

---

### 🧮 FASE 4: Motor de Cálculo

**Branch:** `feat/phase-4-motor-calculo`

* **[PRE-CHECK DOCUMENTAL]** Ler `motor_de_calculo_APRIMORADO.md`.
* **Microtask 4.1:** Remover inflação de corrente de carga ($I_b$). Transferir lógica térmica/agrupamento para o seletor de condutor calculando capacidade real ($I_z'$).
* *Commit:* `refactor(engine): corrige calculo Iz mitigando inversao didatica`


* **Microtask 4.2:** Refatorar a queda de tensão para usar fórmula completa em corrente alternada ($\cos \phi$ e $\operatorname{sen} \phi$).
* *Commit:* `feat(engine): implementa formula rigorosa de queda de tensao AC`


* **Microtask 4.3:** Conectar o `ContextoInstalacao` ao `normative_repository` para cruzar o limite de queda de tensão dinâmico.
* *Commit:* `feat(engine): injeta limites dinâmicos no ContextoInstalacao`


* **[POST-CHECK DOCUMENTAL]** Confirmar se a regra $I_b \le I_n \le I_z'$ está implementada literalmente no código de validação.
* 🧪 **Roteiro de Teste para o Usuário:**
1. Fornecer um script de simulação rodando um circuito de teste com fator de agrupamento severo. A saída do script deve provar que a corrente do disjuntor ($I_n$) foi balizada contra a tabela degradada ($I_z'$), não contra a carga.


* 🛑 **AGUARDAR APROVAÇÃO DO USUÁRIO.** Após aprovação: Merge para `main`.

---

### 🛡️ FASE 5: Integração, Bloqueios e UI

**Branch:** `feat/phase-5-bloqueios-ux`

* **[PRE-CHECK DOCUMENTAL]** Ler `entidade_circuito.md` e `entidade_carga.md`.
* **Microtask 5.1:** Atualizar API de Circuitos para rejeitar payload sem `zona_governante` e `proposta_id`.
* *Commit:* `feat(api): impoe presenca de zona_governante e proposta_id em circuitos`


* **Microtask 5.2:** Atualizar Wizard de Cargas (UI) para exigir `justificativa_ajuste` ao detectar alteração de valor normativo original.
* *Commit:* `feat(ux): exige justificativa textual para ajuste de cargas normativas`


* **Microtask 5.3:** Implementar *Tela de Revisão Técnica* antes de salvar Zonas e exibir a Zona Mais Severa explicitamente no painel de dimensionamento do Circuito.
* *Commit:* `feat(ux): adiciona tela de revisao tecnica de zonas e destaque de severidade`


* **[POST-CHECK DOCUMENTAL]** Revisar se todas as entidades estão rastreáveis e justificadas.
* 🧪 **Roteiro de Teste para o Usuário:**
1. Ir para a UI, alterar a potência de uma carga de iluminação normativa. Tentar avançar (o sistema deve bloquear pedindo texto).
2. Criar um circuito misturando cargas de Sala e Banheiro. O card deve piscar "Zona Mais Severa: Banheiro".


* 🛑 **AGUARDAR APROVAÇÃO FINAL DO USUÁRIO.** Após aprovação: Merge para `main`.