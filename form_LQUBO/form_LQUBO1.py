import numpy as np


class LQUBO:

    def __init__(self,
                 objective_function=None,
                 switch_network=None,
                 num_activation_vectors=None,
                 activation_vec_hamming_dist=1,
                 max_hamming_dist=None):

        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError("Objective Function missing")

        if switch_network:
            self.switch_network = switch_network
        else:
            raise AttributeError("Switch Network Missing")

        if num_activation_vectors:
            self.n_qubo = num_activation_vectors
        else:
            raise AttributeError("Need to know size of LQUBO")

        self.activation_vec_hd = activation_vec_hamming_dist
        if max_hamming_dist > 2:
            self.max_hd = max_hamming_dist
        else:
            self.max_hd = None

    @staticmethod
    def swap(input_list, first_entry, second_entry):
        input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
        return input_list

    def form_activation_vector(self, binary):
        """
        Function forms a activation vector by swapping the first activation_vec_hd entries with random positions in
        the vector.  This results in a vector that has the length of the depth of the switch network and the
        hamming distance as defined by the class.
        """
        for index in range(self.activation_vec_hd):
            self.swap(binary, index, np.random.randint(self.switch_network.depth))
        return binary

    def form_activation_matrix(self):
        """
        Function forms an activation matrix based on number and hamming distance of activation vectors.
        """
        activation_matrix = []
        for i in range(self.n_qubo):
            activation_matrix.append(np.zeros(self.switch_network.depth))

        for i in range(len(activation_matrix)):
            for j in range(self.activation_vec_hd):
                activation_matrix[i][j] = 1
            # only swap first n_qubo qubits to preserve total weight qubit
            self.form_activation_vector(activation_matrix[i][:self.switch_network.depth])

        return activation_matrix

    def form_lqubo(self, q):

        if self.n_qubo == self.switch_network.depth and self.activation_vec_hd == 1:
            activation_matrix = np.identity(n=self.n_qubo)
        else:
            activation_matrix = self.form_activation_matrix()

        p = self.switch_network.permute(q)
        v = self.objective_function(p)
        qubo = dict()

        for i in range(self.n_qubo):
            delta_q = activation_matrix[i]
            q_new = np.mod(q + delta_q, 2)
            p_new = self.switch_network.permute(q_new)
            v_new = self.objective_function(p_new)
            qubo[(i, i)] = v_new - v

        for i in range(self.n_qubo):
            for j in range(i + 1, self.n_qubo):
                delta_q = np.mod(activation_matrix[i] + activation_matrix[j], 2)
                q_new = np.mod(q + delta_q, 2)
                p_new = self.switch_network.permute(q_new)
                v_new = self.objective_function(p_new)
                qubo[(i, j)] = v_new - v - qubo[(i, i)] - qubo[(j, j)]

        if self.max_hd:
            inverse = [(value, key) for key, value in qubo.items()]
            min_val = min(inverse)[0]
            max_val = max(inverse)[0]

            # penalty value
            p = (1.8 * (max_val + min_val)) / (1 - (self.max_hd / 2)) ** 2
            a = (self.max_hd + 2) / 2

            # Adding penalty into main qubo
            for i in range(self.n_qubo):
                qubo[(i, i)] = qubo[(i, i)] + (p - 2 * p * a)
                for j in range(i + 1, self.n_qubo):
                    qubo[(i, j)] = qubo[(i, j)] + 2 * p

        return qubo, activation_matrix

