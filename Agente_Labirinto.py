import random
from Interface_Agente import Agente

# --- Parâmetros de Q-Learning ---
ALPHA = 0.1
GAMMA = 0.9
EPSILON_START = 1.0
EPSILON_DECAY = 0.9995
MIN_EPSILON = 0.01

ACOES = [(0, -1), (0, 1), (-1, 0), (1, 0)]


class AgenteLabirinto(Agente):
    def __init__(self):
        self.recompensa_acumulada = 0
        self.q_table = {}
        self.learning_mode = True
        self.estado_anterior = None
        self.acao_anterior = None
        self.estado_atual = None
        self.epsilon = EPSILON_START

        self.alpha = ALPHA
        self.gamma = GAMMA

    def _get_q_valores(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = {acao: 0.0 for acao in ACOES}
        return self.q_table[estado]

    def _escolhe_melhor_acao(self, estado):
        q_valores = self._get_q_valores(estado)
        max_q = max(q_valores.values())

        # Procura a primeira ação que atinge o valor máximo
        for acao, q in q_valores.items():
            if q == max_q:
                return acao  # Devolve a primeira ação vencedora

        # fallback (não deve acontecer)
        return random.choice(ACOES)

    def observacao(self, obs):
        pass

    def atualiza_posicao(self, nova_pos):
        self.estado_atual = nova_pos

    def age(self):
        self.estado_anterior = self.estado_atual

        if self.learning_mode and random.random() < self.epsilon:
            acao = random.choice(ACOES)
        else:
            acao = self._escolhe_melhor_acao(self.estado_atual)

        self.acao_anterior = acao
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

        if self.learning_mode and self.estado_anterior is not None and self.acao_anterior is not None:
            s = self.estado_anterior
            a = self.acao_anterior
            r = recompensa
            s_prime = self.estado_atual

            q_s = self._get_q_valores(s)
            q_s_prime = self._get_q_valores(s_prime)

            q_atual = q_s[a]
            max_q_prime = max(q_s_prime.values())

            novo_q = (1 - self.alpha) * q_atual + self.alpha * (r + self.gamma * max_q_prime)

            q_s[a] = novo_q

            if self.epsilon > MIN_EPSILON:
                self.epsilon *= EPSILON_DECAY