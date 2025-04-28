# pcm medium ==> eutectic paraffin (n-octadecane , n-nonadecane)
# coolant ==> water + ethylene glycol (50%)
T_pcm_max = 33 # °C
density_pcm = 751 # kg/m^3
C_pcm = 2.1 # J/g.K
L_f_pcm = 220 # kJ/kg
k_pcm = 2.3 # W/m.K

cp_cool = 3.55 # J/g.K
density_coolant = 1055 # kg/m^3
# temp_inlet_coolant = 


import numpy as np
import matplotlib.pyplot as plt

# Constants (example values - adjust as needed)
# cp_cool = 4.18  # Specific heat of coolant [kJ/kg·K] (water)
#  = 80  # Maximum PCM temperature [°C]


Q_gen_range = np.linspace(10, 50, 100)  # Heat generation range [W]
T_in_range = np.linspace(27, 31, 100)  # Inlet temperature range [°C]

# Equation: m_dot_limiting = Q_gen / (cp_cool * (T_pcm_max - T_in)) 
def calculate_m_dot(Q_gen, T_in):
    return Q_gen / (cp_cool * (T_pcm_max - T_in))

# Create grids for plotting
Q_gen_grid, T_in_grid = np.meshgrid(Q_gen_range, T_in_range)
m_dot_grid = calculate_m_dot(Q_gen_grid, T_in_grid)

# Plot 1: m_dot vs T_in for fixed Q_gen values
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
for Q_gen in [10, 20, 30 , 40, 50]:
    m_dot = calculate_m_dot(Q_gen, T_in_range)
    plt.plot(T_in_range, m_dot, label=f'Q_gen = {Q_gen} W')
plt.xlabel('Inlet Temperature, T_in (°C)')
plt.ylabel('Coolant Flow Rate, m_dot (g/s)')
plt.title('m_dot vs T_in for different Q_gen')
plt.legend()
plt.grid(True)

# Plot 2: Q_gen vs T_in for fixed m_dot values
plt.subplot(1, 3, 2)
for m_dot in [0.5, 1.0, 1.5, 2.0]:
    Q_gen = m_dot * cp_cool * (T_pcm_max - T_in_range)
    plt.plot(T_in_range, Q_gen, label=f'm_dot = {m_dot} kg/s')
plt.xlabel('Inlet Temperature, T_in (°C)')
plt.ylabel('Heat Generation, Q_gen (W)')
plt.title('Q_gen vs T_in for different m_dot')
plt.legend()
plt.grid(True)

# Plot 3: Q_gen vs m_dot for fixed T_in values
plt.subplot(1, 3, 3)
for T_in in [27, 29, 31, 32]:
    m_dot = calculate_m_dot(Q_gen_range, T_in)
    plt.plot(m_dot, Q_gen_range, label=f'T_in = {T_in} °C')
plt.xlabel('Coolant Flow Rate, m_dot (g/s)')
plt.ylabel('Heat Generation, Q_gen (W)')
plt.title('Q_gen vs m_dot for different T_in')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

from mpl_toolkits.mplot3d import Axes3D

mask = m_dot_grid > 0  # Boolean mask for valid regions

# Apply the mask to all grids
Q_gen_valid = np.where(mask, Q_gen_grid, np.nan)  # Replace invalid with NaN
T_in_valid = np.where(mask, T_in_grid, np.nan)
m_dot_valid = np.where(mask, m_dot_grid, np.nan)

# --- Create 3D Plot ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot only valid points (NaN values are skipped)
surf = ax.plot_surface(
    Q_gen_valid, T_in_valid, m_dot_valid,
    cmap='viridis', edgecolor='none', alpha=0.8
)

# Labels and title
ax.set_xlabel('Heat Generation, $Q_{gen}$ (W)', fontsize=12)
ax.set_ylabel('Inlet Temperature, $T_{in}$ (°C)', fontsize=12)
ax.set_zlabel('Coolant Flow Rate, $\dot{m}$ (kg/s)', fontsize=12)
ax.set_title('3D Plot: Valid Regions ($\dot{m} > 0$)', fontsize=14)

# Colorbar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='$\dot{m}$ (kg/s)')

# Adjust view angle
ax.view_init(elev=25, azim=45)

plt.tight_layout()
plt.show()