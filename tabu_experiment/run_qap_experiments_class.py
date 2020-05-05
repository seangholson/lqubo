from utilities.objective_functions import QAPObjectiveFunction
from experiment_code.experiment_class import Experiment
from experiment_code.statistics_class import ExperimentStatistics


class RunExperimentsAndPlotStatsQAP:

    def __init__(self, num_trials=None, sampler='Tabu', save_csv=None):

        self.num_trials = num_trials
        self.sampler = sampler
        self.problem_type = 'qap'
        self.save_csv = save_csv

        experiment_type_and_of_lqubo_had = {'iter_lim': {'percent error': [[], []],
                                                         'failure to obtain optimal': [[], []],
                                                         'timing code': [[], []],
                                                         'number of iterations': [[], []]},
                                            'objective function': [],
                                            'domain': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
                                            'max hd': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_nug = {'iter_lim': {'percent error': [[], []],
                                                         'failure to obtain optimal': [[], []],
                                                         'timing code': [[], []],
                                                         'number of iterations': [[], []]},
                                            'objective function': [],
                                            'domain': ['12', '14', '15', '16a', '16b', '17', '18', '20'],
                                            'max hd': [0, 0, 0, 0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_wp_had = {'iter_lim': {'percent error': [[], []],
                                                            'failure to obtain optimal': [[], []],
                                                            'timing code': [[], []],
                                                            'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
                                               'max hd': [4.92, 5.87, 7.92, 8.44, 9.75, 9.77, 10.52, 12.12, 11.7]}

        experiment_type_and_of_lqubo_wp_nug = {'iter_lim': {'percent error': [[], []],
                                                            'failure to obtain optimal': [[], []],
                                                            'timing code': [[], []],
                                                            'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['12', '14', '15', '16a', '16b', '17', '18', '20'],
                                               'max hd': [8, 8.6, 8.94, 9.92, 10.36, 11.15, 11.21, 11.61]}

        experiment_type_and_of_lqubo_ws_had = {'iter_lim': {'percent error': [[], []],
                                                            'failure to obtain optimal': [[], []],
                                                            'timing code': [[], []],
                                                            'number of iterations': [[], []]},
                                               'objective function': [],
                                               'domain': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
                                               'max hd': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_ws_nug = {'iter_lim': {'percent error': [[], []],
                                                            'failure to obtain optimal': [[], []],
                                                            'timing code': [[], []],
                                                            'number of iterations': [[], []]},

                                               'objective function': [],
                                               'domain': ['12', '14', '15', '16a', '16b', '17', '18', '20'],
                                               'max hd': [0, 0, 0, 0, 0, 0, 0, 0]}

        experiment_type_and_of_lqubo_wp_and_ws_had = {'iter_lim': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                                      'objective function': [],
                                                      'domain': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
                                                      'max hd': [4.92, 5.87, 7.92, 8.44, 9.75, 9.77, 10.52, 12.12, 11.7]}

        experiment_type_and_of_lqubo_wp_and_ws_nug = {'iter_lim': {'percent error': [[], []],
                                                                   'failure to obtain optimal': [[], []],
                                                                   'timing code': [[], []],
                                                                   'number of iterations': [[], []]},
                                                      'objective function': [],
                                                      'domain': ['12', '14', '15', '16a', '16b', '17', '18', '20'],
                                                      'max hd': [8, 8.6, 8.94, 9.92, 10.36, 11.15, 11.21, 11.61]}

        qap_instance_lqubo = {'had': experiment_type_and_of_lqubo_had, 'nug': experiment_type_and_of_lqubo_nug}
        qap_instance_lqubo_wp = {'had': experiment_type_and_of_lqubo_wp_had, 'nug': experiment_type_and_of_lqubo_wp_nug}
        qap_instance_lqubo_ws = {'had': experiment_type_and_of_lqubo_ws_had, 'nug': experiment_type_and_of_lqubo_ws_nug}
        qap_instance_lqubo_wp_and_ws = {'had': experiment_type_and_of_lqubo_wp_and_ws_had,
                                        'nug': experiment_type_and_of_lqubo_wp_and_ws_nug}
        self.results_data = {'LQUBO WS': qap_instance_lqubo_ws, 'LQUBO': qap_instance_lqubo,
                             'LQUBO WP': qap_instance_lqubo_wp, 'LQUBO WP and WS': qap_instance_lqubo_wp_and_ws}

        self.solvers = ['LQUBO', 'LQUBO WP and WS', 'LQUBO WP', 'LQUBO WS']
        self.qap_instance = ['had', 'nug']
        self.experiment_type = ['iter_lim']

        # Initialize objective function vectors for all solvers and qap instances
        for solver in self.solvers:
            for instance in self.qap_instance:
                for size in self.results_data[solver][instance]['domain']:
                    self.results_data[solver][instance]['objective function'].append(
                        QAPObjectiveFunction(dat_file= instance+size+'.dat', sln_file=instance+size+'.sln'))

    def run_lqubo_experiments(self):

        for instance in self.qap_instance:
            for experiment in self.experiment_type:
                for of_index in range(len(self.results_data['LQUBO'][instance]['domain'])):
                    run_experiment = Experiment(objective_function=self.results_data['LQUBO'][instance]['objective function'][of_index],
                                                num_trials=self.num_trials,
                                                solver='LQUBO',
                                                instance=instance,
                                                save_csv=self.save_csv,
                                                problem_type=self.problem_type,
                                                max_hd=self.results_data['LQUBO'][instance]['max hd'][of_index],
                                                size=self.results_data['LQUBO'][instance]['domain'][of_index],
                                                sampler_type=self.sampler,
                                                experiment_type=experiment)
                    experiment_stats = ExperimentStatistics(results_dict=run_experiment.run_experiment())
                    experiment_stats_results = experiment_stats.run_stats()
                    self.results_data['LQUBO'][instance][experiment]['percent error'][0].append(
                        experiment_stats_results['percent_error'][0])
                    self.results_data['LQUBO'][instance][experiment]['percent error'][1].append(
                        experiment_stats_results['percent_error'][1])
                    self.results_data['LQUBO'][instance][experiment]['failure to obtain optimal'][0].append(
                        1 - experiment_stats_results['obtain_optimal'][0])
                    self.results_data['LQUBO'][instance][experiment]['failure to obtain optimal'][1].append(
                        experiment_stats_results['obtain_optimal'][1])
                    self.results_data['LQUBO'][instance][experiment]['timing code'][0].append(
                        experiment_stats_results['timing_code'][0])
                    self.results_data['LQUBO'][instance][experiment]['timing code'][1].append(
                        experiment_stats_results['timing_code'][1])
                    self.results_data['LQUBO'][instance][experiment]['number of iterations'][0].append(
                        experiment_stats_results['number_of_iterations'][0])
                    self.results_data['LQUBO'][instance][experiment]['number of iterations'][1].append(
                        experiment_stats_results['number_of_iterations'][1])

    def run_lqubo_wp_experiments(self):

        for instance in self.qap_instance:
            for experiment in self.experiment_type:
                for of_index in range(len(self.results_data['LQUBO_WP'][instance]['domain'])):
                    run_experiment = Experiment(
                        objective_function=self.results_data['LQUBO_WP'][instance]['objective function'][of_index],
                        num_trials=self.num_trials,
                        solver='LQUBO_WP',
                        instance=instance,
                        save_csv=self.save_csv,
                        problem_type=self.problem_type,
                        max_hd=self.results_data['LQUBO_WP'][instance]['max hd'][of_index],
                        size=self.results_data['LQUBO_WP'][instance]['domain'][of_index],
                        sampler_type=self.sampler,
                        experiment_type=experiment)
                    experiment_stats = ExperimentStatistics(results_dict=run_experiment.run_experiment())
                    experiment_stats_results = experiment_stats.run_stats()
                    self.results_data['LQUBO_WP'][instance][experiment]['percent error'][0].append(
                        experiment_stats_results['percent_error'][0])
                    self.results_data['LQUBO_WP'][instance][experiment]['percent error'][1].append(
                        experiment_stats_results['percent_error'][1])
                    self.results_data['LQUBO_WP'][instance][experiment]['failure to obtain optimal'][0].append(
                        1 - experiment_stats_results['obtain_optimal'][0])
                    self.results_data['LQUBO_WP'][instance][experiment]['failure to obtain optimal'][1].append(
                        experiment_stats_results['obtain_optimal'][1])
                    self.results_data['LQUBO_WP'][instance][experiment]['timing code'][0].append(
                        experiment_stats_results['timing_code'][0])
                    self.results_data['LQUBO_WP'][instance][experiment]['timing code'][1].append(
                        experiment_stats_results['timing_code'][1])
                    self.results_data['LQUBO_WP'][instance][experiment]['number of iterations'][0].append(
                        experiment_stats_results['number_of_iterations'][0])
                    self.results_data['LQUBO_WP'][instance][experiment]['number of iterations'][1].append(
                        experiment_stats_results['number_of_iterations'][1])

    def run_lqubo_ws_experiments(self):

        for instance in self.qap_instance:
            for experiment in self.experiment_type:
                for of_index in range(len(self.results_data['LQUBO_WS'][instance]['domain'])):
                    run_experiment = Experiment(
                        objective_function=self.results_data['LQUBO_WS'][instance]['objective function'][of_index],
                        num_trials=self.num_trials,
                        solver='LQUBO_WS',
                        instance=instance,
                        save_csv=self.save_csv,
                        problem_type=self.problem_type,
                        max_hd=self.results_data['LQUBO_WS'][instance]['max hd'][of_index],
                        size=self.results_data['LQUBO_WS'][instance]['domain'][of_index],
                        sampler_type=self.sampler,
                        experiment_type=experiment)
                    experiment_stats = ExperimentStatistics(results_dict=run_experiment.run_experiment())
                    experiment_stats_results = experiment_stats.run_stats()
                    self.results_data['LQUBO_WS'][instance][experiment]['percent error'][0].append(
                        experiment_stats_results['percent_error'][0])
                    self.results_data['LQUBO_WS'][instance][experiment]['percent error'][1].append(
                        experiment_stats_results['percent_error'][1])
                    self.results_data['LQUBO_WS'][instance][experiment]['failure to obtain optimal'][0].append(
                        1 - experiment_stats_results['obtain_optimal'][0])
                    self.results_data['LQUBO_WS'][instance][experiment]['failure to obtain optimal'][1].append(
                        experiment_stats_results['obtain_optimal'][1])
                    self.results_data['LQUBO_WS'][instance][experiment]['timing code'][0].append(
                        experiment_stats_results['timing_code'][0])
                    self.results_data['LQUBO_WS'][instance][experiment]['timing code'][1].append(
                        experiment_stats_results['timing_code'][1])
                    self.results_data['LQUBO_WS'][instance][experiment]['number of iterations'][0].append(
                        experiment_stats_results['number_of_iterations'][0])
                    self.results_data['LQUBO_WS'][instance][experiment]['number of iterations'][1].append(
                        experiment_stats_results['number_of_iterations'][1])

    def run_lqubo_wp_and_ws_experiments(self):

        for instance in self.qap_instance:
            for experiment in self.experiment_type:
                for of_index in range(len(self.results_data['LQUBO_WP_and_WS'][instance]['domain'])):
                    run_experiment = Experiment(
                        objective_function=self.results_data['LQUBO_WP_and_WS'][instance]['objective function'][of_index],
                        num_trials=self.num_trials,
                        solver='LQUBO_WP_and_WS',
                        instance=instance,
                        save_csv=self.save_csv,
                        problem_type=self.problem_type,
                        max_hd=self.results_data['LQUBO_WP_and_WS'][instance]['max hd'][of_index],
                        size=self.results_data['LQUBO_WP_and_WS'][instance]['domain'][of_index],
                        sampler_type=self.sampler,
                        experiment_type=experiment)
                    experiment_stats = ExperimentStatistics(results_dict=run_experiment.run_experiment())
                    experiment_stats_results = experiment_stats.run_stats()
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['percent error'][0].append(
                        experiment_stats_results['percent_error'][0])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['percent error'][1].append(
                        experiment_stats_results['percent_error'][1])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['failure to obtain optimal'][0].append(
                        1 - experiment_stats_results['obtain_optimal'][0])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['failure to obtain optimal'][1].append(
                        experiment_stats_results['obtain_optimal'][1])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['timing code'][0].append(
                        experiment_stats_results['timing_code'][0])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['timing code'][1].append(
                        experiment_stats_results['timing_code'][1])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['number of iterations'][0].append(
                        experiment_stats_results['number_of_iterations'][0])
                    self.results_data['LQUBO_WP_and_WS'][instance][experiment]['number of iterations'][1].append(
                        experiment_stats_results['number_of_iterations'][1])

