import random


class AgenteFarol:
    def __init__(self):
        self.recompensa_acumulada = 0
        self.ultima_observacao = None

        # Variável para controlar se estamos a treinar ou a testar
        # True = Explora e preenche tabela (Learning Mode) [cite: 79]
        # False = Usa apenas o que já sabe (Test Mode) [cite: 83]
        self.learning_mode = True

    def observacao(self, obs):
        # obs é um tuplo (distancia_x, distancia_y)
        self.ultima_observacao = obs

    def age(self):
        # Ações possíveis: (dx, dy) incluindo diagonais
        acoes = [
            (0, -1), (0, 1), (-1, 0), (1, 0),  # Cima, Baixo, Esq, Dir
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonais
        ]

        # LÓGICA DE DECISÃO:
        # Por enquanto é aleatório (Random Walk).
        # Futuramente aqui entrará o "epsilon-greedy" (escolher entre explorar ou usar Q-Table)
        return random.choice(acoes)

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

        if self.learning_mode:
            # AQUI ENTRARÁ O ALGORITMO DE APRENDIZAGEM (ex: Q-Learning update)
            # TabelaQ[estado][acao] = ...
            pass