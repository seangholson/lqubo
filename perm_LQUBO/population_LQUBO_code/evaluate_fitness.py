import numpy as np


def evaluate_fitness(population=None, objective_function=None):
    fitness_array = []
    for member in population:
        fitness_array.append(objective_function(member))

    return fitness_array


def max_fitness(fitness_array=None):

    return min(fitness_array)


def min_fitness(fitness_array=None):

    return max(fitness_array)


def avg_fitness(fitness_array=None):

    return np.average(fitness_array)

