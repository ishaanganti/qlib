import numpy as np
from qlib.operators import pauli_z, pauli_y, pauli_x, creation, annihilation, identity
from qlib.utils import tensor

def rabi_hamiltonian(bsize, Omega, g):
    cavity = tensor(identity(2), creation(bsize) * annihilation(bsize))
    tls = (0.5) * tensor(pauli_z(), identity(bsize))
    interaction1 = tensor(pauli_x(), annihilation(bsize))
    interaction2 = tensor(pauli_x(), creation(bsize))

    combined = cavity + Omega * tls + g * (interaction1 + interaction2)
    return combined