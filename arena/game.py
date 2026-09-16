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

    dano = 0


    # TODO 2
    #
    # Crie 20% de chance
    # de ataque crítico.

    critico = False


    # TODO 3
    #
    # Se for crítico:
    #
    # dano = dano * 2


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


    # TODO 2
    #
    # Calcule o novo HP.
    #
    # Lembre:
    #
    # HP máximo = 100

    novo_hp = hp_atual


    # TODO 3
    #
    # Calcule quanto realmente
    # foi recuperado.

    quantidade_curada = 0


    return novo_hp, quantidade_curada


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


    return (
        0,
        False,
        ultimo_especial,
        "🔥 Especial ainda não implementado"
    )