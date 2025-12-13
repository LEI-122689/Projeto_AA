import time
# Importar as classes dos outros ficheiros
from Ambiente_Labirinto import AmbienteLabirinto
from Agente_Labirinto import AgenteLabirinto
from Ambiente_Farol import AmbienteFarol
from Agente_Farol import AgenteFarol
from Agente_Novelty import AgenteNovelty

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

        # --- CORREÇÃO IMPORTANTE: Guardar a dificuldade ---
        # Isto é essencial para o Pygame conseguir escrever "Dificuldade: DIFICIL" no título
        self.dificuldade_atual = dificuldade

        # 1. Escolher e Carregar o Ambiente
        if tipo_problema == "farol":
            print(f"-> A carregar Problema: Farol ({dificuldade.upper()}) | Algoritmo: {algoritmo.upper()}")
            # Passamos a dificuldade para o ambiente carregar as pedras/correntes certas
            self.ambiente = AmbienteFarol(mapa_tipo=dificuldade)
            # Guardar observação inicial (necessário para inicializar o agente)
            obs_inicial = self.ambiente.observacaoPara()

        elif tipo_problema == "labirinto":
            print(f"-> A carregar Problema: Labirinto ({dificuldade.upper()}) | Algoritmo: {algoritmo.upper()}")
            self.ambiente = AmbienteLabirinto(dificuldade)
            obs_inicial = self.ambiente.agente_pos

        else:
            raise Exception("Problema desconhecido! Escolhe 'farol' ou 'labirinto'.")

        # 2. Escolher e Configurar o Agente
        if algoritmo == "novelty":
            # --- Configuração Agente NOVELTY ---
            self.agente = AgenteNovelty()

            # O Novelty precisa de MUITO mais passos porque anda a explorar às cegas
            self.max_passos = 2000

            # Inicialização da memória do agente
            if tipo_problema == "farol":
                # Nota: No executa_episodio forçamos as coordenadas absolutas,
                # mas aqui inicializamos com o standard do ambiente para não dar erro.
                self.agente.observacao(obs_inicial)
            elif tipo_problema == "labirinto":
                self.agente.atualiza_posicao(obs_inicial)

        elif algoritmo == "qlearning":
            # --- Configuração Agente Q-LEARNING (Teus Agentes Originais) ---
            if tipo_problema == "farol":
                self.agente = AgenteFarol()
                self.agente.observacao(obs_inicial)
                self.max_passos = 500  # O Farol resolve-se depressa se ele souber o caminho

            elif tipo_problema == "labirinto":
                self.agente = AgenteLabirinto()
                self.agente.atualiza_posicao(obs_inicial)

                # Ajuste fino: Labirinto Difícil precisa de mais tempo que o Fácil
                if dificuldade == "dificil":
                    self.max_passos = 500
                else:
                    self.max_passos = 200
        else:
            raise Exception(f"Algoritmo '{algoritmo}' não reconhecido. Usa 'qlearning' ou 'novelty'.")

        # 3. Limpeza do Visualizador Antigo
        # Se mudarmos de problema a meio, temos de matar a janela antiga para criar uma nova com o tamanho certo
        if self.visualizador:
            self.visualizador.fechar()
        self.visualizador = None

    def executa_episodio(self, renderizar=False):
        self.passos = 0
        terminou = False

        # Reset do ambiente
        self.ambiente.reset()
        self.agente.recompensa_acumulada = 0

        # --- CORREÇÃO NOVELTY (Farol e Labirinto) ---
        # O Novelty precisa SEMPRE de coordenadas (x,y)
        if isinstance(self.agente, AgenteNovelty):
            self.agente.observacao(self.ambiente.agente_pos)
            self.agente.historico_recente = []
            self.agente.ja_agiu = False
        else:
            # Q-Learning (Comportamento Original)
            if self.modo == "labirinto":
                self.agente.atualiza_posicao(self.ambiente.agente_pos)
            elif self.modo == "farol":
                self.agente.observacao(self.ambiente.observacaoPara())

        # Inicializar Pygame
        if renderizar and VisualizadorPygame:
            # Ir buscar a dificuldade guardada no self.cria()
            # Se der erro aqui, certifica-te que adicionaste 'self.dificuldade_atual = dificuldade' no método cria()
            dif = getattr(self, "dificuldade_atual", "N/A")
            nome_agente = "Novelty" if isinstance(self.agente, AgenteNovelty) else "Q-Learning"

            self.visualizador = VisualizadorPygame(
                self.ambiente,
                self.modo,
                self.max_passos,
                self.fps,
                dif,  # Argumento novo 1
                nome_agente  # Argumento novo 2
            )

        while not terminou and self.passos < self.max_passos:

            if self.visualizador:
                sucesso = self.ambiente.jogo_terminou()
                self.visualizador.desenha(self.passos, self.agente.recompensa_acumulada, terminou, sucesso,
                                          self.agente.epsilon)

            # 1. Percepção
            obs_raw = self.ambiente.observacaoPara()

            # --- FORÇAR COORDENADAS PARA NOVELTY ---
            if isinstance(self.agente, AgenteNovelty):
                self.agente.observacao(self.ambiente.agente_pos)
            else:
                self.agente.observacao(obs_raw)

            # 2. Ação
            acao = self.agente.age()

            # 3. Execução
            recompensa = self.ambiente.agir(acao)

            # 4. Atualização
            if self.modo == "labirinto" and not isinstance(self.agente, AgenteNovelty):
                self.agente.atualiza_posicao(self.ambiente.agente_pos)

            self.agente.avaliacaoEstadoAtual(recompensa)

            if self.ambiente.jogo_terminou():
                terminou = True

            self.passos += 1

        sucesso = self.ambiente.jogo_terminou()

        # Desenho final e pausa curta
        if self.visualizador:
            self.visualizador.desenha(self.passos, self.agente.recompensa_acumulada, terminou, sucesso,
                                      self.agente.epsilon)
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
    sim.cria("labirinto", "dificil", "qlearning")
    sim.fps = 10
    sim.executa(episodios_treino=1000, episodios_teste=100)