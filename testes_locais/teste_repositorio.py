import sys
import os

# Garantir que o diretório raiz está no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain_core.engine.normative_repository import NormativeRepository
from domain_core.engine.zona_resolver import ZonaResolver

def run_tests():
    print("=== TESTE DA FASE 1: FUNDAÇÃO NORMATIVA ===")
    
    # 1. Testando o Repositório Normativo
    print("\n--- 1. Inicializando NormativeRepository ---")
    repo = NormativeRepository()
    
    rho_cobre = repo.get_resistividade("cobre")
    print(f"Resistividade Cobre (via repo): {rho_cobre}")
    assert rho_cobre == 0.0225, "Erro: Resistividade do cobre incorreta."
    
    rho_aluminio = repo.get_resistividade("aluminio")
    print(f"Resistividade Alumínio (via repo): {rho_aluminio}")
    assert rho_aluminio == 0.036, "Erro: Resistividade do alumínio incorreta."
    
    limite_tensao_ilum = repo.get_limite_queda_tensao("iluminacao", "terminal")
    print(f"Limite Queda de Tensão (Iluminação/Terminal): {limite_tensao_ilum}%")
    
    # 2. Testando o ZonaResolver
    print("\n--- 2. Inicializando ZonaResolver ---")
    resolver = ZonaResolver(repo)
    
    print("-> Teste A: Preset 'RES_MOLHADA'")
    zona_preset = resolver.resolver_de_preset("RES_MOLHADA")
    print(f"Resultado Preset: {zona_preset}")
    assert zona_preset["categoria_a"]["PresencaAgua"] == "AD3", "Erro no mapeamento do preset RES_MOLHADA."

    print("\n-> Teste B: Respostas do Wizard")
    respostas = {
        "presenca_agua": "chuveiro_lavagem",
        "competencia_pessoas": "publico_alta_densidade",
        "temperatura": "climatizado",
        "estrutura_contato": "metalica_condutiva",
        "risco_incendio": "alvenaria"
    }
    zona_wizard = resolver.resolver_de_wizard(respostas)
    print(f"Resultado Wizard:\n {zona_wizard}")
    
    assert zona_wizard["categoria_a"]["PresencaAgua"] == "AD3"
    assert zona_wizard["categoria_b"]["Fuga"] == "BD3"
    assert zona_wizard["categoria_c"]["ContatoTerra"] == "BC3"
    
    print("\n--- SUCESSO! A base normativa esta operante e os hardcodes blindados. ---")

if __name__ == "__main__":
    run_tests()
