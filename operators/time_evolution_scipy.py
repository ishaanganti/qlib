from numpy import arange
from scipy.linalg import expm
from scipy.sparse import csr_matrix, csc_matrix
from scipy.integrate import solve_ivp, ode
from scipy.sparse.linalg import expm_multiply
from qlib.quantum_objects import oper, ket, bra

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

def time_evolve_loop(H: oper, t0: float, tf: float, step: float, psi0: ket, method="integrate"):
    """
    Time evolution over a range using SciPy.
    H: Hamiltonian
    t0: initial time
    tf: final time
    step: step size
    psi0: initial state vector (numpy array)
    method: 'integrate' or 'exponential'
    """
    # sparse matrix representation
    H = csr_matrix(H.to_matrix())
    psi0 = psi0.to_vector()
    times = arange(t0, tf, step)

    if method == "integrate":
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

    elif method == "exponential":
        evolved_states = [expm_multiply(-1j * H * t, psi0) for t in times]
        return evolved_states