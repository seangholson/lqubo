import numpy as np


class LQUBOWithPenalty:
    """
    When the Local QUBO is unconstrained we find that this approximation gets worse as the hamming weight of the
    resulting delta_q vector increases (when more switches are flipped, it is less likely to get a decrease in objective
    function).  This class incorporates the quadratic penalty for lower hamming weight vectors.
    """
    def __init__(self, objective_function=None, switch_network=None, n_qubo=None, max_hd=None):
        self.network = switch_network
        self.n_qubo = n_qubo
        self.objective_function = objective_function
        self.max_hd = max_hd

    def form_lqubo(self, q):

        p = self.network.permute(q)
        v = self.objective_function(p)
        ident = np.identity(self.n_qubo)
        qubo = dict()

        # main QUBO without penalty
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

        inverse = [(value, key) for key, value in qubo.items()]
        min_val = min(inverse)[0]
        max_val = max(inverse)[0]

        # penalty value
        p = (1.8*(max_val + abs(min_val)))/(1 - (self.max_hd/2))**2
        a = (self.max_hd + 2)/2

        # Adding penalty into main qubo
        for i in range(self.n_qubo):
            qubo[(i, i)] = qubo[(i, i)] + (p - 2*p*a)
            for j in range(i + 1, self.n_qubo):
                qubo[(i, j)] = qubo[(i, j)] + 2*p

        return qubo, ident, p*((self.max_hd + 2)/2)**2


