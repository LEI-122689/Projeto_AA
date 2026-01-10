import random
from Interface_Agente import Agente


class AgenteNovelty(Agente):
    def __init__(self):
        self.visitas = {}
        self.paredes_conhecidas = set()

        self.estado_atual = None
        self.posicao_anterior = None
        self.acao_anterior = None

        # --- NOVO: Variável para guardar onde está o objetivo ---
        self.objetivo_detectado = None
        # ------------------------------------------------------

        self.acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Memória de Curto Prazo (Taboo List)
        self.historico_recente = []
        self.ja_agiu = False

        # Compatibilidade
        self.recompensa_acumulada = 0
        self.epsilon = 0.0
        self.learning_mode = False

    # --- ALTERAÇÃO 1: Receber o alvo opcional ---
    def observacao(self, obs, alvo=None):
        self.estado_atual = obs
        self.objetivo_detectado = alvo  # Guarda o alvo se o sensor o vir

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
        if len(self.historico_recente) > 4:
            self.historico_recente.pop(0)

        self.posicao_anterior = self.estado_atual

    def age(self):
        cx, cy = self.estado_atual

        # 1. Identificar todas as células vizinhas que não são paredes
        candidatos_validos = []
        for acao in self.acoes:
            dx, dy = acao
            vizinho = (cx + dx, cy + dy)
            if vizinho not in self.paredes_conhecidas:
                candidatos_validos.append((vizinho, acao))

        # Se estiver encurralado, tenta qualquer coisa
        if not candidatos_validos:
            acao = random.choice(self.acoes)
            self.acao_anterior = acao
            self.ja_agiu = True
            return acao

        # --- LÓGICA HÍBRIDA CORRIGIDA ---

        usar_novelty = True  # Por defeito, assumimos que vamos explorar

        # SE virmos o objetivo, tentamos ser Gulosos, MAS com memória!
        if self.objetivo_detectado is not None:
            tx, ty = self.objetivo_detectado

            # Procurar movimentos que:
            # 1. Nos aproximem do alvo (ou mantenham perto)
            # 2. NÃO estejam na memória recente (EVITA O LOOP DE 2 CASAS)

            melhor_acao_gulosa = None
            menor_distancia = float('inf')

            dist_atual = abs(tx - cx) + abs(ty - cy)
            encontrou_caminho_limpo = False

            for vizinho, acao in candidatos_validos:
                # Se este vizinho está na lista tabu, IGNORA-O no modo guloso
                if vizinho in self.historico_recente:
                    continue

                vx, vy = vizinho
                dist_vizinho = abs(tx - vx) + abs(ty - vy)

                # Só aceitamos se a distância for menor ou igual
                # E for a melhor opção encontrada até agora
                if dist_vizinho < menor_distancia:
                    menor_distancia = dist_vizinho
                    melhor_acao_gulosa = acao
                    encontrou_caminho_limpo = True

            # Se encontrámos um movimento válido que nos aproxima E não é repetido:
            if encontrou_caminho_limpo:
                self.acao_anterior = melhor_acao_gulosa
                self.ja_agiu = True
                return melhor_acao_gulosa

            # SE NÃO ENCONTRÁMOS (porque o caminho direto está bloqueado ou é repetido):
            # O 'usar_novelty' continua True.
            # O agente "desiste" de ir direto e volta a usar a Novidade para contornar o obstáculo.

        # ----------------------------------------------------
        # MODO NOVELTY (Exploração / Contorno)
        # ----------------------------------------------------

        candidatos_com_score = []
        random.shuffle(candidatos_validos)

        for vizinho, acao in candidatos_validos:
            score = self.visitas.get(vizinho, 0)

            # Penalidade Tabu
            if vizinho in self.historico_recente:
                score += 1000

            candidatos_com_score.append((score, acao))

        min_score = min(candidatos_com_score, key=lambda x: x[0])[0]
        melhores_opcoes = [acao for (s, acao) in candidatos_com_score if s == min_score]
        acao = random.choice(melhores_opcoes)

        self.acao_anterior = acao
        self.ja_agiu = True
        return acao

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_acumulada += recompensa

    def atualiza_posicao(self, nova_pos):
        # Nota: O Simulador deve chamar observacao() em vez disto para passar o alvo
        pass