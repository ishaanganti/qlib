import numpy as np
from qlib.operators import * 
from qlib import oper, qprint
from qlib.utils import tensor

def tc_hamiltonian(cavity_bsize: int, num_tls: int, Omega: float, g: float) -> oper:
    """
    Construct the TC model hamiltonian for a given number of TLS and basis size.

    Parameters:
    cavity_bsize: Basis size for the cavity mode (number of Fock states)
    num_tls: Number of two-level systems (TLS)
    Omega: Frequency of the TLS
    g: Coupling strength between the TLS and the cavity mode

    Returns:
    hamiltonian: Hamiltonian matrix representing the TC model
    """

    id_cavity = identity(cavity_bsize)
    cavity_hamiltonian = tensor(identity(2**num_tls), creation(cavity_bsize) * annihilation(cavity_bsize)) 
    tls_hamiltonian = tensor(zeros(2**num_tls), zeros(cavity_bsize))
    interaction_hamiltonian = tensor(zeros(2**num_tls), zeros(cavity_bsize))
    for i in range(num_tls):
        left_identities = identity(2**i)
        right_identities = identity(2**(num_tls - i - 1))
        curr_tls = pauli_z()
        tls_hamiltonian += Omega * tensor(left_identities, curr_tls, right_identities, id_cavity)
        curr_interact = (g / np.sqrt(num_tls)) * (tensor(left_identities, pauli_m(), right_identities, creation(cavity_bsize)) + tensor(left_identities, pauli_p(), right_identities, annihilation(cavity_bsize)))
        interaction_hamiltonian += curr_interact 

    hamiltonian = cavity_hamiltonian + 0.5 * tls_hamiltonian + interaction_hamiltonian
    return hamiltonian

def reduced_tc_hamiltonian(cavity_bsize: int, num_tls: int, Omega: float, g: float) -> oper:
    """
    Construct the reduced TC model hamiltonian via the
    angular momentum basis for a given number of TLS and basis size.

    Parameters:
    cavity_bsize: Basis size for the cavity mode (number of Fock states)
    num_tls: Number of two-level systems (TLS)
    Omega: Frequency of the TLS
    g: Coupling strength between the TLS and the cavity mode

    Returns:
    hamiltonian: Hamiltonian matrix representing the reduced TC model
    """

    id_tls = identity(int(num_tls + 1))
    id_cavity = identity(cavity_bsize)
    tls_hamiltonian = Omega * tensor(j_z(num_tls), id_cavity)
    cavity_hamiltonian = tensor(id_tls, creation(cavity_bsize) * annihilation(cavity_bsize))
    interaction_hamiltonian = (g / np.sqrt(num_tls)) * (tensor(j_p(num_tls), annihilation(cavity_bsize)) + tensor(j_m(num_tls), creation(cavity_bsize)))

    hamiltonian = tls_hamiltonian + cavity_hamiltonian + interaction_hamiltonian
    return hamiltonian 