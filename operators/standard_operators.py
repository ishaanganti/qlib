import numpy as np
from qlib.quantum_objects import oper, ket, bra

def zeros(N: int) -> oper:
    """
    Create an N x N zero operator.

    Paramters: 
    N (int): The dimension of the zero matrix. 

    Returns:
    oper: The zero operator as an oper object.
    """
    return oper(np.zeros((N, N), dtype=complex))

def identity(N: int) -> oper:
    """
    Create an N x N identity operator.

    Parameters:
    N (int): The dimension of the identity matrix.

    Returns:
    oper: The identity operator as an oper object.
    """
    return oper(np.eye(N, dtype=complex))

def projection(N: ket) -> oper:
    """
    Create a projection operator for the given ket or bra.

    Parameters:
    N (ket): The ket vector.

    Returns:
    oper: The projection operator as an oper object.
    """
    if isinstance(N, ket):
        return N * N.dag()
    raise TypeError("Projection can only be computed for ket objects.")

def parity(N: int) -> oper:
    """
    Construct the parity operator for a finite-dimensional Hilbert space.

    Parameters:
    N (int): The dimension of the Hilbert space.

    Returns:
    oper: The parity operator as a qlib operator object.
    """
    return oper(np.diag([(-1)**n for n in range(N)]))
