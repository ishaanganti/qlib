from qlib import *
import matplotlib.pyplot as plt
import numpy as np

'''
Two plots illustrating the commonly used rotating wave
approximation in quantum optics. The parameters of this demo
are set up to match the assumptions under which the approximation
can be made, and the two resulting expected value plots demonstrate
why the counter-rotating terms can be discarded. 
'''

Omega, omega0, omegaL = 1, 49.99, 50
H0 = omega0 * 0.5 * oper([[1, 0], [0, -1]]) 
def H_RWA(t):
    eg = -Omega * np.exp(-1j * omegaL * t) - Omega * np.exp(1j * omegaL * t)
    ge = -Omega * np.exp(-1j * omegaL * t) - Omega * np.exp(1j * omegaL * t)
    return H0 + oper([[0, eg], [ge, 0]])
def H_Normal(t):
    return H0 + oper([[0, -np.exp(-1j * omegaL * t)], [-np.exp(1j * omegaL * t), 0]])

xp_excited, xp_ground = projection(state(2, 0)), projection(state(2, 1))

psi0 = ket([1, 0])
t0, tf = 0, 10
step = 0.001 # needs to be small to see small oscillations
state_list = time_evolve_loop(H_RWA, t0, tf, step, psi0)
state_list_rwa = time_evolve_loop(H_Normal, t0, tf, step, psi0)

fig_rwa, ax_rwa = expectation_line_plot(state_list_rwa, xp_excited, t0, tf, "clean")
fig_normal, ax_normal = expectation_line_plot(state_list, xp_excited, t0, tf, "clean")
plt.show()