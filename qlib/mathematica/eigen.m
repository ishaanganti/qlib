BeginPackage["Eigensystems`"];

eigensystem::usage="Computes the eigensystem (eigenvalues and eigenstates) of a Hamiltonian.";
eigenvalues::usage="Computes the eigenvalues of a Hamiltonian.";
eigenstates::usage="Computes the eigenstates of a Hamiltonian.";

Begin["`Private`"];

eigensystem[H_]:=Module[{vals,vecs},
    {vals,vecs}=Eigensystem[H];
    Return[{vals,vecs}]
]

eigenvalues[H_]:=Module[{vals},
    vals=Eigenvalues[H];
    Return[vals]
]

eigenstates[H_]:=Module[{vecs},
    vecs=Eigenvectors[H];
    Return[vecs]
]

End[];
EndPackage[];