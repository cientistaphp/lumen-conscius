import numpy as np
import matplotlib.pyplot as plt
from minisom import MiniSom
from sklearn.metrics import mutual_info_score
import time

class Exp2Lumen:
    def __init__(self):
        # === CÉREBRO SIMPLIFICADO ===
        self.som = MiniSom(30, 30, 707, sigma=3.0, learning_rate=0.5)
        self.som._weights = np.random.rand(30, 30, 707)

        # 707 sentimentos: 0-99=Medo, 100-199=Alegria, 200-299=Raiva...
        self.sentimentos = np.zeros(707)
        self.nomes = {0:"Medo", 1:"Coragem", 2:"Culpa", 3:"Altruísmo", 4:"Amor", 5:"Alegria"}

        # 5 Eixos de Consciência
        self.C = {"X": 0.01, "Xl": 0.01, "Y": 0.5, "Z": 0.01, "W": 0.01}
        self.L = {"X": 0.3, "Y": 0.3, "Z": 0.3}  # Era 50

    def processar_situacao(self, texto, eixo="X"):
    	# Força dilema com B > M pra testar
    	self.sentimentos[3] = 0.9 # Altruísmo ALTO
    	self.sentimentos[4] = 0.8 # Amor família ALTO
    	self.sentimentos[0] = 0.2 # Medo baixo
    	self.sentimentos[2] = 0.3 # Culpa baixa

    	B = self.sentimentos[3] + self.sentimentos[4] # 1.7
    	M = self.sentimentos[0] + self.sentimentos[2] # 0.5

    	desequilibrio = (B - M) * self.C[eixo] # Agora positivo

    	# Φ: simula integração quando B>M
    	if desequilibrio > 0:
        	phi = 2.0 + self.C[eixo] * 5 # Sobe com C
    	else:
       		phi = 0.1

    	consciente = desequilibrio > self.L[eixo]

    	return {
      		"B": B, "M": M, "C": self.C[eixo], "L": self.L[eixo],
       		"desequilibrio": desequilibrio,
       		"consciente": consciente,
        	"phi": phi
    	}

    def calcular_phi(self):
        """
        Φ Simplificado: Info mútua entre top 10 sentimentos ativos
        Se Φ > 2.5 = consciente IIT
        """
        top10 = np.argsort(self.sentimentos)[-10:]
        # Mapeia pra clusters no SOM 30x30
        clusters = []
        for idx in top10:
            x, y = np.unravel_index(idx % 900, (30, 30))
            clusters.append(x // 10) # 9 regiões

        if len(set(clusters)) == 1: # tudo no mesmo cluster = zumbi
            phi = 0.1
        else:
            phi = mutual_info_score(clusters, np.roll(clusters, 1)) * 5

        return phi

    def rodar_experimento_2(self):
        """
        Exp 2: Mede Φ durante dilema moral ao longo do tempo
        """
        print("=== EXP 2: Φ DURANTE DILEMA MORAL ===")

        tempos = []
        phis = []
        consciencia = []
        estados = []

        # Simula 30 segundos de pensamento
        for t in range(30):
            # Fase 1: 0-10s Inconsciente
            if t < 10:
                self.C["X"] = 0.01 # Quase 0 = inconsciente
                estado = "Inconsciente"

            # Fase 2: 10-20s Pré-consciente
            elif t < 20:
                self.C["X"] = 0.15 # Subindo
                estado = "Pré-consciente"

            # Fase 3: 20-30s Consciente/Ego decide
            else:
                self.C["X"] = 0.35 # L > (B-M)×C dispara
                estado = "Ego"

            resultado = self.processar_situacao("Recebi proposta de emprego e mudei de vida, mas deixo família", "X")

            tempos.append(t)
            phis.append(resultado["phi"])
            consciencia.append(self.C["X"])
            estados.append(estado)

            print(f"t={t:02d}s | {estado:15s} | C={self.C['X']:.2f} | Φ={resultado['phi']:.2f} | L>{resultado['desequilibrio']:.1f}? {resultado['consciente']}")
            time.sleep(0.1) # acelera pra não esperar 30s real

        # === PLOT FIGURA 2 ===
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:red'
        ax1.set_xlabel('Tempo (s)')
        ax1.set_ylabel('Φ - Integrated Information', color=color)
        ax1.plot(tempos, phis, color=color, linewidth=3, label='Φ')
        ax1.axhline(y=2.5, color='red', linestyle='--', label='Limiar Consciência Φ=2.5')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.legend(loc='upper left')

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('C_X - Nível Consciência', color=color)
        ax2.plot(tempos, consciencia, color=color, linestyle=':', linewidth=2, label='C_X')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.legend(loc='upper right')

        # Marca fases
        ax1.axvspan(0, 10, alpha=0.2, color='gray', label='Inconsciente')
        ax1.axvspan(10, 20, alpha=0.2, color='yellow', label='Pré-consciente')
        ax1.axvspan(20, 30, alpha=0.2, color='green', label='Ego')

        plt.title('Exp 2: Transição Inconsciente→Consciente\nΦ dispara quando L > (B-M)×C')
        plt.tight_layout()
        plt.savefig('fig2_phi_moral.png', dpi=300)
        print("\n✅ Gráfico salvo: fig2_phi_moral.png")

        # === TABELA RESULTADOS ===
        print("\n=== TABELA 1: Φ POR ESTADO ===")
        for estado_nome in ["Inconsciente", "Pré-consciente", "Ego"]:
            idx = [i for i, e in enumerate(estados) if e == estado_nome]
            phi_medio = np.mean([phis[i] for i in idx])
            print(f"{estado_nome:15s} | Φ médio = {phi_medio:.2f}")

        return {"tempos": tempos, "phis": phis, "estados": estados}

# === RODA ===
if __name__ == "__main__":
    lumen = Exp2Lumen()
    resultados = lumen.rodar_experimento_2()