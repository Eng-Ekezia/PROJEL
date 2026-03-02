from typing import Dict, List, Any, Optional
from domain_core.engine.contexto_instalacao import ContextoInstalacao, RestricoesNormativas, FatorCorrecao
from domain_core.engine.normative_repository import NormativeRepository

class RegrasZonaEngine:
    """
    Responsável por converter influências externas em restrições normativas aplicáveis.
    """
    
    def __init__(self):
        self.repo = NormativeRepository()
    
    def aplicar_regras(self, contexto: ContextoInstalacao) -> RestricoesNormativas:
        """
        Avalia as influências da zona e preenche as restrições normativas.
        Consulta regras_normativas_5410.yaml
        """
        # Busca queda de tensão baseada no tipo de circuito
        # No futuro, podemos usar a zona_governante para mais contextos
        limite_queda = self.repo.get_limite_queda_tensao(
            tipo_circuito=contexto.circuito.tipo_circuito.value,
            tipo_ponto="terminal"
        )
        restricoes = RestricoesNormativas(limite_queda_tensao_pct=limite_queda)
        influencias = contexto.influencias_externas
        regras_all = self.repo.get_todas_regras()
        
        for regra in regras_all:
            # Avalia se a regra se aplica a este contexto
            if self._regra_se_aplica(regra, influencias):
                self._aplicar_consequencias(regra, restricoes)
                restricoes.observacoes.append(f"Regra {regra['id']}: {regra['descricao']} (Ref: {regra.get('referencia', {}).get('capitulo')})")
                
        return restricoes
        
    def _regra_se_aplica(self, regra: Dict[str, Any], influencias: Dict[str, str]) -> bool:
        condicoes = regra.get('condicoes', {}).get('influencias', {})
        if not condicoes:
            return False
            
        # Para que a regra se aplique, basta que uma das influências exigidas pela regra
        # esteja presente com um dos códigos restritos
        for tipo_influencia, codigos_gatilho in condicoes.items():
            # Match exato de chave no Pydantic dump das influencias (ex: temp_ambiente -> AA4)
            # Precisamos mapear as chaves do YAML para as chaves do nosso Enum Influencias.
            # No YAML: TemperaturaAmbiente: [AA5, AA6] ...
            # No nosso código (domain_core/enums/influencias.py) temos variaveis com chaves snake_case.
            # Faremos um match leniente para suportar essa migração.
            
            # Buscar valor real da influencia no contexto
            valor_no_contexto = self._encontrar_valor_influencia(tipo_influencia, influencias)
            
            if valor_no_contexto and valor_no_contexto in codigos_gatilho:
                return True
                
        return False
        
    def _encontrar_valor_influencia(self, chave_yaml: str, influencias: Dict[str, str]) -> Optional[str]:
        """Traduz ChaveCamelCase para chave_snake_case ou checa valores diretos"""
        import re
        snake_case_key = re.sub(r'(?<!^)(=[A-Z])', r'_\1', chave_yaml).lower()
        
        # Tenta a chave exata camelCase
        if chave_yaml in influencias:
            return influencias[chave_yaml]
        
        # Tenta snake_case
        if snake_case_key in influencias:
            return influencias[snake_case_key]
            
        # Fallback: As vezes o dict vem algo como {'meio_ambiente': {'temperatura_ambiente': 'AA4'}}
        # Simplificação: procurar o valor se a extrutura for chata
        for k, v in influencias.items():
            if isinstance(v, str) and isinstance(chave_yaml, str) and v.upper().startswith(chave_yaml[:2].upper()):
                return v # Ex: Procura código começando com AA se for temperatura
                
        # Se for flat e apenas os enums string (ex: 'AA4'):
        for v in influencias.values():
            if isinstance(v, str):
                return v
                
        return None

    def _aplicar_consequencias(self, regra: Dict[str, Any], restricoes: RestricoesNormativas):
        consequencias = regra.get('consequencias', {})
        
        obrigar = consequencias.get('obrigar', {})
        if 'dispositivo' in obrigar:
            disp = obrigar['dispositivo']
            if disp.get('tipo') == 'DR' and disp.get('sensibilidade_max') == '30mA':
                restricoes.exige_dr_30ma = True
            if disp.get('tipo') == 'DPS':
                restricoes.exige_dps = True
                
        aplicar = consequencias.get('aplicar', {})
        if 'fator_correcao' in aplicar:
            fc = aplicar['fator_correcao']
            if fc.get('tipo') == 'temperatura':
                # Simplificação: O valor REAL do fator exige tabela específica de cabo
                # Adicionamos um placeholder genérico que a seleção de condutor resolverá
                restricoes.fatores_correcao.append(
                    FatorCorrecao(tipo="temperatura", valor=1.0, referencia=fc.get('tabela', 'Tabela 43'))
                )
