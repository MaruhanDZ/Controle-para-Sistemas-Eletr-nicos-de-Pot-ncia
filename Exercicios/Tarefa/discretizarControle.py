import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# ============================================================
# CONTROLADOR CONTÍNUO
# ============================================================

numControlador = [
    2.71673615e+11,
    6.87826487e+14,
    4.35361818e+17
]

denControlador = [
    1.00000000e+00,
    1.18360766e+09,
    4.15258556e+13,
    0.00000000e+00
]

C = signal.TransferFunction(
    numControlador,
    denControlador
)


# ============================================================
# PERÍODO DE AMOSTRAGEM
# ============================================================

Ts = 1 / 15000


# ============================================================
# DISCRETIZAÇÃO - BACKWARD EULER
# ============================================================

Cd = signal.cont2discrete(
    (numControlador, denControlador),
    Ts,
    method='backward_diff'
)

numControladorDiscretizado = Cd[0].flatten()
denControladorDiscretizado = Cd[1].flatten()

Cz = signal.TransferFunction(
    numControladorDiscretizado,
    denControladorDiscretizado,
    dt=Ts
)


print("Controlador contínuo:")
print(C)

print("\nControlador discreto:")
print(Cz)

print("\nNumerador discreto:")
print(numControladorDiscretizado)

print("\nDenominador discreto:")
print(denControladorDiscretizado)


# ============================================================
# DIAGRAMA DE BODE
# ============================================================

# Frequências em Hz
f = np.logspace(0, np.log10(7500), 2000)

# Converter Hz -> rad/s
w = 2 * np.pi * f


# ------------------------------------------------------------
# Controlador contínuo
# ------------------------------------------------------------

w_cont, mag_cont, phase_cont = signal.bode(
    C,
    w=w
)


# ------------------------------------------------------------
# Controlador discreto
# ------------------------------------------------------------

# Avaliação da resposta em frequência do sistema discreto
_, H_disc = signal.dfreqresp(
    Cz,
    w=w * Ts
)

mag_disc = 20 * np.log10(np.abs(H_disc))
phase_disc = np.unwrap(np.angle(H_disc)) * 180 / np.pi


# ============================================================
# PLOT
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(10, 8),
    sharex=True
)


# ------------------------------------------------------------
# MAGNITUDE
# ------------------------------------------------------------

ax1.semilogx(
    f,
    mag_cont,
    label='Contínuo C(s)',
    linewidth=2
)

ax1.semilogx(
    f,
    mag_disc,
    '--',
    label='Discreto C(z) - Backward Euler',
    linewidth=2
)

ax1.set_ylabel('Magnitude [dB]')
ax1.set_title('Diagrama de Bode - Controlador')
ax1.grid(True, which='both')
ax1.legend()


# ------------------------------------------------------------
# FASE
# ------------------------------------------------------------

ax2.semilogx(
    f,
    phase_cont,
    label='Contínuo C(s)',
    linewidth=2
)

ax2.semilogx(
    f,
    phase_disc,
    '--',
    label='Discreto C(z) - Backward Euler',
    linewidth=2
)

ax2.set_xlabel('Frequência [Hz]')
ax2.set_ylabel('Fase [°]')
ax2.grid(True, which='both')
ax2.legend()


# Limite de Nyquist
ax1.axvline(
    1 / (2 * Ts),
    linestyle=':',
    linewidth=1.5,
    label='Nyquist'
)

ax2.axvline(
    1 / (2 * Ts),
    linestyle=':',
    linewidth=1.5
)

plt.tight_layout()
plt.show()