from qlib import oper
import numpy as np
from scipy.linalg import eigh, eigvals


def eigenvalues(op):
    """
    Returns the eigenvalues of the matrix wrapped in the oper class.
    """

    return eigvals(op.to_matrix())

def eigenstates(op):
    """
    Returns the eigenstates (eigenvectors) of the matrix wrapped in the oper class.
    """

    _, eigenvectors = eigh(op.to_matrix())
    return eigenvectors

def eigensystem(op):
    """
    Returns a tuple of eigenvalues and eigenstates (eigenvectors) of the matrix wrapped in the oper class.
    """
    eigenvalues, eigenvectors = eigh(op.to_matrix())
    return eigenvalues, eigenvectors