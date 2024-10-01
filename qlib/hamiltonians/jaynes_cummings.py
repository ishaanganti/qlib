import numpy as np
from qlib.operators import pauli_z, pauli_m, pauli_p, creation, annihilation, identity
from qlib.utils import tensor

def jc_hamiltonian(bsize, Omega, g):

    cavity = tensor(identity(2), creation(bsize) * annihilation(bsize))
    tls = (0.5) * tensor(pauli_z(), identity(bsize))
    interaction1 = tensor(pauli_p(), annihilation(bsize))
    interaction2 = tensor(pauli_m(), creation(bsize))

    combined = cavity + Omega * tls + g * (interaction1 + interaction2)
    return combined