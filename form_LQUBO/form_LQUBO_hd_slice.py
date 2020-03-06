import numpy as np


class HDSliceLQUBO:
    """
    Rather than forming a LQUBO using the basis vectors of the identity matrix to get the change in objective
    function that are 1 and 2 switch flips away from the current switch setting, instead we can take the basis vectors
    of a random matrix.  This technique (slicing) allows for bigger jumps in the space of possible switch settings.
    """
    def __init__(self,
                 objective_function=None,
                 switch_network=None,
                 n_qubo=None,
                 slice_hd=None,
                 num_slice_vectors=None):
        self.network = switch_network
        self.n_qubo = n_qubo
        self.slice_hd = slice_hd
        self.objective_function = objective_function
        if num_slice_vectors:
            self.num_slice_vectors = num_slice_vectors
        else:
            self.num_slice_vectors = self.n_qubo

    @staticmethod
    def swap(input_list, first_entry, second_entry):
        input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
        return input_list

    def random_binary(self, binary):
        for index in range(self.slice_hd):
            self.swap(binary, index, np.random.randint(self.n_qubo))
        return binary

    def form_hd_slice(self):
        """
        Function forms a random slice to form lqubo
        """
        hd_slice = []
        for i in range(self.num_slice_vectors):
            hd_slice.append(np.zeros(self.n_qubo))

        for i in range(len(hd_slice)):
            for j in range(self.slice_hd):
                hd_slice[i][j] = 1
            # only swap first n_qubo qubits to preserve total weight qubit
            self.random_binary(hd_slice[i][:self.n_qubo])

        return hd_slice

    def form_lqubo(self, q):

        p = self.network.permute(q)
        v = self.objective_function(p)
        qubo = dict()

        random_slice = self.form_hd_slice()

        for i in range(self.num_slice_vectors):
            delta_q = random_slice[i]
            q_new = np.mod(q + delta_q, 2)
            p_new = self.network.permute(q_new)
            v_new = self.objective_function(p_new)
            qubo[(i, i)] = v_new - v

        for i in range(self.num_slice_vectors):
            for j in range(i + 1, self.num_slice_vectors):
                delta_q = np.mod(random_slice[i] + random_slice[j], 2)
                q_new = np.mod(q + delta_q, 2)
                p_new = self.network.permute(q_new)
                v_new = self.objective_function(p_new)
                qubo[(i, j)] = v_new - v - qubo[(i, i)] - qubo[(j, j)]

        return qubo, random_slice, 0
