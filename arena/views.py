from django.shortcuts import render

# Create your views here.
import random

from django.http import HttpResponseNotAllowed

from django.shortcuts import (
    redirect,
    render,
)

from .game import (
    DIFICULDADES,
    HP_MAX_JOGADOR,
    ataque_boss,
    ataque_especial,
    ataque_normal,
    curar,
    defender,
    tentar_aplicar_queimadura,
)


# ============================================
# FRASES DO BOSS
# ============================================

FRASES_BOSS = [

    "WORKS ON MY MACHINE!",

    "ERRO 500!",

    "MERGE CONFLICT!",

    "NULL REFERENCE!",

    "VOCÊ ESQUECEU O COMMIT!",

    "FUNCIONAVA ONTEM!",

]


# ============================================
# RANKING FICTÍCIO
# ============================================

RANKING_BASE = [

    {
        "nome": "Ada",
        "pontos": 1700
    },

    {
        "nome": "Grace",
        "pontos": 1400
    },

    {
        "nome": "Linus",
        "pontos": 1100
    },

]


# ============================================
# ESTADO INICIAL
# ============================================

def estado_inicial(
    nome="Squad Django",
    dificuldade="normal"
):

    if dificuldade not in DIFICULDADES:
        dificuldade = "normal"

    config = DIFICULDADES[dificuldade]

    return {

        "nome": nome,

        "dificuldade": dificuldade,

        "dificuldade_escolhida": False,

        "hp_jogador": HP_MAX_JOGADOR,

        "hp_boss": config["hp_boss"],

        "hp_boss_max": config["hp_boss"],

        "mult_dano_boss": config["mult_dano_boss"],

        "turno": 1,

        "pontos": 0,

        "dano_total": 0,

        "ultimo_especial": -99,

        "reducao_proximo_dano": 0,

        "queimadura_turnos": 0,

        "queimadura_dano": 0,

        "mensagem":
            "⚔️ Escolha a dificuldade para começar!",

        "boss_fala":
            "EU FUNCIONAVA ONTEM!",

        "critico": False,

        "efeito": "",

    }


# ============================================
# SESSÃO
# ============================================

def obter_estado(request):

    estado = request.session.get(
        "arena_estado"
    )

    # Se não existe estado salvo, ou se é um
    # estado "antigo" (de antes das missões
    # extras) e está faltando algum campo novo,
    # começa um estado novo do zero.

    if (
        not estado
        or
        "hp_boss_max" not in estado
        or
        "dificuldade_escolhida" not in estado
    ):

        nome_anterior = (
            estado.get("nome", "Squad Django")
            if estado
            else "Squad Django"
        )

        estado = estado_inicial(
            nome_anterior
        )

        request.session[
            "arena_estado"
        ] = estado

    return estado


def salvar_estado(
    request,
    estado
):

    request.session[
        "arena_estado"
    ] = estado

    request.session.modified = True


# ============================================
# RANKING
# ============================================

def montar_ranking(estado):

    ranking = [

        dict(item)

        for item in RANKING_BASE
    ]


    jogador = {

        "nome":
            estado["nome"],

        "pontos":
            estado["pontos"],

        "jogador":
            True,

    }


    ranking.append(
        jogador
    )


    ranking.sort(

        key=lambda item:
            item["pontos"],

        reverse=True
    )


    resultado = []

    posicao_jogador = None


    for posicao, item in enumerate(
        ranking,
        start=1
    ):

        item = dict(item)

        item["posicao"] = posicao


        if item.get("jogador"):

            posicao_jogador = item


        if posicao <= 4:

            resultado.append(item)


    if (
        posicao_jogador
        and
        posicao_jogador["posicao"] > 4
    ):

        resultado.append(
            posicao_jogador
        )


    return resultado


# ============================================
# TELA PRINCIPAL
# ============================================

def arena(request):

    estado = obter_estado(
        request
    )


    venceu = (
        estado["hp_boss"] <= 0
    )


    perdeu = (
        estado["hp_jogador"] <= 0
    )


    terminou = (
        venceu or perdeu
    )


    # ----------------------------------------
    # COOLDOWN DO ESPECIAL
    # ----------------------------------------

    if (
        estado["ultimo_especial"] < 0
    ):

        cooldown_restante = 0

    else:

        cooldown_restante = max(

            0,

            3 - (
                estado["turno"]
                -
                estado["ultimo_especial"]
            )
        )


    # ----------------------------------------
    # CONTEXTO DO TEMPLATE
    # ----------------------------------------

    contexto = {

        **estado,

        "hp_max_jogador":
            HP_MAX_JOGADOR,

        "hp_max_boss":
            estado["hp_boss_max"],

        "hp_jogador_pct":
            max(
                0,
                (
                    estado["hp_jogador"]
                    /
                    HP_MAX_JOGADOR
                ) * 100
            ),

        "hp_boss_pct":
            max(
                0,
                (
                    estado["hp_boss"]
                    /
                    estado["hp_boss_max"]
                ) * 100
            ),

        "venceu":
            venceu,

        "perdeu":
            perdeu,

        "terminou":
            terminou,

        "cooldown_restante":
            cooldown_restante,

        "ranking":
            montar_ranking(estado),

        "dificuldades":
            list(DIFICULDADES.keys()),

    }


    # Efeitos visuais
    # acontecem apenas uma vez.

    estado["critico"] = False

    estado["efeito"] = ""


    salvar_estado(
        request,
        estado
    )


    return render(

        request,

        "arena/arena.html",

        contexto
    )


# ============================================
# AÇÕES
# ============================================

def executar_acao(
    request,
    acao
):

    if request.method != "POST":

        return HttpResponseNotAllowed(
            ["POST"]
        )


    estado = obter_estado(
        request
    )


    # Se a dificuldade ainda não
    # foi escolhida, não há ação.

    if not estado.get(
        "dificuldade_escolhida"
    ):

        return redirect(
            "arena:arena"
        )


    # Se alguém já morreu,
    # não há nova ação.

    if (
        estado["hp_jogador"] <= 0
        or
        estado["hp_boss"] <= 0
    ):

        return redirect(
            "arena:arena"
        )


    estado["critico"] = False

    estado["efeito"] = ""


    # ========================================
    # ATAQUE NORMAL
    # ========================================

    if acao == "atacar":

        dano, critico = (
            ataque_normal()
        )


        dano = max(
            0,
            int(dano)
        )


        dano_real = min(
            dano,
            estado["hp_boss"]
        )


        estado["hp_boss"] = max(

            0,

            estado["hp_boss"]
            -
            dano
        )


        estado["dano_total"] += (
            dano_real
        )


        estado["pontos"] += (
            dano_real * 10
        )


        estado["critico"] = (
            bool(critico)
        )


        estado["efeito"] = "boss"


        if critico:

            estado["pontos"] += 100

            estado["mensagem"] = (
                f"💥 CRÍTICO! "
                f"Você causou "
                f"{dano_real} de dano!"
            )


            # ------------------------------------
            # MISSÃO EXTRA — QUEIMADURA
            # ------------------------------------

            (
                aplicou_queimadura,
                turnos_queimadura,
                dano_queimadura
            ) = tentar_aplicar_queimadura(
                critico
            )

            if aplicou_queimadura:

                estado["queimadura_turnos"] = (
                    turnos_queimadura
                )

                estado["queimadura_dano"] = (
                    dano_queimadura
                )

                estado["mensagem"] += (
                    " 🔥 O Boss pegou fogo!"
                )

        else:

            estado["mensagem"] = (
                f"⚔️ Você causou "
                f"{dano_real} de dano."
            )


    # ========================================
    # CURA
    # ========================================

    elif acao == "curar":

        hp_anterior = (
            estado["hp_jogador"]
        )


        (
            novo_hp,
            quantidade_curada
        ) = curar(
            hp_anterior
        )


        estado["hp_jogador"] = (
            int(novo_hp)
        )


        estado["mensagem"] = (
            f"💚 Você recuperou "
            f"{int(quantidade_curada)} HP."
        )


        estado["efeito"] = "cura"


    # ========================================
    # ESPECIAL
    # ========================================

    elif acao == "especial":

        (
            dano,
            acertou,
            novo_ultimo,
            mensagem
        ) = ataque_especial(

            estado["turno"],

            estado["ultimo_especial"]
        )


        estado[
            "ultimo_especial"
        ] = int(
            novo_ultimo
        )


        estado["mensagem"] = (
            mensagem
        )


        if acertou:

            dano = max(
                0,
                int(dano)
            )


            dano_real = min(
                dano,
                estado["hp_boss"]
            )


            estado["hp_boss"] = max(

                0,

                estado["hp_boss"]
                -
                dano
            )


            estado["dano_total"] += (
                dano_real
            )


            estado["pontos"] += (
                dano_real * 12
            )


            estado["efeito"] = "boss"


    # ========================================
    # DEFENDER
    # ========================================

    elif acao == "defender":

        reducao, mensagem = defender()

        estado["reducao_proximo_dano"] = (
            reducao
        )

        estado["mensagem"] = mensagem

        estado["efeito"] = "defesa"


    else:

        return redirect(
            "arena:arena"
        )


    # ========================================
    # QUEIMADURA (tick por turno)
    # ========================================

    if estado.get("queimadura_turnos", 0) > 0:

        dano_queimadura = estado[
            "queimadura_dano"
        ]

        dano_real_queimadura = min(
            dano_queimadura,
            estado["hp_boss"]
        )

        estado["hp_boss"] = max(
            0,
            estado["hp_boss"] - dano_queimadura
        )

        estado["dano_total"] += (
            dano_real_queimadura
        )

        estado["pontos"] += (
            dano_real_queimadura * 5
        )

        estado["queimadura_turnos"] -= 1

        estado["mensagem"] += (
            f" 🔥 A queimadura causou "
            f"{dano_real_queimadura} de dano."
        )


    # ========================================
    # VITÓRIA
    # ========================================

    if estado["hp_boss"] <= 0:

        # bônus pela vitória

        estado["pontos"] += 500


        # bônus pelo HP restante

        estado["pontos"] += (

            max(
                0,
                estado["hp_jogador"]
            )
            *
            5
        )


        estado["mensagem"] += (
            " 🏆 PRODUCTION BUG DERROTADO!"
        )


        salvar_estado(
            request,
            estado
        )


        return redirect(
            "arena:arena"
        )


    # ========================================
    # CONTRA-ATAQUE DO BOSS
    # ========================================

    dano_recebido = (
        ataque_boss()
    )


    # MISSÃO EXTRA — DIFICULDADE
    # aplica o multiplicador de dano do Boss

    dano_recebido = int(
        dano_recebido
        *
        estado.get("mult_dano_boss", 1.0)
    )


    # MISSÃO EXTRA — DEFENDER
    # reduz o golpe se o jogador se defendeu

    if estado.get("reducao_proximo_dano", 0) > 0:

        dano_recebido = int(
            dano_recebido
            *
            (1 - estado["reducao_proximo_dano"])
        )

        estado["reducao_proximo_dano"] = 0

        estado["mensagem"] += (
            " 🛡️ Sua defesa reduziu o golpe!"
        )


    estado["hp_jogador"] = max(

        0,

        estado["hp_jogador"]
        -
        dano_recebido
    )


    estado["boss_fala"] = (
        random.choice(
            FRASES_BOSS
        )
    )


    if (
        estado["efeito"]
        !=
        "cura"
    ):

        estado["efeito"] = (
            "jogador"
        )


    estado["mensagem"] += (

        f" 👹 O Boss "
        f"contra-atacou: "
        f"-{dano_recebido} HP."
    )


    # ========================================
    # DERROTA
    # ========================================

    if (
        estado["hp_jogador"] <= 0
    ):

        estado["mensagem"] += (
            " ☠️ Você foi derrotado."
        )


    estado["turno"] += 1


    salvar_estado(
        request,
        estado
    )


    return redirect(
        "arena:arena"
    )


# ============================================
# NOME
# ============================================

def definir_nome(request):

    if request.method != "POST":

        return HttpResponseNotAllowed(
            ["POST"]
        )


    estado = obter_estado(
        request
    )


    nome = request.POST.get(
        "nome",
        ""
    ).strip()


    if nome:

        estado["nome"] = (
            nome[:20]
        )


    salvar_estado(
        request,
        estado
    )


    return redirect(
        "arena:arena"
    )


# ============================================
# DIFICULDADE
# ============================================

def definir_dificuldade(request):

    if request.method != "POST":

        return HttpResponseNotAllowed(
            ["POST"]
        )


    estado_atual = obter_estado(
        request
    )


    dificuldade = request.POST.get(
        "dificuldade",
        "normal"
    )


    nome = estado_atual.get(
        "nome",
        "Squad Django"
    )


    novo_estado = estado_inicial(
        nome,
        dificuldade
    )

    novo_estado["dificuldade_escolhida"] = True

    novo_estado["mensagem"] = (
        "⚔️ O Production Bug apareceu!"
    )


    salvar_estado(
        request,
        novo_estado
    )


    return redirect(
        "arena:arena"
    )


# ============================================
# REINICIAR
# ============================================

def reiniciar(request):

    if request.method != "POST":

        return HttpResponseNotAllowed(
            ["POST"]
        )


    estado_atual = (
        obter_estado(request)
    )


    nome = estado_atual.get(
        "nome",
        "Squad Django"
    )


    salvar_estado(

        request,

        estado_inicial(nome)
    )


    return redirect(
        "arena:arena"
    )