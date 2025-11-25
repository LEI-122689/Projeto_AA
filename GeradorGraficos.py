import matplotlib.pyplot as plt
import numpy as np
from Simulador import Simulador


def correr_experiencia(tipo_problema, n_episodios):
    print(f"--- A gerar dados para: {tipo_problema} ---")
    sim = Simulador()
    sim.cria(tipo_problema)

    # Listas para guardar o histórico
    historico_recompensas = []
    historico_passos = []

    # Vamos sobrepor o método executa para podermos guardar os dados
    # Forçamos o modo de aprendizagem
    sim.agente.learning_mode = True

    for i in range(n_episodios):
        # Executa um episódio (renderizar=False para ser rápido)
        _, passos, recompensa = sim.executa_episodio(renderizar=False)

        historico_recompensas.append(recompensa)
        historico_passos.append(passos)

        if i % 100 == 0:
            print(f"Episódio {i}/{n_episodios} processado...")

    return historico_recompensas, historico_passos


def desenhar_grafico(nome_problema, recompensas, passos):
    # Suavizar a curva (Média Móvel) para o gráfico ficar mais bonito
    window = 50  # Média dos últimos 50 episódios
    rec_suave = np.convolve(recompensas, np.ones(window) / window, mode='valid')
    passos_suave = np.convolve(passos, np.ones(window) / window, mode='valid')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Gráfico 1: Recompensa
    ax1.plot(recompensas, alpha=0.3, color='blue', label='Real')  # Dados brutos transparentes
    ax1.plot(rec_suave, color='darkblue', linewidth=2, label='Média Móvel (Tendência)')
    ax1.set_title(f"Curva de Aprendizagem - {nome_problema}: Recompensa")
    ax1.set_ylabel("Recompensa Total")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Passos
    ax2.plot(passos, alpha=0.3, color='orange', label='Real')
    ax2.plot(passos_suave, color='red', linewidth=2, label='Média Móvel (Tendência)')
    ax2.set_title(f"Eficiência - {nome_problema}: Passos até ao Objetivo")
    ax2.set_xlabel("Episódios")
    ax2.set_ylabel("Número de Passos")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"grafico_{nome_problema.lower()}.png")
    print(f"Gráfico guardado como: grafico_{nome_problema.lower()}.png")
    plt.show()


if __name__ == "__main__":
    # 1. Gerar Gráfico do FAROL
    rec_f, passos_f = correr_experiencia("farol", 1000)
    desenhar_grafico("Farol", rec_f, passos_f)

    # 2. Gerar Gráfico do LABIRINTO
    rec_l, passos_l = correr_experiencia("labirinto", 500)
    desenhar_grafico("Labirinto", rec_l, passos_l)