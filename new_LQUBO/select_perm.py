from new_LQUBO.next_perm import NextPerm
import numpy as np


class Select:

    def __init__(self,
                 objective_function=None,
                 response_record=None,
                 data_dict_p=None,
                 current_p=None):
        self.objective_function = objective_function
        self.n_qubo = self.objective_function.n - 1
        self.response_rec = response_record
        self.data_dict_p = data_dict_p
        self.current_p = current_p
        self.selection_made = False
        self.selected_p = 0
        self.selected_v = 0
        self.selected_response = 0

    @staticmethod
    def p_in_data(data, p):
        """
        Function designed to give a boolean if switch setting q is in the data_dict
        """
        # data is expected to be a list

        all_tests = []

        for arr in data:
            # arr is a numpy array

            comparison = arr == p

            # all elements of of numpy arrays are equal
            all_tests.append(np.all(comparison))

        # when the loop is done return if all of the arrays matched
        return any(all_tests)

    def select(self):

        for response in self.response_rec:
            next_perm = NextPerm(lqubo_result=response[0], current_perm=self.current_p).next_perm()
            if not self.p_in_data(data=self.data_dict_p, p=next_perm):
                self.selected_response = response
                self.selected_p = next_perm
                self.selected_v = self.objective_function(self.selected_p)
                self.selection_made = True
                return self.selected_p, self.selected_v, self.selected_response

        if not self.selection_made:
            self.selected_p = np.random.permutation(self.n_qubo + 1)
            self.selected_v = self.objective_function(self.selected_p)
            self.selected_response = "Random"
            return self.selected_p, self.selected_v, self.selected_response

