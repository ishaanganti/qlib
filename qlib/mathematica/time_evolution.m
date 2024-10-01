BeginPackage["QuantumComputation`"];

timeEvolve::usage = "Time evolution operator assuming a time-independent Hamiltonian."
expTimeEvolve::usage = "Repeated use of time evolution operator (matrix exponential) assuming a time-independent Hamiltonian."
numericalTimeEvolve::usage = "Usage of NDSolveValue to numerically integrate Schrodinger equation."

Begin["`Private`"];

timeEvolve[H_, t_, psi0_:Null] := Module[{},
    If[psi0 === Null, Return[MatrixExp[-I H t]], Return[MatrixExp[-I H t, psi0]]]
]

numericalTimeEvolve[H_, t0_, tf_, step_, psi0_] := Module[{tRange, schEq, initCond},
    tRange = Range[t0, tf, step];
    schEq = D[\[Psi][t], t] == -I H.\[Psi][t];
    initCond = \[Psi][0] == Normal[psi0];
    \[Psi]sol = NDSolveValue[{schEq, initCond}, \[Psi], {t, t0, tf}, MaxStepSize -> step];
    Return[ArrayFlatten[Table[\[Psi]sol[time], {time, tRange}]]]
]

expTimeEvolve[H_, t0_, tf_, step_, psi0_:Null] := Module[{times, evolvedStates},
    times = Range[t0, tf, step];
    If[psi0 === Null, 
        evolvedStates = Table[MatrixExp[-I SparseArray[H] t], {t, times}], 
        evolvedStates = Table[MatrixExp[-I SparseArray[H] t].psi0, {t, times}]
    ];
    Return[ArrayFlatten[{{evolvedStates}}]]
]


End[];
EndPackage[];