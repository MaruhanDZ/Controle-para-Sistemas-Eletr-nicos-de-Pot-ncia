import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
wr = 2*np.pi*60
alpha = np.linspace(0, 5, 500)  # Range de 0 a 5 conforme o eixo X da imagem

# Parâmetros da planta
Vdc = 400
L = 0.005
R = 0.5

# Equações implementadas
kp = ((alpha * np.sqrt(alpha) * wr * L ) - R) / Vdc
kr = (wr**2 * (alpha**2 - 1) * L) / (2 * Vdc)

# Configuração da figura e dos subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6.5))

# --- Gráfico 1: Ganho Proporcional (Kp) vs alpha ---
ax1.plot(alpha, kp, color='blue', linewidth=1.8, label=r'$\mathrm{K_p(\alpha)}$')
ax1.axhline(0, color='red', linestyle='--', alpha=0.6, linewidth=1.2, label=r'Limiar de Estabilidade ($\mathrm{K_p = 0}$)')

ax1.set_title(r'Ganho Proporcional ($\mathbf{K_p}$) vs $\mathbf{\alpha}$', fontweight='bold', fontsize=11)
ax1.set_xlabel(r'$\alpha$')
ax1.set_ylabel(r'$\mathrm{K_p}$')
ax1.set_xlim(0, 5)
ax1.set_xticks(np.arange(0, 5.5, 0.5))
ax1.grid(True, linestyle='-', alpha=0.5)
ax1.tick_params(direction='in', top=True, right=True, length=4, width=1.2)
ax1.legend(loc='upper left', frameon=True, edgecolor='black', fancybox=False)

# --- Gráfico 2: Ganho Ressonante (Kr) vs alpha ---
ax2.plot(alpha, kr, color='magenta', linewidth=1.8, label=r'$\mathrm{K_r(\alpha)}$')
ax2.axhline(0, color='red', linestyle='--', alpha=0.6, linewidth=1.2, label=r'Limiar de Estabilidade ($\mathrm{K_r = 0}$)')

ax2.set_title(r'Ganho Ressonante ($\mathbf{K_r}$) vs $\mathbf{\alpha}$', fontweight='bold', fontsize=11)
ax2.set_xlabel(r'$\alpha$')
ax2.set_ylabel(r'$\mathrm{K_r}$')
ax2.set_xlim(0, 5)
ax2.set_xticks(np.arange(0, 5.5, 0.5))
ax2.grid(True, linestyle='-', alpha=0.5)
ax2.tick_params(direction='in', top=True, right=True, length=4, width=1.2)
ax2.legend(loc='upper left', frameon=True, edgecolor='black', fancybox=False)

# Ajuste automático de espaçamento entre os gráficos
plt.tight_layout()
plt.show()