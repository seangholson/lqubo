# Project locals:
from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
from utilities.objective_functions import QAPObjectiveFunction


# The objective function to test:
obj_f = QAPObjectiveFunction(dat_file='had16.dat', 
                               sln_file='had16.sln')

experiment_config = {
    'save_csv': False,
    'experiment_type': 'iter_lim',
    'num_trials': 2,
    'solver': 'LQUBO WP',
    'max_hd': 11,
    'sampler_type': 'Tabu',
    'objective_function': obj_f,
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
print('Frequency of obtaining optimal mean and standard deviation:')
print('\t{}'.format(freq_opt))
print('Timing of code mean and standard deviation:')
print('\t{}'.format(timing))
print('Number of iterations mean and standard deviation:')
print('\t{}'.format(n_iters))
