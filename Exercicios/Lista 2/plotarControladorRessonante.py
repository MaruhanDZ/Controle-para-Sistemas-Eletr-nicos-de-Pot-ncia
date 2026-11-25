
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ============================================================
# PLANTA
# ============================================================

Vdc = 400
L = 0.005
R = 0.5

num = [Vdc]
den = [L, R]

FT = signal.TransferFunction(num, den)

# ============================================================
# CONTROLADOR PROPORCIONAL RESSONANTE (PR)
# ============================================================

alpha = 3
wr = 2*np.pi*60 # frequencia ressonante em rad/s

kp = ( (alpha * np.sqrt(alpha) * wr * L) - R ) / Vdc

kr = ( wr**2 * ( alpha**2 - 1 ) * L ) / (2*Vdc)

numControlador = [kp, 2*kr, kp*wr**2]
denControlador = [1, 0, wr**2]

C = signal.TransferFunction(numControlador, denControlador)

# ============================================================
# FUNÇÃO DE TRANSFERÊNCIA DE MALHA ABERTA
# ============================================================

numMalha = np.polymul(num, numControlador)
denMalha = np.polymul(den, denControlador)

FT_C = signal.TransferFunction(numMalha, denMalha)

# ============================================================
# FUNÇÃO DE TRANSFERÊNCIA DE MALHA FECHADA
# REALIMENTAÇÃO UNITÁRIA NEGATIVA
# ============================================================

# T(s) = FT(s)*C(s) / (1 + FT(s)*C(s))

numMF = numMalha
denMF = np.polyadd(denMalha, numMalha)

MF = signal.TransferFunction(numMF, denMF)

# ============================================================
# EXIBIR FUNÇÕES DE TRANSFERÊNCIA
# ============================================================

print("========================================")
print("PLANTA FT(s)")
print("========================================")
print(FT)

print("\n========================================")
print("CONTROLADOR PR C(s)")
print("========================================")
print(C)

print("\n========================================")
print("MALHA ABERTA FT(s)*C(s)")
print("========================================")
print(FT_C)

print("\n========================================")
print("MALHA FECHADA T(s)")
print("========================================")
print(MF)

# ============================================================
# RESPOSTA A UMA REFERÊNCIA SENOIDAL (60 Hz)
# ============================================================

t = np.linspace(0, 0.2, 2000)  # 0,2 s (~12 ciclos de 60 Hz) para ver o transitório e o regime
ref = np.sin(wr * t)           # referência senoidal unitária em wr

_, y, _ = signal.lsim(MF, U=ref, T=t)

# ============================================================
# GRÁFICO
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(t, ref, color="black", linestyle="--", linewidth=1.2, label="Referência senoidal (60 Hz)")
plt.plot(t, y, linewidth=1.5, label="Malha fechada")

plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.title("Resposta a Referência Senoidal - Sistema em Malha Fechada")

plt.grid(True, which="both", linestyle=":")
plt.legend()

plt.tight_layout()
plt.show()
