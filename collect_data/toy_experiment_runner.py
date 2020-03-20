from utilities.objective_functions import QAPObjectiveFunction
from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics

"""
To get familiar with the experiment runner, this file is meant to mess around with the parameters that feed into the 
experiment runner.  Here you can tweak the objective function file...
"""

"""
Save csv is a boolean to decide if you want your experiment to be exported as a csv.  For our purposes, this should be
False until you are ready to run the full suite of problems on the D-Wave machine in collect_experiment_data.py.
"""

save_csv = False

"""
Currently Hadley - Rendl size 16 however you may load in any objective function in the data/dat dir
"""

obj_fcn = QAPObjectiveFunction(dat_file='had16.dat', sln_file='had16.sln')

"""
Experiment type allows you to switch between a time limit experiment ('time_lim') or a iteration limit experiment
('iter_lim')
"""

experiment_type = 'iter_lim'

"""
Num trials is the number of trials you want to execute in a single experiment
"""

num_trials = 10

"""
With the solver parameter you have a number of options to play with.  Though we have not talked about it as much,
incorporated in this repository is the option to create a Local QUBO (LQUBO) using the basis of the identity matrix
as slicing vectors, a random slice Local QUBO (Rand Slice LQUBO) which generates random vectors of arbitrary hamming
weight as basis vectors for the LQUBO, and a Hamming Distance Slice Local QUBO (HD Slice LQUBO) which generates random
vectors with a hamming weight of 2 (as it is now configured) as basis vectors for the LQUBO.

In addition to the type of LQUBO you have the option to use the sorting method and/ or add a penalty to the LQUBO based
on max hamming distance input.  These combinations of penalty and sorting are noted by WP (with penalty), WS (with 
sorting), WP and WS (with penalty and sorting).

To summarize, there are 12 possible solver strings to pick from:

'LQUBO'
'LQUBO WP'
'LQUBO WS'
'LQUBO WP and WS'
'Rand Slice LQUBO'
'Rand Slice LQUBO WS'
'Rand Slice LQUBO WP'
'Rand Slice LQUBO WP and WS'
'HD Slice LQUBO'
'HD Slice LQUBO WS'
'HD Slice LQUBO WP'
'HD Slice LQUBO WP and WS'

Note: if a solver doesn't have a penalty, set the max hamming distance parameter to 0
"""

solver = 'LQUBO WP'
max_hd = 11

"""
Sampler parameter allows you to choose one of 3 D-Wave samplers to minimize your QUBO:

'Tabu' is a classical tabu algorithm.  This is the fastest of the classical methods but there is not much variation in
its response so using the sorting method with this sampler doesn't have much of an effect on performance.

'SA' is a classical simulated annealing algorithm.  This algorithm takes the most time of the 3 samplers.

'QPU' is the option to solve QUBOs using D-Wave quantum annealing hardware.  This will work when your API token is 
configured.
"""
sampler = 'Tabu'

experiment = Experiment(save_csv=save_csv,
                        max_hd=max_hd,
                        objective_function=obj_fcn,
                        num_trials=num_trials,
                        solver=solver,
                        sampler_type=sampler,
                        experiment_type=experiment_type)
experiment_stats = ExperimentStatistics(experiment.run_experiment())
experiment_stats_result = experiment_stats.run_stats()

print('Percent error mean and standard deviation {}'.format(experiment_stats_result['percent_error']))
print('Frequency of obtaining optimal mean and standard deviation {}'.format(experiment_stats_result['obtain_optimal']))
print('Timing of code mean and standard deviation {}'.format(experiment_stats_result['timing_code']))
print('Number of iterations mean and standard deviation {}'.format(experiment_stats_result['number_of_iterations']))



