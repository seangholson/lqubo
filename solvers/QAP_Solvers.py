import numpy as np
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from dimod import SimulatedAnnealingSampler
import itertools


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
        if dwave_sampler:
            self.dwave_solver = dwave_sampler
            self.qpu = True
            if dwave_sampler_kwargs:
                self.sampler_kwargs = dwave_sampler_kwargs
            else:
                self.sampler_kwargs = dict()
        else:
            self.dwave_solver = SimulatedAnnealingSampler()
            self.sampler_kwargs = {
                'num_reads': 10
            }

        # Initialize iteration parameters:
        self.n_iters = 10

    def minimize_objective(self):

        ident = np.identity(self.n_qubo)

        # Initialize bitstring
        q = np.random.randint(0, 2, size=self.n_qubo)
        p = self.network.permute(q)
        v = self.objective_function(p)

        data_dict = dict()
        data_dict['q_vec'] = [q]
        data_dict['p_vec'] = [p]
        data_dict['v_vec'] = [v]
        data_dict['Termination cause'] = []

        for _ in range(self.n_iters):

            # Build the Local QUBO by creating all delta_q's that are hamming distance 2
            # from the current q.  For each of those, the new q gives a permutation (via
            # the network encoding) and hence a new objective function value.  The deltas
            # in the objective function values are what populate the qubo.
            qubo = dict()
            for i in range(self.n_qubo):
                delta_q = ident[i, :]
                q_new = np.mod(q + delta_q, 2)
                p_new = self.network.permute(q_new)
                v_new = self.objective_function(p_new)
                qubo[(i, i)] = v_new - v
                for j in range(i+1, self.n_qubo):
                    delta_q = ident[i, :] + ident[j, :]
                    q_new = np.mod(q + delta_q, 2)
                    p_new = self.network.permute(q_new)
                    v_new = self.objective_function(p_new)
                    qubo[(i, j)] = v_new - v

            # Solve the QUBO for delta_q
            if self.qpu:
                self.sampler_kwargs.update({
                    'chain_strength': 1.5*abs(max(qubo.values(), key=abs)),
                    'num_reads': 1000
                })
            response = self.dwave_solver.sample_qubo(qubo, **self.sampler_kwargs)
            delta_q = response.record[0][0]

            # Update the new q:
            q = np.mod(q + delta_q, 2)
            p = self.network.permute(q)
            v = self.objective_function(p)

            secondary_qpu_read = False
            for delta_q in response.record:
                # Look through all responses in num reads to see if current q has been visited
                q = np.mod(q + delta_q[0], 2)
                p = self.network.permute(q)
                v = self.objective_function(p)
                if not self.q_in_data(data=data_dict['q_vec'], q=q):
                    # If the current q is not already in data_dict then it is a valid q and break for loop.
                    # If the current q is in data_dict then secondary_qpu_read will remain false.
                    secondary_qpu_read = True
                    break

            if not secondary_qpu_read:
                # If all responses in num reads have been visited then there are no more valid qpu samples.
                # Therefore if secondary_qpu_read remains false at end of for loop above then code is terminated
                # and csv is produced.

                delta_q = response.record[0][0]
                q = np.mod(q + delta_q, 2)
                p = self.network.permute(q)
                v = self.objective_function(p)
                data_dict['q_vec'].append(q)
                data_dict['p_vec'].append(p)
                data_dict['v_vec'].append(v)
                data_dict['Termination cause'].append('Redundant QPU samples')

                return min(data_dict['v_vec']), data_dict['p_vec'][data_dict['v_vec'].index(min(data_dict['v_vec']))], \
                    data_dict

            data_dict['q_vec'].append(q)
            data_dict['p_vec'].append(p)
            data_dict['v_vec'].append(v)

        data_dict['Termination cause'].append('No more iterations')

        return min(data_dict['v_vec']), data_dict['p_vec'][data_dict['v_vec'].index(min(data_dict['v_vec']))], data_dict

    def q_in_data(self, data, q):
        # data is expected to be a list

        all_tests = []

        for arr in data:
            # arr is a numpy array

            comparison = arr == q

            # all elements of of numpy arrays are equal
            all_tests.append(np.all(comparison))

        # when the loop is done return if all of the arrays matched
        return any(all_tests)


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

