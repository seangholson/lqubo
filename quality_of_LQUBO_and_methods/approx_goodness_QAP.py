import numpy as np
from utilities.objective_functions import TSPObjectiveFunction, QAPObjectiveFunction
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from form_LQUBO.form_LQUBO_penalty import LQUBOWithPenalty
from form_LQUBO.form_LQUBO_rand_slice import RandSliceLQUBO
from form_LQUBO.form_LQUBO_hd_slice import HDSliceLQUBO
from form_LQUBO.from_LQUBO_hd_slice_penalty import HDSliceLQUBOPenalty
from form_LQUBO.form_LQUBO_rand_slice_penalty import RandSliceLQUBOPenalty
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy import stats
ax = plt.figure().gca()


class ObjectiveFunction:
    def __init__(self, objective_function=None):
        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError('Objective function missing.')


class LocalQUBOGoodness(ObjectiveFunction):
    """
    For a specified objective function and LQUBO type, LocalQUBOGoodness class has 2 useful visual functions that can
    be run from the command line.
    """
    def __init__(self,
                 objective_function=None,
                 max_hd=None,
                 hd_slice=None,
                 num_points=None,
                 num_slice_vectors=None,
                 lqubo_type=None,
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

        if num_points:
            self.num_points = num_points
        else:
            self.num_points = 200

        # Initialize random bitstring
        self.q = np.random.randint(0, 2, size=self.n_qubo)
        self.p = self.network.permute(self.q)
        self.v = self.objective_function(self.p)

        if type(objective_function) == TSPObjectiveFunction:
            self.OF_type = 'TSP'
        else:
            self.OF_type = 'QAP'

        self.max_hd = max_hd
        self.lqubo_type = lqubo_type

        if lqubo_type == 'LQUBO':
            self.form_qubo = LQUBO(objective_function=self.objective_function,
                                   switch_network=self.network,
                                   n_qubo=self.n_qubo).form_lqubo(q=self.q)
            self.hd_slice = 1
        elif lqubo_type == 'LQUBO WP':
            self.form_qubo = LQUBOWithPenalty(objective_function=self.objective_function,
                                              switch_network=self.network,
                                              n_qubo=self.n_qubo,
                                              max_hd=self.max_hd).form_lqubo(q=self.q)
            self.hd_slice = 1
        elif lqubo_type == 'Rand Slice LQUBO':
            self.form_qubo = RandSliceLQUBO(objective_function=self.objective_function,
                                            switch_network=self.network,
                                            n_qubo=self.n_qubo).form_lqubo(q=self.q)
            self.hd_slice = 'rand'
        elif lqubo_type == 'Rand Slice LQUBO WP':
            self.form_qubo = RandSliceLQUBOPenalty(objective_function=self.objective_function,
                                                   switch_network=self.network,
                                                   n_qubo=self.n_qubo,
                                                   max_hd=self.max_hd).form_lqubo(q=self.q)
            self.hd_slice = 'rand'
        elif lqubo_type == 'HD Slice LQUBO':
            self.form_qubo = HDSliceLQUBO(objective_function=self.objective_function,
                                          switch_network=self.network,
                                          n_qubo=self.n_qubo,
                                          num_slice_vectors=num_slice_vectors,
                                          slice_hd=hd_slice).form_lqubo(q=self.q)
            self.hd_slice = hd_slice
            if num_slice_vectors:
                self.n_qubo = num_slice_vectors
        elif lqubo_type == 'HD Slice LQUBO WP':
            self.form_qubo = HDSliceLQUBOPenalty(objective_function=self.objective_function,
                                                 switch_network=self.network,
                                                 n_qubo=self.n_qubo,
                                                 max_hd=self.max_hd,
                                                 num_slice_vectors=num_slice_vectors,
                                                 slice_hd=hd_slice).form_lqubo(q=self.q)
            self.hd_slice = hd_slice
            if num_slice_vectors:
                self.n_qubo = num_slice_vectors

        self.qubo = np.zeros((self.n_qubo, self.n_qubo))
        self.basis_matrix = []

        for i in range(self.n_qubo):
            self.basis_matrix.append(self.form_qubo[1][i])

        self.additive_constant = self.form_qubo[2]
        for i in range(self.n_qubo):
            for j in range(self.n_qubo):
                if i <= j:
                    self.qubo[i][j] = self.form_qubo[0][(i, j)]

    def plot_goodness(self, hamming_dist):

        """
        Given a specified hamming dist (int), plot_goodness will produce a scatter plot of the LQUBO change in objective
        function versus the actual change in objective function.
        """

        if hamming_dist:
            hamming_dist = hamming_dist
        else:
            raise AttributeError('Hamming dist missing.')

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(self.n_qubo))
            return binary

        # delta q of specified hamming dist
        hd = []
        x = []
        y = []

        for i in range(self.num_points):
            hd.append(np.zeros(self.n_qubo))

        for i in range(len(hd)):
            for j in range(hamming_dist):
                hd[i][j] = 1
            # only swap first n_qubo qubits to preserve total weight qubit
            random_binary(hd[i][:self.n_qubo])

        for vec in hd:
            q_new = np.mod(self.q + np.matmul(vec[:self.n_qubo], self.basis_matrix), 2)
            p_new = self.network.permute(q_new)
            v_new = self.objective_function(p_new)
            x.append(v_new - self.v)
            y.append(np.matmul(np.matmul(vec, self.qubo), np.transpose(vec)) + self.additive_constant)

        plt.scatter(x, y, label='HD = {}'.format(hamming_dist))

        plt.xlabel("true delta obj")
        plt.ylabel("local qubo delta obj")
        plt.title('n = {} {}, Activation Vector HD = {} '.format(self.n_qap, self.OF_type, self.hd_slice))

        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.legend(loc='upper left')
        plt.show()

    def plot_r_squared(self):

        """
        plot_r_squared function will take objective function from the base class and produce multiple scatter plots to
        retrieve the R squared value for a specified hamming distance.  Then for a hamming dist from 1 to 20 it will
        produce a plot of the R squared val versus the input hamming dist.
        """

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(self.n_qubo))
            return binary

        r_val = []
        hamming_weight = []
        for hamming_dist in range(20):

            hamming_dist = hamming_dist + 1
            hd = []
            x = []
            y = []

            for i in range(self.num_points):
                hd.append(np.zeros(self.n_qubo))

            for i in range(len(hd)):
                for j in range(hamming_dist):
                    hd[i][j] = 1
                random_binary(hd[i])

            for vec in hd:
                q_new = np.mod(self.q + np.matmul(vec, self.basis_matrix), 2)
                p_new = self.network.permute(q_new)
                v_new = self.objective_function(p_new)
                x.append(v_new - self.v)
                y.append(np.matmul(np.matmul(vec, self.qubo), np.transpose(vec)))

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            r_val.append(r_value**2)
            hamming_weight.append(hamming_dist)

        plt.plot(hamming_weight, r_val, label='n = {} {}, activation vector HD = {}'.format(self.n_qap,
                                                                                            self.OF_type,
                                                                                            self.hd_slice))

        plt.scatter(hamming_weight, r_val)
        plt.xticks(hamming_weight)
        plt.xlabel("Hamming dist")
        plt.ylabel("R Squared")
        plt.title('Hamming dist of LQUBO vs R Squared of scatter plot')
        plt.legend(loc='best')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()

    def find_max_hd(self):

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(self.n_qubo))
            return binary

        r_val = []
        hamming_weight = []
        for hamming_dist in range(20):

            hamming_dist = hamming_dist + 1
            hd = []
            x = []
            y = []

            for i in range(self.num_points):
                hd.append(np.zeros(self.n_qubo))

            for i in range(len(hd)):
                for j in range(hamming_dist):
                    hd[i][j] = 1
                random_binary(hd[i])

            for vec in hd:
                q_new = np.mod(self.q + np.matmul(vec, self.basis_matrix), 2)
                p_new = self.network.permute(q_new)
                v_new = self.objective_function(p_new)
                x.append(v_new - self.v)
                y.append(np.matmul(np.matmul(vec, self.qubo), np.transpose(vec)))

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            r_val.append(r_value**2)
            hamming_weight.append(hamming_dist)

