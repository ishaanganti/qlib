from qlib.quantum_objects import oper, bra, ket
from typing import Union
import numpy as np

def commutator(A: oper, B: oper) -> oper:
    if isinstance(A, oper) and isinstance(B, oper):
        return A * B - B * A
    raise TypeError("Commutator can only be computed with two oper objects")

def tensor(*args: Union[oper, ket, bra]) -> Union[oper, ket, bra]:
    """
    Compute the tensor product of multiple quantum objects.

    Parameters:
    args (oper, ket, or bra): Quantum objects to tensor.

    Returns:
    oper, ket, or bra: The tensor product of the quantum objects.
    """
    if not args:
        raise ValueError("At least one input is required")

    result = args[0]
    for obj in args[1:]:
        if isinstance(result, oper) and isinstance(obj, oper):
            result = oper(np.kron(result.to_matrix(), obj.to_matrix()))
        elif isinstance(result, ket) and isinstance(obj, ket):
            result = ket(np.kron(result.to_vector(), obj.to_vector()))
        elif isinstance(result, bra) and isinstance(obj, bra):
            result = bra(np.kron(result.to_vector(), obj.to_vector()))
        else:
            raise TypeError("Cannot tensor objects of these types")
    
    return result

def tensor2(op1, op2):
    """
    Compute the tensor product of two quantum objects.
    
    Parameters:
    op1 (oper, ket, or bra): The first quantum object.
    op2 (oper, ket, or bra): The second quantum object.
    
    Returns:
    oper, ket, or bra: The tensor product of the two quantum objects.
    """
    if isinstance(op1, oper) and isinstance(op2, oper):
        result = np.kron(op1.to_matrix(), op2.to_matrix())
        return oper(result)
    elif isinstance(op1, ket) and isinstance(op2, ket):
        result = np.kron(op1.to_vector(), op2.to_vector())
        return ket(result)
    elif isinstance(op1, bra) and isinstance(op2, bra):
        result = np.kron(op1.to_vector(), op2.to_vector())
        return bra(result)
    else:
        raise TypeError("Cannot tensor objects of these types")