# Bug Arena **

Jogo de batalha por turnos feito em Django, criado para a disciplina de
Desenvolvimento de Sistemas (SENAI TDS). O jogador enfrenta o **Production
Bug**, um chefe que representa os clássicos problemas de quem programa.

---

## Como rodar o projeto

```bash
# ativar a venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# instalar dependências (se necessário)
pip install -r requirements.txt

# rodar o servidor
python manage.py runserver
```

Depois é só acessar `http://127.0.0.1:8000/` no navegador.

---

## O que foi feito

### Bugs corrigidos (arquivo `arena/game.py`)

O professor entregou o jogo com três funções incompletas. Foram implementadas:

- **`ataque_normal()`** — dano aleatório entre 8 e 18, com 20% de chance de
  crítico (dano dobrado).
- **`curar()`** — recupera entre 10 e 20 de HP, sem ultrapassar o máximo de
  100.
- **`ataque_especial()`** — dano entre 20 e 35, com 30% de chance de falhar
  e cooldown de 3 turnos entre usos.

### Missões extras implementadas

| Dificuldade | Missão | O que faz |
|---|---|---|
| ★ Fácil | **Defender** | Novo botão de ação: o jogador abre mão do ataque na rodada para reduzir o próximo contra-ataque do Boss em 50%. |
| ★★ Média | **Escolha de dificuldade** | Antes da luta, o jogador escolhe Fácil, Normal ou Difícil. Isso altera o HP do Boss (90 / 120 / 150) e o multiplicador de dano do seu contra-ataque (0.7x / 1.0x / 1.3x). |
| ★★★ Difícil | **Queimadura** | Todo ataque crítico tem 50% de chance de incendiar o Boss, causando 4 de dano extra automaticamente por 3 turnos seguidos, mesmo que o jogador escolha curar ou defender nesses turnos. |

---

## Estrutura do projeto

```
arena/
├── game.py          # regras do jogo (ataques, cura, dificuldade, queimadura, defender)
├── views.py          # fluxo da partida (sessão, turnos, pontuação)
├── urls.py            # rotas do app
├── templates/arena/arena.html   # interface
└── static/arena/arena.css        # estilo

config/
└── urls.py            # inclui as rotas do app arena
```
