# 📘 ARQUITETURA DO MOTOR NBR – VERSÃO CONTEXTUALIZADA (ALINHADA AO PROJEL)

---

# 1. Princípio Fundamental

O motor não dimensiona apenas um circuito.

Ele dimensiona:

> Circuito sob condições ambientais específicas,
> em uma zona específica,
> dentro de um local específico,
> pertencente a um projeto específico.

Ou seja:

A unidade real de cálculo não é o circuito isolado.
É o circuito contextualizado.

---

# 2. Modelo Conceitual Expandido

Antes:

```
Circuito → cálculo → resultado
```

Agora:

```
Projeto
   ↓
Local
   ↓
Zona (influências externas)
   ↓
Circuito
   ↓
Motor NBR contextual
   ↓
Resultado dimensionado
```

---

# 3. Nova Estrutura do Motor

```
domain_core/
 ├── engine/
 │    ├── dimensionador_projeto.py
 │    ├── contexto_instalacao.py
 │    ├── influencias_externas.py
 │    ├── regras_zona.py
 │    ├── calculo_corrente.py
 │    ├── selecao_condutor.py
 │    ├── selecao_disjuntor.py
 │    ├── calculo_queda_tensao.py
 │    ├── validacoes_normativas.py
 │    └── resultado_builder.py
```

Agora o motor tem uma camada explícita de contexto.

---

# 4. Camada de Contexto de Instalação

Arquivo: `contexto_instalacao.py`

Classe central:

```python
class ContextoInstalacao:
    projeto
    local
    zona
    circuito

    influencias_externas
    restricoes_normativas
```

Responsabilidades:

* Consolidar todas as variáveis ambientais
* Traduzir atributos de Zona em restrições técnicas

---

# 5. Influências Externas (Ponto Crítico)

Arquivo: `influencias_externas.py`

Mapeia:

* Zona úmida
* Área externa
* Área molhada
* Local com presença de público
* Ambiente industrial
* Temperatura elevada
* Ambiente agressivo
* Atmosfera explosiva (se aplicável)

Cada influência gera:

* Fator de correção térmica
* Restrição de método de instalação
* Exigência de grau IP
* Exigência de DR
* Limite máximo de queda de tensão
* Exigência de separação física

---

# 6. Como Zona Impacta o Motor

Exemplo: Zona úmida

Impactos normativos possíveis:

* Obrigatoriedade de DR ≤ 30 mA
* Restrição de método de instalação
* Correção de capacidade de condução
* Limite diferente de queda de tensão

Fluxo no motor:

```
Zona.tipo_zona == "umida"
    ↓
influencias_externas.identificar()
    ↓
aplicar_fator_correcao_temperatura()
    ↓
forçar_exigencia_DR()
    ↓
ajustar_limite_queda_tensao()
```

Agora o motor não ignora o ambiente.

Ele reage ao ambiente.

---

# 7. Fluxo Completo com Influências Externas

```
DimensionadorProjeto.execute()

    para cada circuito:

        contexto = ContextoInstalacao(...)
        
        restricoes = regras_zona.gerar_restricoes(contexto)

        corrente = calcular_corrente()

        secao = selecionar_condutor(
            corrente,
            metodo_instalacao,
            restricoes.fatores_correcao
        )

        queda = calcular_queda_tensao()

        disjuntor = selecionar_disjuntor(
            corrente,
            restricoes.exigencias_protecao
        )

        validar_norma(contexto, resultado)

        gerar ResultadoDimensionamento
```

---

# 8. Nível de Influência no Resultado

ResultadoDimensionamento deve agora incluir:

* corrente_calculada
* secao_recomendada
* queda_tensao_percentual
* disjuntor_recomendado
* exige_DR (bool)
* exige_IP_especifico
* fatores_correcao_aplicados[]
* atende_norma
* inconformidades[]
* justificativa_normativa[]

Agora o resultado não é só numérico.

Ele é pedagógico.

---

# 9. Integração com NBR5410.json

O repositório normativo deve conter:

* Tabelas de capacidade de condução
* Fatores de correção térmica
* Regras específicas por tipo de ambiente
* Limites de queda de tensão por tipo de circuito
* Requisitos de proteção adicional

API sugerida:

```python
normas.get_fator_correcao_temperatura(ambiente)
normas.get_exigencia_dr(tipo_zona)
normas.get_limite_queda_tensao(tipo_circuito, ambiente)
normas.get_grau_ip_minimo(zona)
```

---

# 10. Diferença Fundamental

Motor simplificado:

> "Qual seção atende a corrente?"

Motor PROJEL contextual:

> "Qual seção atende a corrente sob essas condições ambientais e respeita todas as exigências normativas aplicáveis a este contexto?"

Essa é a diferença entre ferramenta acadêmica séria e calculadora genérica.

---

# 11. Impacto Arquitetural

O motor passa a ter três camadas:

1. Camada contextual (zona e ambiente)
2. Camada matemática (corrente, queda)
3. Camada normativa (validação cruzada)

Todas independentes da API.
