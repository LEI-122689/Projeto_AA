import random
from Interface_Agente import Agente


class AgenteNovelty(Agente):
    def __init__(self):
        self.visitas = {}
        self.paredes_conhecidas = set()
        self.estado_atual = None
        self.posicao_anterior = None
        self.acao_anterior = None
        self.objetivo_detectado = None  # Guarda info do sensor

        self.acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.historico_recente = []  # Tabu list
        self.ja_agiu = False

        # Compatibilidade
        self.recompensa_acumulada = 0
        self.epsilon = 0.0
        self.learning_mode = False

    def observacao(self, obs, alvo=None):
        self.estado_atual = obs
        self.objetivo_detectado = alvo

        # 1. Paredes
        if self.ja_agiu and self.posicao_anterior == self.estado_atual and self.acao_anterior is not None:
            dx, dy = self.acao_anterior
            cx, cy = self.estado_atual
            self.paredes_conhecidas.add((cx + dx, cy + dy))
        self.ja_agiu = False

        # 2. Visitas
        if self.estado_atual not in self.visitas:
            self.visitas[self.estado_atual] = 0
        self.visitas[self.estado_atual] += 1

        # 3. Histórico
        self.historico_recente.append(self.estado_atual)
        if len(self.historico_recente) > 4:
            self.historico_recente.pop(0)

        self.posicao_anterior = self.estado_atual

    def age(self):
        cx, cy = self.estado_atual
        candidatos = []
        random.shuffle(self.acoes)

        for acao in self.acoes:
            dx, dy = acao
            vizinho = (cx + dx, cy + dy)

            # Filtro básico: Paredes
            if vizinho in self.paredes_conhecidas:
                continue

            # --- CÁLCULO DO SCORE (Decisão do Agente) ---
            # O agente escolhe o vizinho com MENOR score

            score = self.visitas.get(vizinho, 0)

            # A. Penalidade se esteve lá recentemente (Tabu)
            if vizinho in self.historico_recente:
                score += 1000

            # B. Incentivo se for o Objetivo (Sensor)
            # Em vez de forçar a ida, damos um score "muito baixo" (muito atrativo)
            # Assim mantemos a lógica de "Minimizar Score" consistente.
            if self.objetivo_detectado is not None:
                if vizinho == self.objetivo_detectado:
                    score -= 5000

            candidatos.append((score, acao))

        # Escolha
        if not candidatos:
            acao = random.choice(self.acoes)  # Encurralado
        else:
            # Seleciona o melhor baseada na pontuação calculada acima
            min_score = min(candidatos, key=lambda x: x[0])[0]
            melhores = [acao for (s, acao) in candidatos if s == min_score]
            acao = random.choice(melhores)

        self.acao_anterior = acao
        self.ja_agiu = True
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

    def atualiza_posicao(self, nova_pos):
        pass