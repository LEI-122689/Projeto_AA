import time
from Ambiente_Labirinto import AmbienteLabirinto
from Agente_Labirinto import AgenteLabirinto
from Ambiente_Farol import AmbienteFarol
from Agente_Farol import AgenteFarol
from Agente_Novelty import AgenteNovelty
from Sensor import Sensor

try:
    from Pygame_Simulador import VisualizadorPygame
except ImportError:
    print("Aviso: Pygame não instalado.")
    VisualizadorPygame = None


class Simulador:
    def __init__(self):
        self.ambiente = None
        self.agente = None
        self.passos = 0
        self.max_passos = 500
        self.modo = ""
        self.visualizador = None
        self.fps = 10
        self.sensor = None
        self.dificuldade_atual = "facil"

    def cria(self, tipo_problema, dificuldade="facil", algoritmo="qlearning"):
        self.modo = tipo_problema
        self.dificuldade_atual = dificuldade

        if tipo_problema == "farol":
            print(f"-> Farol ({dificuldade}) | Agente: {algoritmo}")
            self.ambiente = AmbienteFarol(mapa_tipo=dificuldade)

            # CORREÇÃO 1: Formato correto na criação
            vetor_inicial = self.ambiente.observacaoPara()
            obs_inicial = (vetor_inicial, (0, 0, 0, 0))

        elif tipo_problema == "labirinto":
            print(f"-> Labirinto ({dificuldade}) | Agente: {algoritmo}")
            self.ambiente = AmbienteLabirinto(dificuldade)
            obs_inicial = self.ambiente.agente_pos

        else:
            raise Exception("Problema desconhecido.")

        self.sensor = Sensor(self.ambiente, dificuldade)

        if algoritmo == "novelty":
            self.agente = AgenteNovelty()
            self.max_passos = 2000
            if tipo_problema == "farol":
                self.agente.observacao(self.ambiente.agente_pos)
            elif tipo_problema == "labirinto":
                self.agente.atualiza_posicao(obs_inicial)

        elif algoritmo == "qlearning":
            if tipo_problema == "farol":
                self.agente = AgenteFarol()
                self.agente.observacao(obs_inicial)
                self.max_passos = 500
            elif tipo_problema == "labirinto":
                self.agente = AgenteLabirinto()
                self.agente.atualiza_posicao(obs_inicial)
                if dificuldade == "dificil":
                    self.max_passos = 500
                else:
                    self.max_passos = 200
        else:
            raise Exception(f"Algoritmo '{algoritmo}' não reconhecido.")

        if self.visualizador:
            self.visualizador.fechar()
        self.visualizador = None

    def executa_episodio(self, renderizar=False):
        self.passos = 0
        terminou = False
        self.ambiente.reset()
        self.agente.recompensa_acumulada = 0

        # --- PREPARAÇÃO / RESET ---
        if isinstance(self.agente, AgenteNovelty):
            self.agente.observacao(self.ambiente.agente_pos)
            self.agente.historico_recente = []
            self.agente.ja_agiu = False
            self.agente.objetivo_detectado = None
        else:
            if self.modo == "labirinto":
                self.agente.atualiza_posicao(self.ambiente.agente_pos)
            elif self.modo == "farol":
                # --- CORREÇÃO 2: Formato correto no Reset ---
                # AQUI ESTAVA O ERRO. Tem de ser Tupla, não apenas vetor.
                v_ini = self.ambiente.observacaoPara()
                self.agente.observacao((v_ini, (0, 0, 0, 0)))
                # --------------------------------------------

        if renderizar and VisualizadorPygame:
            dif = getattr(self, "dificuldade_atual", "N/A")
            nome_agente = "Novelty" if isinstance(self.agente, AgenteNovelty) else "Q-Learning"
            self.visualizador = VisualizadorPygame(self.ambiente, self.modo, self.max_passos, self.fps, dif,
                                                   nome_agente)

        while not terminou and self.passos < self.max_passos:
            pos_objetivo = self.sensor.get_posicao_objetivo()

            if self.visualizador:
                sucesso = self.ambiente.jogo_terminou()
                self.visualizador.desenha(self.passos, self.agente.recompensa_acumulada, terminou, sucesso,
                                          self.agente.epsilon, sensor_alvo=pos_objetivo)

            # PERCEPÇÃO
            if isinstance(self.agente, AgenteNovelty):
                self.agente.observacao(self.ambiente.agente_pos, alvo=pos_objetivo)

            elif isinstance(self.agente, AgenteFarol):
                # Calcular Vector
                obs_vector = None
                if pos_objetivo is not None:
                    ax, ay = self.ambiente.agente_pos
                    fx, fy = pos_objetivo
                    obs_vector = (fx - ax, fy - ay)

                # Calcular Obstáculos (Código do teu simulador)
                ax, ay = self.ambiente.agente_pos
                mapa = self.ambiente.mapa_obstaculos
                max_y = len(mapa)
                max_x = len(mapa[0])
                vizinhos_bloqueados = []
                check_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                for dx, dy in check_dirs:
                    nx, ny = ax + dx, ay + dy
                    if 0 <= nx < max_x and 0 <= ny < max_y:
                        terreno = mapa[ny][nx]
                        bloqueado = 1 if terreno in [1, 2] else 0
                        vizinhos_bloqueados.append(bloqueado)
                    else:
                        vizinhos_bloqueados.append(1)

                # Enviar Tupla
                self.agente.observacao((obs_vector, tuple(vizinhos_bloqueados)))

            elif isinstance(self.agente, AgenteLabirinto):
                self.agente.observacao(None)

            acao = self.agente.age()
            recompensa = self.ambiente.agir(acao)

            if self.modo == "labirinto" and not isinstance(self.agente, AgenteNovelty):
                self.agente.atualiza_posicao(self.ambiente.agente_pos)

            self.agente.avaliacaoEstadoAtual(recompensa)
            if self.ambiente.jogo_terminou(): terminou = True
            self.passos += 1

        sucesso = self.ambiente.jogo_terminou()
        if self.visualizador:
            self.visualizador.desenha(self.passos, self.agente.recompensa_acumulada, terminou, sucesso,
                                      self.agente.epsilon, sensor_alvo=None)
            time.sleep(0.5)
            self.visualizador.fechar()
            self.visualizador = None

        return sucesso, self.passos, self.agente.recompensa_acumulada

    def executa(self, episodios_treino=1000, episodios_teste=100):
        if self.ambiente is None or self.agente is None:
            print("Erro: Tens de correr sim.cria() primeiro!")
            return

        print(f"\n>>> INÍCIO DO TREINO ({episodios_treino} episódios)")
        self.agente.learning_mode = True

        for episodio in range(1, episodios_treino + 1):
            render = (episodio == episodios_treino)  # 1ª Visualização (Fim Treino)
            sucesso, passos, recompensa = self.executa_episodio(renderizar=render)
            if episodio % 100 == 0:
                print(f"   [Treino] Ep {episodio}/{episodios_treino} | Passos: {passos} | Rec: {recompensa:.1f}")

        print("\n>>> FIM DO TREINO. A MUDAR PARA MODO DE TESTE...")
        self.agente.learning_mode = False
        self.agente.epsilon = 0.0

        print(f">>> INÍCIO DO TESTE ({episodios_teste} episódios)")
        sucessos_teste = 0
        total_passos_teste = 0

        for episodio in range(1, episodios_teste + 1):
            render = (episodio == episodios_teste)  # 2ª Visualização (Fim Teste)
            sucesso, passos, recompensa = self.executa_episodio(renderizar=render)
            if sucesso: sucessos_teste += 1
            total_passos_teste += passos

        taxa = (sucessos_teste / episodios_teste) * 100
        media_passos = total_passos_teste / episodios_teste
        print(f"\nRESULTADOS FINAIS ({self.modo.upper()}):")
        print(f"Taxa de Sucesso: {taxa:.1f}%")
        print(f"Média de Passos: {media_passos:.1f}")


if __name__ == "__main__":
    sim = Simulador()
    sim.cria("labirinto", "dificil", "novelty")
    sim.fps = 10
    sim.executa(episodios_treino=1000, episodios_teste=100)