import time
import sys
# Importar as classes dos outros ficheiros
from Ambiente_Labirinto import AmbienteLabirinto
from Agente_Labirinto import AgenteLabirinto
from Ambiente_Farol import AmbienteFarol
from Agente_Farol import AgenteFarol
from Agente_Novelty import AgenteNovelty

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
        self.max_passos = 200
        self.visualizador = None
        self.fps = 10  # FPS padrão para visualização
        self.modo = ""
        self.populacao = []

    def cria(self, tipo_problema):
        self.modo = tipo_problema

        if tipo_problema == "farol":
            print("-> Carregando Farol (Q-Learning)")
            self.ambiente = AmbienteFarol()
            self.agente = AgenteFarol()
            self.agente.observacao(self.ambiente.observacaoPara())

        elif tipo_problema == "labirinto":
            print("-> A carregar Problema 3: Labirinto (Q-Learning)")
            print("-> Carregando Labirinto (Q-Learning)")
            self.ambiente = AmbienteLabirinto()
            self.agente = AgenteLabirinto()
            self.agente.atualiza_posicao(self.ambiente.agente_pos)


        elif tipo_problema == "novelty":
            print("-> Carregando Labirinto (Evolutivo - Novelty Search)")
            self.ambiente = AmbienteLabirinto()
            self.populacao = [AgenteNovelty() for _ in range(50)]
            self.agente = self.populacao[0]
        else:
            raise Exception("Modo desconhecido. Escolhe: 'farol', 'labirinto' ou 'novelty'")

        if self.visualizador:
            self.visualizador.fechar()
        self.visualizador = None

    def executa_episodio(self, renderizar=False):
        self.passos = 0
        terminou = False

        # Resetar ambiente e agente
        if self.modo == "labirinto":
            self.ambiente = AmbienteLabirinto()
            self.agente.recompensa_acumulada = 0
            self.agente.atualiza_posicao(self.ambiente.agente_pos)
        # Reset adequado a cada tipo
        if "labirinto" in self.modo or "novelty" in self.modo:
            self.ambiente = AmbienteLabirinto()
            self.agente.recompensa_acumulada = 0
            if hasattr(self.agente, "atualiza_posicao"):
                self.agente.atualiza_posicao(self.ambiente.agente_pos)
            if hasattr(self.agente, "observacao"):
                self.agente.observacao(self.ambiente.observacaoPara())

        elif self.modo == "farol":
            self.ambiente.reset()
            self.agente.recompensa_acumulada = 0
            self.agente.observacao(self.ambiente.observacaoPara())

        # Inicializar o Pygame
        if renderizar and VisualizadorPygame:
            self.visualizador = VisualizadorPygame(self.ambiente, self.modo, self.max_passos, self.fps)

        # O Ciclo de Simulação
        # Loop Principal
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
            # Ciclo Perceção-Ação
            percepcao = self.ambiente.observacaoPara()
            self.agente.observacao(percepcao)

            acao = self.agente.age()
            recompensa = self.ambiente.agir(acao)

            # Atualizações
            if hasattr(self.agente, "atualiza_posicao"):
                self.agente.atualiza_posicao(self.ambiente.agente_pos)

            self.agente.avaliacaoEstadoAtual(recompensa)

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
                if renderizar:
                    print("SUCESSO!")
                    self.ambiente.render()

            self.passos += 1
            if renderizar: time.sleep(0.1)

        return sucesso, self.passos, self.agente.recompensa_acumulada

    def executa(self, num_episodios=1000):
        if self.ambiente is None or self.agente is None:
            print("Erro: Tens de correr sim.cria() primeiro!")
            return
    # --- LÓGICA DE NOVIDADE ---
    def calcular_novidade(self, arquivo_posicoes):
        k = 5
        for agente in self.populacao:
            meu_x, meu_y = agente.posicao_final
            distancias = []
            todos_comparaveis = self.populacao + arquivo_posicoes

            for outro in todos_comparaveis:
                if outro == agente: continue
                if isinstance(outro, tuple):
                    ox, oy = outro
                else:
                    ox, oy = outro.posicao_final
                d = np.sqrt((meu_x - ox) ** 2 + (meu_y - oy) ** 2)
                distancias.append(d)

            distancias.sort()
            vizinhos_proximos = distancias[:k]

            if len(vizinhos_proximos) > 0:
                agente.score_novidade = sum(vizinhos_proximos) / len(vizinhos_proximos)
            else:
                agente.score_novidade = 0

    def executa(self):
        if self.ambiente is None: return

        if self.modo != "novelty":
            # --- MODO CLÁSSICO (Q-Learning) ---
            # AQUI ESTÃO OS PRINTS DE VOLTA
            num_episodios = 1000 if self.modo == "farol" else 500

            self.agente.learning_mode = True
            print(f"--- A CORRER: {self.modo} ({num_episodios} Episódios) ---")

            for ep in range(1, num_episodios + 1):
                sucesso, passos, rec = self.executa_episodio(renderizar=False)

                # Print Detalhado a cada 10%
                if ep % (num_episodios // 10) == 0 or ep == 1:
                    print(
                        f"Ep {ep}/{num_episodios} | Sucesso: {sucesso} | Passos: {passos} | Recompensa: {rec:.2f} | Epsilon: {self.agente.epsilon:.4f}")

            print("\n=== DEMONSTRAÇÃO FINAL ===")
            self.agente.learning_mode = False
            self.executa_episodio(renderizar=True)

        else:
            # --- MODO EVOLUTIVO (NOVELTY SEARCH) ---
            print("--- A INICIAR EVOLUÇÃO (NOVELTY SEARCH) ---")
            geracoes = 50
            arquivo_novidade = []

            melhor_agente_global = None

            for g in range(geracoes):
                sucessos_na_geracao = 0

        # Loop de Episódios
        for episodio in range(1, num_episodios + 1):
            render_agora = (episodio == num_episodios)
                for individuo in self.populacao:
                    self.agente = individuo
                    sucesso, passos, _ = self.executa_episodio(renderizar=False)
                    individuo.posicao_final = self.ambiente.agente_pos

                    if sucesso:
                        sucessos_na_geracao += 1
                        melhor_agente_global = copy.deepcopy(individuo)
                        print(f"--> SOLUÇÃO ENCONTRADA NA GERAÇÃO {g}!")

            if episodio % (num_episodios // 10) == 0 or episodio == num_episodios or episodio == 1:
                print(
                    f"Episódio {episodio}/{num_episodios} | Sucesso: {sucesso} | Passos: {passos} | Recompensa Total: {recompensa_total:.2f} | Epsilon: {self.agente.epsilon:.4f}")
                if sucessos_na_geracao > 0: break

                self.calcular_novidade(arquivo_novidade)
                arquivo_novidade.append(self.populacao[0].posicao_final)

                self.populacao.sort(key=lambda x: x.score_novidade, reverse=True)
                elite = self.populacao[:10]

                nova_populacao = []
                while len(nova_populacao) < 20:
                    pai = random.choice(elite)
                    filho = copy.deepcopy(pai)
                    filho.mutate(taxa=0.2)
                    nova_populacao.append(filho)

                self.populacao = nova_populacao
                print(f"Geração {g} | Max Novidade: {elite[0].score_novidade:.2f}")

            print("\n=== DEMONSTRAÇÃO DO MELHOR AGENTE EVOLUÍDO ===")
            if melhor_agente_global:
                self.agente = melhor_agente_global
                self.executa_episodio(renderizar=True)
            else:
                print("A evolução não encontrou a saída a tempo.")

if __name__ == "__main__":
    sim = Simulador()
     sim.fps = 5
    #sim.cria("farol")
    #sim.cria("labirinto")
    sim.cria("novelty")
    sim.executa()