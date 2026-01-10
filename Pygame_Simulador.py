import pygame
import sys
import time
import math  # Para Farol: calcular a luz

# --- Constantes de Visualização ---
TamanhoBloco = 30
Preto = (0, 0, 0)
Branco = (255, 255, 255)
Verde = (255, 255, 0)  # Farol (Luz)
Vermelho = (200, 0, 0)  # Parede / Farol (Centro)
Azul = (0, 0, 255)  # Agente
Amarelo = (255, 255, 0)  # Saída / Objetivo
Cinzento_Escuro = (60, 60, 60)  # Pedras/Recifes
Azul_Escuro = (0, 0, 100)  # Correntes Fortes
Magenta = (255, 0, 255)  # Cor do Laser do Sensor


class VisualizadorPygame:
    def __init__(self, ambiente, problema, max_passos, fps, dificuldade, nome_agente):
        pygame.init()
        self.ambiente = ambiente
        self.problema = problema
        self.max_passos = max_passos
        self.FPS_limite = fps

        if problema == 'labirinto':
            self.size_x = ambiente.size
            self.size_y = ambiente.size
        elif problema == 'farol':
            self.size_x = ambiente.size_x
            self.size_y = ambiente.size_y

        self.largura = self.size_x * TamanhoBloco
        self.altura = self.size_y * TamanhoBloco + 50

        self.ecran = pygame.display.set_mode((self.largura, self.altura))

        titulo = f"FPS: {fps} | Problema: {problema.upper()} | Dificuldade: {dificuldade.upper()} | Agente: {nome_agente.upper()}"
        pygame.display.set_caption(titulo)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        self.terminou = False
        self.sucesso = False
        self.recompensa = 0
        self.passos_atuais = 0

    def _desenha_labirinto(self):
        self.ecran.fill(Branco)

        for y in range(self.size_y):
            for x in range(self.size_x):
                rect = pygame.Rect(x * TamanhoBloco, y * TamanhoBloco, TamanhoBloco, TamanhoBloco)

                cor_bloco = Branco
                coisa = self.ambiente.get_coisa_em(x, y)

                if coisa.name == "Parede":
                    cor_bloco = Preto
                elif coisa.name == "Saida":
                    cor_bloco = Amarelo

                pygame.draw.rect(self.ecran, cor_bloco, rect)
                pygame.draw.rect(self.ecran, Preto, rect, 1)

                if self.ambiente.agente_pos == (x, y):
                    pygame.draw.circle(self.ecran, Azul, rect.center, TamanhoBloco // 3)

    def _desenha_farol(self):
        fx, fy = self.ambiente.farol_x, self.ambiente.farol_y
        ax, ay = self.ambiente.agente_pos
        mapa = self.ambiente.mapa_obstaculos

        # Lógica da Luz
        direcoes = [
            (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1)
        ]
        dir_atual = direcoes[self.ambiente.tempo_luz % 8]
        luz_coords = []
        for i in range(1, 4):
            lx = fx + (dir_atual[0] * i)
            ly = fy + (dir_atual[1] * i)
            luz_coords.append((lx, ly))

        # Desenho do ambiente
        for y in range(self.size_y):
            for x in range(self.size_x):
                rect = pygame.Rect(x * TamanhoBloco, y * TamanhoBloco, TamanhoBloco, TamanhoBloco)

                terreno = mapa[y][x]
                if terreno == 3:  # Farol
                    cor_bloco = Vermelho
                elif terreno == 2:  # Correntes
                    cor_bloco = Azul_Escuro
                elif terreno == 1:  # Pedras
                    cor_bloco = Cinzento_Escuro
                else:  # Água
                    cor_bloco = Branco

                # Sobrepor a Luz
                if (x, y) in luz_coords and terreno != 3:
                    cor_bloco = Verde

                pygame.draw.rect(self.ecran, cor_bloco, rect)
                pygame.draw.rect(self.ecran, Preto, rect, 1)

                # Desenhar Agente
                if (x, y) == (ax, ay):
                    pygame.draw.circle(self.ecran, Azul, rect.center, TamanhoBloco // 3)

        self.ambiente.tempo_luz += 1

    def _desenha_painel(self, epsilon):
        painel_rect = pygame.Rect(0, self.size_y * TamanhoBloco, self.largura, 50)
        pygame.draw.rect(self.ecran, (200, 200, 200), painel_rect)

        if self.terminou:
            status_cor = Verde if self.sucesso else Vermelho
            status_msg = " SUCESSO! " if self.sucesso else " LIMITE ATINGIDO "
        else:
            status_cor = Preto
            status_msg = ""

        status_text = f"Passo: {self.passos_atuais}/{self.max_passos} | Rec: {self.recompensa:.2f} | Eps: {epsilon:.2f} {status_msg}"

        texto_render = self.font.render(status_text, True, status_cor)
        self.ecran.blit(texto_render, (10, self.size_y * TamanhoBloco + 15))

    # --- AQUI ESTAVA O PROBLEMA: Garante que este método existe e está alinhado ---
    def desenha(self, passos, recompensa, terminou, sucesso, epsilon, sensor_alvo=None):
        """ Chamado pelo Simulador para atualizar o estado e desenhar. """

        self.passos_atuais = passos
        self.recompensa = recompensa
        self.terminou = terminou
        self.sucesso = sucesso

        # 1. Processar Eventos Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fechar()
                sys.exit()

        # 2. Desenhar o Ambiente
        if self.problema == 'labirinto':
            self._desenha_labirinto()
        elif self.problema == 'farol':
            self._desenha_farol()

        # --- VISUALIZAÇÃO DO SENSOR (LASER) ---
        if sensor_alvo is not None:
            ax, ay = self.ambiente.agente_pos
            tx, ty = sensor_alvo

            # Centro dos blocos
            start_pos = (ax * TamanhoBloco + TamanhoBloco // 2, ay * TamanhoBloco + TamanhoBloco // 2)
            end_pos = (tx * TamanhoBloco + TamanhoBloco // 2, ty * TamanhoBloco + TamanhoBloco // 2)

            # Linha Magenta
            pygame.draw.line(self.ecran, Magenta, start_pos, end_pos, 3)
            pygame.draw.circle(self.ecran, Magenta, end_pos, 5)

        # 3. Desenhar o Painel
        self._desenha_painel(epsilon)

        # 4. Atualizar o Ecrã
        pygame.display.flip()
        self.clock.tick(self.FPS_limite)

    def fechar(self):
        try:
            pygame.quit()
        except Exception:
            pass