from experiment_code.switch_network_experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
from utilities.objective_functions import TSPObjectiveFunction
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("--sge_task_id",
                    type=int,
                    default=1)
args = parser.parse_args()
sge_task_id = args.sge_task_id


num_trials = 250
num_iters = 100
num_reads = 250

obj_array = list(range(4, 21))

solver_array = [
    'LQUBO',
    'LQUBO WP',
    'LQUBO WS',
    'LQUBO WP and WS',
    'Rand Slice LQUBO',
    'Rand Slice LQUBO WS',
    'HD Slice LQUBO',
    'HD Slice LQUBO WS'
]

max_hd_array = [4.53, 4.79, 4.58, 4.56, 5.09, 5.84, 6.35, 6.86, 7.46, 8.39, 9.14, 9.28, 8.87, 15.14, 15.38, 15.51,
                14.67]

#  Decode the sge_task_id into index for solver and obj fcn array
obj_index = np.mod(sge_task_id, len(obj_array))
solver_index = np.mod(sge_task_id, len(solver_array))

obj_fcn = TSPObjectiveFunction(num_points=obj_array[obj_index])
solver = solver_array[solver_index]

if 'WP' in solver:
    max_hd = max_hd_array[obj_index]
else:
    max_hd = 0


experiment = Experiment(
    save_csv=True,
    max_hd=max_hd,
    solver=solver,
    objective_function=obj_fcn,
    experiment_type='iter_lim',
    sampler_type='Tabu',
    num_trials=num_trials,
    instance='tsp',
    problem_type='tsp',
    num_iters=num_iters,
    num_reads=num_reads
)
run_experiment = experiment.run_experiment()
stats = ExperimentStatistics(results_dict=run_experiment).run_stats()





