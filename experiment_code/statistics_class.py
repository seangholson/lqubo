import statistics as stat


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

        self.approx_ans = self.results_dict['approx_ans']
        self.percent_error = self.results_dict['percent_error']
        self.obtain_optimal = self.results_dict['obtain_optimal']
        self.timing_code = self.results_dict['timing_code']
        self.num_iters = self.results_dict['number_of_iterations']

    def run_stats(self):
        stats = dict()
        stats['solver_qap_size_experiment_type'] = self.results_dict['solver_qap_size_experiment_type']
        stats['approx_ans'] = [stat.mean(self.approx_ans), stat.stdev(self.approx_ans)]
        stats['percent_error'] = [stat.mean(self.percent_error), stat.stdev(self.percent_error)]
        stats['obtain_optimal'] = [stat.mean(self.obtain_optimal), stat.stdev(self.obtain_optimal)]
        stats['timing_code'] = [stat.mean(self.timing_code), stat.stdev(self.timing_code)]
        stats['number_of_iterations'] = [stat.mean(self.num_iters), stat.stdev(self.num_iters)]

        return stats



