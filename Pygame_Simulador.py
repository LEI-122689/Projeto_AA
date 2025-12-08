import pygame
import sys
import time
import math

# --- Constantes de Visualização ---
TamanhoBloco = 30
Preto = (0, 0, 0)
Branco = (255, 255, 255)
Verde = (0, 150, 0)
Vermelho = (200, 0, 0)
Azul = (0, 0, 255)
Amarelo = (255, 255, 0)


class VisualizadorPygame:
    def __init__(self, ambiente, problema, max_passos, fps):
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
        pygame.display.set_caption(f"Simulador SMA - {problema.upper()} | FPS: {fps}")
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
        self.ecran.fill(Branco)

        fx, fy = self.ambiente.farol_x, self.ambiente.farol_y
        ax, ay = self.ambiente.agente_pos

        # Lógica para desenhar o feixe de luz
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

        for y in range(self.size_y):
            for x in range(self.size_x):
                rect = pygame.Rect(x * TamanhoBloco, y * TamanhoBloco, TamanhoBloco, TamanhoBloco)

                cor_bloco = Branco

                if (x, y) in luz_coords:
                    cor_bloco = Verde  # Luz

                if (x, y) == (fx, fy):
                    cor_bloco = Vermelho  # Centro do Farol

                pygame.draw.rect(self.ecran, cor_bloco, rect)
                pygame.draw.rect(self.ecran, Preto, rect, 1)

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

        status_text = f"Passo: {self.passos_atuais} / {self.max_passos} | Recompensa: {self.recompensa:.2f} | Epsilon: {epsilon:.4f} {status_msg}"

        texto_render = self.font.render(status_text, True, status_cor)
        self.ecran.blit(texto_render, (10, self.size_y * TamanhoBloco + 15))

    def desenha(self, passos, recompensa, terminou, sucesso, epsilon):
        self.passos_atuais = passos
        self.recompensa = recompensa
        self.terminou = terminou
        self.sucesso = sucesso

        # 1. Processar Eventos Pygame (Fecho da janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                # 2. Desenhar o Ambiente
        if self.problema == 'labirinto':
            self._desenha_labirinto()
        elif self.problema == 'farol':
            self._desenha_farol()

        # 3. Desenhar o Painel de Métricas
        self._desenha_painel(epsilon)

        # 4. Atualizar o Ecrã
        pygame.display.flip()

        # 5. Limitar a velocidade de atualização
        self.clock.tick(self.FPS_limite)

    def fechar(self):
        try:
            pygame.quit()
        except Exception:
            pass