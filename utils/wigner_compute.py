from qlib import bra, ket, oper
import numpy as np
from scipy.special import genlaguerre
from scipy.special import factorial

def compute_wigner(rho: oper | ket, xvec: list, yvec: list, g=np.sqrt(2), method = "laguerre"):
    """
    Compute the Wigner function of a given density matrix over a given mesh. 
    
    Parameters:
    rho (oper, ket): The state. 
    xvec (list): An array with all the x values to evaluate the wigner function at. 
    yvec (list): An array with all the y values to evaluate the wigner function at. 
    g (float): A scaling constant for the phase space coordinates. 
    method (String): The method by which to evaluate the wigner function.
    
    returns:    
    w (list[list]): a 2d array with the wigner function evaluations at each (x, p) value. 
    xvec (list): an array with all the x values the wigner function was evaluated at. 
    yvec (list): an array with all the y values the wigner function was evaluated at. 
    """
    if(method == "laguerre"):
        return wigner_laguerre(rho, xvec, yvec, g=np.sqrt(2))
    else:
        return None # needs to be implemented

def wigner_laguerre(rho: oper | ket, xvec: list, yvec: list, g=np.sqrt(2)):
    """
    Compute the Wigner function of a given density matrix via the
    Laguerre polynomial formula (see H.J. Groenewold, 1946). This
    method is fast and especially good for sparser systems. Notably, 
    this method lacks covergence issues.    
    
    returns:    
    w (list[list]): a 2d array with the wigner function evaluations at each (x, p) value. 
    xvec (list): an array with all the x values the wigner function was evaluated at. 
    yvec (list): an array with all the y values the wigner function was evaluated at. 
    """
    # conversion to density matrix 
    if isinstance(rho, ket):
        rho = rho.to_density_matrix().to_matrix()
    else:
        rho = rho.to_matrix()
    
    M = rho.shape[0]
    X, Y = np.meshgrid(xvec, yvec)
    A = 0.5 * g * (X + 1j * Y)
    B = 4 * np.abs(A)**2
    W = np.zeros_like(A, dtype=complex)
    
    for m in range(M):
        for n in range(M):
            if rho[m, n] != 0:
                coeff = rho[m, n] * (-1)**(m)
                if m <= n:
                    factor = (2 * A)**(n - m) * np.sqrt(factorial(m) / factorial(n))
                    laguerre = genlaguerre(m, n - m)(B)
                else:
                    factor = (2 * np.conj(A))**(m - n) * np.sqrt(factorial(n) / factorial(m))
                    laguerre = genlaguerre(n, m - n)(B)
                W += coeff * factor * laguerre

    W *= np.exp(-B / 2) / np.pi
    return np.real(W) * (g**2 / 2), xvec, yvec