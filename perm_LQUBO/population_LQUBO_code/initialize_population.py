import numpy as np


def initialize_population(population_size=None, n_obj=None):

    initial_population = []
    for _ in range(population_size):
        initial_population.append(np.random.permutation(n_obj))

    return initial_population

