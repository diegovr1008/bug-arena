"""
BUG ARENA — ARQUIVO DOS ALUNOS

MISSÕES:

1) Implementar ataque_normal()
2) Implementar curar()
3) DESAFIO: crítico de 20%
4) BOSS CHALLENGE: ataque_especial()

Evite alterar os nomes das funções
e a quantidade de valores retornados.
"""


import random


HP_MAX_JOGADOR = 100

HP_MAX_BOSS = 120


# ============================================
# MISSÃO EXTRA ★★ — ESCOLHA DE DIFICULDADE
# ============================================
#
# Cada dificuldade altera o HP do Boss e
# um multiplicador aplicado no dano que
# o Boss causa no contra-ataque.

DIFICULDADES = {

    "facil": {
        "hp_boss": 90,
        "mult_dano_boss": 0.7,
    },

    "normal": {
        "hp_boss": 120,
        "mult_dano_boss": 1.0,
    },

    "dificil": {
        "hp_boss": 150,
        "mult_dano_boss": 1.3,
    },

}


# ============================================
# MISSÃO 1 + DESAFIO
# ============================================

def ataque_normal():

    """
    Retorna:

        dano
        critico


    MISSÃO 1:

    - dano aleatório entre 8 e 18


    DESAFIO:

    - 20% de chance de crítico
    - se for crítico, dano x2
    """

    # TODO 1
    #
    # Gere um dano aleatório
    # entre 8 e 18.

    dano = random.randint(8, 18)


    # TODO 2
    #
    # Crie 20% de chance
    # de ataque crítico.

    critico = random.random() < 0.2


    # TODO 3
    #
    # Se for crítico:
    #
    # dano = dano * 2

    if critico:
        dano = dano * 2


    return dano, critico


# ============================================
# MISSÃO 2
# ============================================

def curar(hp_atual):

    """
    Retorna:

        novo_hp
        quantidade_curada


    REGRAS:

    - sorteie uma cura entre 10 e 20
    - HP nunca pode ultrapassar 100
    - quantidade_curada deve representar
      quanto foi recuperado de verdade


    EXEMPLO:

    hp_atual = 95

    cura sorteada = 20

    novo_hp = 100

    quantidade_curada = 5
    """

    # TODO 1
    #
    # Sorteie uma cura
    # entre 10 e 20.

    cura_sorteada = random.randint(10, 20)


    # TODO 2
    #
    # Calcule o novo HP.
    #
    # Lembre:
    #
    # HP máximo = 100

    novo_hp = min(100, hp_atual + cura_sorteada)


    # TODO 3
    #
    # Calcule quanto realmente
    # foi recuperado.

    quantidade_curada = novo_hp - hp_atual


    return novo_hp, quantidade_curada


# ============================================
# MISSÃO EXTRA ★ — DEFENDER
# ============================================
#
# O jogador abre mão do ataque nesta rodada
# para reduzir o próximo contra-ataque do
# Boss em 50%.

def defender():

    """
    Retorna:

        reducao    (fração, 0.5 = -50%)
        mensagem
    """

    reducao = 0.5

    mensagem = (
        "🛡️ Você se preparou para o golpe! "
        "O próximo contra-ataque do Boss "
        "será reduzido em 50%."
    )

    return reducao, mensagem


# ============================================
# MISSÃO EXTRA ★★★ — QUEIMADURA
# ============================================
#
# Todo ataque CRÍTICO tem 50% de chance de
# incendiar o Boss: 4 de dano extra por
# turno, durante 3 turnos.

def tentar_aplicar_queimadura(critico):

    """
    Retorna:

        aplicou
        turnos
        dano_por_turno
    """

    if not critico:
        return False, 0, 0

    aplicou = random.random() < 0.5

    if not aplicou:
        return False, 0, 0

    return True, 3, 4


# ============================================
# BOSS
# ============================================

def ataque_boss():

    """
    Esta parte já está pronta.

    O Boss causa entre
    6 e 16 de dano.
    """

    return random.randint(6, 16)


# ============================================
# BOSS CHALLENGE
# ============================================

def ataque_especial(
    turno,
    ultimo_especial
):

    """
    Retorna:

        dano
        acertou
        novo_ultimo_especial
        mensagem


    REGRAS:

    - só pode ser usado novamente
      depois de 3 turnos

    - 30% de chance de falhar

    - se acertar:
      dano entre 20 e 35

    - mesmo se falhar,
      entra em cooldown
    """

    # TODO BOSS CHALLENGE

    # Ainda em cooldown?
    # (ultimo_especial < 0 significa "nunca usado ainda")

    if (
        ultimo_especial >= 0
        and (turno - ultimo_especial) < 3
    ):

        turnos_restantes = 3 - (turno - ultimo_especial)

        return (
            0,
            False,
            ultimo_especial,
            f"⏳ Especial em cooldown! "
            f"Faltam {turnos_restantes} turno(s)."
        )


    # 30% de chance de falhar
    # => 70% de chance de acertar

    acertou = random.random() >= 0.3


    if acertou:

        dano = random.randint(20, 35)

        mensagem = (
            f"🔥 ESPECIAL! "
            f"Você causou {dano} de dano!"
        )

    else:

        dano = 0

        mensagem = "🔥 O ataque especial falhou!"


    # Independente de acertar ou errar,
    # o especial entra em cooldown a partir
    # deste turno.

    novo_ultimo_especial = turno


    return (
        dano,
        acertou,
        novo_ultimo_especial,
        mensagem
    )