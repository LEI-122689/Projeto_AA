import random
from Interface_Agente import Agente


class AgenteNovelty(Agente):
    def __init__(self):
        self.visitas = {}
        self.paredes_conhecidas = set()

        self.estado_atual = None
        self.posicao_anterior = None
        self.acao_anterior = None

        self.acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # --- NOVIDADE: Memória de Curto Prazo (Taboo List) ---
        # Guarda as últimas 4 posições para evitar loops imediatos
        self.historico_recente = []

        # Flag técnica para o bug do simulador
        self.ja_agiu = False

        # Compatibilidade
        self.recompensa_acumulada = 0
        self.epsilon = 0.0
        self.learning_mode = False

    def observacao(self, obs):
        self.estado_atual = obs

        # 1. Deteção de Paredes
        if self.ja_agiu:
            if self.posicao_anterior == self.estado_atual and self.acao_anterior is not None:
                dx, dy = self.acao_anterior
                cx, cy = self.estado_atual
                self.paredes_conhecidas.add((cx + dx, cy + dy))
            self.ja_agiu = False

        # 2. Registar Visita Global
        if self.estado_atual not in self.visitas:
            self.visitas[self.estado_atual] = 0
        self.visitas[self.estado_atual] += 1

        # 3. Atualizar Histórico Recente
        self.historico_recente.append(self.estado_atual)
        if len(self.historico_recente) > 4:  # Lembra-se dos últimos 4 passos
            self.historico_recente.pop(0)

        self.posicao_anterior = self.estado_atual

    def age(self):
        cx, cy = self.estado_atual
        candidatos = []

        # Baralhar ações para evitar tendências de movimento (vício de ir sempre Norte)
        random.shuffle(self.acoes)

        for acao in self.acoes:
            dx, dy = acao
            vizinho = (cx + dx, cy + dy)

            # Se é parede, ignora
            if vizinho in self.paredes_conhecidas:
                continue

            # --- CÁLCULO DO SCORE (Visitas + Penalidade Recente) ---
            score = self.visitas.get(vizinho, 0)

            # Se estive lá recentemente, adiciono uma penalidade temporária GIGANTE
            if vizinho in self.historico_recente:
                score += 1000

            candidatos.append((score, acao))

        # Se estiver encurralado (tudo parece mau), tenta qualquer coisa
        if not candidatos:
            acao = random.choice(self.acoes)
        else:
            # Escolhe o vizinho com MENOR score (Menos visitas E não visitado recentemente)
            min_score = min(candidatos, key=lambda x: x[0])[0]
            melhores_opcoes = [acao for (s, acao) in candidatos if s == min_score]
            acao = random.choice(melhores_opcoes)

        self.acao_anterior = acao
        self.ja_agiu = True
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

    def atualiza_posicao(self, nova_pos):
        self.observacao(nova_pos)