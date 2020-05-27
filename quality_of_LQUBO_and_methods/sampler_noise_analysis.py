import numpy as np
from switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from form_LQUBO.form_LQUBO import LQUBO
from utilities.objective_functions import QAPObjectiveFunction
from dimod import SimulatedAnnealingSampler
from tabu import TabuSampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import statistics as stat
import matplotlib.pyplot as plt


def remove_redundant_binaries(binary_list, delta_switch):
    return[value for value in binary_list if np.all(value == delta_switch) != True]


class NumUniqueReadsHad:

    def __init__(self,
                 sampler=None,
                 num_reads=None,
                 num_trials=None):

        domain = ['4', '6', '8', '10', '12', '14', '16', '18', '20']
        objective_functions = []
        for size in domain:
            objective_functions.append(QAPObjectiveFunction(dat_file='had'+size+'.dat'))
        if num_reads:
            self.num_reads = num_reads
        else:
            self.num_reads = 100

        sampler_kwargs = {
            'num_reads': self.num_reads
        }

        if num_trials:
            num_trials = num_trials
        else:
            num_trials = 100

        if sampler == 'QPU':
            dwave_solver = EmbeddingComposite(DWaveSampler())
        elif sampler == 'SA':
            dwave_solver = SimulatedAnnealingSampler()
        elif sampler == 'Tabu':
            dwave_solver = TabuSampler()
        else:
            raise TypeError("Invalid Sampler Type")

        self.data = {'average': [], 'standard deviation': [], 'domain': domain, 'domain with QUBO size': []}
        for objective_function in objective_functions:
            n_qap = objective_function.n
            s = SortingNetwork(n_qap)
            p = PermutationNetwork(n_qap)
            if s.depth <= p.depth:
                network = s
            else:
                network = p
            self.data['domain with QUBO size'].append('{} ({})'.format(n_qap, network.depth))
            unique_bin_val = []
            for trial in range(num_trials):
                binary_vals = []

                q = np.random.randint(0, 2, size=network.depth)
                qubo = LQUBO(objective_function=objective_function, switch_network=network, n_qubo=network.depth)
                formed_qubo = qubo.form_lqubo(q=q)[0]

                response = dwave_solver.sample_qubo(formed_qubo, **sampler_kwargs)
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

    def plot_data(self):

        plt.errorbar(x=self.data['domain with QUBO size'], y=self.data['average'], yerr=self.data['standard deviation'])
        plt.scatter(x=self.data['domain with QUBO size'], y=self.data['average'])
        plt.xlabel("QAP Size (QUBO Size)")
        plt.ylabel("Number of Unique Reads (Out of {} Reads)".format(self.num_reads))
        plt.suptitle("'Noise' Analysis of D-Wave Tabu Sampler (had)")
        plt.show()


class NumUniqueReadsNug:

    def __init__(self,
                 sampler=None,
                 num_reads=None,
                 num_trials=None):

        domain = ['12', '14', '15', '16a', '16b', '17', '18', '20']
        objective_functions = []
        for size in domain:
            objective_functions.append(QAPObjectiveFunction(dat_file='nug'+size+'.dat'))
        if num_reads:
            self.num_reads = num_reads
        else:
            self.num_reads = 100

        sampler_kwargs = {
            'num_reads': self.num_reads
        }

        if num_trials:
            num_trials = num_trials
        else:
            num_trials = 100

        if sampler == 'QPU':
            dwave_solver = EmbeddingComposite(DWaveSampler())
        elif sampler == 'SA':
            dwave_solver = SimulatedAnnealingSampler()
        elif sampler == 'Tabu':
            dwave_solver = TabuSampler()
        else:
            raise TypeError("Invalid Sampler Type")

        self.data = {'average': [], 'standard deviation': [], 'domain': domain, 'domain with QUBO size': []}
        for objective_function in objective_functions:
            n_qap = objective_function.n
            s = SortingNetwork(n_qap)
            p = PermutationNetwork(n_qap)
            if s.depth <= p.depth:
                network = s
            else:
                network = p
            self.data['domain with QUBO size'].append('{} ({})'.format(objective_function.dat_file.replace('nug', '').
                                                                       replace('.dat', ''), network.depth))
            unique_bin_val = []
            for trial in range(num_trials):
                binary_vals = []

                q = np.random.randint(0, 2, size=network.depth)
                qubo = LQUBO(objective_function=objective_function, switch_network=network, n_qubo=network.depth)
                formed_qubo = qubo.form_lqubo(q=q)[0]

                response = dwave_solver.sample_qubo(formed_qubo, **sampler_kwargs)
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

    def plot_data(self):

        plt.errorbar(x=self.data['domain with QUBO size'], y=self.data['average'], yerr=self.data['standard deviation'])
        plt.scatter(x=self.data['domain with QUBO size'], y=self.data['average'])
        plt.xlabel("QAP Size (QUBO Size)")
        plt.ylabel("Number of Unique Reads (Out of {} Reads)".format(self.num_reads))
        plt.suptitle("'Noise' Analysis of D-Wave Tabu Sampler (nug)")
        plt.show()


had = NumUniqueReadsHad(sampler='Tabu', num_trials=100, num_reads=250)
nug = NumUniqueReadsNug(sampler='Tabu', num_trials=100, num_reads=250)
had.plot_data()
nug.plot_data()
