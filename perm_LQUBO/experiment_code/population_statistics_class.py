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

        self.solver = self.results_dict['solver, size, experiment type, problem type, instance, answer'][0]
        self.size = self.results_dict['solver, size, experiment type, problem type, instance, answer'][1]
        self.experiment_type = self.results_dict['solver, size, experiment type, problem type, instance, answer'][2]
        self.problem_type = self.results_dict['solver, size, experiment type, problem type, instance, answer'][3]
        self.instance = self.results_dict['solver, size, experiment type, problem type, instance, answer'][4]
        self.save_csv = self.results_dict['solver, size, experiment type, problem type, instance, answer'][5]
        self.answer = self.results_dict['solver, size, experiment type, problem type, instance, answer'][6]

        self.approx_ans = self.results_dict['approx_ans']
        self.percent_error = self.results_dict['percent_error']
        self.obtain_optimal = self.results_dict['obtain_optimal']
        self.timing_code = self.results_dict['timing_code']
        self.num_iters = self.results_dict['number_of_iterations']
        self.v_vectors = self.results_dict['max_fitness']
        self.avg_form_lqubo = self.results_dict['average_form_lqubo']
        self.avg_solve_lqubo = self.results_dict['average_solve_lqubo']
        self.full_data_dict = self.results_dict['data_dict']
        self.avg_fitness = self.results_dict['average_fitness']
        self.min_fitness = self.results_dict['min_fitness']

        if isinstance(self.size, int):
            self.size = str(self.size)

    def collect_convergence_vals(self):
        #  If the problem is of size 20 and you are saving CSV files, you can see the convergence of the LQUBO
        #  algorithm by looking at the convergence CSV
        len_convergence_vec = (len(self.v_vectors[0]) - 1) / 5 + 1
        convergence_vec = []
        avg_convergence_vec = []
        min_convergence_vec = []
        for _ in range(int(len_convergence_vec)):
            convergence_vec.append([])
            avg_convergence_vec.append([])
            min_convergence_vec.append([])
        # arrays in convergence_vec will be filled with the min val of algorithm for every 5 iterations
        # for example, if run for 50 iterations there are 10 arrays to be filled
        for vec in self.v_vectors:
            convergence_vec[0].append(vec[0])
            for iteration in range(len(convergence_vec) - 1):
                iteration_number = (iteration + 1) * 5
                convergence_val = min(vec[:iteration_number])
                convergence_vec[iteration + 1].append(convergence_val)

        for vec in self.avg_fitness:
            avg_convergence_vec[0].append(vec[0])
            for iteration in range(len(convergence_vec) - 1):
                iteration_number = (iteration + 1) * 5
                convergence_val = min(vec[:iteration_number])
                avg_convergence_vec[iteration + 1].append(convergence_val)

        for vec in self.min_fitness:
            min_convergence_vec[0].append(vec[0])
            for iteration in range(len(convergence_vec) - 1):
                iteration_number = (iteration + 1) * 5
                convergence_val = min(vec[:iteration_number])
                min_convergence_vec[iteration + 1].append(convergence_val)

        max_fit_percent_error_convergence_vals = []
        avg_fit_percent_error_convergence_vals = []
        min_fit_percent_error_convergence_vals = []
        for vec in convergence_vec:
            avg_convergence_val = stat.mean(vec)
            percent_error_val = abs(avg_convergence_val - self.answer) / self.answer
            max_fit_percent_error_convergence_vals.append(percent_error_val)

        for vec in avg_convergence_vec:
            avg_convergence_val = stat.mean(vec)
            percent_error_val = abs(avg_convergence_val - self.answer) / self.answer
            avg_fit_percent_error_convergence_vals.append(percent_error_val)

        for vec in min_convergence_vec:
            avg_convergence_val = stat.mean(vec)
            percent_error_val = abs(avg_convergence_val - self.answer) / self.answer
            min_fit_percent_error_convergence_vals.append(percent_error_val)

        domain = [0]
        for i in range(len(convergence_vec) - 1):
            domain.append((i + 1) * 5)

        convergence_dict = {'domain': domain,
                            'max fit convergence percent error vals': max_fit_percent_error_convergence_vals,
                            'avg fit convergence percent error vals': avg_fit_percent_error_convergence_vals,
                            'min fit convergence percent error vals': min_fit_percent_error_convergence_vals}
        return convergence_dict

    def run_stats(self):
        stats = dict()

        stats['percent_error'] = [stat.mean(self.percent_error), stat.stdev(self.percent_error)]
        stats['obtain_optimal'] = [stat.mean(self.obtain_optimal), stat.stdev(self.obtain_optimal)]
        stats['timing_code'] = [stat.mean(self.timing_code), stat.stdev(self.timing_code)]
        stats['avg_form_lqubo'] = [stat.mean(self.avg_form_lqubo), stat.stdev(self.avg_form_lqubo)]
        stats['avg_solve_lqubo'] = [stat.mean(self.avg_solve_lqubo), stat.stdev(self.avg_solve_lqubo)]
        stats['number_of_iterations'] = [stat.mean(self.num_iters), stat.stdev(self.num_iters)]

        if self.save_csv:
            stats_df = pd.DataFrame(data=stats)
            stats_df.to_csv(('./perm_LQUBO/results/' + 'experiment_data/' + self.instance + '/' + self.experiment_type + '/' +
                            self.solver + '_' + self.size + '.csv').replace(' ', '_'))

        if self.save_csv and int(self.size) == 20:
            convergence_dict = self.collect_convergence_vals()
            convergence_df = pd.DataFrame(data=convergence_dict)
            convergence_df.to_csv(('./perm_LQUBO/results/' + 'convergence/' + self.instance + '_' + self.solver + '_' + self.size
                                  + '.csv').replace(' ', '_'))
        return stats



