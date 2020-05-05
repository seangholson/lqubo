# LQUBO: Local QUBO Iterative Solver

The Local Quadratic Unconstrained Binary Optimization  package augments 
current-generation Noisy Intermediate Scale Quantum (NISQ) computers
such as the [D-Wave Systems](https://www.dwavesys.com/) quantum 
annealer.

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

## NOTE about the D-Wave Ocean SDK

The LQUBO is designed primarily for the D-Wave Systems Ocean SDK.  The
SDK comes packaged with classical, offline QUBO samplers that emulate
the results given by their quantum annealing hardware.  This is 
sufficient for algorithm prototyping.  

However, to use their actual quantum annealing hardware, please visit 
[their website](https://docs.ocean.dwavesys.com/en/latest/getting_started.html#gs) 
for  additional information.
