import numpy as np
from perm_LQUBO.form_new_LQUBO import NewLQUBO
from perm_LQUBO.select_perm import Select
from dimod import SimulatedAnnealingSampler
from tabu import TabuSampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import time


class Solver:
    """
    This is the base class for the solver method.
    """
    def __init__(self, objective_function=None):
        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError('Objective function missing.')

    def minimize_objective(self):
        raise NotImplementedError


class LocalQUBOIterativeSolver(Solver):
    """
    The Local-QUBO Solver uses a switch/permutation network to encode the QAP permutation
    in a bitstring.
    """
    def __init__(self,
                 objective_function=None,
                 dwave_sampler=None,
                 dwave_sampler_kwargs=None,
                 experiment_type=None,
                 num_reads=None,
                 num_iters=None):
        super().__init__(objective_function=objective_function)

        # Initialize switch network:
        # The default behavior here is to choose the smaller of either permutation or
        # sorting networks for the given input size.
        self.n_obj = self.objective_function.n

        self.n_qubo = self.n_obj - 1
        self.dwave_solver = None
        self.sampler_kwargs = None
        self.qpu = False

        # Initialize dwave sampler:
        if dwave_sampler == 'QPU':
            self.dwave_solver = EmbeddingComposite(DWaveSampler())
            self.qpu = True
            if dwave_sampler_kwargs:
                self.sampler_kwargs = dwave_sampler_kwargs
            else:
                self.sampler_kwargs = dict()
        elif dwave_sampler == 'SA':
            self.dwave_solver = SimulatedAnnealingSampler()
            if num_reads:
                self.sampler_kwargs = {
                    'num_reads': num_reads
                }
            else:
                self.sampler_kwargs = {
                    'num_reads': 25
                }
        elif dwave_sampler == 'Tabu':
            self.dwave_solver = TabuSampler()
            if num_reads:
                self.sampler_kwargs = {
                    'num_reads': num_reads
                }
            else:
                self.sampler_kwargs = {
                    'num_reads': 250
                }

        self.stopwatch = 0

        # Initialize type of experiment
        # When running a timed experiment there is a high number of iterations and a 30 sec wall clock
        # When running a iteration experiment there is a iteration limit of 30 and no wall clock
        if experiment_type == 'time_lim':
            self.n_iters = 1000
            self.time_limit = 30

        if experiment_type == 'iter_lim' and num_iters:
            self.n_iters = num_iters
            self.time_limit = False
        else:
            self.n_iters = 50
            self.time_limit = False

        self.form_qubo = NewLQUBO(objective_function=self.objective_function)

        self.solution = self.objective_function.min_v

        self.selection = Select

    def minimize_objective(self):
        start_code = time.time()

        p = np.random.permutation(self.n_obj)
        v = self.objective_function(p)
        delta_q = None

        data_dict = dict()
        data_dict['p_vec'] = [p]
        data_dict['v_vec'] = [v]

        # Initialize bitstring

        begin_loop = time.time()
        self.stopwatch = begin_loop - start_code
        for iteration in range(self.n_iters):

            # If there is a timing limit and the stopwatch is greater than the timing limit then break
            if self.time_limit and self.time_limit <= self.stopwatch:
                break
            start_iteration = time.time()

            # Build the Local QUBO by creating all delta_q's that are hamming distance 2
            # from the current q.  For each of those, the new q gives a permutation (via
            # the network encoding) and hence a new objective function value.  The deltas
            # in the objective function values are what populate the qubo.
            qubo = self.form_qubo.form_lqubo(p=p)

            # Solve the QUBO for delta_q
            if self.qpu:
                self.sampler_kwargs.update({
                    'chain_strength': 1.5*abs(max(qubo.values(), key=abs)),
                    'num_reads': 1000
                })

            response = self.dwave_solver.sample_qubo(qubo, **self.sampler_kwargs)
            select_response = self.selection(objective_function=self.objective_function,
                                             response_record=response.record,
                                             data_dict_p=data_dict['p_vec'],
                                             current_p=p).select()
            p = select_response[0]
            v = select_response[1]

            data_dict['p_vec'].append(p)
            data_dict['v_vec'].append(v)

            end_iteration = time.time()
            self.stopwatch += end_iteration - start_iteration

        end_code = time.time()
        timing_code = end_code - start_code

        lqubo_ans = min(data_dict['v_vec'])
        num_iters = len(data_dict['v_vec']) - 1

        if lqubo_ans == self.solution:
            obtain_optimal = 1
            percent_error = 0
        else:
            percent_error = abs(self.solution - lqubo_ans) / self.solution * 100
            obtain_optimal = 0

        return lqubo_ans, percent_error, obtain_optimal, timing_code, num_iters, data_dict, data_dict['v_vec']
