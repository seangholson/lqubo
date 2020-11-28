import numpy as np


class NewLQUBO:
    """
    This class forms a LQUBO or a local approximation to the objective function, and can be evaluated by a D-Wave
    Quantum Annealer.  A local QUBO is formed by populating linear entries with change in objective function that are
    one switch flip away from the current setting and quadratic entries with change in objective function that are two
    switch flips away from the current switch setting.  By construction, the local QUBO will result in the exact change
    in objective function for vectors of hamming distance 1 and 2.
    """
    def __init__(self,
                 objective_function=None):

        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError("Objective Function missing")

    @staticmethod
    def single_swap(input_list, entry):
        output_list = input_list.copy()
        output_list[0], output_list[entry] = output_list[entry], output_list[0]
        return output_list

    @staticmethod
    def double_swap(input_list, entry1, entry2):
        output_list = input_list.copy()
        output_list[0], output_list[entry1] = output_list[entry1], output_list[0]
        output_list[0], output_list[entry2] = output_list[entry2], output_list[0]
        return output_list

    def form_lqubo(self, p):
        v = self.objective_function(p)
        n_qubo = len(p) - 1
        qubo = dict()
        for i in range(n_qubo):
            p_new = self.single_swap(p, i + 1)
            v_new = self.objective_function(p_new)
            qubo[(i, i)] = v_new - v

        for i in range(n_qubo):
            for j in range(i + 1, n_qubo):
                p_new = self.double_swap(p, i + 1, j + 1)
                v_new = self.objective_function(p_new)
                qubo[(i, j)] = v_new - v - qubo[(i, i)] - qubo[(j, j)]

        return qubo





