from typing import Dict, Any, List
from .normative_repository import NormativeRepository

class ZonaResolver:
    """
    O Tradutor Didático do PROJEL.
    Converte declarações simplificadas ou respostas do usuário sobre o ambiente 
    em um contexto normativo rigoroso (os códigos de influências da NBR 5410).
    """

    def __init__(self, repository: NormativeRepository = None):
        self.repo = repository or NormativeRepository()

    def resolver_de_preset(self, preset_id: str) -> Dict[str, Any]:
        """
        Recebe o identificador do preset ("RES_SECA", "RES_MOLHADA", etc.) e 
        devolve as categorias normativas mapeadas.
        Garante que presets bloqueados (industriais) ou desconhecidos sejam rejeitados.
        """
        if preset_id.startswith("IND_"):
            raise ValueError("Projetos industriais não utilizam presets fechados.")
            
        return self.repo.get_influencias_by_preset(preset_id)

    def resolver_de_wizard(self, respostas: Dict[str, str]) -> Dict[str, Any]:
        """
        Recebe as respostas do usuário baseadas nas perguntas textuais do Wizard 
        e mapeia para as siglas normativas correspondentes.
        """
        influencias_a = {}
        influencias_b = {}
        influencias_c = {}

        # 1. Presença de Água (AD)
        agua = respostas.get("presenca_agua")
        if agua == "nunca":
            influencias_a["PresencaAgua"] = "AD1"
        elif agua == "limpeza":
            influencias_a["PresencaAgua"] = "AD2"
        elif agua == "chuveiro_lavagem":
            influencias_a["PresencaAgua"] = "AD3" # Adotado como default alto para chuveiro. Pode ser AD4.
        elif agua == "imerso":
            influencias_a["PresencaAgua"] = "AD7"

        # 2. Competência e Fluxo de Pessoas (BA e BD)
        pessoas = respostas.get("competencia_pessoas")
        if pessoas == "familia":
            influencias_a["CompetenciaPessoas"] = "BA1"
        elif pessoas == "criancas":
            influencias_a["CompetenciaPessoas"] = "BA2"
        elif pessoas == "publico_alta_densidade":
            influencias_a["CompetenciaPessoas"] = "BA1"
            influencias_b["Fuga"] = "BD3"
        elif pessoas == "tecnicos":
            influencias_a["CompetenciaPessoas"] = "BA5"

        # 3. Temperatura Ambiente (AA)
        temperatura = respostas.get("temperatura")
        if temperatura == "climatizado":
            influencias_a["TemperaturaAmbiente"] = "AA4"
        elif temperatura == "muito_quente":
            influencias_a["TemperaturaAmbiente"] = "AA6"

        # 4. Estrutura e Contato (BC e CB)
        estrutura = respostas.get("estrutura_contato")
        if estrutura == "nao":
            influencias_c["ContatoTerra"] = "BC1"
            influencias_c["EstruturaContato"] = "CB1"
        elif estrutura == "poucas":
            influencias_c["ContatoTerra"] = "BC2"
        elif estrutura == "metalica_condutiva":
            influencias_c["ContatoTerra"] = "BC3"
            influencias_c["EstruturaContato"] = "CB2"
            
        # 5. Risco de Incêndio (CA e BE)
        incendio = respostas.get("risco_incendio")
        if incendio == "alvenaria":
            influencias_c["ConstrucaoMateriais"] = "CA1"
            # BE1 omitido por default a menos que estritamente exigido
        elif incendio == "madeira":
            influencias_c["ConstrucaoMateriais"] = "CA2"
            # BE2 poderia ser ativado se mapeado no SCHEMA
        elif incendio == "explosao":
            raise ValueError("Projeto industrial com atmosfera explosiva (BE3) detectado pelo wizard. Exige revisão.")

        return {
            "categoria_a": influencias_a,
            "categoria_b": influencias_b,
            "categoria_c": influencias_c
        }
