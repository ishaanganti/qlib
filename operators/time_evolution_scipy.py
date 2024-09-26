##########################################################
# Page Structure: 
# 1. Main logic/decision-making function
# 2. Integration solver functions
# 3. Exponential solver functions
#     a. This includes extra functions for parallelization
# 4. Eigenexpansion based solver (best approach for closed 
#    systems w/ time-independent hamiltonians.)

### IMPORTS ###
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix, csc_matrix, coo_array, coo_matrix, bsr_matrix
from scipy.integrate import solve_ivp, ode
from scipy.sparse.linalg import expm_multiply
from qlib.quantum_objects import oper, ket, bra
from qlib.solvers import eigensystem
from multiprocessing import Pool

### SECTION 1 ###
def time_evolve(H: oper, t: float, psi0=None):
    """
    Time evolution using matrix exponential.
    H: Hamiltonian (numpy array)
    t: time (float)
    psi0: initial state vector (numpy array)
    """
    # sparse matrix representation
    H = csr_matrix(H.to_matrix())
    if psi0 is None:
        # time evolution operator U = exp(-iHt)
        U = expm(-1j * H * t)
        return oper(U)
    else:
        evolved_state = expm_multiply(-1j * H * t, psi0.to_vector())
        return ket(evolved_state)

def time_evolve_loop(H: oper, t0: float, tf: float, step: float, psi0: ket, method: str = "integrate", parallelize: bool=False, tol: float = 0.01):
    """
    Time evolution over a range using SciPy.
    H: Hamiltonian
    t0: initial time
    tf: final time
    step: step size
    psi0: initial state vector (numpy array)
    method: 'eigenexpand', 'integrate', or 'exponential'
    """
    # sparse matrix representation
    if(not callable(H)):
        H_sparse = csr_matrix(H.to_matrix())
    psi0 = psi0.to_vector()
    times = np.arange(t0, tf, step)

    if method == "integrate" and not parallelize:
        return evolve_chunk_integrate(H_sparse, t0, tf, step, psi0)
    # this is currently still too slow. 
    elif method == "exponential":
        if parallelize:
            return evolve_chunk_exponential_parallel(H_sparse, times, step, psi0)
        else:
            return evolve_chunk_exponential(H_sparse, times, step, psi0)
    elif method == "eigenexpand":
        if parallelize:
            # not implemented yet
            print("This method hasn't been implemented yet!")
        else:
            return eigenreduce_solve(H, psi0, t0, tf, step, tol)


### SECTION 2 ###
def evolve_chunk_integrate(H: oper, t0: float, tf: float, step: float, psi0: ket):
    if callable(H):
        def sch_eq(t, psi):
            H_t_sparse = csr_matrix(H(t).to_matrix())  
            return -1j * H_t_sparse.dot(psi)
    else:
        def sch_eq(t, psi):
            return -1j * H.dot(psi)

    # benchmarking suggests zvode is good for at least dicke-like models.
    solver = ode(sch_eq)
    solver.set_integrator('zvode')
    solver.set_initial_value(psi0, t0)

    evolved_states = []
    while solver.successful() and solver.t < tf:
        solver.integrate(solver.t + step)
        evolved_states.append(ket(solver.y))  

    return evolved_states

### SECTION 3 ###
def evolve_chunk_exponential(H: oper, times, step: float, psi0: ket):
    """
    Individual matrix exponential steps for the sequential execution. 
    """
    evolved_states = [ket(expm_multiply(-1j * H * t, psi0)) for t in times]
    return evolved_states 

def compute_exponential_evolution(args):
    """
    Helper for parallel evolution of the state using the matrix exponential method. 
    """
    H, t, psi0 = args
    return ket(expm_multiply(-1j * H * t, psi0))

def evolve_chunk_exponential_parallel(H, times, step: float, psi0):
    """
    Parallel evolution of the state using the matrix exponential method for each time step.
    """
    args = [(H, t, psi0) for t in times]
    
    with Pool() as pool:
        evolved_states = pool.map(compute_exponential_evolution, args)
    return evolved_states

def eigenreduce_solve(H, psi0, t0, tf, grain, threshold=0.01):
    eigv, eigs = eigensystem(H)
    projections = np.array([np.vdot(psi0, eigs[:,i]) for i in range(len(eigs))])
    significant_indices = np.where(np.abs(projections) > threshold)[0]

    significant_eigenvalues = eigv[significant_indices]
    significant_eigenvectors = eigs[:, significant_indices]
    significant_projections = projections[significant_indices]

    times = np.arange(t0, tf, grain)
    phases = np.exp(-1j * np.outer(significant_eigenvalues, times))
    states_matrix = significant_eigenvectors @ (significant_projections[:, None] * phases)
    states = [ket(state) for state in states_matrix.T]

    return states
