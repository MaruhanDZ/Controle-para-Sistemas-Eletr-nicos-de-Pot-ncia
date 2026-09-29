import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ============================================================
# Função de transferência contínua
# ============================================================

num = [225]
den = [1, 100]

system = signal.TransferFunction(num, den)

# ============================================================
# Sistemas discretos
# ============================================================

# Tempo de amostragem
Ts = 0.01       # segundos
fs = 1 / Ts     # frequência de amostragem = 100 Hz

# ------------------------------------------------------------
# Backward Euler
#
# G(z) = 10 / (z^-1 + 11)
#
# Para freqz:
# Numerador  = 10
# Denominador = 11 + z^-1
#
# ------------------------------------------------------------
T = 1
numBack = [10]
denBack = [1 + 10*T, -1]
# ------------------------------------------------------------
# Tustin
#
# G(z) = 5 / (z^2 - 1)
#
# Multiplicando numerador e denominador por z^-2:
#
# G(z) = 5 z^-2 / (1 - z^-2)
#
# Portanto:
#
# Numerador   = 5 z^-2
# Denominador = 1 - z^-2
#
# ------------------------------------------------------------

numTustin = [0, 0, 5]
denTustin = [1, 5*T, -1 + 5*T]

# ============================================================
# Frequência
# ============================================================

# Frequência em Hz
f = np.logspace(-2, np.log10(fs / 2), 2000)

# Frequência angular digital normalizada
# freqz trabalha com rad/amostra
omega = 2 * np.pi * f / fs

# ============================================================
# Bode - Sistema contínuo
# ============================================================

w_cont, mag_cont, phase_cont = signal.bode(
    system,
    w=2 * np.pi * f
)

# ============================================================
# Bode - Backward Euler
# ============================================================

_, H_back = signal.freqz(
    numBack,
    denBack,
    worN=omega
)

mag_back = 20 * np.log10(np.abs(H_back))
phase_back = np.unwrap(np.angle(H_back)) * 180 / np.pi

# ============================================================
# Bode - Tustin
# ============================================================

_, H_tustin = signal.freqz(
    numTustin,
    denTustin,
    worN=omega
)

mag_tustin = 20 * np.log10(np.abs(H_tustin))
phase_tustin = np.unwrap(np.angle(H_tustin)) * 180 / np.pi

# ============================================================
# Imprimir funções
# ============================================================

print("===================================================")
print("Sistema contínuo")
print("===================================================")
print(system)

print("\n===================================================")
print("Backward Euler")
print("===================================================")
print("G(z) = 10 / (11 + z^-1)")

print("\n===================================================")
print("Tustin")
print("===================================================")
print("G(z) = 5 z^-2 / (1 - z^-2)")

print("\nFrequência de amostragem:")
print(f"fs = {fs:.2f} Hz")

# ============================================================
# Plot
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(10, 8),
    sharex=True
)

# ------------------------------------------------------------
# Magnitude
# ------------------------------------------------------------

ax1.semilogx(
    f,
    mag_cont,
    label="Contínuo"
)

ax1.semilogx(
    f,
    mag_back,
    label="Backward Euler"
)

ax1.semilogx(
    f,
    mag_tustin,
    label="Tustin"
)

ax1.set_ylabel("Magnitude (dB)")
ax1.set_title("Diagrama de Bode - Comparação")
ax1.grid(True, which="both", linestyle=":")
ax1.legend()

# ------------------------------------------------------------
# Fase
# ------------------------------------------------------------

ax2.semilogx(
    f,
    phase_cont,
    label="Contínuo"
)

ax2.semilogx(
    f,
    phase_back,
    label="Backward Euler"
)

ax2.semilogx(
    f,
    phase_tustin,
    label="Tustin"
)

ax2.set_xlabel("Frequência (Hz)")
ax2.set_ylabel("Fase (graus)")
ax2.grid(True, which="both", linestyle=":")
ax2.legend()

plt.tight_layout()
plt.show()