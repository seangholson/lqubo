import statistics as stat
import pandas as pd


class ExperimentStatistics:
    """
    This class is designed to run statistics on the results of an experiment
    """
    def __init__(self, results_dict=None):

        # Initialize results dictionary
        if results_dict:
            self.results_dict = results_dict
        else:
            raise AttributeError('Results missing.')

        self.solver = self.results_dict['solver_size_experiment_type_problem_type_instance'][0]
        self.size = self.results_dict['solver_size_experiment_type_problem_type_instance'][1]
        self.experiment_type = self.results_dict['solver_size_experiment_type_problem_type_instance'][2]
        self.problem_type = self.results_dict['solver_size_experiment_type_problem_type_instance'][3]
        self.instance = self.results_dict['solver_size_experiment_type_problem_type_instance'][4]
        self.save_csv = self.results_dict['solver_size_experiment_type_problem_type_instance'][5]

        self.approx_ans = self.results_dict['approx_ans']
        self.percent_error = self.results_dict['percent_error']
        self.obtain_optimal = self.results_dict['obtain_optimal']
        self.timing_code = self.results_dict['timing_code']
        self.num_iters = self.results_dict['number_of_iterations']

    def run_stats(self):
        stats = dict()

        stats['percent_error'] = [stat.mean(self.percent_error), stat.stdev(self.percent_error)]
        stats['obtain_optimal'] = [stat.mean(self.obtain_optimal), stat.stdev(self.obtain_optimal)]
        stats['timing_code'] = [stat.mean(self.timing_code), stat.stdev(self.timing_code)]
        stats['number_of_iterations'] = [stat.mean(self.num_iters), stat.stdev(self.num_iters)]

        stats_df = pd.DataFrame(data=stats)

        if self.save_csv:
            stats_df.to_csv('./results/' + self.problem_type + '/' + self.instance + '/' + self.experiment_type + '/' +
                            self.solver + '_' + self.size + '.csv')

        return stats



