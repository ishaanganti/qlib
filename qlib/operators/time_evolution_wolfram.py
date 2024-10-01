import os
import numpy as np
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from qlib import *

script_dir = os.path.dirname(os.path.abspath(__file__))
math_dir = os.path.join(script_dir, '..', 'mathematica')

def time_evolve_wolfram(H, t, psi0=None):
    H = H.to_matrix().tolist()
    if(psi0):
        psi0 = psi0.to_vector().tolist()

    session = WolframLanguageSession()

    session.evaluate(wlexpr(f'SetDirectory["{math_dir}"]'))
    session.evaluate(wl.Get('time_evolution.m'))
    session.evaluate(wl.Needs('QuantumComputation`'))
    res = session.evaluate(
        wl.QuantumComputation.timeEvolve(H, t, psi0)
    )
    session.terminate()
    return ket(res)

def time_evolve_loop_wolfram(H, t0, tf, step, psi0, method="integrate"):
    H = H.to_matrix().tolist()
    psi0 = psi0.to_vector().tolist()
    session = WolframLanguageSession()

    session.evaluate(wlexpr(f'SetDirectory["{math_dir}"]'))
    session.evaluate(wl.Get('time_evolution.m'))
    session.evaluate(wl.Needs('QuantumComputation`'))
    res = 0
    if(method == "integrate"):
        res = session.evaluate(
            wl.QuantumComputation.numericalTimeEvolve(H, t0, tf, step, psi0)
        )
    elif(method == "exponential"):
        res = session.evaluate(
            wl.QuantumComputation.expTimeEvolve(H, t0, tf, step, psi0)
        )
    session.terminate()
    converted = np.array(res)
    n = len(converted)
    list_of_states = [None] * n

    for i in range(n):
        list_of_states[i] = ket(converted[i])
    return list_of_states

def time_evolve_loop_test(H, t0, tf, points, psi0):
    H = H.to_matrix().tolist()
    psi0 = psi0.to_vector().tolist()
    session = WolframLanguageSession()

    session.evaluate(wlexpr(f'SetDirectory["{math_dir}"]'))
    session.evaluate(wl.Get('time_evolution.m'))
    session.evaluate(wl.Needs('QuantumComputation`'))
    res = session.evaluate(
        wl.QuantumComputation.numericalTimeEvolveLoop(H, t0, tf, points, psi0)
    )
    session.terminate()
    converted = np.array(res)
    n = len(converted)
    list_of_states = [None] * n

    for i in range(n):
        list_of_states[i] = ket(converted[i])
    return list_of_states


def process_wolfram_result(str_arr):
    processed_string = str_arr.replace(']', '],').replace('[ ', '[').replace('  ', ', ')
    processed_string = processed_string.strip(', ')
    processed_array = eval(processed_string.replace('j', 'j'))  # ensure complex numbers are handled correctly
    processed_array_np = np.array(processed_array)

    return processed_array_np 