import time
# Importar as classes dos outros ficheiros
from Ambiente_Labirinto import AmbienteLabirinto
from Agente_Labirinto import AgenteLabirinto
from Ambiente_Farol import AmbienteFarol
from Agente_Farol import AgenteFarol
from Agente_Novelty import AgenteNovelty
from Sensor import Sensor

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

    def cria(self, tipo_problema, dificuldade="facil", algoritmo="qlearning"):
        self.modo = tipo_problema
        self.dificuldade_atual = dificuldade # Importante para a GUI

        # 1. Carregar Ambiente
        if tipo_problema == "farol":
            print(f"-> Farol ({dificuldade}) | Agente: {algoritmo}")
            self.ambiente = AmbienteFarol(mapa_tipo=dificuldade)
            obs_inicial = self.ambiente.observacaoPara() # Obs original (será filtrada depois)

        elif tipo_problema == "labirinto":
            print(f"-> Labirinto ({dificuldade}) | Agente: {algoritmo}")
            self.ambiente = AmbienteLabirinto(dificuldade)
            obs_inicial = self.ambiente.agente_pos

        else:
            raise Exception("Problema desconhecido.")

        # --- NOVO: Inicializar o Sensor ---
        self.sensor = Sensor(self.ambiente, dificuldade)
        # ----------------------------------

        # 2. Configurar Agente
        if algoritmo == "novelty":
            self.agente = AgenteNovelty()
            self.max_passos = 2000
            if tipo_problema == "farol":
                self.agente.observacao(obs_inicial)
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
                # Ajuste para labirinto dificil
                if dificuldade == "dificil": self.max_passos = 500
                else: self.max_passos = 200
        else:
             raise Exception(f"Algoritmo '{algoritmo}' não reconhecido.")

        if self.visualizador:
            self.visualizador.fechar()
        self.visualizador = None

    def executa_episodio(self, renderizar=False):
        self.passos = 0
        terminou = False

        # Reset do ambiente
        self.ambiente.reset()
        self.agente.recompensa_acumulada = 0

        # --- PREPARAÇÃO DO NOVELTY ---
        # O Novelty precisa de limpar a memória de curto prazo a cada episódio
        if isinstance(self.agente, AgenteNovelty):
            self.agente.observacao(self.ambiente.agente_pos)
            self.agente.historico_recente = []
            self.agente.ja_agiu = False
        else:
            # Preparação Q-Learning (Reset posições iniciais)
            if self.modo == "labirinto":
                self.agente.atualiza_posicao(self.ambiente.agente_pos)
            elif self.modo == "farol":
                # Nota: A observação inicial do Farol será atualizada logo no loop
                # mas convém inicializar para evitar erros
                self.agente.observacao(self.ambiente.observacaoPara())

        # --- INICIALIZAR PYGAME ---
        if renderizar and VisualizadorPygame:
            dif = getattr(self, "dificuldade_atual", "N/A")
            nome_agente = "Novelty" if isinstance(self.agente, AgenteNovelty) else "Q-Learning"

            self.visualizador = VisualizadorPygame(
                self.ambiente,
                self.modo,
                self.max_passos,
                self.fps,
                dif,
                nome_agente
            )

        # --- LOOP DO EPISÓDIO ---
        while not terminou and self.passos < self.max_passos:

            # 1. CONSULTAR O SENSOR (Onde está o objetivo?)
            pos_objetivo = self.sensor.get_posicao_objetivo()

            # 2. ATUALIZAR VISUALIZADOR (Desenha o "Laser" se o sensor vir o objetivo)
            if self.visualizador:
                sucesso = self.ambiente.jogo_terminou()
                self.visualizador.desenha(
                    self.passos,
                    self.agente.recompensa_acumulada,
                    terminou,
                    sucesso,
                    self.agente.epsilon,
                    sensor_alvo=pos_objetivo  # <--- Passamos o alvo para desenhar a linha
                )

            # 3. PERCEPÇÃO (O que o Agente "Vê")
            if isinstance(self.agente, AgenteNovelty):
                # --- ALTERAÇÃO AQUI ---
                # Passamos a posição do agente E a posição do objetivo (se visível)
                self.agente.observacao(self.ambiente.agente_pos, alvo=pos_objetivo)

            elif isinstance(self.agente, AgenteFarol):
                # O Agente Farol precisa de saber a Direção (Vetor)
                if pos_objetivo is not None:
                    # Sensor vê o farol -> Calculamos o vetor (dx, dy)
                    ax, ay = self.ambiente.agente_pos
                    fx, fy = pos_objetivo
                    obs = (fx - ax, fy - ay)
                else:
                    # Sensor não vê nada -> Agente fica cego (None)
                    obs = None

                self.agente.observacao(obs)

            elif isinstance(self.agente, AgenteLabirinto):
                # O Labirinto Q-Learning usa apenas a posição interna (já atualizada abaixo)
                self.agente.observacao(None)

            # 4. AÇÃO
            acao = self.agente.age()

            # 5. EXECUÇÃO NO AMBIENTE
            recompensa = self.ambiente.agir(acao)

            # 6. ATUALIZAÇÃO DO AGENTE
            # Se for labirinto (Q-Learning), temos de dizer onde ele "aterrou"
            if self.modo == "labirinto" and not isinstance(self.agente, AgenteNovelty):
                self.agente.atualiza_posicao(self.ambiente.agente_pos)

            # Aprender (Update Q-Table ou Novelty Score)
            self.agente.avaliacaoEstadoAtual(recompensa)

            if self.ambiente.jogo_terminou():
                terminou = True

            self.passos += 1

        # --- FIM DO LOOP ---

        sucesso = self.ambiente.jogo_terminou()

        # Desenho Final (Pausa para veres o resultado)
        if self.visualizador:
            self.visualizador.desenha(
                self.passos,
                self.agente.recompensa_acumulada,
                terminou,
                sucesso,
                self.agente.epsilon,
                sensor_alvo=None  # Removemos a linha no fim
            )
            time.sleep(0.5)
            self.visualizador.fechar()
            self.visualizador = None

        return sucesso, self.passos, self.agente.recompensa_acumulada

    def executa(self, episodios_treino=1000, episodios_teste=100):
        if self.ambiente is None or self.agente is None:
            print("Erro: Tens de correr sim.cria() primeiro!")
            return

        # --- FASE 1: APRENDIZAGEM ---
        print(f"\n>>> INÍCIO DO TREINO ({episodios_treino} episódios)")
        print(f"    Modo: Learning=TRUE | Epsilon=Dinâmico")

        # Garantir que o agente está configurado para aprender
        self.agente.learning_mode = True
        # (O epsilon já está alto por defeito no init do agente)

        for episodio in range(1, episodios_treino + 1):
            # Renderizar apenas o último episódio do treino para confirmares que ele aprendeu
            render = (episodio == episodios_treino)

            sucesso, passos, recompensa = self.executa_episodio(renderizar=render)

            # Logs periódicos para saberes que não encravou
            if episodio % 100 == 0:
                print(f"   [Treino] Ep {episodio}/{episodios_treino} | Passos: {passos} | Rec: {recompensa:.1f}")

        # --- O SWITCH (MUDANÇA DE MODO) ---
        print("\n>>> FIM DO TREINO. A MUDAR PARA MODO DE TESTE...")
        self.agente.learning_mode = False  # Para de atualizar a Q-Table/Memória [cite: 85]
        self.agente.epsilon = 0.0  # Para de explorar (Greedy puro)

        # --- FASE 2: TESTE / AVALIAÇÃO ---
        print(f">>> INÍCIO DO TESTE ({episodios_teste} episódios)")
        print(f"    Modo: Learning=FALSE | Epsilon=0.0")

        sucessos_teste = 0
        total_passos_teste = 0

        for episodio in range(1, episodios_teste + 1):
            # No teste, podes querer ver mais vezes, ou apenas o último
            render = (episodio == episodios_teste)

            sucesso, passos, recompensa = self.executa_episodio(renderizar=render)

            if sucesso:
                sucessos_teste += 1
            total_passos_teste += passos

        # --- RESULTADOS FINAIS ---
        taxa = (sucessos_teste / episodios_teste) * 100
        media_passos = total_passos_teste / episodios_teste

        print("\n" + "=" * 40)
        print(f"RESULTADOS FINAIS ({self.modo.upper()}):")
        print(f"Taxa de Sucesso: {taxa:.1f}%")
        print(f"Média de Passos: {media_passos:.1f}")
        print("=" * 40)


# Exemplo de uso:
if __name__ == "__main__":
    sim = Simulador()
    #sim.cria("farol", "dificil", "novelty")
    sim.cria("farol", "dificil", "qlearning")
    sim.fps = 10
    sim.executa(episodios_treino=1000, episodios_teste=100)