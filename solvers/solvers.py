import numpy as np
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from form_LQUBO.form_LQUBO_penalty import LQUBOWithPenalty
from form_LQUBO.form_LQUBO_rand_slice import RandSliceLQUBO
from form_LQUBO.form_LQUBO_hd_slice import HDSliceLQUBO
from form_LQUBO.from_LQUBO_hd_slice_penalty import HDSliceLQUBOPenalty
from form_LQUBO.form_LQUBO_rand_slice_penalty import RandSliceLQUBOPenalty
from dimod import SimulatedAnnealingSampler
from tabu import TabuSampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import itertools
from response_selection.selection import CheckAndSelect, Select
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


class QAPEnumerator(Solver):
    """
    The QAP Enumerator Solver iterates over all permutations as output by itertools.
    """
    def __init__(self,
                 objective_function=None):
        super().__init__(objective_function=objective_function)

    def minimize_objective(self):
        min_v = np.inf
        minimizing_ps = []
        for p in itertools.permutations(range(self.objective_function.n)):
            v = self.objective_function(p)
            if v < min_v:
                min_v = v
                minimizing_ps.clear()
                minimizing_ps.append(list(p))
            elif v == min_v:
                minimizing_ps.append(list(p))
        return min_v, minimizing_ps


class QUBOEnumerator(Solver):
    """
    The QUBO Enumerator Solver iterates over all bitstrings.
    """
    def __init__(self,
                 objective_function=None):
        super().__init__(objective_function=objective_function)

    def minimize_objective(self):
        def convert_to_binary(val, size):
            # This helper function converts an int 'val' into a binary np.array
            # of size 'size'
            return np.array(list(np.binary_repr(val, size))).astype(np.int64)

        n = self.objective_function.n
        min_v = np.inf
        minimizing_qs = []
        for i in range(2**n):
            q = convert_to_binary(i, n)
            v = self.objective_function(q)
            if v < min_v:
                min_v = v
                minimizing_qs.clear()
                minimizing_qs.append(q)
            elif v == min_v:
                minimizing_qs.append(q)
        return min_v, minimizing_qs


class LocalQUBOIterativeSolver(Solver):
    """
    The Local-QUBO Solver uses a switch/permutation network to encode the QAP permutation
    in a bitstring.
    """
    def __init__(self,
                 objective_function=None,
                 dwave_sampler=None,
                 dwave_sampler_kwargs=None,
                 lqubo_type=None,
                 max_hd=None,
                 selection_type='check and select',
                 experiment_type=None,
                 num_reads=None,
                 num_iters=None,
                 network_type='minimum'):
        super().__init__(objective_function=objective_function)

        # Initialize switch network:
        # The default behavior here is to choose the smaller of either permutation or
        # sorting networks for the given input size.
        self.n_qap = self.objective_function.n
        if network_type == 'sorting':
            self.network = SortingNetwork(self.n_qap)
        elif network_type == 'permutation':
            self.network = PermutationNetwork(self.n_qap)
        elif network_type == 'minimum':
            s = SortingNetwork(self.n_qap)
            p = PermutationNetwork(self.n_qap)
            if s.depth <= p.depth:
                self.network = s
            else:
                self.network = p
        else:
            raise TypeError('Network type {} not recognized'.format(str(network_type)))
        self.n_qubo = self.network.depth
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

        if max_hd:
            self.max_hd = max_hd

        if lqubo_type == 'LQUBO' or 'LQUBO WS':
            self.form_qubo = LQUBO(objective_function=self.objective_function,
                                   switch_network=self.network,
                                   n_qubo=self.n_qubo)
        elif lqubo_type == 'LQUBO WP' or 'LQUBO WP and WS':
            self.form_qubo = LQUBOWithPenalty(objective_function=self.objective_function,
                                              switch_network=self.network,
                                              n_qubo=self.n_qubo,
                                              max_hd=self.max_hd)
        elif lqubo_type == 'Rand Slice LQUBO' or 'Rand Slice LQUBO WS':
            self.form_qubo = RandSliceLQUBO(objective_function=self.objective_function,
                                            switch_network=self.network,
                                            n_qubo=self.n_qubo)
        elif lqubo_type == 'Rand Slice LQUBO WP' or 'Rand Slice LQUBO WP and WS':
            self.form_qubo = RandSliceLQUBOPenalty(objective_function=self.objective_function,
                                                   switch_network=self.network,
                                                   n_qubo=self.n_qubo,
                                                   max_hd=self.max_hd)
        elif lqubo_type == 'HD Slice LQUBO' or 'HD Slice LQUBO WS':
            self.form_qubo = HDSliceLQUBO(objective_function=self.objective_function,
                                          switch_network=self.network,
                                          n_qubo=self.n_qubo,
                                          # num_slice_vectors=num_slice_vectors,
                                          slice_hd=2)
        elif lqubo_type == 'HD Slice LQUBO WP' or 'HD Slice LQUBO WP and WS':
            self.form_qubo = HDSliceLQUBOPenalty(objective_function=self.objective_function,
                                                 switch_network=self.network,
                                                 n_qubo=self.n_qubo,
                                                 max_hd=self.max_hd,
                                                 # num_slice_vectors=num_slice_vectors,
                                                 slice_hd=2)

        self.solution = self.objective_function.min_v

        if selection_type == 'check and select':
            self.selection = CheckAndSelect
        elif selection_type == 'select':
            self.selection = Select

    def minimize_objective(self):
        start_code = time.time()

        q = np.random.randint(0, 2, size=self.n_qubo)
        p = self.network.permute(q)
        v = self.objective_function(p)
        delta_q = None

        data_dict = dict()
        data_dict['q_vec'] = [q]
        data_dict['p_vec'] = [p]
        data_dict['v_vec'] = [v]
        data_dict['delta_q_vec'] = [['random switch setting']]

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
            qubo = self.form_qubo.form_lqubo(q=q)[0]
            delta_q_basis = self.form_qubo.form_lqubo(q=q)[1]

            # Solve the QUBO for delta_q
            if self.qpu:
                self.sampler_kwargs.update({
                    'chain_strength': 1.5*abs(max(qubo.values(), key=abs)),
                    'num_reads': 1000
                })

            retries = 10
            while retries > 0:
                try:
                    response = self.dwave_solver.sample_qubo(qubo, **self.sampler_kwargs)
                    select_response = self.selection(objective_function=self.objective_function,
                                                     switch_network=self.network,
                                                     response_record=response.record,
                                                     delta_q_basis=delta_q_basis,
                                                     data_dict_qvecs=data_dict['q_vec'],
                                                     current_q=q).select()
                    q = select_response[0]
                    p = select_response[1]
                    v = select_response[2]
                    delta_q = select_response[3]
                    break
                except ValueError:
                    print('retrying QUBO...')
                    retries -= 1

            if retries == 0:
                q = np.random.randint(0, 2, size=self.n_qubo)
                p = self.network.permute(q)
                v = self.objective_function(p)
                delta_q = None

                data_dict['q_vec'] = [q]
                data_dict['p_vec'] = [p]
                data_dict['v_vec'] = [v]
                data_dict['delta_q_vec'] = [['random switch setting']]

            data_dict['q_vec'].append(q)
            data_dict['p_vec'].append(p)
            data_dict['v_vec'].append(v)
            data_dict['delta_q_vec'].append(delta_q)

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


class NaturalEncodingSolver(Solver):
    """
    This Natural Encoding solver is how QAP is normally formulated as a QUBO.  This requires a binary variable for every
    entry of the permutation matrix.  As it is set up, you can solve this formulation by using the D-Wave
    QPU or D-Wave Simulated Annealing.
    """

    def __init__(self,
                 objective_function=None,
                 dwave_sampler=None,
                 dwave_sampler_kwargs=None):
        super().__init__(objective_function=objective_function)

        self.n = self.objective_function.n
        self.flow = self.objective_function.flow
        self.dist = self.objective_function.dist
        self.qpu = False

        # Initialize dwave sampler:
        if dwave_sampler:
            self.qpu = True
            self.dwave_solver = dwave_sampler
            if dwave_sampler_kwargs:
                self.sampler_kwargs = dwave_sampler_kwargs
            else:
                self.sampler_kwargs = dict()
        else:
            self.dwave_solver = SimulatedAnnealingSampler()
            self.sampler_kwargs = {
                'num_reads': 10
            }

        self.solution = self.objective_function.min_v

        if type(self.dwave_solver) == SimulatedAnnealingSampler:
            self.iteration_number = 10
        else:
            self.iteration_number = 1

        self.OF_tracker = np.zeros(self.iteration_number)

        self.energy = None
        self.sample = None

    def minimize_objective(self):

        identity = np.identity(self.n)
        a = np.ones((self.n, self.n))
        np.fill_diagonal(a, 0)
        qap = np.kron(self.flow, self.dist)
        p = 1.5*np.amax(np.amax(qap))
        quadratic_penalty = p*np.kron(a, identity) + p*np.kron(identity, a) - 2*p*np.kron(identity, identity)
        natural_qubo = qap + quadratic_penalty
        additive_const = 2*self.n*p

        for i in range(self.n ** 2):  # makes the QUBO Upper triangular
            for j in range(self.n ** 2):
                if j > i:
                    natural_qubo[i][j] = 2 * natural_qubo[i][j]
                elif i > j:
                    natural_qubo[i][j] = 0
        b = {}  # QUBO in dictionary form
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                if i <= j:
                    b[(i, j)] = natural_qubo[i][j]

        if self.qpu:
            self.sampler_kwargs.update({
                'chain_strength': 1.5 * abs(max(b.values(), key=abs)),
                'num_reads': 1000
            })

        qubo_dictionary = dict(b)

        response = self.dwave_solver.sample_qubo(qubo_dictionary, **self.sampler_kwargs)

        if type(self.dwave_solver) == SimulatedAnnealingSampler:
            for i in range(self.iteration_number):
                self.OF_tracker[i] = response.record[i][1] + additive_const
            self.energy = min(self.OF_tracker)
            self.sample = response.record[np.where(self.OF_tracker == self.energy)][0][0]
        else:
            self.sample = response.record[0][0]
            self.energy = response.record[0][1] + additive_const
            self.OF_tracker[0] = self.energy

        return self.sample, self.energy

