import numpy as np
from qlib.quantum_objects import oper, ket, bra

def j_p(num_tls: int) -> oper:
    """
    Construct the J+ (raising) operator for a given number of TLS.
    """
    j = num_tls / 2  
    dim = int(2 * j + 1)  
    j_plus_matrix = np.zeros((dim, dim), dtype=complex)
    
    for m in np.arange(-j, j, 1):  
        row = int(j + m)
        col = int(j + m + 1)
        j_plus_matrix[row, col] = np.sqrt(j * (j + 1) - m * (m + 1))
    
    return oper(j_plus_matrix)

def j_m(num_tls: int) -> oper:
    """
    Construct the J- (lowering) operator for a given number of TLS.
    """
    j = num_tls / 2  
    dim = int(2 * j + 1)  
    j_minus_matrix = np.zeros((dim, dim), dtype=complex)
    
    for m in np.arange(-j + 1, j + 1, 1):  
        row = int(j + m)
        col = int(j + m - 1)
        j_minus_matrix[row, col] = np.sqrt(j * (j + 1) - m * (m - 1))
    
    return oper(j_minus_matrix)

def j_z(num_tls: int) -> oper:
    """
    Construct the Jz operator for a given number of TLS.
    """
    j = num_tls / 2  
    dim = int(2 * j + 1)  
    j_z_matrix = np.zeros((dim, dim), dtype=complex)
    
    for m in np.arange(j, -j - 1, -1): 
        row = int(j - m)
        j_z_matrix[row, row] = m
    
    return oper(j_z_matrix)