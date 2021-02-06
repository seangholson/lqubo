import numpy as np


class TournamentSelection:

    def __init__(self,
                 final_population_size=None,
                 previous_population=None,
                 lqubo_population=None,
                 objective_function=None):

        if objective_function:
            self.objective_function = objective_function
        else:
            raise TypeError('Objective Function Missing')

        self.final_population_size = final_population_size
        self.total_population = previous_population + lqubo_population

    # Select 4 random chromosomes and best fit of 4 pass selection
    def tournament_selection(self, population):
        rand_chromosomes = []
        fitness = []
        for _ in range(4):
            chromosome = population[np.random.randint(0, len(population))]
            rand_chromosomes.append(chromosome)
            fitness.append(self.objective_function(chromosome))

        return rand_chromosomes[fitness.index(min(fitness))]

    def select_population(self):

        selected_population = []
        for _ in range(self.final_population_size):
            selected_population.append(self.tournament_selection(population=self.total_population))
        return selected_population


class BestFitPopulation:

    def __init__(self,
                 final_population_size=None,
                 previous_population=None,
                 lqubo_population=None,
                 objective_function=None):

        if objective_function:
            self.objective_function = objective_function
        else:
            raise TypeError('Objective Function Missing')

        self.final_population_size = final_population_size
        self.total_population = previous_population + lqubo_population

    @staticmethod
    def sort_first(val):
        return val[0]

    def order_responses(self):

        ordered_response = []
        for perm in self.total_population:
            v_new = self.objective_function(perm)
            ordered_response.append([v_new, perm])

        ordered_response.sort(key=self.sort_first)

        return ordered_response

    def return_population(self):

        ordered_responses = self.order_responses()
        selected_population = []
        for index in range(self.final_population_size):
            selected_population.append(ordered_responses[index][1])

        return selected_population


