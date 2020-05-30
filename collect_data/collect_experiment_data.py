from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
from utilities.objective_functions import QAPObjectiveFunction
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("--sge_task_id",
                    type=int,
                    default=1)
args = parser.parse_args()
sge_task_id = args.sge_task_id


num_trials = 100
num_iters = 100
num_reads = 250

obj_array = [
    'had4',
    'had6',
    'had8',
    'had10',
    'had12',
    'had14',
    'had16',
    'had18',
    'had20',
    'nug12',
    'nug14',
    'nug15',
    'nug16a',
    'nug16b',
    'nug17',
    'nug18',
    'nug20',
]

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

max_hd_array = {'had': [4.92, 5.87, 7.92, 8.44, 9.75, 9.77, 10.52, 12.12, 11.7],
                'nug': [8, 8.6, 8.94, 9.92, 10.36, 11.15, 11.21, 11.61]}

#  Decode the sge_task_id into index for solver and obj fcn array
obj_index = np.mod(sge_task_id, len(obj_array))
solver_index = np.mod(sge_task_id, len(solver_array))

obj_fcn = QAPObjectiveFunction(dat_file=obj_array[obj_index] + '.dat',
                               sln_file=obj_array[obj_index] + '.sln')
solver = solver_array[solver_index]

if 'had' in obj_array[obj_index]:
    instance = 'had'
    size = obj_array[obj_index].replace(instance, '')
    if 'WP' in solver:
        max_hd = max_hd_array[instance][obj_index]
    else:
        max_hd = 0
else:
    instance = 'nug'
    size = obj_array[obj_index].replace(instance, '')
    if 'WP' in solver:
        max_hd = max_hd_array[instance][obj_index - 9]
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
    size=size,
    instance=instance,
    problem_type='QAP',
    num_iters=num_iters,
    num_reads=num_reads
)
run_experiment = experiment.run_experiment()
stats = ExperimentStatistics(results_dict=run_experiment).run_stats()




