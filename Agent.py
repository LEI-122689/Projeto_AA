import random


class AgenteLabirinto:
    def __init__(self):
        self.recompensa_acumulada = 0

    def age(self):
        # As ações possíveis: Cima, Baixo, Esquerda, Direita
        # (dx, dy)
        actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Por enquanto é "burro" (aleatório)
        return random.choice(actions)

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa
        # Aqui mais tarde vais adicionar a lógica de aprendizagem
        # Ex: Se recompensa foi má, evita fazer a mesma ação