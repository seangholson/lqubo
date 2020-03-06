from utilities.objective_functions import QAPObjectiveFunction
from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics
import matplotlib.pyplot as plt


class RunExperimentsAndPlotStatsQAP:

    def __init__(self, num_trials=None):

        self.num_trials = num_trials
        experiment_type_and_of_ga_had = {'time limit': {'percent error': [[], []],
                                                        'failure to obtain optimal': [[], []],
                                                        'timing code': [[], []],
                                                        'number of iterations': [[], []]},
                                         'iteration limit': {'percent error': [[], []],
                                                             'failure to obtain optimal': [[], []],
                                                             'timing code': [[], []],
                                                             'number of iterations': [[], []]},
                                         'objective function': [],
                                         'domain': ['4', '6', '8', '10', '12', '14', '16', '18', '20']}

        experiment_type_and_of_ga_nug = {'time limit': {'percent error': [[], []],
                                                        'failure to obtain optimal': [[], []],
                                                        'timing code': [[], []],
                                                        'number of iterations': [[], []]},
                                         'iteration limit': {'percent error': [[], []],
                                                             'failure to obtain optimal': [[], []],
                                                             'timing code': [[], []],
                                                             'number of iterations': [[], []]},
                                         'objective function': [],
                                         'domain': ['12', '14', '15', '16a', '16b', '17', '18', '20']}

        experiment_type_and_of_lqubo_had = {'time limit': {'percent error': [[], []],
                                                           'failure to obtain optimal': [[], []],
                                                           'timing code': [[], []],
                                                           'number of iterations': [[], []]},
                                            'iteration limit': {'percent error': [[], []],
                                                                'failure to obtain optimal': [[], []],
                                                                'timing code': [[], []],
                                                                'number of iterations': [[], []]},
                                            'objective function': [],
                                            'domain': ['4', '6', '8', '10', '12', '14', '16']}

        experiment_type_and_of_lqubo_nug = {'time limit': {'percent error': [[], []],
                                                           'failure to obtain optimal': [[], []],
                                                           'timing code': [[], []],
                                                           'number of iterations': [[], []]},
                                            'iteration limit': {'percent error': [[], []],
                                                                'failure to obtain optimal': [[], []],
                                                                'timing code': [[], []],
                                                                'number of iterations': [[], []]},
                                            'objective function': [],
                                            'domain': ['12', '14', '15', '16a', '16b']}

        experiment_type_and_of_lqubo_wp_had = {'time limit': {'percent error': [[], []],
                                                              'failure to obtain optimal': [[], []],
                                                              'timing code': [[], []],
                                                              'number of iterations': [[], []]},
                                               'iteration limit': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['4', '6', '8', '10', '12', '14', '16']}

        experiment_type_and_of_lqubo_wp_nug = {'time limit': {'percent error': [[], []],
                                                              'failure to obtain optimal': [[], []],
                                                              'timing code': [[], []],
                                                              'number of iterations': [[], []]},
                                               'iteration limit': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['12', '14', '15', '16a', '16b']}

        qap_instance_ga = {'had': experiment_type_and_of_ga_had, 'nug': experiment_type_and_of_ga_nug}
        qap_instance_lqubo = {'had': experiment_type_and_of_lqubo_had, 'nug': experiment_type_and_of_lqubo_nug}
        qap_instance_lqubo_wp = {'had': experiment_type_and_of_lqubo_wp_had, 'nug': experiment_type_and_of_lqubo_wp_nug}
        self.results_data = {'GA': qap_instance_ga, 'LQUBO': qap_instance_lqubo, 'LQUBO WP and WS': qap_instance_lqubo_wp}

        self.solvers = ['LQUBO', 'LQUBO WP and WS']
        self.qap_instance = ['had', 'nug']
        self.experiment_type = ['iteration limit', 'time limit']

        # Initialize objective function vectors for all solvers and qap instances
        for solver in self.solvers:
            for instance in self.qap_instance:
                for size in self.results_data[solver][instance]['domain']:
                    self.results_data[solver][instance]['objective function'].append(
                        QAPObjectiveFunction(dat_file= instance+size+'.dat', sln_file=instance+size+'.sln'))

    def run_experiments(self):

        for solver in self.solvers:
            for instance in self.qap_instance:
                for experiment in self.experiment_type:
                    for objective_function in self.results_data[solver][instance]['objective function']:
                        run_experiment = Experiment(objective_function=objective_function,
                                                    num_trials=self.num_trials,
                                                    solver=solver,
                                                    sampler_type='Tabu',
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
        plt.scatter(self.results_data['GA']['had']['domain'],
                    self.results_data['GA']['had']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['GA']['had']['domain'],
                     self.results_data['GA']['had']['time limit']['percent error'][0],
                     yerr=self.results_data['GA']['had']['time limit']['percent error'][1],
                     label='GA')
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
        plt.xlabel('QAP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['GA']['had']['domain'],
                    self.results_data['GA']['had']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['GA']['had']['domain'],
                     self.results_data['GA']['had']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['GA']['had']['time limit']['failure to obtain optimal'][1],
                     label='GA')
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
        plt.ylim(0, 1)
        plt.legend(loc='lower right')
        plt.xlabel('QAP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['GA']['had']['domain'],
                    self.results_data['GA']['had']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['GA']['had']['domain'],
                     self.results_data['GA']['had']['time limit']['number of iterations'][0],
                     yerr=self.results_data['GA']['had']['time limit']['number of iterations'][1],
                     label='GA')
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
        plt.xlabel('QAP Size')
        plt.ylabel('Number of Iterations')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Hadley-Rendl 30 sec Time Limit')
        plt.show()

    def plot_time_lim_nug(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['GA']['nug']['domain'],
                    self.results_data['GA']['nug']['time limit']['percent error'][0])
        plt.errorbar(self.results_data['GA']['nug']['domain'],
                     self.results_data['GA']['nug']['time limit']['percent error'][0],
                     yerr=self.results_data['GA']['nug']['time limit']['percent error'][1],
                     label='GA')
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

        plt.xlabel('QAP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['GA']['nug']['domain'],
                    self.results_data['GA']['nug']['time limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['GA']['nug']['domain'],
                     self.results_data['GA']['nug']['time limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['GA']['nug']['time limit']['failure to obtain optimal'][1],
                     label='GA')
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
        plt.ylim(0, 1)
        plt.legend(loc='lower right')
        plt.xlabel('QAP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['GA']['nug']['domain'],
                    self.results_data['GA']['nug']['time limit']['number of iterations'][0])
        plt.errorbar(self.results_data['GA']['nug']['domain'],
                     self.results_data['GA']['nug']['time limit']['number of iterations'][0],
                     yerr=self.results_data['GA']['nug']['time limit']['number of iterations'][1],
                     label='GA')
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
        plt.xlabel('QAP Size')
        plt.ylabel('Number of Iterations')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Nugent-Ruml 30 sec Time Limit')
        plt.show()

    def plot_iter_lim_had(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['GA']['had']['domain'],
                    self.results_data['GA']['had']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['GA']['had']['domain'],
                     self.results_data['GA']['had']['iteration limit']['percent error'][0],
                     yerr=self.results_data['GA']['had']['iteration limit']['percent error'][1],
                     label='GA')
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
        plt.xlabel('QAP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['GA']['had']['domain'],
                    self.results_data['GA']['had']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['GA']['had']['domain'],
                     self.results_data['GA']['had']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['GA']['had']['iteration limit']['failure to obtain optimal'][1],
                     label='GA')
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
        plt.ylim(0, 1)
        plt.legend(loc='lower right')
        plt.xlabel('QAP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['GA']['had']['domain'],
                    self.results_data['GA']['had']['iteration limit']['timing code'][0])
        plt.errorbar(self.results_data['GA']['had']['domain'],
                     self.results_data['GA']['had']['iteration limit']['timing code'][0],
                     yerr=self.results_data['GA']['had']['iteration limit']['timing code'][1],
                     label='GA')
        plt.scatter(self.results_data['LQUBO']['had']['domain'],
                    self.results_data['LQUBO']['had']['iteration limit']['timing code'][0])
        plt.errorbar(self.results_data['LQUBO']['had']['domain'],
                     self.results_data['LQUBO']['had']['iteration limit']['timing code'][0],
                     yerr=self.results_data['LQUBO']['had']['iteration limit']['timing code'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['had']['domain'],
                    self.results_data['LQUBO WP']['had']['iteration limit']['timing code'][0])
        plt.errorbar(self.results_data['LQUBO WP']['had']['domain'],
                     self.results_data['LQUBO WP']['had']['iteration limit']['timing code'][0],
                     yerr=self.results_data['LQUBO WP']['had']['iteration limit']['timing code'][1],
                     label='LQUBO w/ Penalty')
        plt.xlabel('QAP Size')
        plt.ylabel('Timing of code')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Hadley-Rendl 30 Iteration Limit')
        plt.show()

    def plot_iter_lim_nug(self):

        plt.figure(figsize=(13, 4))
        plt.subplot(131)
        plt.scatter(self.results_data['GA']['nug']['domain'],
                    self.results_data['GA']['nug']['iteration limit']['percent error'][0])
        plt.errorbar(self.results_data['GA']['nug']['domain'],
                     self.results_data['GA']['nug']['iteration limit']['percent error'][0],
                     yerr=self.results_data['GA']['nug']['iteration limit']['percent error'][1],
                     label='GA')
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
        plt.xlabel('QAP Size')
        plt.ylabel('Percent Error')

        plt.subplot(132)
        plt.scatter(self.results_data['GA']['nug']['domain'],
                    self.results_data['GA']['nug']['iteration limit']['failure to obtain optimal'][0])
        plt.errorbar(self.results_data['GA']['nug']['domain'],
                     self.results_data['GA']['nug']['iteration limit']['failure to obtain optimal'][0],
                     yerr=self.results_data['GA']['nug']['iteration limit']['failure to obtain optimal'][1],
                     label='GA')
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
        plt.ylim(0, 1)
        plt.legend(loc='lower right')
        plt.xlabel('QAP Size')
        plt.ylabel('Failure to Obtain Optimal')

        plt.subplot(133)
        plt.scatter(self.results_data['GA']['nug']['domain'],
                    self.results_data['GA']['nug']['iteration limit']['timing code'][0])
        plt.errorbar(self.results_data['GA']['nug']['domain'],
                     self.results_data['GA']['nug']['iteration limit']['timing code'][0],
                     yerr=self.results_data['GA']['nug']['iteration limit']['timing code'][1],
                     label='GA')
        plt.scatter(self.results_data['LQUBO']['nug']['domain'],
                    self.results_data['LQUBO']['nug']['iteration limit']['timing code'][0])
        plt.errorbar(self.results_data['LQUBO']['nug']['domain'],
                     self.results_data['LQUBO']['nug']['iteration limit']['timing code'][0],
                     yerr=self.results_data['LQUBO']['nug']['iteration limit']['timing code'][1],
                     label='LQUBO')
        plt.scatter(self.results_data['LQUBO WP']['nug']['domain'],
                    self.results_data['LQUBO WP']['nug']['iteration limit']['timing code'][0])
        plt.errorbar(self.results_data['LQUBO WP']['nug']['domain'],
                     self.results_data['LQUBO WP']['nug']['iteration limit']['timing code'][0],
                     yerr=self.results_data['LQUBO WP']['nug']['iteration limit']['timing code'][1],
                     label='LQUBO w/ Penalty')
        plt.xlabel('QAP Size')
        plt.ylabel('Timing of code')
        plt.subplots_adjust(wspace=.2)
        plt.suptitle('Nugent-Ruml 30 Iteration Limit')
        plt.show()










