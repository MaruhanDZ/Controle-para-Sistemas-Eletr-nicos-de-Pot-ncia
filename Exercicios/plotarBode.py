import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ============================================================
# Função de transferência
# ============================================================

# Frequência (Hz)
f = np.logspace(-2, 2, 10000)

# Frequência angular
w = 2 * np.pi * f

num = [225]

den = [1, 100]

system = signal.TransferFunction(num, den)
print(system)

# ============================================================
# Diagrama de Bode
# ============================================================

w, magnitude, phase = signal.bode(system, w=w)

# ============================================================
# Plot
# ============================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

# Magnitude
ax1.semilogx(f, magnitude)
ax1.set_ylabel("Magnitude (dB)")
ax1.set_title("Diagrama de Bode")
ax1.grid(True, which="both", linestyle=":")

# Fase
ax2.semilogx(f, phase)
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Phase (deg)")
ax2.grid(True, which="both", linestyle=":")

plt.tight_layout()
plt.show()