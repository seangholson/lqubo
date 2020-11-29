# LQUBO: Local QUBO Iterative Solver

The Local Quadratic Unconstrained Binary Optimization package augments 
current-generation Noisy Intermediate Scale Quantum (NISQ) computers
such as the [D-Wave Systems](https://www.dwavesys.com/) quantum 
annealer.

This public repository is part of an ongoing research effort between Sean Gholson, C. Carlo Fazioli, and 
Edward (Denny) Dahl in hybrid-quantum algorithms.

## Installation

The LQUBO package is in active pre-alpha development.  The recommended
procedure for use is to:

* Clone the git repository
* Create and activate a virtual environment
* Pip install the package

For example,

    $ git clone git@github.com:seangholson/lqubo.git
    $ python -m venv path/to/your/new/quantum_computing_venv
    $ source path/to/your/new/quantum_computing_venv/bin/activate
    $ pip install --upgrade pip
    $ pip install -e lqubo

This installation procedure will install the requirements identified in
the 
[setup.py](https://github.com/seangholson/lqubo/blob/master/setup.py)
file, which includes the 
[dwave-ocean-sdk](https://github.com/dwavesystems/dwave-ocean-sdk).  

## Verifying Your Install

The cloned repository has test scripts designed to verify that your 
installation was successful.  The scripts are located in the `examples/`
directory.  Run them to check that everything is working.  

## Project Overview and Additional Documentation

The Local QUBO algorithm is a hybrid-quantum algorithm with a scalable encoding that is capable of solving 
combinatorial optimization problems.  While traditional Ising Hamiltonian formulations of optimization problems have 
played a massive role in the application of quantum computing to real-world problems, their encodings tend to not scale 
well with problem size.  For example, a Quadratic Assignment Problem (QAP) of size n requires n<sup>2 </sup>variables 
and qubits to be solved via Ising Hamiltonian/ QUBO formulation.  Given the low qubit count of NISQ hardware, this 
encoding can be expensive for current quantum computing devices.


The LQUBO algorithm is an attempt to bypass these large encodings by iteratively picking a point in search space,
forming a (Local QUBO) approximation with a scalable encoding around that point, and optimizing for a new point with a
lower objective function value. As the LQUBO algorithm repeats this process, it will iteratively approach towards the 
optimal answer.

This repository is an open testbed for the LQUBO algorithm on various instances of QAP and TSP problems.  As we
benchmark this method, we are continuing to learn from our mistakes to improve the performance and scaling of the 
algorithm.

In this repository there are two main directories that explore the functionality of the LQUBO algorithm.  The first 
directory labeled `switch_network_LQUBO` contains the codebase for the switch newtork encoding of the LQUBO algorithm.
After many months of testing we have found that this particular encoding produces a high relative error due its 
exponential increase of redundant switches.  The results of this encoding can be found in the 
`switch_network_LQUBO/results` directory.

Since finding these critical issues with the switch network encoding, we have been able to formulate an LQUBO encoding 
using only permutations, removing the need for a switch network.  The code base for this encoding can be found in the 
`perm_LQUBO` directory.  This new encoding has resulted in a multi-factor reduction in relative error and requires n-1
qubits vs the O(n(log(n))) qubits from the switch network encoding.  This section of the codebase is still undergoing 
changes as we are continuing to explore this new formulation.


## NOTE: The D-Wave Ocean SDK

The LQUBO is designed primarily for the D-Wave Systems Ocean SDK.  The
SDK comes packaged with classical, offline QUBO samplers that emulate
the results given by their quantum annealing hardware.  This is 
sufficient for algorithm prototyping.  

However, to use their actual quantum annealing hardware, please visit 
[their website](https://docs.ocean.dwavesys.com/en/latest/getting_started.html#gs) 
for  additional information.
