from tabu import TabuSampler
import statistics as stat


qubo = dict()
n_qubo = 129

kwargs = {
    'num_reads': 100
}

max_hd = 13


max_val = 20
min_val = 0

p = (1.8 * (max_val + abs(min_val))) / (1 - (max_hd / 2)) ** 2
a = (max_hd + 2) / 2

for i in range(n_qubo):
    qubo[(i, i)] = 0

for i in range(n_qubo):
    for j in range(i + 1, n_qubo):
        qubo[(i, j)] = 0


# Adding penalty into main qubo
for i in range(n_qubo):
    qubo[(i, i)] = qubo[(i, i)] + (p - 2 * p * a)
    for j in range(i + 1, n_qubo):
        qubo[(i, j)] = qubo[(i, j)] + 2 * p

response = TabuSampler().sample_qubo(qubo, **kwargs)

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




