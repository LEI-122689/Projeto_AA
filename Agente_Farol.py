import random
from Interface_Agente import Agente
from typing import Tuple, Any

# --- Parâmetros de Q-Learning ---
ALPHA = 0.1
GAMMA = 0.9
EPSILON_START = 1.0
EPSILON_DECAY = 0.9999
MIN_EPSILON = 0.01

ACOES = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, O, E

# Mapeamento do vetor (dx, dy) normalizado para o estado discreto (direção)
DIRECOES_MAP = {
    (0, -1): "N", (1, -1): "NE", (1, 0): "E", (1, 1): "SE",
    (0, 1): "S", (-1, 1): "SW", (-1, 0): "W", (-1, -1): "NW"
}


class AgenteFarol(Agente):
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

    def atualiza_posicao(self, nova_pos):
        pass  # Não usado no Farol

    def _converte_vetor_para_estado(self, vetor: Tuple[int, int]) -> str:
        """ Converte o vetor de distância (observação) num estado discreto (direção). """
        dx, dy = vetor

        # Normaliza o vetor para apenas a direção (+1, -1, 0)
        norm_x = 0
        if dx > 0:
            norm_x = 1
        elif dx < 0:
            norm_x = -1

        norm_y = 0
        if dy > 0:
            norm_y = 1
        elif dy < 0:
            norm_y = -1

        if (norm_x, norm_y) == (0, 0):
            return "FAROL"

        return DIRECOES_MAP.get((norm_x, norm_y), "UNKNOWN")

    def _get_q_valores(self, estado: str) -> dict:
        """ Devolve os Q-valores para um estado, inicializando se for novo. """
        if estado not in self.q_table:
            self.q_table[estado] = {acao: 0.0 for acao in ACOES}
        return self.q_table[estado]

    def _escolhe_melhor_acao(self, estado: str) -> Tuple[int, int]:
        """ Escolhe a ação com o maior valor Q (Explotação). """
        q_valores = self._get_q_valores(estado)
        max_q = max(q_valores.values())
        melhores_acoes = [acao for acao, q in q_valores.items() if q == max_q]
        return random.choice(melhores_acoes)  # Desempate aleatório

    def observacao(self, obs: Any):
        """ Recebe a observação (vetor de diferença) e converte-a no estado 's'. """
        self.estado_atual = self._converte_vetor_para_estado(obs)

    def age(self) -> Tuple[int, int]:
        """ Implementa a política Epsilon-Greedy. """
        self.estado_anterior = self.estado_atual

        if self.learning_mode and random.random() < self.epsilon:
            acao = random.choice(ACOES)  # Exploração
        else:
            acao = self._escolhe_melhor_acao(self.estado_atual)  # Explotação

        self.acao_anterior = acao
        return acao

    def avaliacaoEstadoAtual(self, recompensa: float):
        """ Implementa a regra de atualização Q-Learning. """
        self.recompensa_acumulada += recompensa

        if self.learning_mode and self.estado_anterior is not None and self.acao_anterior is not None:
            s = self.estado_anterior
            a = self.acao_anterior
            r = recompensa
            s_prime = self.estado_atual

            q_s = self._get_q_valores(s)

            # Se o estado seguinte é o terminal, o max_Q(s', a') é 0.
            if s_prime == "FAROL":
                max_q_prime = 0.0
            else:
                q_s_prime = self._get_q_valores(s_prime)
                max_q_prime = max(q_s_prime.values())

            q_atual = q_s[a]

            # Fórmula Q-Learning: Q(s, a) = (1 - alpha) * Q(s, a) + alpha * (r + gamma * max_Q(s', a'))
            novo_q = (1 - self.alpha) * q_atual + self.alpha * (r + self.gamma * max_q_prime)

            q_s[a] = novo_q

            # Decaimento do Epsilon
            if self.epsilon > MIN_EPSILON:
                self.epsilon *= EPSILON_DECAY