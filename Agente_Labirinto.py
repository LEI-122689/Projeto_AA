import random
from Interface_Agente import Agente

# Definir os parâmetros e a Q-table
ALPHA = 0.1  # Taxa de Aprendizagem
GAMMA = 0.9  # Fator de Desconto
EPSILON = 1.0  # Probabilidade inicial de exploração (100%)
EPSILON_DECAY = 0.9995  # Fator de decaimento do epsilon por passo
MIN_EPSILON = 0.01  # Mínimo de exploração

# Ações possíveis: (dx, dy)
ACOES = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Cima, Baixo, Esquerda, Direita


class AgenteLabirinto:
    def __init__(self):
        self.recompensa_acumulada = 0
        self.q_table = {}  # Tabela Q: (x, y) -> {acao: valor_q}
        self.learning_mode = True

        # Variáveis para o Q-Learning
        self.estado_anterior = None
        self.acao_anterior = None
        self.estado_atual = (0, 0)  # Assumimos que começa em (0, 0)
        self.epsilon = EPSILON

        # Parâmetros de RL
        self.alpha = ALPHA
        self.gamma = GAMMA

    # --- Métodos de Conversão e Iniciação da Q-Table ---

    def _get_q_valores(self, estado):
        """ Inicializa ou retorna o dicionário de Q-valores para um dado estado. """
        if estado not in self.q_table:
            # Inicializa todos os valores Q para 0 neste novo estado
            self.q_table[estado] = {acao: 0.0 for acao in ACOES}
        return self.q_table[estado]

    def _escolhe_melhor_acao(self, estado):
        """ Escolhe a ação com o maior valor Q (Explotação). """
        q_valores = self._get_q_valores(estado)

        # Encontrar o valor máximo
        max_q = max(q_valores.values())

        # Encontrar todas as ações que dão esse valor máximo (para desempate aleatório)
        melhores_acoes = [acao for acao, q in q_valores.items() if q == max_q]

        return random.choice(melhores_acoes)

    # --- Métodos do Interface ---

    def observacao(self, obs):
        # A observação no labirinto é o objeto (Parede, Vazio, Objetivo) na posição do agente
        # Mas para o Q-Learning, o estado é a POSIÇÃO, que é atualizada em self.avaliacaoEstadoAtual
        # Este método apenas guarda o objeto observado para referência, se necessário
        pass

    def atualiza_posicao(self, nova_pos):
        """ Chamado pelo Simulador para dar a posição atual ao Agente. """
        self.estado_atual = nova_pos

    def age(self):
        # Guardar o estado e a ação antes de agir
        self.estado_anterior = self.estado_atual

        if self.learning_mode and random.random() < self.epsilon:
            # EXPLORAÇÃO: Escolhe aleatoriamente
            acao = random.choice(ACOES)
        else:
            # EXPLOTAÇÃO: Escolhe a melhor ação da Q-table
            acao = self._escolhe_melhor_acao(self.estado_atual)

        self.acao_anterior = acao
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

        # ----------------------------------------------------
        # LÓGICA DE APRENDIZAGEM (Q-LEARNING)
        # ----------------------------------------------------
        if self.learning_mode and self.estado_anterior is not None:
            s = self.estado_anterior
            a = self.acao_anterior
            r = recompensa
            s_prime = self.estado_atual

            q_atual = self._get_q_valores(s)[a]

            # 1. Calcular o máximo Q para o novo estado (s')
            q_s_prime = self._get_q_valores(s_prime)
            max_q_prime = max(q_s_prime.values())

            # 2. Aplicar a fórmula Q-Learning
            # Q(s, a) <- (1 - alpha) * Q(s, a) + alpha * (r + gamma * max_a' Q(s', a'))
            novo_q = (1 - self.alpha) * q_atual + self.alpha * (r + self.gamma * max_q_prime)

            # 3. Atualizar a Q-table
            self.q_table[s][a] = novo_q

            # 4. Decaimento do Epsilon (Exploração)
            if self.epsilon > MIN_EPSILON:
                self.epsilon *= EPSILON_DECAY