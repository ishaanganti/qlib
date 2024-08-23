import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix, spmatrix
from scipy.sparse.linalg import LinearOperator, expm_multiply, aslinearoperator
from qlib.quantum_objects import oper, ket, bra

def time_evolve(H, t, v=None, method="pade"):
    """
    Evolve the system using the specified method.
    
    Parameters:
    H (oper): The Hamiltonian operator.
    t (float): The time duration for evolution.
    v (ket, optional): The initial state vector for the Krylov method.
    method (str): The method to use for computing the matrix exponential ('pade' or 'krylov').
    
    Returns:
    ket or oper: The evolved state if initial state is provided, otherwise the time evolution operator.
    """
    if method not in ["pade", "krylov"]:
        print("Not a valid method. Valid methods include 'krylov' and 'pade'.")
        return

    if method == "pade":
        U = pade_exponential(H, t)
        if v is not None:
            return ket(U.dot(v.to_vector()))
        return oper(U)
    
    if method == "krylov":
        if v is None:
            raise ValueError("Initial state must be provided for Krylov method.")
        return krylov_exponential(H, t, v) 

def krylov_exponential(H, t, v, tol=1e-10, max_iter=100):
    H_mat = H.to_matrix()
    if not isinstance(H_mat, spmatrix):
        H_mat = csr_matrix(H_mat)
    H_oper = aslinearoperator(H_mat)
    v_vec = v.to_vector()
    
    krylov_expm = expm_multiply(-1j * H_oper * t, v_vec)
    return ket(krylov_expm)

def pade_exponential(H, t):
    """
    Computes time evolution operator via Pade approximant. 
    
    Parameters:
    H (oper): The Hamiltonian to be exponentiated.
    t (double): The time at which the time evolution is performed until. 

    Returns:
    The time evolution operator for the given Hamiltonian and time as 
    an oper object.
    """
    return expm(-1j * H.to_matrix() * t)