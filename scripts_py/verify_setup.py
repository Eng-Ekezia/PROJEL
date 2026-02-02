import sys
import os

# Adiciona o diretorio atual ao path
sys.path.append(os.getcwd())

try:
    from pydantic import ValidationError
    from domain_core.schemas.circuito import Circuito
    from domain_core.enums.circuitos import TipoCircuito
    
    print("✅ [SETUP] Importações do Python e Pydantic OK.")

    # Teste 1: Criação Válida
    c1 = Circuito(
        id="uuid-1", identificador="C1", tipo_circuito=TipoCircuito.TUG, zona_id="z1",
        tensao_nominal=127, comprimento_m=10, metodo_instalacao="B1", material_condutor="cobre",
        isolacao="PVC", temperatura_ambiente=30, circuitos_agrupados=1,
        potencia_instalada_W=1200 # Apenas potencia
    )
    print(f"✅ [DOMINIO] Circuito válido criado com sucesso: {c1.identificador}")

    # Teste 2: Regra de Engenharia (Potencia E Corrente juntos = Erro)
    try:
        c_erro = Circuito(
            id="uuid-2", identificador="C_ERR", tipo_circuito=TipoCircuito.TUG, zona_id="z1",
            tensao_nominal=127, comprimento_m=10, metodo_instalacao="B1", material_condutor="cobre",
            isolacao="PVC", temperatura_ambiente=30, circuitos_agrupados=1,
            potencia_instalada_W=1000,
            corrente_nominal_A=10 # ERRO PROPOSITAL
        )
        print("❌ [FALHA] O sistema permitiu Potência e Corrente simultâneos (violação da regra).")
    except ValidationError as e:
        print("✅ [REGRAS] Validação de Potência vs Corrente funcionando! O sistema barrou dados ambíguos.")

    print("\n🚀 TUDO PRONTO! O SETUP ESTÁ FUNCIONAL.")

except ImportError as e:
    print(f"❌ [ERRO] Falta instalar dependências. Rode: pip install -r requirements.txt\nDetalhe: {e}")
except Exception as e:
    print(f"❌ [ERRO] Falha inesperada: {e}")
