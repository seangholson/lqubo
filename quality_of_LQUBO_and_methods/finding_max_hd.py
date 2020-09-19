import numpy as np
import statistics as stat
from utilities.objective_functions import TSPObjectiveFunction, QAPObjectiveFunction
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from scipy import stats
import time


class MaxHDSolver:
    """
    MaxHDSolver class can be run from the command line and given the full suite of experiment_data, tsp, had, and nug instances will
    display an a array of 'good' max hd values to use for LQUBOs with a penalty.  This is based on the R squared value
    of the hamming distance plots.
    """
    def __init__(self,
                 activation_vec_hamming_dist=1,
                 num_points=200,
                 num_activation_vectors=None):

        self.num_points = num_points
        self.activation_vec_hd = activation_vec_hamming_dist
        self.num_activation_vec = num_activation_vectors

        had_qap = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}
        nug_qap = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}

        tsp_data = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}

        had = {'experiment_data': had_qap, 'instances': ['4', '6', '8', '10', '12', '14', '16', '18', '20']}
        nug = {'experiment_data': nug_qap, 'instances': ['12', '14', '15', '16a', '16b', '17', '18', '20']}
        tsp = {'experiment_data': tsp_data, 'instances': list(range(4, 21))}

        self.max_hd_dict = {'had': had, 'nug': nug, 'tsp': tsp, 'total time to compute max hd code': []}

        """
        Generates and organizes all objective functions to be used later
        """

        for instance in ['had', 'nug']:
            for size in self.max_hd_dict[instance]['instances']:
                qap_of = QAPObjectiveFunction(dat_file=instance+size+'.dat', sln_file=instance+size+'.sln')

                self.max_hd_dict[instance]['experiment_data']['objective function'].append(qap_of)

        for size in self.max_hd_dict['tsp']['instances']:
            tsp_of = TSPObjectiveFunction(num_points=size)

            self.max_hd_dict['tsp']['experiment_data']['objective function'].append(tsp_of)

    def find_max_hd(self):

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary, n):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(n))
            return binary

        start_code = time.time()
        for instance in ['tsp', 'had', 'nug']:
            for problem_index in range(len(self.max_hd_dict[instance]['instances'])):
                start_time = time.time()
                max_hd_list = []
                for iteration in range(100):

                    """
                    For each iteration, this function we will generate a random switch setting and build a LQUBO
                    around it.  Given that LQUBO it will generate the R squared of the LQUBO scatter plot and will 
                    increase in hamming dist if the R squared is above the 0.05 cutoff.  When a specified hamming 
                    dist is below the 0.05 cutoff it will be recorded.  When the 100 iterations are over, the val in
                    the max hd array is the average of each cutoff hamming distance.
                    """

                    objective_function = self.max_hd_dict[instance]['experiment_data']['objective function'][problem_index]

                    s = SortingNetwork(objective_function.n)
                    p = PermutationNetwork(objective_function.n)
                    if s.depth <= p.depth:
                        network = s
                    else:
                        network = p

                    n_qubo = network.depth

                    # Initialize random bitstring
                    q = np.random.randint(0, 2, size=n_qubo)
                    perm = network.permute(q)
                    v = objective_function(perm)
                    if self.num_activation_vec:
                        n_qubo = self.num_activation_vec
                    else:
                        n_qubo = network.depth

                    form_qubo = LQUBO(objective_function=objective_function,
                                      switch_network=network,
                                      num_activation_vectors=n_qubo,
                                      activation_vec_hamming_dist=self.activation_vec_hd).form_lqubo(q=q)

                    qubo = np.zeros((n_qubo, n_qubo))

                    basis = form_qubo[1]

                    for i in range(n_qubo):
                        for j in range(n_qubo):
                            if i <= j:
                                qubo[i][j] = form_qubo[0][(i, j)]

                    r_val = []
                    hamming_weight = []
                    for hamming_dist in range(n_qubo):

                        hamming_dist = hamming_dist + 1
                        hd = []
                        x = []
                        y = []

                        for i in range(self.num_points):
                            hd.append(np.zeros(n_qubo))

                        for i in range(len(hd)):
                            for j in range(hamming_dist):
                                hd[i][j] = 1
                            random_binary(hd[i], n_qubo)

                        for vec in hd:
                            q_new = np.mod(q + np.matmul(vec, basis), 2)
                            p_new = network.permute(q_new)
                            v_new = objective_function(p_new)
                            x.append(v_new - v)
                            y.append(np.matmul(np.matmul(vec, qubo), np.transpose(vec)))

                        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                        r_val.append(r_value ** 2)
                        hamming_weight.append(hamming_dist)

                        if r_value**2 < 0.05:
                            max_hd_list.append(hamming_weight[r_val.index(r_value**2)])
                            break

                avg_max_hd = stat.mean(max_hd_list)
                end_time = time.time()
                self.max_hd_dict[instance]['experiment_data']['max hd vals'].append(avg_max_hd)
                self.max_hd_dict[instance]['experiment_data']['time to compute max hd'].append(end_time - start_time)

        """
        In addition to computing the max hd val the max hd dict will record the total amount of time it took to generate
        the data as well as the time to compute the max hd for a specified objective function
        """

        end_code = time.time()
        self.max_hd_dict['total time to compute max hd code'].append(end_code - start_code)
        return self.max_hd_dict
