import numpy as np


class RandSliceLQUBO:
    """
    Rather than forming a LQUBO using the basis vectors of the identity matrix to get the change in objective
    function that are 1 and 2 switch flips away from the current switch setting, instead we can take the basis vectors
    of a random matrix.  This technique (slicing) allows for bigger jumps in the space of possible switch settings.
    """
    def __init__(self, objective_function=None, switch_network=None, n_qubo=None):
        self.network = switch_network
        self.n_qubo = n_qubo
        self.objective_function = objective_function

    def form_rand_slice(self):
        """
        Function forms a random slice to form lqubo
        """
        random_slice = []
        for i in range(self.n_qubo):
            random_slice.append(np.random.randint(0, 2, size=self.n_qubo))

        return random_slice

    def form_lqubo(self, q):

        p = self.network.permute(q)
        v = self.objective_function(p)
        qubo = dict()

        random_slice = self.form_rand_slice()

        for i in range(self.n_qubo):
            delta_q = random_slice[i]
            q_new = np.mod(q + delta_q, 2)
            p_new = self.network.permute(q_new)
            v_new = self.objective_function(p_new)
            qubo[(i, i)] = v_new - v

        for i in range(self.n_qubo):
            for j in range(i + 1, self.n_qubo):
                delta_q = np.mod(random_slice[i] + random_slice[j], 2)
                q_new = np.mod(q + delta_q, 2)
                p_new = self.network.permute(q_new)
                v_new = self.objective_function(p_new)
                qubo[(i, j)] = v_new - v - qubo[(i, i)] - qubo[(j, j)]

        return qubo, random_slice, 0
