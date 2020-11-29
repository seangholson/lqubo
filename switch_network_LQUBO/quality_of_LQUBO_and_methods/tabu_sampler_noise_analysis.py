import numpy as np
from switch_network_LQUBO.switch_networks.switch_networks import SortingNetwork, PermutationNetwork
from switch_network_LQUBO.form_LQUBO.form_LQUBO import LQUBO
from utilities.objective_functions import QAPObjectiveFunction
from tabu import TabuSampler
import statistics as stat
import matplotlib.pyplot as plt
import pandas as pd


def remove_redundant_binaries(binary_list, delta_switch):
    return[value for value in binary_list if np.all(value == delta_switch) != True]


class NumUniqueReadsHad:

    def __init__(self,
                 num_reads=None,
                 num_trials=None):

        self.domain = ['4', '6', '8', '10', '12', '14', '16', '18', '20']
        objective_functions = []
        for size in self.domain:
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

        dwave_solver = TabuSampler()

        self.data = {'average': [], 'standard deviation': [], 'domain': self.domain, 'domain with QUBO size': []}
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
                qubo = LQUBO(objective_function=objective_function, switch_network=network, num_activation_vectors=network.depth)
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

        domain = ['4', '6', '8', '10', '12', '14', '16']
        qpu_data = {'average': [], 'standard_deviation': [], 'domain with QUBO size': []}
        for instance in range(len(domain)):
            qpu_data['average'].append(pd.read_csv('./results/noise_analysis/QPUhad' + domain[instance] + '.csv')[
                                           'average'][0])
            qpu_data['standard_deviation'].append(pd.read_csv('./results/noise_analysis/QPUhad' + domain[instance] +
                                                              '.csv')['standard deviation'][0])
            qpu_data['domain with QUBO size'].append(self.data['domain with QUBO size'][instance])

        plt.errorbar(x=qpu_data['domain with QUBO size'], y=qpu_data['average'], yerr=qpu_data['standard_deviation'],
                     label='QPU')
        plt.scatter(x=qpu_data['domain with QUBO size'], y=qpu_data['average'])
        plt.errorbar(x=self.data['domain with QUBO size'], y=self.data['average'], yerr=self.data['standard deviation'],
                     label='Tabu')
        plt.scatter(x=self.data['domain with QUBO size'], y=self.data['average'])
        plt.xlabel("QAP Size (QUBO Size)")
        plt.ylabel("Number of Unique Reads (Out of {} Reads)".format(self.num_reads))
        plt.suptitle("'Noise' Analysis of D-Wave Tabu Sampler (had)")
        plt.legend(loc='upper left')
        plt.show()


class NumUniqueReadsNug:

    def __init__(self,
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

        dwave_solver = TabuSampler()

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
                qubo = LQUBO(objective_function=objective_function, switch_network=network, num_activation_vectors=network.depth)
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

        domain = ['12', '14', '15', '16a', '16b']
        qpu_data = {'average': [], 'standard_deviation': [], 'domain with QUBO size': []}
        for instance in range(len(domain)):
            qpu_data['average'].append(pd.read_csv('./results/noise_analysis/QPUnug' + domain[instance] + '.csv')[
                                           'average'][0])
            qpu_data['standard_deviation'].append(pd.read_csv('./results/noise_analysis/QPUnug' + domain[instance] +
                                                              '.csv')['standard deviation'][0])
            qpu_data['domain with QUBO size'].append(self.data['domain with QUBO size'][instance])

        plt.errorbar(x=qpu_data['domain with QUBO size'], y=qpu_data['average'], yerr=qpu_data['standard_deviation'],
                     label='QPU')
        plt.scatter(x=qpu_data['domain with QUBO size'], y=qpu_data['average'])
        plt.errorbar(x=self.data['domain with QUBO size'], y=self.data['average'], yerr=self.data['standard deviation'],
                     label='Tabu')
        plt.scatter(x=self.data['domain with QUBO size'], y=self.data['average'])
        plt.xlabel("QAP Size (QUBO Size)")
        plt.ylabel("Number of Unique Reads (Out of {} Reads)".format(self.num_reads))
        plt.suptitle("'Noise' Analysis of D-Wave Tabu Sampler (nug)")
        plt.legend(loc='upper left')
        plt.show()


had = NumUniqueReadsHad(num_trials=100, num_reads=100)
nug = NumUniqueReadsNug(num_trials=100, num_reads=100)
had.plot_data()
nug.plot_data()
