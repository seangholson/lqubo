import numpy as np
from perm_LQUBO.form_new_LQUBO import NewLQUBO
from perm_LQUBO.population_LQUBO_code.initialize_population import initialize_population
from perm_LQUBO.population_LQUBO_code.tournament_selection import TournamentSelection, BestFitPopulation
from perm_LQUBO.population_LQUBO_code.evaluate_fitness import evaluate_fitness, max_fitness, min_fitness, avg_fitness
from perm_LQUBO.population_LQUBO_code.collect_lqubo_population import CollectLQUBOPopulation

from dimod import SimulatedAnnealingSampler
from tabu import TabuSampler
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import time


class Solver:
    """
    This is the base class for the solver method.
    """
    def __init__(self, objective_function=None):
        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError('Objective function missing.')

    def minimize_objective(self):
        raise NotImplementedError


class PopulationLQUBOSolver(Solver):
    """
    The Local-QUBO Solver uses a switch/permutation network to encode the QAP permutation
    in a bitstring.
    """
    def __init__(self,
                 objective_function=None,
                 dwave_sampler=None,
                 dwave_sampler_kwargs=None,
                 experiment_type=None,
                 population_size=1,
                 num_reads=1,
                 num_iters=None):
        super().__init__(objective_function=objective_function)

        self.n_obj = self.objective_function.n

        self.n_qubo = self.n_obj - 1
        self.dwave_solver = None
        self.sampler_kwargs = None
        self.qpu = False
        self.population_size = population_size
        self.num_reads = num_reads

        # Initialize dwave sampler:
        if dwave_sampler == 'QPU':
            self.dwave_solver = EmbeddingComposite(DWaveSampler())
            self.qpu = True
            if dwave_sampler_kwargs:
                self.sampler_kwargs = dwave_sampler_kwargs
            else:
                self.sampler_kwargs = dict()
        elif dwave_sampler == 'SA':
            self.dwave_solver = SimulatedAnnealingSampler()
            if num_reads:
                self.sampler_kwargs = {
                    'num_reads': num_reads
                }
            else:
                self.sampler_kwargs = {
                    'num_reads': 25
                }
        elif dwave_sampler == 'Tabu':
            self.dwave_solver = TabuSampler()
            if num_reads:
                self.sampler_kwargs = {
                    'num_reads': num_reads
                }
            else:
                self.sampler_kwargs = {
                    'num_reads': 250
                }

        self.stopwatch = 0

        if experiment_type == 'time_lim':
            self.n_iters = 1000
            self.time_limit = 30

        if experiment_type == 'iter_lim' and num_iters:
            self.n_iters = num_iters
            self.time_limit = False
        else:
            self.n_iters = 50
            self.time_limit = False

        self.form_qubo = NewLQUBO(objective_function=self.objective_function)

        self.solution = self.objective_function.min_v

    def minimize_objective(self):
        start_code = time.time()

        population = initialize_population(population_size=self.population_size, n_obj=self.n_obj)
        evaluated_fitness = evaluate_fitness(population=population, objective_function=self.objective_function)
        max_fit = max_fitness(fitness_array=evaluated_fitness)
        min_fit = min_fitness(fitness_array=evaluated_fitness)
        avg_fit = avg_fitness(fitness_array=evaluated_fitness)

        data_dict = dict()
        data_dict['max_fitness'] = [max_fit]
        data_dict['min_fitness'] = [min_fit]
        data_dict['avg_fitness'] = [avg_fit]

        # Initialize bitstring

        begin_loop = time.time()
        self.stopwatch = begin_loop - start_code
        for iteration in range(self.n_iters):

            # If there is a timing limit and the stopwatch is greater than the timing limit then break
            if self.time_limit and self.time_limit <= self.stopwatch:
                break
            start_iteration = time.time()

            total_lqubo_population = []
            for perm in population:
                lqubo = self.form_qubo.form_lqubo(p=perm)

                # Solve the LQUBO for new permutations
                if self.qpu:
                    self.sampler_kwargs.update({
                        'chain_strength': 1.5*abs(max(lqubo.values(), key=abs)),
                        'num_reads': 1000
                    })

                response = self.dwave_solver.sample_qubo(lqubo, **self.sampler_kwargs)
                lqubo_population = CollectLQUBOPopulation(objective_function=self.objective_function,
                                                          response_record=response.record,
                                                          current_perm=perm).collect_population()
                total_lqubo_population += lqubo_population

            tournament_selection = BestFitPopulation(final_population_size=self.population_size,
                                                     lqubo_population=total_lqubo_population,
                                                     previous_population=population,
                                                     objective_function=self.objective_function)

            # Compile new population from tournament selection
            population = tournament_selection.return_population()
            evaluated_fitness = evaluate_fitness(population=population, objective_function=self.objective_function)
            max_fit = max_fitness(fitness_array=evaluated_fitness)
            min_fit = min_fitness(fitness_array=evaluated_fitness)
            avg_fit = avg_fitness(fitness_array=evaluated_fitness)

            data_dict['max_fitness'].append(max_fit)
            data_dict['min_fitness'].append(min_fit)
            data_dict['avg_fitness'].append(avg_fit)

            end_iteration = time.time()
            self.stopwatch += end_iteration - start_iteration

        end_code = time.time()
        timing_code = end_code - start_code

        lqubo_ans = min(data_dict['max_fitness'])
        num_iters = len(data_dict['max_fitness']) - 1

        if lqubo_ans == self.solution:
            obtain_optimal = 1
            percent_error = 0
        else:
            percent_error = abs(self.solution - lqubo_ans) / self.solution * 100
            obtain_optimal = 0

        return lqubo_ans, percent_error, obtain_optimal, timing_code, num_iters, data_dict, data_dict['max_fitness']
