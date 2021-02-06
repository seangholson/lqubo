from perm_LQUBO.experiment_code.population_lqubo_experiment_class import Experiment
from perm_LQUBO.experiment_code.population_statistics_class import ExperimentStatistics
from utilities.objective_functions import QAPObjectiveFunction, TSPObjectiveFunction
import argparse

# sge id should go from 1-272

parser = argparse.ArgumentParser()
parser.add_argument("--sge_task_id",
                    type=int,
                    default=1)
args = parser.parse_args()
sge_task_id = args.sge_task_id

num_trials = 100
num_iters = 100


if sge_task_id <= 34:
    population_size = 1
    num_reads = 1000
    obj_index = sge_task_id - 1
elif 34 < sge_task_id <= 68:
    population_size = 1000
    num_reads = 1
    obj_index = sge_task_id - 35
elif 68 < sge_task_id <= 102:
    population_size = 500
    num_reads = 2
    obj_index = sge_task_id - 69
elif 102 < sge_task_id <= 136:
    population_size = 200
    num_reads = 5
    obj_index = sge_task_id - 103
elif 136 < sge_task_id <= 170:
    population_size = 1
    num_reads = 250
    obj_index = sge_task_id - 137
elif 170 < sge_task_id <= 204:
    population_size = 250
    num_reads = 1
    obj_index = sge_task_id - 171
elif 204 < sge_task_id <= 238:
    population_size = 125
    num_reads = 2
    obj_index = sge_task_id - 205
elif 238 < sge_task_id <= 272:
    population_size = 50
    num_reads = 5
    obj_index = sge_task_id - 239
else:
    obj_index = None
    num_reads = None
    population_size = None


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


if obj_index < 17:
    obj_fcn = QAPObjectiveFunction(dat_file=obj_array[obj_index] + '.dat',
                                   sln_file=obj_array[obj_index] + '.sln')

    if 'had' in obj_array[obj_index]:
        instance = 'had'
    else:
        instance = 'nug'

    size = obj_array[obj_index].replace(instance, '')

    experiment = Experiment(
        save_csv=True,
        population_size=population_size,
        objective_function=obj_fcn,
        experiment_type='iter_lim',
        size=size,
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

    size = obj_array[obj_index].replace(instance, '')

    experiment = Experiment(
        save_csv=True,
        population_size=population_size,
        objective_function=obj_fcn,
        experiment_type='iter_lim',
        size=size,
        sampler_type='Tabu',
        num_trials=num_trials,
        instance=instance,
        problem_type='TSP',
        num_iters=num_iters,
        num_reads=num_reads
    )
    run_experiment = experiment.run_experiment()
    stats = ExperimentStatistics(results_dict=run_experiment).run_stats()




