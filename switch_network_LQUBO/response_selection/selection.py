import numpy as np


class CheckAndSelect:
    """
    Check and select class is designed to take all or the first 50 QPU responses (depending on length of
    response.record) and order the responses by which responses have the greatest change in objective function.
    Then by evaluating q_in_data we either select a new switch setting in the ordered list or pick a random
    switch setting.
    """
    def __init__(self,
                 objective_function=None,
                 switch_network=None,
                 response_record=None,
                 delta_q_basis=None,
                 data_dict_qvecs=None,
                 current_q=None):

        self.objective_function = objective_function
        self.network = switch_network
        self.n_qubo = self.network.depth
        self.response_rec = response_record
        self.data_dict_qvecs = data_dict_qvecs
        self.delta_q_basis = delta_q_basis
        self.current_q = current_q
        self.all_q_in_data = True
        self.selected_q = 0
        self.selected_p = 0
        self.selected_v = 0
        self.selected_response = 0

    @staticmethod
    def sort_first(val):
        return val[0]

    @staticmethod
    def q_in_data(data, q):
        """
        Function designed to give a boolean if switch setting q is in the data_dict
        """
        # data is expected to be a list

        all_tests = []

        for arr in data:
            # arr is a numpy array

            comparison = arr == q

            # all elements of of numpy arrays are equal
            all_tests.append(np.all(comparison))

        # when the loop is done return if all of the arrays matched
        return any(all_tests)

    def order_responses(self, response_list):
        """
        Function designed to compile a nested list with the first entry being the new objective function value of a
        given response.  Then it will sort the list from smallest new OF value to greatest new OF value.
        """
        ordered_response = []
        for response in response_list:
            q_new = np.mod(self.current_q + np.matmul(response[0], self.delta_q_basis), 2)
            p_new = self.network.permute(q_new)
            v_new = self.objective_function(p_new)
            ordered_response.append([v_new, q_new, p_new, response[0]])

        ordered_response.sort(key=self.sort_first)

        return ordered_response

    def select_response(self, ordered_response):
        """
        Function that will go through the ordered response list and check if the new switch settings that correspond
        with low new objective function values are in the data dict. If not then we select and return the vals
        associated with that response.  If so, all_q_in_data will remain true and will feed into decision for check
        and select fcn.
        """
        for response in ordered_response:
            if not self.q_in_data(q=response[1], data=self.data_dict_qvecs):
                self.selected_q = response[1]
                self.selected_v = response[0]
                self.selected_p = response[2]
                self.selected_response = response[3]
                self.all_q_in_data = False
                break

        return self.selected_q, self.selected_p, self.selected_v, self.selected_response

    def select(self):
        """
        First check if there are more than 50 responses.  If so then take the assign response list to be the first 50
        values, otherwise let response list be equal to the response variable.
        """
        if len(self.response_rec) < 50:
            more_responses = False
            response_list = self.response_rec
        else:
            more_responses = True
            response_list = self.response_rec[:50]

        """
        Then order the responses and select
        """
        ordered_responses = self.order_responses(response_list=response_list)
        selection = self.select_response(ordered_response=ordered_responses)

        if not self.all_q_in_data:
            """
            If there is a response in the ordered responses that doesn't result in a new q that is not in the data dict 
            then return the selection
            """
            return selection[0], selection[1], selection[2], selection[3]
        elif self.all_q_in_data and more_responses:
            """
            If all response vals result in a new q that is already in data dict AND there are more than 50 responses in
            the response variable, then order and select from the remaining response values. 
            """
            response_list = self.response_rec[50:]
            ordered_responses = self.order_responses(response_list=response_list)
            selection = self.select_response(ordered_response=ordered_responses)
            if self.all_q_in_data:
                """
                If the remaining response values result in a new q that is already in data dict then generate a random 
                new q and return the corresponding perm and OF vals.
                """
                self.selected_q = np.random.randint(0, 2, size=self.n_qubo)
                self.selected_p = self.network.permute(self.selected_q)
                self.selected_v = self.objective_function(self.selected_p)
                self.selected_response = ['random switch setting']

                return self.selected_q, self.selected_p, self.selected_v, self.selected_response
            else:
                """
                Otherwise return the selected values
                """
                return selection[0], selection[1], selection[2], selection[3]

        elif self.all_q_in_data and not more_responses:
            """
            If there are no more responses AND all_q_in_data is still true then generate random new q and return 
            corresponding perm and OF vals.
            """
            self.selected_q = np.random.randint(0, 2, size=self.n_qubo)
            self.selected_p = self.network.permute(self.selected_q)
            self.selected_v = self.objective_function(self.selected_p)
            self.selected_response = ['random delta switch setting']

            return self.selected_q, self.selected_p, self.selected_v, self.selected_response


class Select:

    def __init__(self,
                 objective_function=None,
                 switch_network=None,
                 response_record=None,
                 data_dict_qvecs=None,
                 delta_q_basis=None,
                 current_q=None):
        self.objective_function = objective_function
        self.network = switch_network
        self.n_qubo = self.network.depth
        self.response_rec = response_record
        self.data_dict_qvecs = data_dict_qvecs
        self.delta_q_basis = delta_q_basis
        self.current_q = current_q
        self.all_q_in_data = True
        self.selected_q = 0
        self.selected_p = 0
        self.selected_v = 0
        self.selected_response = 0

    @staticmethod
    def q_in_data(data, q):
        """
        Function designed to give a boolean if switch setting q is in the data_dict
        """
        # data is expected to be a list

        all_tests = []

        for arr in data:
            # arr is a numpy array

            comparison = arr == q

            # all elements of of numpy arrays are equal
            all_tests.append(np.all(comparison))

        # when the loop is done return if all of the arrays matched
        return any(all_tests)

    def select_response(self, response_var):
        """
        Function that will go through the response list and check if the new switch settings are in the data dict.
        If not then we select and return the vals associated with that response.  If so, all_q_in_data will remain true
        and will feed into decision for check and select fcn.
        """
        for response in response_var:
            self.selected_q = np.mod(self.current_q + np.matmul(response[0], self.delta_q_basis), 2)
            if not self.q_in_data(q=self.selected_q, data=self.data_dict_qvecs):
                self.selected_p = self.network.permute(self.selected_q)
                self.selected_v = self.objective_function(self.selected_p)
                self.selected_response = response[0]
                self.all_q_in_data = False
                break

        return self.selected_q, self.selected_p, self.selected_v, self.selected_response

    def select(self):
        """
        First check if there are more than 50 responses.  If so then take the assign response list to be the first 50
        values, otherwise let response list be equal to the response variable.
        """
        if len(self.response_rec) < 50:
            more_responses = False
            response_list = self.response_rec
        else:
            more_responses = True
            response_list = self.response_rec[:50]

        """
        Then order the responses and select
        """
        selection = self.select_response(response_var=response_list)

        if not self.all_q_in_data:
            """
            If there is a response in the ordered responses that doesn't result in a new q that is not in the data dict 
            then return the selection
            """
            return selection[0], selection[1], selection[2], selection[3]
        elif self.all_q_in_data and more_responses:
            """
            If all response vals result in a new q that is already in data dict AND there are more than 50 responses in
            the response variable, then order and select from the remaining response values. 
            """
            response_list = self.response_rec[50:]
            selection = self.select_response(response_var=response_list)
            if self.all_q_in_data:
                """
                If the remaining response values result in a new q that is already in data dict then generate a random 
                new q and return the corresponding perm and OF vals.
                """
                self.selected_q = np.random.randint(0, 2, size=self.n_qubo)
                self.selected_p = self.network.permute(self.selected_q)
                self.selected_v = self.objective_function(self.selected_p)
                self.selected_response = ['random switch setting']

                return self.selected_q, self.selected_p, self.selected_v, self.selected_response
            else:
                """
                Otherwise return the selected values
                """
                return selection[0], selection[1], selection[2], selection[3]

        elif self.all_q_in_data and not more_responses:
            """
            If there are no more responses AND all_q_in_data is still true then generate random new q and return 
            corresponding perm and OF vals.
            """
            self.selected_q = np.random.randint(0, 2, size=self.n_qubo)
            self.selected_p = self.network.permute(self.selected_q)
            self.selected_v = self.objective_function(self.selected_p)
            self.selected_response = ['random delta switch setting']

            return self.selected_q, self.selected_p, self.selected_v, self.selected_response
