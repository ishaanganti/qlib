from qlib import oper
import numpy as np

def eigenvalues(op):
    """
    Returns the eigenvalues of the matrix wrapped in the oper class.
    """

    return np.linalg.eigvals(op.matrix)

def eigenstates(op):
    """
    Returns the eigenstates (eigenvectors) of the matrix wrapped in the oper class.
    """

    _, eigenvectors = np.linalg.eig(op.matrix)
    return eigenvectors

def eigensystem(op):
    """
    Returns a tuple of eigenvalues and eigenstates (eigenvectors) of the matrix wrapped in the oper class.
    """

    eigenvalues, eigenvectors = np.linalg.eig(op.to_matrix())
    return eigenvalues, eigenvectors