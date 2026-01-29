# Contratos UX ↔ Backend  
## PROJEL – Entradas, Saídas e Responsabilidades

Este documento define os **contratos formais de comunicação**
entre a interface do usuário (UX / Frontend) e o Backend do PROJEL.

Seu objetivo é:
- evitar lógica duplicada
- preservar o domínio
- garantir previsibilidade
- permitir evolução independente das camadas

UX nunca “decide engenharia”.
Backend nunca “inventa contexto”.

---

## 1. Princípio fundamental dos contratos

> **Toda decisão relevante é um dado explícito.**

Não existem:
- defaults ocultos
- decisões implícitas
- inferências silenciosas

Se algo impacta a norma, **isso aparece no contrato**.

---

## 2. Tipos de contratos existentes

O PROJEL trabalha com três grandes categorias de contrato:

1. Contratos de **entrada humana estruturada**
2. Contratos de **validação e resposta normativa**
3. Contratos de **resultado técnico**

---

## 3. Contrato: Criação de Projeto

### UX → Backend

```json
{
  "nome": "Projeto Residencial Exemplo",
  "tipo_projeto": "RESIDENCIAL",
  "sistema_eletrico": "TRIFASICO",
  "tensao_nominal": 220,
  "esquema_aterramento": "TN_S",
  "descricao_aterramento": "Aterramento conforme padrão local"
}
````

### Backend → UX

```json
{
  "projeto_id": "uuid",
  "status": "CRIADO"
}
```

### Observações

* Backend apenas valida formato e enums
* Nenhuma decisão normativa ocorre aqui

---

## 4. Contrato: Criação de Zona por Preset

### UX → Backend

```json
{
  "nome": "Área Molhada",
  "origem": "PRESET",
  "preset_id": "RES_MOLHADA",
  "tipo_projeto": "RESIDENCIAL"
}
```

### Backend → UX

```json
{
  "zona_id": "uuid",
  "origem": "PRESET",
  "influencias_externas": [
    {
      "categoria": "A",
      "codigo": "AC",
      "classe": 3
    },
    {
      "categoria": "B",
      "codigo": "BA",
      "classe": 2
    },
    {
      "categoria": "C",
      "codigo": "CB",
      "classe": 2
    }
  ],
  "impactos_normativos": [
    "Exigência provável de DR",
    "Atenção à proteção contra choque"
  ]
}
```

### Regra

* UX não envia influências prontas
* Backend resolve o preset → influências

---

## 5. Contrato: Criação de Zona via Wizard

### UX → Backend

```json
{
  "nome": "Área Industrial Úmida",
  "origem": "CUSTOM",
  "respostas_wizard": {
    "presenca_agua": true,
    "poeira_condutiva": false,
    "usuarios": "TREINADOS",
    "estrutura_metalica": true,
    "acesso_publico": false
  }
}
```

### Backend → UX

```json
{
  "zona_id": "uuid",
  "origem": "CUSTOM",
  "influencias_externas": [
    {
      "categoria": "A",
      "codigo": "AD",
      "classe": 3
    },
    {
      "categoria": "B",
      "codigo": "BB",
      "classe": 1
    },
    {
      "categoria": "C",
      "codigo": "CC",
      "classe": 2
    }
  ],
  "justificativa_normativa": "Influências definidas a partir das condições ambientais informadas"
}
```

---

## 6. Contrato: Criação de Circuito

### UX → Backend

```json
{
  "identificador": "C1",
  "tipo_circuito": "ILUMINACAO",
  "zona_id": "uuid",
  "comprimento_m": 35,
  "metodo_instalacao": "B1",
  "material_condutor": "COBRE",
  "isolacao": "PVC",
  "temperatura_ambiente": 30,
  "agrupamento": 2,
  "potencia_va": 1200,
  "criticidade": "NORMAL",
  "sobrescreve_influencias": false
}
```

### Regra

* Se `sobrescreve_influencias = true`, UX **deve** enviar respostas adicionais
* Backend valida coerência e herança

---

## 7. Contrato: Validação Pré-Dimensionamento

### UX → Backend

```json
{
  "projeto_id": "uuid"
}
```

### Backend → UX

```json
{
  "status": "BLOQUEADO",
  "pendencias": [
    "Zona 'Garagem' não possui influência da categoria B",
    "Circuito C3 sem método de instalação"
  ]
}
```

Ou:

```json
{
  "status": "PRONTO"
}
```

---

## 8. Contrato: Dimensionamento

### UX → Backend

```json
{
  "projeto_id": "uuid"
}
```

### Backend → UX

```json
{
  "resultados": [
    {
      "circuito": "C1",
      "corrente_projeto": 5.45,
      "secao_condutor_mm2": 2.5,
      "disjuntor_a": 10,
      "queda_tensao_percentual": 2.1,
      "status": "OK",
      "alertas": []
    },
    {
      "circuito": "C2",
      "status": "ALERTA",
      "alertas": [
        "Queda de tensão próxima ao limite normativo"
      ]
    }
  ]
}
```

---

## 9. Contrato: Detalhamento Didático (opcional)

### UX → Backend

```json
{
  "circuito_id": "uuid",
  "modo": "DIDATICO"
}
```

### Backend → UX

```json
{
  "formulas": [
    "Ib = P / (V * cosφ)"
  ],
  "fatores_correcao": {
    "temperatura": 0.94,
    "agrupamento": 0.8
  },
  "referencias_normativas": [
    "NBR 5410 – Seção 6"
  ],
  "explicacao": "A seção foi escolhida considerando fatores de correção aplicáveis"
}
```

---

## 10. Contratos de erro e bloqueio

### Formato padrão de erro

```json
{
  "erro": "DECISAO_INVALIDA",
  "mensagem": "Método de instalação incompatível com influências externas",
  "referencia_normativa": "NBR 5410 – 6.2.3"
}
```

UX **não interpreta erro**.
UX apenas exibe e orienta correção.

---

## 11. Considerações finais

Esses contratos garantem que:

* UX guia, mas não decide
* Backend orquestra, mas não calcula fora do domínio
* Domínio permanece íntegro
* Decisões são rastreáveis

Qualquer mudança de UX ou Backend
deve respeitar estes contratos,
ou o sistema perde coerência técnica e didática.
