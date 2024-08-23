from qlib import *
import matplotlib.pyplot as plt

'''
A standard plot illustrating the collapse and revivals of 
probabilities in the Jaynes-Cummings model assuming an initial
coherent state in the cavity mode and an excited state in the
TLS. 
'''

Omega = 1
coupling = 0.3
cavity_bsize = 40
H = jc_hamiltonian(cavity_bsize, Omega, coupling)
cavity_psi0, tls_psi0 = coherent(cavity_bsize, 4.0), state(2, 0)
combined_psi0 = tensor(tls_psi0, cavity_psi0)
t0, tf = 0, 400
grain = 0.25 # finer grain

states = time_evolve_loop(H, t0, tf, 0.25, combined_psi0, "exponential")
excited_population = tensor(projection(state(2, 0)), identity(cavity_bsize))
fig, ax = expectation_line_plot(states, excited_population, t0, tf, "clean_inverted")
plt.show()