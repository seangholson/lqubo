# Built-ins:
from datetime import datetime

# Installed packages:

# Project locals:
from perm_LQUBO.solvers.Population_Based_LQUBO import PopulationLQUBOSolver

# These are the valid experiment types:
experiment_types = [
    'time_lim',
    'iter_lim',
]

# These are the valid D-Wave sampler types:
sampler_types = [
    'SA',
    'QPU',
    'Tabu',
]


class Experiment:
    """
    This class is designed to run multiple trials of a solver for a
    specified QAP/ TSP and collect data.
    """
    def __init__(self,
                 save_csv=None,
                 instance=None,
                 problem_type=None,
                 population_size=None,
                 objective_function=None,
                 num_trials=None,
                 num_reads=None,
                 num_iters=None,
                 solver="Population_Based_LQUBO",
                 sampler_type=None,
                 experiment_type=None):

        # Initialize objective function
        if objective_function:
            self.objective_function = objective_function
            self.answer = objective_function.min_v
        else:
            raise AttributeError('Objective function missing.')

        # Initialize number of trials in experiment
        if num_trials:
            self.num_trials = num_trials
        else:
            self.num_trials = 10

        self.population_size = population_size
        self.num_reads = num_reads
        self.instance = instance
        self.problem_type = problem_type
        self.size = str(objective_function.n)
        self.save_csv = save_csv

        # Initialize solver based on type of experiment and sampler and/ or penalty if necessary
        if experiment_type not in experiment_types:
            err_msg = f'Experiment {experiment_type} must be one of {experiment_types}'
            raise ValueError(err_msg)

        if sampler_type not in sampler_types:
            err_msg = f'Sampler {sampler_type} must be one of {sampler_types}'
            raise ValueError(err_msg)

        self.solver_str = solver + "_ps_" + str(self.population_size) + "_nr_" + str(num_reads)
        self.experiment_str = experiment_type
        self.sampler_str = sampler_type

        self.solver = PopulationLQUBOSolver(objective_function=objective_function,
                                            population_size=self.population_size,
                                            dwave_sampler=sampler_type,
                                            experiment_type=experiment_type,
                                            num_reads=self.num_reads,
                                            num_iters=num_iters)

    def run_experiment(self):
        results = dict()
        main_key = 'solver, size, experiment type, problem type, instance, answer'
        results[main_key] = [self.solver_str,
                             self.size,
                             self.experiment_str,
                             self.problem_type,
                             self.instance,
                             self.save_csv,
                             self.answer]
        results['approx_ans'] = []
        results['percent_error'] = []
        results['obtain_optimal'] = []
        results['timing_code'] = []
        results['number_of_iterations'] = []
        results['max_fitness'] = []

        for trial in range(self.num_trials):
            t = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            f = self.objective_function.dat_file
            s = self.solver_str
            e = self.experiment_str
            print(f'{t} {f} {s} {e} trial {trial+1} starting trial')

            solver = self.solver
            solver_ans = solver.minimize_objective()

            results['approx_ans'].append(solver_ans[0])
            results['percent_error'].append(solver_ans[1])
            results['obtain_optimal'].append(solver_ans[2])
            results['timing_code'].append(solver_ans[3])
            results['number_of_iterations'].append(solver_ans[4])
            results['trial_{}_data_dict'.format(trial + 1)] = solver_ans[5]
            results['max_fitness'].append(solver_ans[6])

        t = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f = self.objective_function.dat_file
        s = self.solver_str
        print(f'{t} {f} {s} experiment finished')

        return results


