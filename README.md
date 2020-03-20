###LQUBO Iterative Solver Guide
In this readme we will address the ideas necessary to run a large experiments of the Local QUBO iterative solver using 
D-Wave quantum annealing

#Necessary imports to run experiments
To run the LQUBO iterative solver the following need to be installed in your virtual environment:

-numpy
-pandas
-dwave-ocean-sdk

Note: To run LQUBO iterative solver off of a D-Wave machine, install the dwave-ocean-sdk and use the command 'dwave 
config create' to enter in your API Token.

#Running Toy Problem
In the collect_data directory there is a python file named toy_experiment_runner.py that will allow you to play with
the parameters of the LQUBO experiment runner.  The code is commented and indicate the types and meaning of each 
parameter.

**IMPORTANT:** The toy experiment runner as well as a handful of other files in this repo require you to edit the 
configuration of the file so that the working directory is the main QAP-Quantum-Computing directory.  This allows the
data/dat files to be imported properly.

#Running Collect Experiment Data file
Under the collect_data dir is a file named collect_experiment_data.py.  This file allows you to run experiments on the 
suite of qap and tsp problems.  To collect an official set of data with the D-Wave machine you must configure your API
Token, change the working directory to the main QAP-Quantum-Computing directory, and turn the save_csv boolean to True.

#Additional Files to mess with
In the quality_of_LQUBO_and_methods dir there are 3 files to mess around with. finding_max_hd.py is a class object that 
can be run from the command line.  For a given LQUBO type with a penalty, this object will return a dictionary of arrays 
that specify what the best max_hd value is for a given instance and size of qap or tsp.  With those values precomputed,
they can be fed into comparison_of_methods.py which will compare the percent error of any selected solvers.  Lastly,
approx_goodness_qap.py is another class object that can be run from the command line.  For a specified objective 
function and hamming dist, it will produce the scatter plots of the LQUBO change in objective vs actual change in 
objective using the plot_goodness function.  Furthermore, using plot_r_squared function on a specified objective 
function will plot the R squared of the scatter plots as a function of hamming distance.



