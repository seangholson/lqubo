from solvers.solvers import LocalQUBOIterativeSolver
from datetime import datetime


class Experiment:
    """
    This class is designed to run multiple trials of a solver for a specified QAP/ TSP and collect data
    """
    def __init__(self,
                 max_hd=None,
                 objective_function=None,
                 num_trials=None,
                 solver=None,
                 sampler_type=None,
                 experiment_type=None):

        # Initialize objective function
        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError('Objective function missing.')

        # Initialize number of trials in experiment
        if num_trials:
            self.num_trials = num_trials
        else:
            self.num_trials = 10

        # Initialize solver based on type of experiment and sampler and/ or penalty if necessary

        if solver == 'LQUBO':
            self.solver_str = 'LQUBO'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'LQUBO WP'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'LQUBO WS'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'LQUBO WP and WS'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'Rand Slice LQUBO'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'Rand Slice LQUBO WS'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'Rand Slice LQUBO WP'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'Rand Slice LQUBO WP and WS'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'HD Slice LQUBO'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'HD Slice LQUBO WS'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'HD Slice LQUBO WP'
            if experiment_type == 'time limit' or 'iteration limit':
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
            self.solver_str = 'HD Slice LQUBO WP and WS'
            if experiment_type == 'time limit' or 'iteration limit':
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
        results['solver_qap_size_experiment_type'] = [self.solver_str, self.objective_function.n, self.experiment_str]
        results['approx_ans'] = []
        results['percent_error'] = []
        results['obtain_optimal'] = []
        results['timing_code'] = []
        results['number_of_iterations'] = []

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

        print('{} {} {} {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   self.objective_function.dat_file,
                                   self.solver_str,
                                   'finished_experiment'))

        return results


