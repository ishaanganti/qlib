from qlib.quantum_objects import ket, bra, oper
import numpy as np
from scipy.special import factorial


def state(dim, offset):
    arr = [0 for i in range(dim)]
    arr[offset] = 1
    return ket(arr)

def coherent(dim, alpha):
    coeffs = [np.exp(-0.5 * np.abs(alpha)**2) * (alpha**n) / np.sqrt(factorial(n)) for n in range(dim)]
    return ket(coeffs)