import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ============================================================
# FUNÇÕES DE TRANSFERÊNCIA
# ============================================================

# Planta
num = [225]
den = [1, 100]

FT = signal.TransferFunction(num, den)

# Controlador
numControlador = [np.float64(0.0003842340221311719), 1]

denControlador = [np.float64(8.987528142323844e-10), np.float64(1.3633137565120973e-05), 0]

C = signal.TransferFunction(numControlador, denControlador)

# ============================================================
# FT(s) * C(s)
# ============================================================

numMalha = np.polymul(num, numControlador)
denMalha = np.polymul(den, denControlador)

FT_C = signal.TransferFunction(numMalha, denMalha)

print("========================================")
print("PLANTA FT(s)")
print("========================================")
print(FT)

print("\n========================================")
print("CONTROLADOR C(s)")
print("========================================")
print(C)

print("\n========================================")
print("MALHA ABERTA FT(s)*C(s)")
print("========================================")
print(FT_C)


# ============================================================
# FREQUÊNCIA
# ============================================================

# 0,01 Hz até 10 kHz
f = np.logspace(-2, 4, 20000)

# Converter Hz -> rad/s
w = 2 * np.pi * f


# ============================================================
# BODE DA PLANTA
# ============================================================

_, mag_FT, phase_FT = signal.bode(FT, w=w)


# ============================================================
# BODE DA MALHA ABERTA FT(s)*C(s)
# ============================================================

_, mag_FTC, phase_FTC = signal.bode(FT_C, w=w)


# ============================================================
# DIAGRAMA DE BODE
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(10, 8),
    sharex=True
)

# ---------------------------
# Magnitude
# ---------------------------

ax1.semilogx(f, mag_FT, label="FT(s)")
ax1.semilogx(f, mag_FTC, label="FT(s)C(s)")

ax1.axhline(
    0,
    linestyle="--",
    linewidth=1
)

ax1.set_ylabel("Magnitude (dB)")
ax1.set_title("Diagrama de Bode")
ax1.grid(True, which="both", linestyle=":")
ax1.legend()


# ---------------------------
# Fase
# ---------------------------

ax2.semilogx(f, phase_FT, label="FT(s)")
ax2.semilogx(f, phase_FTC, label="FT(s)C(s)")

ax2.set_xlabel("Frequência (Hz)")
ax2.set_ylabel("Fase (graus)")
ax2.grid(True, which="both", linestyle=":")
ax2.legend()

plt.tight_layout()
plt.show()


# ============================================================
# MARGEM DE FASE
# ============================================================

# Encontrar onde magnitude cruza 0 dB
magnitude_linear = 10 ** (mag_FTC / 20)

# Procurar cruzamento de 1 (0 dB)
indices = np.where(
    np.diff(np.sign(magnitude_linear - 1))
)[0]

if len(indices) > 0:

    # Primeiro cruzamento
    i = indices[0]

    # Interpolação logarítmica da frequência
    log_f1 = np.log10(f[i])
    log_f2 = np.log10(f[i + 1])

    m1 = mag_FTC[i]
    m2 = mag_FTC[i + 1]

    log_fc = log_f1 + (0 - m1) * (log_f2 - log_f1) / (m2 - m1)

    fc = 10 ** log_fc

    # Interpolação da fase
    phase_fc = np.interp(
        np.log10(fc),
        np.log10(f),
        phase_FTC
    )

    # Margem de fase
    margem_fase = 180 + phase_fc

    print("\n========================================")
    print("ANÁLISE DA MALHA ABERTA")
    print("========================================")

    print(f"Frequência de cruzamento: {fc:.3f} Hz")
    print(f"Fase na frequência de cruzamento: {phase_fc:.3f}°")
    print(f"Margem de fase: {margem_fase:.3f}°")

else:

    print("\nNão foi encontrado cruzamento em 0 dB.")


# ============================================================
# MARCAR FREQUÊNCIA DE CRUZAMENTO NO GRÁFICO
# ============================================================

if len(indices) > 0:

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(10, 8),
        sharex=True
    )

    # Magnitude
    ax1.semilogx(f, mag_FTC)

    ax1.axhline(
        0,
        linestyle="--",
        linewidth=1
    )

    ax1.axvline(
        fc,
        linestyle="--",
        linewidth=1
    )

    ax1.scatter(
        fc,
        0,
        zorder=5
    )

    ax1.text(
        fc,
        3,
        f"fc = {fc:.2f} Hz",
        ha="center"
    )

    ax1.set_ylabel("Magnitude (dB)")
    ax1.set_title("Bode - FT(s)C(s)")
    ax1.grid(True, which="both", linestyle=":")


    # Fase
    ax2.semilogx(f, phase_FTC)

    ax2.axvline(
        fc,
        linestyle="--",
        linewidth=1
    )

    ax2.axhline(
        -180,
        linestyle="--",
        linewidth=1
    )

    ax2.scatter(
        fc,
        phase_fc,
        zorder=5
    )

    ax2.text(
        fc,
        phase_fc + 10,
        f"MF = {margem_fase:.2f}°",
        ha="center"
    )

    ax2.set_xlabel("Frequência (Hz)")
    ax2.set_ylabel("Fase (graus)")
    ax2.grid(True, which="both", linestyle=":")

    plt.tight_layout()
    plt.show()