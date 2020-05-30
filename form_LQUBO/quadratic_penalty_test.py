from tabu import TabuSampler
import statistics as stat
from form_LQUBO.form_LQUBO_penalty import LQUBOWithPenalty
from utilities.objective_functions import QAPObjectiveFunction
from switch_networks.switch_networks import PermutationNetwork

obj = QAPObjectiveFunction(dat_file='had20.dat', sln_file='had20.sln')
network = PermutationNetwork(n=obj.n)
n_qubo = network.depth

qubo = LQUBOWithPenalty(objective_function=obj, switch_network=network, n_qubo=n_qubo)

kwargs = {
    'num_reads': 100
}

max_hd = 13


response = TabuSampler().sample_qubo(qubo[0], **kwargs)

# collect all binary reads from response and analyze hamming dist of read
binary_reads = []
for read in response.record:
    for num_occurrence in range(read[2]):
        binary_reads.append(read[0])

hamming_dist = []
for binary in binary_reads:
    hamming_dist.append(sum(binary))

print("Average hamming dist: {}".format(stat.mean(hamming_dist)))
print("Std Dev of hamming dist: {}".format(stat.stdev(hamming_dist)))
print("Expected hamming dist in range: 2 - {}".format(max_hd))




