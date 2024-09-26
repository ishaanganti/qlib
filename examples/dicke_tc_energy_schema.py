from qlib import *
import matplotlib.pyplot as plt
from numpy import linspace

'''
Plots comparing the eigenvalues of the Tavis-Cummings and Dicke
Hamiltonians as a function of coupling strength. These plots 
are typically called the 'energy schema' of each model, and
they show how the two models have similar eigenvalues within
the weak coupling. 

For rough comparison, reference figure 15 from the following:
Emary, C., & Brandes, T. (2003). Quantum chaos triggered by 
precursors of a quantum phase transition: The Dicke model. 
Physical Review Letters, 90(4), 044101. 
https://doi.org/10.1103/PhysRevLett.90.044101
'''

num_tls, cavity_bsize, Omega = 5, 20, 1
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

models = [
    (lambda g: reduced_tc_hamiltonian(cavity_bsize, num_tls, Omega, g), 'Tavis-Cummings Model', linspace(0, 4, 400)),
    (lambda g: reduced_dicke_hamiltonian(cavity_bsize, num_tls, Omega, g), 'Dicke Model', linspace(0, 2, 200))
]

for ax, (model_fn, title, g_range) in zip(axs, models):
    energy_schema(model_fn, g_range, ax, title)
    ax.set_xlabel("Coupling Strength (g)")
    ax.set_ylim(bottom=-3.5, top=2)

plt.tight_layout()
plt.show()