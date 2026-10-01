import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# parametros do conversor buck (para obter a planta)
inputVoltage = 100
outputVoltage = 50
loadResistence = 25
indutance = 1.5E-3
capacitance = 470E-6
switchingFrequency = 15E3
PWMAmplitude = 1
voltageSensorGain = 1/100
samplingPeriod = 1/15000


# Parâmetros de projeto para o controlador
desiredCutoffFrequency = 1.5E3
desiredPhaseMargin = 60

# Funções transparência

# Planta de Tensão
numGv = [inputVoltage]
denGv = [capacitance*indutance, indutance/loadResistence, 1]
Gv = signal.TransferFunction(numGv, denGv)
print('Planta de tensão \n', Gv)

# Planta do PWM
numPWM = [1]
denPWM = [PWMAmplitude]
tfPWM = signal.TransferFunction(numPWM, denPWM)

print('Planta do PWM \n', tfPWM)

# Função de transferência do sensor de tensão
numVS = [voltageSensorGain]
denVs = [1]
Vs = signal.TransferFunction(numVS, denVs)
print('Função de transferência do sensor de tensão \n', Vs)


# ------------------------------------------------
# Função de transferência de malha aberta
# ------------------------------------------------

numMA = np.polymul(
    np.polymul(tfPWM.num, Gv.num),
    Vs.num
)

denMA = np.polymul(
    np.polymul(tfPWM.den, Gv.den),
    Vs.den
)

tfMA = signal.TransferFunction(numMA, denMA)

print('Função de transferência de malha aberta:\n', tfMA)


# plotagem do diagrama de bode

# Frequência (Hz)
f = np.logspace(-2, 4, 10000)

# Frequência angular
w = 2 * np.pi * f

# ============================================================
# Diagrama de Bode
# ============================================================

w, magnitude, phase = signal.bode(tfMA, w=w)

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
# ------------------------------------------------
# obter os seguintes dados pelo diagrama de bode plotado
phaseOnDesiredCutoffFrequency = -179.4 #°                                 # ALTERAR CASO MUDAR ALGUMA COISA
gainOnDesiredCutoffFrequency = -35.8 #dB                                  # ALTERAR CASO MUDAR ALGUMA COISA

# converter o ganho em dB para absoluto
realGain = np.power(10, np.abs(gainOnDesiredCutoffFrequency)/20)
print('Ganho Real (a partir do bode) ', realGain)

# Obtenção da fase a ser compensada pelo controlador
alpha = desiredPhaseMargin - phaseOnDesiredCutoffFrequency - 90
print('fase a ser compensada pelo controlador', alpha)

# Obter o fator k
k = np.power(np.tan(np.deg2rad(alpha/4 + 45)), 2)
print('Fator k ', k)

#-------------- Obtenção dos coeficientes do controlador -------------------
# Determinar randomicamente um valor para R1
R1 = 1000
print('R1 ',R1)

C2 = 1/(2*np.pi*desiredCutoffFrequency*realGain*R1)
print('C2 ', C2)

C1 = C2*(k-1)
print('C1 ', C1)

R2 = np.sqrt(k)/(2*np.pi*desiredCutoffFrequency*C1)
print('R2 ', R2)

R3 = R1/(k-1)
print('R3 ', R3)

C3 = 1/(2*np.pi*desiredCutoffFrequency*R3*np.sqrt(k))
print('C3 ', C3)

# Obtenção da função transparência do controlador
numC = [R2*C1*C3*R1 + R2*C1*C3*R3 , R2*C1 + R1*C3 + R3*C3, 1]
denC = [R1*R3*C1*C2*C3, R1*R3*C3*C1 + R1*R3*C3*C2 + R1*R2*C1*C2, R1*C1 + R1*C2, 0] 
tfC = signal.TransferFunction(numC, denC)

print("Função de transferência do Controlador \n", tfC)
