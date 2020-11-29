import numpy as np
from utilities.objective_functions import TSPObjectiveFunction
from perm_LQUBO.form_new_LQUBO import NewLQUBO
from perm_LQUBO.next_perm import NextPerm
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy import stats
ax = plt.figure().gca()


class ObjectiveFunction:
    def __init__(self, objective_function=None):
        if objective_function:
            self.objective_function = objective_function
        else:
            raise AttributeError('Objective function missing.')


class LocalQUBOQuality(ObjectiveFunction):
    """
    For a specified objective function and LQUBO type, LocalQUBOQuality class has 2 useful visual functions that can
    be run from the command line.



    """
    def __init__(self,
                 objective_function=None,
                 num_points=None):
        super().__init__(objective_function=objective_function)

        # Initialize switch network:
        # The default behavior here is to choose the smaller of either permutation or
        # sorting networks for the given input size.
        self.n_problem = self.objective_function.n

        if num_points:
            self.num_points = num_points
        else:
            self.num_points = 200

        # Initialize random bitstring
        self.p = np.random.permutation(self.n_problem)
        self.v = self.objective_function(self.p)
        self.n_qubo = len(self.p) - 1

        if type(objective_function) == TSPObjectiveFunction:
            self.OF_type = 'TSP'
        else:
            self.OF_type = 'QAP'

        self.form_qubo = NewLQUBO(objective_function=self.objective_function).form_lqubo(self.p)

        self.qubo = np.zeros((self.n_qubo, self.n_qubo))

        for i in range(self.n_qubo):
            for j in range(self.n_qubo):
                if i <= j:
                    self.qubo[i][j] = self.form_qubo[(i, j)]

    def q_q_plot(self, hamming_dist):

        """
        Given a specified hamming dist (int), q_q_plot will produce a Q-Q scatter plot of the LQUBO change in objective
        function versus the actual change in objective function.
        """

        if hamming_dist:
            hamming_dist = hamming_dist
        else:
            raise AttributeError('Hamming dist missing.')

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(self.n_qubo))
            return binary

        # delta q of specified hamming dist
        hd = []
        x = []
        y = []

        for i in range(self.num_points):
            hd.append(np.zeros(self.n_qubo))

        for i in range(len(hd)):
            for j in range(hamming_dist):
                hd[i][j] = 1
            # only swap first n_qubo qubits to preserve total weight qubit
            random_binary(hd[i][:self.n_qubo])

        for vec in hd:
            p_new = NextPerm(current_perm=self.p, lqubo_result=vec).next_perm()
            v_new = self.objective_function(p_new)
            x.append(v_new - self.v)
            y.append(np.matmul(np.matmul(vec, self.qubo), np.transpose(vec)))

        plt.scatter(x, y, label='HD = {}'.format(hamming_dist))

        plt.xlabel("true delta obj")
        plt.ylabel("local qubo delta obj")
        plt.title('n = {} {}'.format(self.n_problem, self.OF_type))

        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.legend(loc='upper left')
        plt.show()

    def plot_r_squared(self):

        """
        plot_r_squared function will take objective function from the base class and produce multiple scatter plots to
        retrieve the R squared value for a specified hamming distance.  Then for a hamming dist from 1 to 20 it will
        produce a plot of the R squared val versus the input hamming dist.
        """

        def swap(input_list, first_entry, second_entry):
            input_list[first_entry], input_list[second_entry] = input_list[second_entry], input_list[first_entry]
            return input_list

        def random_binary(binary):
            for index in range(hamming_dist):
                swap(binary, index, np.random.randint(self.n_qubo))
            return binary

        r_val = []
        hamming_weight = []
        for hamming_dist in range(self.n_problem - 1):

            hamming_dist = hamming_dist + 1
            hd = []
            x = []
            y = []

            for i in range(self.num_points):
                hd.append(np.zeros(self.n_qubo))

            for i in range(len(hd)):
                for j in range(hamming_dist):
                    hd[i][j] = 1
                random_binary(hd[i])

            for vec in hd:
                p_new = NextPerm(current_perm=self.p, lqubo_result=vec).next_perm()
                v_new = self.objective_function(p_new)
                x.append(v_new - self.v)
                y.append(np.matmul(np.matmul(vec, self.qubo), np.transpose(vec)))

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            r_val.append(r_value**2)
            hamming_weight.append(hamming_dist)

        plt.plot(hamming_weight, r_val, label='n = {} {}'.format(self.n_problem, self.OF_type))

        plt.scatter(hamming_weight, r_val)
        plt.xticks(hamming_weight)
        plt.xlabel("Hamming dist")
        plt.ylabel("R Squared")
        plt.title('Hamming dist of LQUBO vs R Squared of scatter plot')
        plt.legend(loc='best')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()

