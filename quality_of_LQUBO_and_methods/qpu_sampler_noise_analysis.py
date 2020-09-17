import numpy as np
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import statistics as stat
import pandas as pd


def remove_redundant_binaries(binary_list, delta_switch):
    return[value for value in binary_list if np.all(value == delta_switch) != True]


class QPUUniqueReads:

    def __init__(self,
                 objective_function=None,
                 num_reads=None,
                 num_iters=None):

        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError('Objective function missing.')

        if 'nug' in self.objective_function.dat_file:
            instance = self.objective_function.dat_file.replace('nug', '')
        else:
            instance = self.objective_function.dat_file.replace('had', '')

        if num_reads:
            self.num_reads = num_reads
        else:
            self.num_reads = 100

        if num_iters:
            self.num_iters = num_iters
        else:
            self.num_iters = 100

        self.dwave_solver = EmbeddingComposite(DWaveSampler())

        self.n_qap = self.objective_function.n
        s = SortingNetwork(self.n_qap)
        p = PermutationNetwork(self.n_qap)
        if s.depth <= p.depth:
            self.network = s
        else:
            self.network = p

        self.n_qubo = self.network.depth
        self.data = {'average': [], 'standard deviation': [], 'domain with QUBO size': [instance + '({})'.format(
            self.n_qubo)]}

    def take_data_csv(self):

        sampler_kwargs = {
            'num_reads': self.num_reads
        }
        unique_bin_val = []
        for _ in range(self.num_iters):

            binary_vals = []

            q = np.random.randint(0, 2, size=self.n_qubo)
            qubo = LQUBO(objective_function=self.objective_function, switch_network=self.network, n_qubo=self.n_qubo)
            formed_qubo = qubo.form_lqubo(q=q)[0]

            response = self.dwave_solver.sample_qubo(formed_qubo, **sampler_kwargs)
            reads = response.record
            for read in reads:
                for num_occurrence in range(read[2]):
                    binary_vals.append(read[0])

            num_unique_binary = 0
            while len(binary_vals) != 0:
                num_unique_binary += 1
                delta_q = binary_vals[0]
                binary_vals = remove_redundant_binaries(binary_list=binary_vals, delta_switch=delta_q)

                unique_bin_val.append(num_unique_binary)

        self.data['average'].append(stat.mean(unique_bin_val))
        self.data['standard deviation'].append(stat.stdev(unique_bin_val))
        data = pd.DataFrame(data=self.data)
        data.to_csv('./results/noise_analysis/QPU' + self.objective_function.dat_file.replace('.dat', '') + '.csv')


