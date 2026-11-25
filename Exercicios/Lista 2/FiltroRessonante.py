
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ============================================================
# Frequência
# ============================================================

f = np.logspace(-2, 4, 10000)
w = 2 * np.pi * f

# ============================================================
# Parâmetros do filtro ressonante
# ============================================================

fr = 60
wr = 2 * np.pi * fr

dampingFactor = 0.5
br = 1.5 * 2 * np.pi

# ============================================================
# Funções de transferência
# ============================================================

numIdeal = [2, 0]
denIdeal = [1, 0, wr**2]

numNaoIdeal = [br, 0]
denNaoIdeal = [1, 2 * dampingFactor * br, wr**2]

systemIdeal = signal.TransferFunction(numIdeal, denIdeal)
systemNaoIdeal = signal.TransferFunction(numNaoIdeal, denNaoIdeal)

# ============================================================
# Diagramas de Bode
# ============================================================

w, magIdeal, phaseIdeal = signal.bode(systemIdeal, w=w)
w, magNaoIdeal, phaseNaoIdeal = signal.bode(systemNaoIdeal, w=w)

# ============================================================
# Plot
# ============================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

# Magnitude
ax1.semilogx(f, magIdeal, label="Filtro Ideal")
ax1.semilogx(f, magNaoIdeal, label="Filtro Não Ideal")

ax1.set_ylabel("Magnitude (dB)")
ax1.set_title("Diagrama de Bode")
ax1.grid(True, which="both", linestyle=":")
ax1.legend()

# Fase
ax2.semilogx(f, phaseIdeal, label="Filtro Ideal")
ax2.semilogx(f, phaseNaoIdeal, label="Filtro Não Ideal")

ax2.set_xlabel("Frequência (Hz)")
ax2.set_ylabel("Fase (graus)")
ax2.grid(True, which="both", linestyle=":")
ax2.legend()

plt.tight_layout()
plt.show()
