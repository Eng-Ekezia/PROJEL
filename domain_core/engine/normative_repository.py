import os
import yaml
from typing import Dict, Any, List

class NormativeRepository:
    """
    Serviço encarregado da ingestão determinística e read-only de arquivos YAML 
    (NBR5410.yaml e regras_normativas_5410.yaml) para uso do motor de cálculo.
    """
    _instance = None
    _docs_dir: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs")
    nbr_data: Dict[str, Any] = {}
    regras_data: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NormativeRepository, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        nbr_path = os.path.join(self._docs_dir, "NBR5410.yaml")
        regras_path = os.path.join(self._docs_dir, "regras_normativas_5410.yaml")
        
        with open(nbr_path, 'r', encoding='utf-8') as f:
            self.nbr_data = yaml.safe_load(f)
            
        with open(regras_path, 'r', encoding='utf-8') as f:
            docs = list(yaml.safe_load_all(f))
            # O primeiro doc contem a chave 'regras_normativas', ou as regras tao soltas
            if docs and 'regras_normativas' in docs[0]:
                self.regras_data = {'regras_normativas': docs[0]['regras_normativas']}
                # Captura docs subsequentes e append na lista de regras
                for doc in docs[1:]:
                   if doc and isinstance(doc, list):
                       self.regras_data['regras_normativas'].extend(doc)
                   elif doc and isinstance(doc, dict) and 'regras_normativas' not in doc:
                        # As regras estão diretamente no doc root
                        # O YAML esta formatado com '-' no comeco, o pyyaml pode ler isso
                        pass
            elif docs:
                # O YAML usa --- antes de cada item da lista (invalido pra lista continua)
                # Vamos simplificar: se for lista de dicts (por doc)
                regras = []
                for doc in docs:
                     if isinstance(doc, dict):
                          if 'regras_normativas' in doc:
                               regras.extend(doc['regras_normativas'])
                          else:
                               # Se for um doc isolado que parece regra
                               if 'id' in doc: regras.append(doc)
                     elif isinstance(doc, list):
                          regras.extend(doc)
                self.regras_data = {'regras_normativas': regras}
            else:
                self.regras_data = {'regras_normativas': []}

    def get_todas_regras(self) -> List[Dict[str, Any]]:
        """Retorna todas as regras normativas."""
        return self.regras_data.get('regras_normativas', [])
        
    def get_tabela_ampacidade(self, material: str, isolacao: str, metodo: str, numero_condutores: int) -> Dict[float, float]:
        """
        Retorna a tabela de ampacidade para as condições dadas.
        Retorno: dict onde a chave é a seção (mm2) e o valor é a corrente máxima (A).
        """
        try:
            tabela = self.nbr_data['ampacidade'][material][isolacao][metodo][str(numero_condutores)]
            return {float(k): float(v) for k, v in tabela.items() if v is not None}
        except KeyError:
            return {}
