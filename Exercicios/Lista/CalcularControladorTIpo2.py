import numpy as np
# Prencher com parametros
MFd = 45
FaseFreqCorte = -90
FCdesejada = 1000

ganhodBFCd = -29


# atribuir C2
C2 = 1e-6

# Calcula o ganho real
ganhoRealFCd =  np.power(10, (np.abs(ganhodBFCd)/20)) 
print('Ganho Real FCd: ', ganhoRealFCd)

# Fase a ser compensada
PHIm = MFd - FaseFreqCorte - 90
print('Fase a ser compensada pelo controlador: ', PHIm)

k = np.tan(np.deg2rad(PHIm/2 + 45))
print('K: ', k)

C1 = (k*k - 1) * C2
print('C1: ', C1)

print('C2: ', C2)

R1 = 1/(C2*2*np.pi*FCdesejada*k*ganhoRealFCd)
print('R1: ', R1)

R2 = k/(2*np.pi*FCdesejada*C1)
print('R2: ', R2)

# Calculemo o controlador

numC = [C1*R2, 1]
print(numC)

denC = [R1*R2*C1*C2, R1*C1 + R1*C2, 0]

print(denC)