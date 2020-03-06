import numpy as np


class LQUBO:
    """
    This class forms a LQUBO or a local approximation to the objective function, and can be evaluated by a D-Wave
    Quantum Annealer.  A local QUBO is formed by populating linear entries with change in objective function that are
    one switch flip away from the current setting and quadratic entries with change in objective function that are two
    switch flips away from the current switch setting.  By construction, the local QUBO will result in the exact change
    in objective function for vectors of hamming distance 1 and 2.
    """
    def __init__(self, objective_function=None, switch_network=None, n_qubo=None):
        self.network = switch_network
        self.n_qubo = n_qubo
        self.objective_function = objective_function

    def form_lqubo(self, q):
        p = self.network.permute(q)
        v = self.objective_function(p)
        ident = np.identity(self.n_qubo)
        qubo = dict()

        for i in range(self.n_qubo):
            delta_q = ident[i, :]
            q_new = np.mod(q + delta_q, 2)
            p_new = self.network.permute(q_new)
            v_new = self.objective_function(p_new)
            qubo[(i, i)] = v_new - v

        for i in range(self.n_qubo):
            for j in range(i + 1, self.n_qubo):
                delta_q = ident[i, :] + ident[j, :]
                q_new = np.mod(q + delta_q, 2)
                p_new = self.network.permute(q_new)
                v_new = self.objective_function(p_new)
                qubo[(i, j)] = v_new - v - qubo[(i, i)] - qubo[(j, j)]

        return qubo, ident, 0
