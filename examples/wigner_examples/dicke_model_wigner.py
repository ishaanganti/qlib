from qlib import *
import numpy as np
import matplotlib.pyplot as plt

'''
An animation capturing the dynamics of the Dicke model
model via the Wigner function of the optical cavity. This 
approach propagates the Dicke model over time, traces out the TLS systems
at each time value, and finally calculates the Wigner function
at each time step. 
'''

# setting up complex Dicke system
Omega, coupling, cavity_bsize, K = 1, 0.3, 15, 4
H = reduced_dicke_hamiltonian(cavity_bsize, K, Omega, coupling)
cavity_psi0, tls_psi0 = state(cavity_bsize, 0), state(K+1, 0) # two initial excitations
combined_psi0 = tensor(tls_psi0, cavity_psi0)
t0, tf, grain = 0, 500, 0.5

# evolving system in time, tracing out TLS
states = time_evolve_loop(H, t0, tf, grain, combined_psi0, method="eigenexpand")
for i in range(len(states)):
    states[i] = partial_trace(states[i].to_density_matrix(), [K+1, cavity_bsize], [0])

# setting up plot for wigner animation
x_grid, p_grid = np.linspace(-4, 4, 80), np.linspace(-4, 4, 80)
anim = animate_wigner_3d(states, x_grid, p_grid, interval=0.1, z_axis_bounds=(-0.315, 0.315))
plt.show()