from solvers.solvers import LocalQUBOIterativeSolver
from datetime import datetime


class Experiment:
    """
    This class is designed to run multiple trials of a solver for a specified QAP/ TSP and collect data
    """
    def __init__(self,
                 save_csv=None,
                 max_hd=None,
                 instance=None,
                 size=None,
                 problem_type=None,
                 objective_function=None,
                 num_trials=None,
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

        if solver == 'LQUBO':
            self.solver_str = 'LQUBO'
            if experiment_type == 'time_lim' or 'iteration_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='LQUBO',
                                                           selection_type='select',
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'LQUBO WP':
            self.solver_str = 'LQUBO_WP'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='LQUBO WP',
                                                           selection_type='select',
                                                           max_hd=max_hd,
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'LQUBO WS':
            self.solver_str = 'LQUBO_WS'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='LQUBO',
                                                           selection_type='check and select',
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'LQUBO WP and WS':
            self.solver_str = 'LQUBO_WP_and_WS'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='LQUBO WP',
                                                           selection_type='check and select',
                                                           max_hd=max_hd,
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'Rand Slice LQUBO':
            self.solver_str = 'Rand_Slice_LQUBO'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='Rand Slice LQUBO',
                                                           selection_type='select',
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'Rand Slice LQUBO WS':
            self.solver_str = 'Rand_Slice_LQUBO_WS'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='Rand Slice LQUBO',
                                                           selection_type='check and select',
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'Rand Slice LQUBO WP':
            self.solver_str = 'Rand_Slice_LQUBO_WP'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='Rand Slice LQUBO WP',
                                                           selection_type='select',
                                                           max_hd=max_hd,
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'Rand Slice LQUBO WP and WS':
            self.solver_str = 'Rand_Slice_LQUBO_WP_and_WS'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='Rand Slice LQUBO WP',
                                                           selection_type='check and select',
                                                           max_hd=max_hd,
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'HD Slice LQUBO':
            self.solver_str = 'HD_Slice_LQUBO'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='HD Slice LQUBO',
                                                           selection_type='select',
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'HD Slice LQUBO WS':
            self.solver_str = 'HD_Slice_LQUBO_WS'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='HD Slice LQUBO',
                                                           selection_type='check and select',
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'HD Slice LQUBO WP':
            self.solver_str = 'HD_Slice_LQUBO_WP'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='HD Slice LQUBO WP',
                                                           selection_type='select',
                                                           max_hd=max_hd,
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        elif solver == 'HD Slice LQUBO WP and WS':
            self.solver_str = 'HD_Slice_LQUBO_WP_and_WS'
            if experiment_type == 'iter_lim' or 'time_lim':
                self.experiment_str = experiment_type
                if sampler_type not in ['SA', 'QPU', 'Tabu']:
                    raise AttributeError('Invalid type of sampler.')
                else:
                    self.solver = LocalQUBOIterativeSolver(objective_function=objective_function,
                                                           dwave_sampler=sampler_type,
                                                           lqubo_type='HD Slice LQUBO WP',
                                                           selection_type='check and select',
                                                           max_hd=max_hd,
                                                           experiment_type=experiment_type)
            else:
                raise AttributeError('Invalid type of experiment.')
        else:
            raise AttributeError('Invalid type of solver.')

    def run_experiment(self):
        results = dict()
        results['solver, size, experiment type, problem type, instance, answer'] = [self.solver_str,
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
            print('{} {} {} {} trial {} {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                   self.objective_function.dat_file,
                                                   self.solver_str,
                                                   self.experiment_str,
                                                   trial + 1,
                                                   'starting_trial'))
            solver = self.solver
            solver_ans = solver.minimize_objective()

            results['approx_ans'].append(solver_ans[0])
            results['percent_error'].append(solver_ans[1])
            results['obtain_optimal'].append(solver_ans[2])
            results['timing_code'].append(solver_ans[3])
            results['number_of_iterations'].append(solver_ans[4])
            results['trial_{}_data_dict'.format(trial + 1)] = solver_ans[5]
            results['v_vec'].append(solver_ans[6])

        print('{} {} {} {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   self.objective_function.dat_file,
                                   self.solver_str,
                                   'finished_experiment'))

        return results


