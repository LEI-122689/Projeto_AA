import matplotlib.pyplot as plt
import numpy as np
from Simulador import Simulador


def media_movel(dados, window=20):
    """ Suaviza a linha para ser mais fácil ver a tendência. """
    if len(dados) < window: return dados
    return np.convolve(dados, np.ones(window) / window, mode='valid')


def executar_teste(problema, dificuldade, algoritmo, n_episodios):
    print(f"   -> A testar: {algoritmo.upper()}...")
    sim = Simulador()

    # Carrega o cenário específico
    sim.cria(problema, dificuldade, algoritmo)

    # Força modo de aprendizagem
    sim.agente.learning_mode = True

    historico_passos = []

    for i in range(n_episodios):
        # Renderizar=False para ser rápido
        _, passos, _ = sim.executa_episodio(renderizar=False)
        historico_passos.append(passos)

    return historico_passos


def gerar_grafico_comparativo(problema, dificuldade):
    print(f"\n--- A INICIAR COMPARAÇÃO: {problema.upper()} ({dificuldade.upper()}) ---")

    # Configuração
    EPISODIOS = 500  # Podes aumentar para 1000 se quiseres mais detalhe

    # 1. Obter dados do Q-Learning
    passos_q = executar_teste(problema, dificuldade, "qlearning", EPISODIOS)

    # 2. Obter dados do Novelty
    passos_n = executar_teste(problema, dificuldade, "novelty", EPISODIOS)

    # 3. Gerar o Gráfico
    plt.figure(figsize=(10, 6))

    # Plot Q-Learning (Azul)
    plt.plot(passos_q, color='blue', alpha=0.15, label='_nolegend_')  # Dados brutos (transparente)
    plt.plot(media_movel(passos_q), color='blue', linewidth=2, label='Q-Learning (Treino)')

    # Plot Novelty (Laranja)
    plt.plot(passos_n, color='orange', alpha=0.15, label='_nolegend_')  # Dados brutos
    plt.plot(media_movel(passos_n), color='orange', linewidth=2, label='Novelty (Exploração)')

    # Decoração
    plt.title(f"Comparação de Eficiência: {problema.capitalize()} - {dificuldade.capitalize()}")
    plt.xlabel("Episódios")
    plt.ylabel("Número de Passos até ao Objetivo")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Guardar
    nome_ficheiro = f"comparacao_{problema}_{dificuldade}.png"
    plt.savefig(nome_ficheiro)
    print(f"-> Gráfico guardado: {nome_ficheiro}")
    plt.show()

if __name__ == "__main__":

    # Cenário 1: Labirinto Médio
    #gerar_grafico_comparativo("labirinto", "dificil")

    # Cenário 2: Farol Difícil
    gerar_grafico_comparativo("labirinto", "dificil")