import time
import sys
# Importar as classes dos outros ficheiros
from Ambiente_Labirinto import AmbienteLabirinto
from Agente_Labirinto import AgenteLabirinto
from Ambiente_Farol import AmbienteFarol
from Agente_Farol import AgenteFarol

# Importar o visualizador Pygame
try:
    from Pygame_Simulador import VisualizadorPygame
except ImportError:
    print("Aviso: Pygame não instalado. Instale com 'pip install pygame' para ter GUI.")
    VisualizadorPygame = None


class Simulador:
    def __init__(self):
        self.ambiente = None
        self.agente = None
        self.passos = 0
        self.max_passos = 500  # Aumentado para dificuldades maiores
        self.modo = ""
        self.visualizador = None
        self.fps = 10

        # MÉTODO ATUALIZADO: Adiciona o parâmetro dificuldade

    def cria(self, tipo_problema, dificuldade="facil"):
        self.modo = tipo_problema

        if tipo_problema == "farol":
            print(f"-> A carregar Problema 1: Farol (Dificuldade: {dificuldade.upper()})")
            # CRIA O AMBIENTE COM A DIFICULDADE SELECIONADA
            self.ambiente = AmbienteFarol(mapa_tipo=dificuldade)
            self.agente = AgenteFarol()
            self.agente.observacao(self.ambiente.observacaoPara())
            self.max_passos = 500

        elif tipo_problema == "labirinto":
            print("-> A carregar Problema 3: Labirinto (Q-Learning)")
            self.ambiente = AmbienteLabirinto()
            self.agente = AgenteLabirinto()
            self.agente.atualiza_posicao(self.ambiente.agente_pos)
            self.max_passos = 200

        else:
            raise Exception("Problema desconhecido! Escolhe 'farol' ou 'labirinto'.")

        if self.visualizador:
            self.visualizador.fechar()
        self.visualizador = None

    def executa_episodio(self, renderizar=False):
        self.passos = 0
        terminou = False

        # Reset do ambiente e do agente no início do episódio
        self.ambiente.reset()
        self.agente.recompensa_acumulada = 0

        # Configuração inicial após reset
        if self.modo == "labirinto":
            self.agente.atualiza_posicao(self.ambiente.agente_pos)
        elif self.modo == "farol":
            self.agente.observacao(self.ambiente.observacaoPara())

        # Inicializar o Pygame (se for o último episódio)
        if renderizar and VisualizadorPygame:
            self.visualizador = VisualizadorPygame(self.ambiente, self.modo, self.max_passos, self.fps)

        # O Ciclo de Simulação
        while not terminou and self.passos < self.max_passos:

            # --- Desenho Pygame ---
            if self.visualizador:
                sucesso = self.ambiente.jogo_terminou()
                self.visualizador.desenha(self.passos, self.agente.recompensa_acumulada, terminou, sucesso,
                                          self.agente.epsilon)

            # 1. Percepção
            percepcao = self.ambiente.observacaoPara()
            self.agente.observacao(percepcao)

            # 2. Deliberação e Ação
            acao = self.agente.age()

            # 3. Execução e Recompensa
            recompensa = self.ambiente.agir(acao)

            # 4. Atualização de Posição (só para Labirinto)
            if self.modo == "labirinto":
                self.agente.atualiza_posicao(self.ambiente.agente_pos)

            # 5. Aprendizagem/Avaliação
            self.agente.avaliacaoEstadoAtual(recompensa)

            # 6. Verificar se terminou
            if self.ambiente.jogo_terminou():
                terminou = True

            self.passos += 1

        # --- Desenho final e fecho do Pygame ---
        sucesso = self.ambiente.jogo_terminou()
        if self.visualizador:
            self.visualizador.desenha(self.passos, self.agente.recompensa_acumulada, terminou, sucesso,
                                      self.agente.epsilon)
            time.sleep(1.0)

            try:
                self.visualizador.fechar()
            except Exception:
                pass

            self.visualizador = None

        return sucesso, self.passos, self.agente.recompensa_acumulada

    def executa(self, num_episodios=1000):
        if self.ambiente is None or self.agente is None:
            print("Erro: Tens de correr sim.cria() primeiro!")
            return

        # Ajuste do número de episódios
        if self.modo == "farol":
            num_episodios = 1500
        else:
            num_episodios = 1000

        self.agente.learning_mode = True

        print(f"--- Início da Simulação: {self.modo.upper()} ({num_episodios} Episódios de Aprendizagem) ---")

        for episodio in range(1, num_episodios + 1):
            render_agora = (episodio == num_episodios)

            sucesso, passos, recompensa_total = self.executa_episodio(renderizar=render_agora)

            if episodio % (num_episodios // 10) == 0 or episodio == num_episodios or episodio == 1:
                print(
                    f"Episódio {episodio}/{num_episodios} | Sucesso: {sucesso} | Passos: {passos} | Recompensa Total: {recompensa_total:.2f} | Epsilon: {self.agente.epsilon:.4f}")

        print("--- FIM: Simulação Concluída. ---")


# Exemplo de uso:
if __name__ == "__main__":
    sim = Simulador()
    #sim.cria("farol", dificuldade="dificil")
    sim.cria("labirinto")
    sim.fps = 10
    sim.executa()