import numpy as np
from qlib.quantum_objects import oper, ket, bra

def creation(N: int) -> oper:
    """
    Create an N x N creation operator.

    Parameters:
    N (int): The dimension of the Hilbert space.

    Returns:
    oper: The creation operator as an oper object.
    """
    creation_matrix = np.zeros((N, N), dtype=complex)
    for i in range(1, N):
        creation_matrix[i, i-1] = np.sqrt(i)
    return oper(creation_matrix)

def annihilation(N: int) -> oper:
    """
    Create an N x N annihilation operator.

    Parameters:
    N (int): The dimension of the Hilbert space.

    Returns:
    oper: The annihilation operator as an oper object.
    """
    annihilation_matrix = np.zeros((N, N), dtype=complex)
    for i in range(1, N):
        annihilation_matrix[i-1, i] = np.sqrt(i)
    return oper(annihilation_matrix)