# Built-ins:
from datetime import datetime

# Installed packages:

# Project locals:
from solvers.solvers import LocalQUBOIterativeSolver


# These are this list of valid solver types:
solver_types = [
    'LQUBO',
    'LQUBO WP',
    'LQUBO WS',
    'LQUBO WP and WS',
    'Rand Slice LQUBO',
    'Rand Slice LQUBO WS',
    'Rand Slice LQUBO WP',
    'Rand Slice LQUBO WP and WS',
    'HD Slice LQUBO',
    'HD Slice LQUBO WS',
    'HD Slice LQUBO WP',
    'HD Slice LQUBO WP and WS',
]

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
                 max_hd=None,
                 instance=None,
                 size=None,
                 problem_type=None,
                 objective_function=None,
                 num_trials=None,
                 num_reads=None,
                 num_iters=None,
                 solver=None,
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

        self.instance = instance
        self.problem_type = problem_type
        self.size = size
        self.save_csv = save_csv

        # Initialize solver based on type of experiment and sampler and/ or penalty if necessary
        if solver not in solver_types:
            err_msg = f'Solver {solver} must be one of {solver_types}'
            raise ValueError(err_msg)

        if experiment_type not in experiment_types:
            err_msg = f'Experiment {experiment_type} must be one of {experiment_types}'
            raise ValueError(err_msg)

        if sampler_type not in sampler_types:
            err_msg = f'Sampler {sampler_type} must be one of {sampler_types}'
            raise ValueError(err_msg)

        self.solver_str = solver
        self.experiment_str = experiment_type
        self.sampler_str = sampler_type

        if 'WS' in self.solver_str:
            selection_type = 'check and select'
        else:
            selection_type = 'select'

        self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                               dwave_sampler=sampler_type,
                                               lqubo_type=self.solver_str,
                                               selection_type=selection_type,
                                               max_hd=max_hd,
                                               experiment_type=experiment_type,
                                               num_reads=num_reads,
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
        results['v_vec'] = []

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
            results['v_vec'].append(solver_ans[6])

        t = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f = self.objective_function.dat_file
        s = self.solver_str
        print(f'{t} {f} {s} experiment finished')

        return results


