from experiment_code.perm_experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
from utilities.objective_functions import QAPObjectiveFunction, TSPObjectiveFunction
import argparse

# sge id should go from 1-34

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
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20
]


#  Decode the sge_task_id into index for solver and obj fcn array
obj_index = sge_task_id - 1

if obj_index < 17:
    obj_fcn = QAPObjectiveFunction(dat_file=obj_array[obj_index] + '.dat',
                                   sln_file=obj_array[obj_index] + '.sln')

    if 'had' in obj_array[obj_index]:
        instance = 'had'
    else:
        instance = 'nug'

    experiment = Experiment(
        save_csv=True,
        objective_function=obj_fcn,
        experiment_type='iter_lim',
        sampler_type='Tabu',
        num_trials=num_trials,
        instance=instance,
        problem_type='QAP',
        num_iters=num_iters,
        num_reads=num_reads
    )
    run_experiment = experiment.run_experiment()
    stats = ExperimentStatistics(results_dict=run_experiment).run_stats()
else:
    obj_fcn = TSPObjectiveFunction(num_points=obj_array[obj_index])
    instance = 'tsp'

    experiment = Experiment(
        save_csv=True,
        objective_function=obj_fcn,
        experiment_type='iter_lim',
        sampler_type='Tabu',
        num_trials=num_trials,
        instance=instance,
        problem_type='TSP',
        num_iters=num_iters,
        num_reads=num_reads
    )
    run_experiment = experiment.run_experiment()
    stats = ExperimentStatistics(results_dict=run_experiment).run_stats()




