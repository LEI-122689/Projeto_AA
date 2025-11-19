import random


class AgenteFarol:
    def __init__(self):
        self.recompensa_acumulada = 0
        self.ultima_observacao = None
        self.learning_mode = True

    def observacao(self, obs):
        self.ultima_observacao = obs

    def age(self):
        # --- ALTERADO: Removidas as diagonais ---
        # Ações possíveis: Apenas Cima, Baixo, Esquerda, Direita
        acoes = [
            (0, -1),  # Norte
            (0, 1),  # Sul
            (-1, 0),  # Oeste
            (1, 0)  # Este
        ]

        # O agente escolhe uma destas 4 direções
        return random.choice(acoes)

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

        if self.learning_mode:
            # Futuramente a aprendizagem entra aqui
            pass