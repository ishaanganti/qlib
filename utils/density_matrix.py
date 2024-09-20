from qlib import bra, ket, oper
import numpy as np

def partial_trace(rho: oper, dims: list, subsystems_to_trace_out: list):
    """
    Compute the partial trace of a density matrix over specified subsystems.

    Parameters:
    rho (oper): The density matrix to trace over. 
    dims (list): A list of the dimensions of each subsystem in rho. 
    subsystems_to_trace_out (list): A list of indices indicating which subsystems to trace out.

    Returns: 
    oper: The reduced density matrix after tracing out the specified subsystems.
    """
    rho = rho.to_matrix()
    num_subsystems = len(dims) 

    # make sure all subsystems to be traced out exist
    if any(sub >= num_subsystems for sub in subsystems_to_trace_out):
        raise ValueError("Subsystem indices too large.")
    
    # duplicating to add rows and columns
    reshaped_rho = rho.reshape(dims * 2) 
    for subsystem in sorted(subsystems_to_trace_out, reverse=True): # reverse to keep indices constant
        reshaped_rho = np.trace(reshaped_rho, axis1=subsystem, axis2=subsystem+num_subsystems)
    
    # getting shape of resulting matrix
    remaining_dims = [dims[i] for i in range(num_subsystems) if i not in subsystems_to_trace_out]
    return oper(reshaped_rho.reshape(np.prod(remaining_dims), np.prod(remaining_dims)))
