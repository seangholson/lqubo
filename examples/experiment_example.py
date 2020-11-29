# Project locals:
from experiment_code.switch_network_experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
from utilities.objective_functions import QAPObjectiveFunction, TSPObjectiveFunction


# The objective function to test:
qap_obj = QAPObjectiveFunction(dat_file='had8.dat',
                               sln_file='had8.sln')
tsp_obj = TSPObjectiveFunction(num_points=8)

experiment_config = {
    'save_csv': False,
    'instance': 'tsp',
    'experiment_type': 'iter_lim',
    'num_trials': 2,
    'solver': 'LQUBO',
    'problem_type': 'tsp',
    'max_hd': 11,
    'sampler_type': 'Tabu',
    'objective_function': tsp_obj,
    'num_reads': 10,
    'num_iters': 30
}

test_experiment = Experiment(**experiment_config)
experiment_data = test_experiment.run_experiment()
experiment_stats = ExperimentStatistics(experiment_data)
experiment_stats_result = experiment_stats.run_stats()

pct_err = experiment_stats_result['percent_error']
freq_opt = experiment_stats_result['obtain_optimal']
timing = experiment_stats_result['timing_code']
n_iters = experiment_stats_result['number_of_iterations']

print('Percent error mean and standard deviation:')
print('\t{}'.format(pct_err))
print('Timing of code mean and standard deviation:')
print('\t{}'.format(timing))
print('Number of iterations mean and standard deviation:')
print('\t{}'.format(n_iters))
