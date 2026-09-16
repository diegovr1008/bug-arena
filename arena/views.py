from django.shortcuts import render

# Create your views here.
import random

from django.http import HttpResponseNotAllowed

from django.shortcuts import (
    redirect,
    render,
)

from .game import (
    HP_MAX_BOSS,
    HP_MAX_JOGADOR,
    ataque_boss,
    ataque_especial,
    ataque_normal,
    curar,
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
    nome="Squad Django"
):

    return {

        "nome": nome,

        "hp_jogador": HP_MAX_JOGADOR,

        "hp_boss": HP_MAX_BOSS,

        "turno": 1,

        "pontos": 0,

        "dano_total": 0,

        "ultimo_especial": -99,

        "mensagem":
            "⚔️ O Production Bug apareceu!",

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

    if not estado:

        estado = estado_inicial()

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
            HP_MAX_BOSS,

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
                    HP_MAX_BOSS
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


    else:

        return redirect(
            "arena:arena"
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