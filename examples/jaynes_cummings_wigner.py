from qlib import *
import numpy as np
import matplotlib.pyplot as plt

'''
An animation capturing Rabi oscillations in the Jaynes-Cummings (JC)
model via the Wigner function of the optical cavity. This 
approach propagates the JC model over time, traces out the TLS system
at each time value, and finally calculates the Wigner function
at each time step. 

Verification of correctness is easy to see; the Wigner functions of the
ground state and first excited state in the fock basis are known and 
observed in this animation.
'''

# setting up JC system
Omega, coupling, cavity_bsize = 1, 0.3, 15
H = jc_hamiltonian(cavity_bsize, Omega, coupling)
cavity_psi0, tls_psi0 = state(cavity_bsize, 0), state(2, 0) # one initial excitation
combined_psi0 = tensor(tls_psi0, cavity_psi0)
t0, tf, grain = 0, 500, 0.25

# evolving system in time, tracing out TLS
states = time_evolve_loop(H, t0, tf, grain, combined_psi0)
for i in range(len(states)):
    states[i] = partial_trace(states[i].to_density_matrix(), [2, cavity_bsize], [0])

# setting up plot for wigner animation
x_grid, p_grid = np.linspace(-4, 4, 80), np.linspace(-4, 4, 80)
anim = animate_wigner_3d(states, x_grid, p_grid, z_axis_bounds=(-0.315, 0.315))
plt.show()