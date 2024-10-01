import numpy
from qlib.quantum_objects import oper

def pauli_x():
    return oper([[0, 1], [1, 0]])

def pauli_y():
    return oper([[0, -1j], [1j, 0]])

def pauli_z():
    return oper([[1, 0], [0, -1]])

def pauli_p():
    return oper([[0, 1], [0, 0]])

def pauli_m():
    return oper([[0, 0], [1, 0]])