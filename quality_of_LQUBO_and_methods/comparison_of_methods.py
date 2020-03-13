from utilities.objective_functions import QAPObjectiveFunction
from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
import matplotlib.pyplot as plt

had_domain = ['4', '6', '8', '10', '12', '14', '16']

had_of = []
num_trials = 10

max_hd_list = []


def select_max_hd(solver_str, index):
    global max_hd_list
    if solver_str == 'LQUBO WP':
        max_hd_list = [5, 6, 8, 9, 10, 11, 11]
    elif solver_str == 'HD Slice LQUBO WP':
        max_hd_list = [4, 4, 5, 6, 6, 7, 7]
    elif solver_str == 'LQUBO' or 'HD Slice LQUBO':
        max_hd_list = [0, 0, 0, 0, 0, 0, 0]
    return max_hd_list[index]


for elt in had_domain:
    had_of.append(QAPObjectiveFunction(dat_file='had' + elt + '.dat', sln_file='had' + elt + '.sln'))

solvers = ['LQUBO', 'LQUBO WP', 'HD Slice LQUBO', 'HD Slice LQUBO WP']
data = {'LQUBO': [[], []], 'LQUBO WP': [[], []], 'HD Slice LQUBO': [[], []], 'HD Slice LQUBO WP': [[], []]}

for solver in solvers:
    for of_index in range(len(had_of)):
        run_experiment = Experiment(objective_function=had_of[of_index],
                                    num_trials=num_trials,
                                    solver=solver,
                                    sampler_type='Tabu',
                                    max_hd=select_max_hd(solver, of_index),
                                    experiment_type='iteration limit')
        experiment_stats = ExperimentStatistics(results_dict=run_experiment.run_experiment())
        experiment_stats_results = experiment_stats.run_stats()

        data[solver][0].append(experiment_stats_results['percent_error'][0])
        data[solver][1].append(experiment_stats_results['percent_error'][1])

plt.scatter(had_domain, data['LQUBO'][0])
plt.errorbar(had_domain, data['LQUBO'][0], yerr=data['LQUBO'][1], label='LQUBO')
plt.scatter(had_domain, data['LQUBO WP'][0])
plt.errorbar(had_domain, data['LQUBO WP'][0], yerr=data['LQUBO WP'][1], label='LQUBO WP')
plt.scatter(had_domain, data['HD Slice LQUBO'][0])
plt.errorbar(had_domain, data['HD Slice LQUBO'][0], yerr=data['HD Slice LQUBO'][1], label='HD Slice LQUBO')
plt.scatter(had_domain, data['HD Slice LQUBO WP'][0])
plt.errorbar(had_domain, data['HD Slice LQUBO WP'][0], yerr=data['HD Slice LQUBO WP'][1], label='HD Slice LQUBO WP')

plt.xlabel('QAP Size')
plt.ylabel('Percent Error')
plt.legend(loc='best')
plt.title('QPU Comparison of Methods had iteration limit')
plt.show()


