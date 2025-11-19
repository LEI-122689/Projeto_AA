import random


class AgenteLabirinto:
    def __init__(self):
        self.recompensa_acumulada = 0
        self.ultima_observacao = None
        self.learning_mode = True

    def observacao(self, obs):
        # obs aqui é um objeto (Parede, Vazio, Objetivo)
        # O agente precisa de converter isto numa "chave" útil para memória
        if hasattr(obs, "name"):
            self.ultima_observacao = obs.name  # Guarda "Parede", "Vazio", etc.
        else:
            self.ultima_observacao = "Desconhecido"

    def age(self):
        # Ações possíveis: Cima, Baixo, Esquerda, Direita
        # No labirinto tipicamente não se usam diagonais
        acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Por enquanto, escolhe aleatoriamente
        return random.choice(acoes)

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

        if self.learning_mode:
            # Lógica de atualização da tabela de aprendizagem virá aqui
            pass