import numpy as np
import statistics as stat
from utilities.objective_functions import TSPObjectiveFunction, QAPObjectiveFunction
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from form_LQUBO.form_LQUBO_rand_slice import RandSliceLQUBO
from form_LQUBO.form_LQUBO_hd_slice import HDSliceLQUBO
from scipy import stats


class MaxHDSolver:

    def __init__(self,
                 hd_slice=None,
                 num_points=200,
                 num_slice_vectors=None,
                 lqubo_type=None,):

        self.num_points = num_points

        had_qap = {'qubos': [], 'basis': [], 'objective function': [], 'q': [], 'max hd vals': []}
        had_tsp = {'qubos': [], 'basis': [], 'objective function': [], 'q': [], 'max hd vals': []}
        nug_qap = {'qubos': [], 'basis': [], 'objective function': [], 'q': [], 'max hd vals': []}
        nug_tsp = {'qubos': [], 'basis': [], 'objective function': [], 'q': [], 'max hd vals': []}

        had = {'qap': had_qap, 'tsp': had_tsp, 'instances': ['4', '6', '8', '10', '12', '14', '16']}
        nug = {'qap': nug_qap, 'tsp': nug_tsp, 'instances': ['12', '14', '15', '16a', '16b']}

        self.max_hd_dict = {'had': had, 'nug': nug}
        self.lqubo_type = lqubo_type

        for instance in ['had', 'nug']:
            for size in self.max_hd_dict[instance]['instances']:
                qap_of = QAPObjectiveFunction(dat_file=instance+size+'.dat', sln_file=instance+size+'.sln')
                tsp_of = TSPObjectiveFunction(dat_file=instance + size + '.dat', sln_file=instance + size + '.sln')

                self.max_hd_dict[instance]['qap']['objective function'].append(qap_of)
                self.max_hd_dict[instance]['tsp']['objective function'].append(tsp_of)

                s = SortingNetwork(qap_of.n)
                p = PermutationNetwork(qap_of.n)
                if s.depth <= p.depth:
                    network = s
                else:
                    network = p

                n_qubo = network.depth

                # Initialize random bitstring
                q = np.random.randint(0, 2, size=n_qubo)
                self.max_hd_dict[instance]['qap']['q'].append(q)
                self.max_hd_dict[instance]['tsp']['q'].append(q)

                if lqubo_type == 'LQUBO':
                    form_qap_qubo = LQUBO(objective_function=qap_of,
                                          switch_network=network,
                                          n_qubo=n_qubo).form_lqubo(q=q)
                    form_tsp_qubo = LQUBO(objective_function=tsp_of,
                                          switch_network=network,
                                          n_qubo=n_qubo).form_lqubo(q=q)

                elif lqubo_type == 'Rand Slice LQUBO':
                    form_qap_qubo = RandSliceLQUBO(objective_function=qap_of,
                                                   switch_network=network,
                                                   n_qubo=n_qubo).form_lqubo(q=q)
                    form_tsp_qubo = RandSliceLQUBO(objective_function=tsp_of,
                                                   switch_network=network,
                                                   n_qubo=n_qubo).form_lqubo(q=q)

                elif lqubo_type == 'HD Slice LQUBO':
                    form_qap_qubo = HDSliceLQUBO(objective_function=qap_of,
                                                 switch_network=network,
                                                 n_qubo=n_qubo,
                                                 slice_hd=hd_slice).form_lqubo(q=q)
                    form_tsp_qubo = HDSliceLQUBO(objective_function=tsp_of,
                                                 switch_network=network,
                                                 n_qubo=n_qubo,
                                                 slice_hd=hd_slice).form_lqubo(q=q)
                else:
                    raise TypeError('LQUBO not recognized')

                qap_qubo = np.zeros((n_qubo, n_qubo))
                tsp_qubo = np.zeros((n_qubo, n_qubo))

                qap_basis = form_qap_qubo[1]
                tsp_basis = form_tsp_qubo[1]

                for i in range(n_qubo):
                    for j in range(n_qubo):
                        if i <= j:
                            qap_qubo[i][j] = form_qap_qubo[0][(i, j)]
                            tsp_qubo[i][j] = form_tsp_qubo[0][(i, j)]

                self.max_hd_dict[instance]['qap']['basis'].append(qap_basis)
                self.max_hd_dict[instance]['tsp']['basis'].append(tsp_basis)
                self.max_hd_dict[instance]['qap']['qubos'].append(qap_qubo)
                self.max_hd_dict[instance]['tsp']['qubos'].append(tsp_qubo)

    def find_max_hd(self):

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary, n_qubo):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(n_qubo))
            return binary

        for instance in ['had', 'nug']:
            for problem in ['qap', 'tsp']:
                for problem_index in range(len(self.max_hd_dict[instance]['instances'])):
                    max_hd_list = []

                    objective_function = self.max_hd_dict[instance][problem]['objective function'][problem_index]

                    s = SortingNetwork(objective_function.n)
                    p = PermutationNetwork(objective_function.n)
                    if s.depth <= p.depth:
                        network = s
                    else:
                        network = p

                    n_qubo = network.depth

                    if self.lqubo_type == 'LQUBO':
                        basis = np.identity(network.depth)
                    else:
                        basis = self.max_hd_dict[instance][problem]['basis'][problem_index]

                    q = self.max_hd_dict[instance][problem]['q'][problem_index]
                    p = network.permute(q)
                    v = objective_function(p)

                    for iteration in range(20):
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
                                y.append(np.matmul(np.matmul(vec, self.max_hd_dict[instance][problem]['qubos'][problem_index]), np.transpose(vec)))

                            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                            r_val.append(r_value ** 2)
                            hamming_weight.append(hamming_dist)

                            if r_value**2 < 0.1:
                                max_hd_list.append(hamming_weight[r_val.index(r_value**2)])
                                break

                    avg_max_hd = stat.mean(max_hd_list)
                    self.max_hd_dict[instance][problem]['max hd vals'].append(round(avg_max_hd))

        return self.max_hd_dict['had']['qap']['max hd vals'], self.max_hd_dict['had']['tsp']['max hd vals'], self.max_hd_dict['nug']['qap']['max hd vals'], self.max_hd_dict['nug']['tsp']['max hd vals'],
