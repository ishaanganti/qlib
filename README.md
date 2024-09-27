# qlib

A simple Python library for quantum mechanics simulations. Features include standard operator, bra, and ket manipulation, easy-to-use visualization tools, and frequently used Hamiltonians built in. All expressions are nondimensionalized.

## Basic Syntax

The core objects in the library are the following:
1. oper
2. bra
3. ket
They are constructed given an array (2d for opers) as input, and they can be combined with the standard arithmetic operators. For example, the following code

```
excitation = ket([1, 0])
null_state = ket([0, 0])
pauli_minus_op = pauli_m()
qprint(pauli_minus_op)
qprint(pauli_minus_op * (excitation + null_state))
```

Prints the following result to terminal
```
[[0.000+0.000j, 0.000+0.000j];
 [1.000+0.000j, 0.000+0.000j]]
[0.000+0.000j; 1.000+0.000j]
```

Tensor/Kronecker products are perfomed with the 'tensor' function:
```
excitation = ket([1, 0])
double_excitation = tensor(excitation, excitation)
qprint(double_excitation)
```
The output:
```
[1.000+0.000j; 0.000+0.000j; 0.000+0.000j; 0.000+0.000j]
```

## Time Propagation
Time propagation of a state given a Hamiltonian and a single time t is calculated via the time evolution operator matrix exponential. We support
time-dependent Hamiltonian usage; check the RWA example in the examples folder for usage samples. For propagation of a state over a time range, we support three methods: numerical integration, repeated usage of the time evolution operator, and eigenbasis expansion. Note that numerical integration is the most general method and is the only method that works with time-dependent Hamiltonians. However, for closed systems with time-independent Hamiltonians, the eigenexpansion approach is faster most of the time. Speedups of up to 75x are easily achieved over numerical solvers when this approach is used for systems with Hilbert space dimension less than ~5000 and time range greater than 100; benchmarks comparing these results to QuTiP out soon. 


### Sample
To evolve an excited state to some arbitrary time according to the Pauli Z matrix, we could write
```
t = 10
psi0 = state(2, 0)
psif = time_evolve(pauli_z(), t, psi0)
qprint(psif)
```
This yields the result:
```
[-0.839+0.544j; 0.000+0.000j]
```

## Visualization Support
Currently, the main visualization tools are expectation value plots, energy schemas, and Wigner plots (both plots and animations). Currently, Wigner functions are calculated efficiently using the Laguerre polynomial expansion in the Fock basis. Sample usage all tools can be found in the 'examples' directory. Attached is a sample expectation value plot for the Jaynes-Cummings model:

![Alt text](https://i.imgur.com/bYZYXxU.png)

Wigner plot animations look pretty nice, too. And, they can be rotated for viewing from different angles. Here's a Wignor plot for the Dicke model with 4 TLS and strong coupling: 

https://github.com/user-attachments/assets/35c16153-e1da-47f1-acb5-e41e2639afe4
