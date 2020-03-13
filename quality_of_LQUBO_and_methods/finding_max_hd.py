import numpy as np
import statistics as stat
from utilities.objective_functions import TSPObjectiveFunction, QAPObjectiveFunction
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from form_LQUBO.form_LQUBO_rand_slice import RandSliceLQUBO
from form_LQUBO.form_LQUBO_hd_slice import HDSliceLQUBO
from scipy import stats
import time


class MaxHDSolver:

    def __init__(self,
                 hd_slice=None,
                 num_points=200,
                 num_slice_vectors=None,
                 lqubo_type=None,):

        self.num_points = num_points
        self.hd_slice = hd_slice
        self.num_slice_vectors = num_slice_vectors

        had_qap = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}
        had_tsp = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}
        nug_qap = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}
        nug_tsp = {'objective function': [], 'max hd vals': [], 'time to compute max hd': []}

        had = {'qap': had_qap, 'tsp': had_tsp, 'instances': ['4', '6', '8', '10', '12', '14', '16']}
        nug = {'qap': nug_qap, 'tsp': nug_tsp, 'instances': ['12', '14', '15', '16a', '16b']}

        self.max_hd_dict = {'had': had, 'nug': nug, 'total time to compute max hd code': []}
        self.lqubo_type = lqubo_type

        for instance in ['had', 'nug']:
            for size in self.max_hd_dict[instance]['instances']:
                qap_of = QAPObjectiveFunction(dat_file=instance+size+'.dat', sln_file=instance+size+'.sln')
                tsp_of = TSPObjectiveFunction(dat_file=instance + size + '.dat', sln_file=instance + size + '.sln')

                self.max_hd_dict[instance]['qap']['objective function'].append(qap_of)
                self.max_hd_dict[instance]['tsp']['objective function'].append(tsp_of)

    def find_max_hd(self):

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary, n):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(n))
            return binary

        start_code = time.time()
        for instance in ['had', 'nug']:
            for problem in ['qap', 'tsp']:
                for problem_index in range(len(self.max_hd_dict[instance]['instances'])):
                    start_time = time.time()
                    max_hd_list = []
                    for iteration in range(100):
                        objective_function = self.max_hd_dict[instance][problem]['objective function'][problem_index]

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

                        if self.lqubo_type == 'LQUBO':
                            form_qubo = LQUBO(objective_function=objective_function,
                                              switch_network=network,
                                              n_qubo=n_qubo).form_lqubo(q=q)

                        elif self.lqubo_type == 'Rand Slice LQUBO':
                            form_qubo = RandSliceLQUBO(objective_function=objective_function,
                                                       switch_network=network,
                                                       n_qubo=n_qubo).form_lqubo(q=q)

                        elif self.lqubo_type == 'HD Slice LQUBO':
                            form_qubo = HDSliceLQUBO(objective_function=objective_function,
                                                     switch_network=network,
                                                     n_qubo=n_qubo,
                                                     slice_hd=self.hd_slice).form_lqubo(q=q)

                        else:
                            raise TypeError('LQUBO not recognized')

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
                    self.max_hd_dict[instance][problem]['max hd vals'].append(avg_max_hd)
                    self.max_hd_dict[instance][problem]['time to compute max hd'].append(start_time - end_time)
        end_code = time.time()
        self.max_hd_dict['total time to compute max hd code'].append(start_code - end_code)
        return self.max_hd_dict['had']['qap']['max hd vals'], self.max_hd_dict['had']['tsp']['max hd vals'], self.max_hd_dict['nug']['qap']['max hd vals'], self.max_hd_dict['nug']['tsp']['max hd vals'],
