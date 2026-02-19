from domain_core.schemas.proposta import AnalisePropostaRequest, AnalisePropostaResponse
from domain_core.enums.cargas import TipoCarga

class AnalisadorProposta:
    """
    Serviço de Domínio responsável por validar as intenções de agrupamento de cargas (Propostas).
    Ele aplica regras da NBR 5410 para gerar alertas antes da criação do Circuito definitivo.
    """

    @classmethod
    def analisar_agrupamento(cls, request: AnalisePropostaRequest) -> AnalisePropostaResponse:
        cargas = request.cargas_selecionadas
        zonas = request.zonas_do_projeto

        if not cargas:
            return AnalisePropostaResponse(
                potencia_total_va=0.0, potencia_total_w=0.0,
                locais_envolvidos_ids=[], zonas_envolvidas_ids=[],
                alertas_normativos=["Uma Proposta de Circuito deve conter pelo menos uma Carga."],
                is_valida=False
            )

        pot_va = 0.0
        pot_w = 0.0
        locais_set = set()
        zonas_set = set()

        tem_iluminacao = False
        tem_tug = False
        tem_tue = False

        # 1. Derivação Estrutural (Locais e Zonas) e Somatório Base
        for carga in cargas:
            pot_va += carga.potencia_va
            pot_w += carga.potencia_w
            
            if carga.local_id:
                locais_set.add(carga.local_id)
            if carga.zona_id:
                zonas_set.add(carga.zona_id)

            tipo = carga.tipo
            if tipo == TipoCarga.ILUMINACAO: tem_iluminacao = True
            elif tipo == TipoCarga.TUG: tem_tug = True
            elif tipo in [TipoCarga.TUE, TipoCarga.MOTOR]: tem_tue = True

        alertas = []

        # 2. Regra Normativa: Mistura de Zonas
        if len(zonas_set) > 1:
            nomes_zonas = []
            for z_id in zonas_set:
                zona_encontrada = next((z for z in zonas if z.id == z_id), None)
                nomes_zonas.append(zona_encontrada.nome if zona_encontrada else "Desconhecida")
            
            alertas.append(
                f"Mistura de Zonas: As cargas pertencem a zonas distintas ({', '.join(nomes_zonas)}). "
                "O circuito final herdará as exigências da zona mais rigorosa."
            )

        # 3. Regra Normativa: Separação Iluminação vs Tomadas (NBR 5410 9.5.3)
        if tem_iluminacao and tem_tug:
            alertas.append(
                "Atenção (NBR 5410): Recomenda-se circuitos independentes para iluminação e tomadas "
                "(exceções aplicam-se a locais específicos)."
            )

        # 4. Regra Normativa: Exclusividade de TUE (NBR 5410 9.5.3.2)
        if tem_tue and len(cargas) > 1:
            alertas.append(
                "Atenção (NBR 5410): Equipamentos de Uso Específico (TUE) com corrente nominal superior a 10A "
                "devem, por norma, ter circuitos exclusivos e independentes."
            )

        return AnalisePropostaResponse(
            potencia_total_va=round(pot_va, 2),
            potencia_total_w=round(pot_w, 2),
            locais_envolvidos_ids=list(locais_set),
            zonas_envolvidas_ids=list(zonas_set),
            alertas_normativos=alertas,
            is_valida=True
        )