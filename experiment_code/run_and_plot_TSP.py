from utilities.objective_functions import TSPObjectiveFunction
from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
import matplotlib.pyplot as plt


class RunExperimentsAndPlotStatsTSP:

    def __init__(self, num_trials=None, sampler=None):

        self.num_trials = num_trials
        self.sampler = sampler

        experiment_type_and_of_lqubo_had = {'time limit': {'percent error': [[], []],
                                                           'failure to obtain optimal': [[], []],
                                                           'timing code': [[], []],
                                                           'number of iterations': [[], []]},
                                            'iteration limit': {'percent error': [[], []],
                                                                'failure to obtain optimal': [[], []],
                                                                'timing code': [[], []],
                                                                'number of iterations': [[], []]},
                                            'objective function': [],
                                            'domain': ['4', '6', '8', '10', '12', '14', '16'],
                                            'max hd': [0, 0, 0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_nug = {'time limit': {'percent error': [[], []],
                                                           'failure to obtain optimal': [[], []],
                                                           'timing code': [[], []],
                                                           'number of iterations': [[], []]},
                                            'iteration limit': {'percent error': [[], []],
                                                                'failure to obtain optimal': [[], []],
                                                                'timing code': [[], []],
                                                                'number of iterations': [[], []]},
                                            'objective function': [],
                                            'domain': ['12', '14', '15', '16a', '16b'],
                                            'max hd': [0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_wp_had = {'time limit': {'percent error': [[], []],
                                                              'failure to obtain optimal': [[], []],
                                                              'timing code': [[], []],
                                                              'number of iterations': [[], []]},
                                               'iteration limit': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['4', '6', '8', '10', '12', '14', '16'],
                                               'max hd': [3.71, 4.48, 6.4, 6.41, 8.35, 8.94, 11.48]}

        experiment_type_and_of_lqubo_wp_nug = {'time limit': {'percent error': [[], []],
                                                              'failure to obtain optimal': [[], []],
                                                              'timing code': [[], []],
                                                              'number of iterations': [[], []]},
                                               'iteration limit': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['12', '14', '15', '16a', '16b'],
                                               'max hd': [7.95, 7.92, 8.4, 9.87, 10.37]}

        experiment_type_and_of_lqubo_ws_had = {'time limit': {'percent error': [[], []],
                                                              'failure to obtain optimal': [[], []],
                                                              'timing code': [[], []],
                                                              'number of iterations': [[], []]},
                                               'iteration limit': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['4', '6', '8', '10', '12', '14', '16'],
                                               'max hd': [0, 0, 0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_ws_nug = {'time limit': {'percent error': [[], []],
                                                              'failure to obtain optimal': [[], []],
                                                              'timing code': [[], []],
                                                              'number of iterations': [[], []]},
                                               'iteration limit': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['12', '14', '15', '16a', '16b'],
                                               'max hd': [0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_wp_and_ws_had = {'time limit': {'percent error': [[], []],
                                                                     'failure to obtain optimal': [[], []],
                                                                     'timing code': [[], []],
                                                                     'number of iterations': [[], []]},
                                                      'iteration limit': {'percent error': [[], []],
                                                                          'failure to obtain optimal': [[], []],
                                                                          'timing code': [[], []],
                                                                          'number of iterations': [[], []]},
                                                      'objective function': [],
                                                      'domain': ['4', '6', '8', '10', '12', '14', '16'],
                                                      'max hd': [3.71, 4.48, 6.4, 6.41, 8.35, 8.94, 11.48]}

        experiment_type_and_of_lqubo_wp_and_ws_nug = {'time limit': {'percent error': [[], []],
                                                                     'failure to obtain optimal': [[], []],
                                                                     'timing code': [[], []],
                                                                     'number of iterations': [[], []]},
                                                      'iteration limit': {'percent error': [[], []],
                                                                          'failure to obtain optimal': [[], []],
                                                                          'timing code': [[], []],
                                                                          'number of iterations': [[], []]},
                                                      'objective function': [],
                                                      'domain': ['12', '14', '15', '16a', '16b'],
                                                      'max hd': [7.95, 7.92, 8.4, 9.87, 10.37]}

        tsp_instance_lqubo = {'had': experiment_type_and_of_lqubo_had, 'nug': experiment_type_and_of_lqubo_nug}
        tsp_instance_lqubo_wp = {'had': experiment_type_and_of_lqubo_wp_had, 'nug': experiment_type_and_of_lqubo_wp_nug}
        tsp_instance_lqubo_ws = {'had': experiment_type_and_of_lqubo_ws_had, 'nug': experiment_type_and_of_lqubo_ws_nug}
        tsp_instance_lqubo_wp_and_ws = {'had': experiment_type_and_of_lqubo_wp_and_ws_had,
                                        'nug': experiment_type_and_of_lqubo_wp_and_ws_nug}
        self.results_data = {'LQUBO WS': tsp_instance_lqubo_ws, 'LQUBO': tsp_instance_lqubo,
                             'LQUBO WP': tsp_instance_lqubo_wp, 'LQUBO WP and WS': tsp_instance_lqubo_wp_and_ws}

        self.solvers = ['LQUBO', 'LQUBO WP and WS', 'LQUBO WP', 'LQUBO WS']
        self.TSP_instance = ['had', 'nug']
        self.experiment_type = ['iteration limit', 'time limit']

        # Initialize objective function vectors for all solvers and TSP instances
        for solver in self.solvers:
            for instance in self.TSP_instance:
                for size in self.results_data[solver][instance]['domain']:
                    self.results_data[solver][instance]['objective function'].append(
                        TSPObjectiveFunction(dat_file=instance+size +'.dat', sln_file=instance+size +'.sln'))

    def run_experiments(self):

        for solver in self.solvers:
            for instance in self.TSP_instance:
                for experiment in self.experiment_type:
                    for of_index in range(len(self.results_data[solver][instance]['domain'])):
                        run_experiment = Experiment(objective_function=self.results_data[solver][instance]['objective function'][of_index],
                                                    num_trials=self.num_trials,
                                                    solver=solver,
                                                    max_hd=self.results_data[solver][instance]['max hd'][of_index],
                                                    sampler_type=self.sampler,
                                                    experiment_type=experiment)
                        experiment_stats = ExperimentStatistics(results_dict=run_experiment.run_experiment())
                        experiment_stats_results = experiment_stats.run_stats()
                        self.results_data[solver][instance][experiment]['percent error'][0].append(
                            experiment_stats_results['percent_error'][0])
                        self.results_data[solver][instance][experiment]['percent error'][1].append(
                            experiment_stats_results['percent_error'][1])
                        self.results_data[solver][instance][experiment]['failure to obtain optimal'][0].append(
                            1 - experiment_stats_results['obtain_optimal'][0])
                        self.results_data[solver][instance][experiment]['failure to obtain optimal'][1].append(
                            experiment_stats_results['obtain_optimal'][1])
                        self.results_data[solver][instance][experiment]['timing code'][0].append(
                            experiment_stats_results['timing_code'][0])
                        self.results_data[solver][instance][experiment]['timing code'][1].append(
                            experiment_stats_results['timing_code'][1])
                        self.results_data[solver][instance][experiment]['number of iterations'][0].append(
                            experiment_stats_results['number_of_iterations'][0])
                        self.results_data[solver][instance][experiment]['number of iterations'][1].append(
                            experiment_stats_results['number_of_iterations'][1])

    def plot_time_lim_had(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO']['had']['time limit']['percent error'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP']['had']['time limit']['percent error'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['had']['domain'],
                    self.results_data['LQUBO WS']['had']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WS']['had']['domain'],
                     self.results_data['LQUBO WS']['had']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WS']['had']['time limit']['percent error'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['had']['domain'],
                    self.results_data['LQUBO WP and WS']['had']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['had']['domain'],
                     self.results_data['LQUBO WP and WS']['had']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP and WS']['had']['time limit']['percent error'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO']['had']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP']['had']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['had']['domain'],
                    self.results_data['LQUBO WS']['had']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WS']['had']['domain'],
                     self.results_data['LQUBO WS']['had']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WS']['had']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['had']['domain'],
                    self.results_data['LQUBO WP and WS']['had']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['had']['domain'],
                     self.results_data['LQUBO WP and WS']['had']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP and WS']['had']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='lower right')
        plt.xlabel('TSP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO']['had']['time limit']['number of iterations'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP']['had']['time limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['had']['domain'],
                    self.results_data['LQUBO WS']['had']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WS']['had']['domain'],
                     self.results_data['LQUBO WS']['had']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WS']['had']['time limit']['number of iterations'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['had']['domain'],
                    self.results_data['LQUBO WP and WS']['had']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['had']['domain'],
                     self.results_data['LQUBO WP and WS']['had']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP and WS']['had']['time limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Number of Iterations')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Hadley-Rendl 30 sec Time Limit')
        plt.show()

    def plot_time_lim_nug(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO']['nug']['time limit']['percent error'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['time limit']['percent error'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['nug']['domain'],
                    self.results_data['LQUBO WS']['nug']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WS']['nug']['domain'],
                     self.results_data['LQUBO WS']['nug']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WS']['nug']['time limit']['percent error'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['nug']['domain'],
                    self.results_data['LQUBO WP and WS']['nug']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['nug']['domain'],
                     self.results_data['LQUBO WP and WS']['nug']['time limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP and WS']['nug']['time limit']['percent error'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO']['nug']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['nug']['domain'],
                    self.results_data['LQUBO WS']['nug']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WS']['nug']['domain'],
                     self.results_data['LQUBO WS']['nug']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WS']['nug']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['nug']['domain'],
                    self.results_data['LQUBO WP and WS']['nug']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['nug']['domain'],
                     self.results_data['LQUBO WP and WS']['nug']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP and WS']['nug']['time limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='lower right')
        plt.xlabel('TSP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO']['nug']['time limit']['number of iterations'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['time limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['nug']['domain'],
                    self.results_data['LQUBO WS']['nug']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WS']['nug']['domain'],
                     self.results_data['LQUBO WS']['nug']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WS']['nug']['time limit']['number of iterations'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['nug']['domain'],
                    self.results_data['LQUBO WP and WS']['nug']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['nug']['domain'],
                     self.results_data['LQUBO WP and WS']['nug']['time limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP and WS']['nug']['time limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Number of Iterations')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Nugent-Ruml 30 sec Time Limit')
        plt.show()

    def plot_iter_lim_had(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO']['had']['iteration limit']['percent error'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP']['had']['iteration limit']['percent error'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['had']['domain'],
                    self.results_data['LQUBO WS']['had']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WS']['had']['domain'],
                     self.results_data['LQUBO WS']['had']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WS']['had']['iteration limit']['percent error'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['had']['domain'],
                    self.results_data['LQUBO WP and WS']['had']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['had']['domain'],
                     self.results_data['LQUBO WP and WS']['had']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP and WS']['had']['iteration limit']['percent error'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO']['had']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP']['had']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['had']['domain'],
                    self.results_data['LQUBO WS']['had']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WS']['had']['domain'],
                     self.results_data['LQUBO WS']['had']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WS']['had']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['had']['domain'],
                    self.results_data['LQUBO WP and WS']['had']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['had']['domain'],
                     self.results_data['LQUBO WP and WS']['had']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP and WS']['had']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='lower right')
        plt.xlabel('TSP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO']['had']['iteration limit']['number of iterations'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP']['had']['iteration limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['had']['domain'],
                    self.results_data['LQUBO WS']['had']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WS']['had']['domain'],
                     self.results_data['LQUBO WS']['had']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WS']['had']['iteration limit']['number of iterations'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['had']['domain'],
                    self.results_data['LQUBO WP and WS']['had']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['had']['domain'],
                     self.results_data['LQUBO WP and WS']['had']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP and WS']['had']['iteration limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Timing of code')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Hadley-Rendl 30 Iteration Limit')
        plt.show()

    def plot_iter_lim_nug(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO']['nug']['iteration limit']['percent error'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['iteration limit']['percent error'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['nug']['domain'],
                    self.results_data['LQUBO WS']['nug']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WS']['nug']['domain'],
                     self.results_data['LQUBO WS']['nug']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WS']['nug']['iteration limit']['percent error'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['nug']['domain'],
                    self.results_data['LQUBO WP and WS']['nug']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['nug']['domain'],
                     self.results_data['LQUBO WP and WS']['nug']['iteration limit']['percent error'][0],
                     yerr=self.results_data['LQUBO WP and WS']['nug']['iteration limit']['percent error'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO']['nug']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['nug']['domain'],
                    self.results_data['LQUBO WS']['nug']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WS']['nug']['domain'],
                     self.results_data['LQUBO WS']['nug']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WS']['nug']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['nug']['domain'],
                    self.results_data['LQUBO WP and WS']['nug']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['nug']['domain'],
                     self.results_data['LQUBO WP and WS']['nug']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['LQUBO WP and WS']['nug']['iteration limit']['failure to obtain optimal'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='lower right')
        plt.xlabel('TSP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO']['nug']['iteration limit']['number of iterations'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['iteration limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty')
        plt.scatter(self.results_data['LQUBO WS']['nug']['domain'],
                    self.results_data['LQUBO WS']['nug']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WS']['nug']['domain'],
                     self.results_data['LQUBO WS']['nug']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WS']['nug']['iteration limit']['number of iterations'][1],
                     label='LQUBO w/ Sorting')
        plt.scatter(self.results_data['LQUBO WP and WS']['nug']['domain'],
                    self.results_data['LQUBO WP and WS']['nug']['iteration limit']['number of iterations'][0])
        plt.errorbar(self.results_data['LQUBO WP and WS']['nug']['domain'],
                     self.results_data['LQUBO WP and WS']['nug']['iteration limit']['number of iterations'][0],
                     yerr=self.results_data['LQUBO WP and WS']['nug']['iteration limit']['number of iterations'][1],
                     label='LQUBO w/ Penalty and Sorting')
        plt.xlabel('TSP Size')
        plt.ylabel('Timing of code')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Nugent-Ruml 30 Iteration Limit')
        plt.show()




