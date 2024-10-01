from qlib import *
from qlib.solvers.eigen import eigenvalues
import matplotlib.pyplot as plt
import numpy as np


def energy_schema(hamiltonian_fn, param_range, ax, title):
    eigv_list = []
    for param in param_range:
        H = hamiltonian_fn(param)
        evals = sorted(eigenvalues(H))
        eigv_list.append(evals)
    eigv_list = np.array(eigv_list)
    
    for i in range(eigv_list.shape[1]):
        ax.plot(param_range, eigv_list[:, i], color='black')

    ax.set_title(title)
    ax.set_ylabel("Eigenvalues")