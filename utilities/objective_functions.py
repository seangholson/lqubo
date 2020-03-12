import numpy as np
from utilities.data_loading import parse_dat_file, parse_sln_file


class ObjectiveFunction:
    """
    This is the base class for an objective function.
    Broadly speaking, it's a thing that takes an input (vector, matrix, whatever)
    and associates an output real scalar with it.
    Typically, we want to find the minimum value for the output, and which
    particular input(s) led to that minimum output.
    """
    def __init__(self):
        """
        enum_limit is a maximum size for which the objective function will
        compute it's own minimum value by enumeration

        min_v, min_x are the optimum and location of optimum
        """
        self.min_v = None
        self.min_x = None

    def __call__(self, *args, **kwargs):
        # This makes the class instances callable, so the object itself is the objective function
        raise NotImplementedError

    def compare(self, x):
        # This returns the relative error of the objective function evaluated at x, wrt the actual min
        if not self.min_v or not self.min_x:
            print('No known optimum for comparison')
            return np.inf
        v = self(x)
        return (v - self.min_v) / self.min_v


class QUBOObjectiveFunction(ObjectiveFunction):
    """
    The QUBO objective function is in the form of a Hamiltonian over bitstrings.
    """
    def __init__(self,
                 qubo=None):
        super().__init__()
        if isinstance(qubo, dict):
            self.n = max([max(indices) for indices in qubo.keys()]) + 1
            self.qubo = np.zeros([self.n, self.n])
            for indices, val in qubo.items():
                self.qubo[indices] = val
        elif isinstance(qubo, np.ndarray):
            self.qubo = qubo
            self.n = self.qubo.shape[0]
        else:
            raise TypeError('Input qubo must be dict or np.ndarray.')

        if not np.allclose(self.qubo, np.triu(self.qubo)):
            raise TypeError('Input array should be upper triangular.')

    def __call__(self, q):
        return q @ self.qubo @ q.transpose()


class QAPObjectiveFunction(ObjectiveFunction):
    """
    The QAP objective function is in the form of flow and distance matrices over permutations.
    """
    def __init__(self,
                 dat_file=None,
                 dist=None,
                 flow=None,
                 sln_file=None):
        super().__init__()
        if dat_file:
            self.n, self.dist, self.flow = parse_dat_file(dat_file=dat_file)
            self.dat_file = dat_file
        elif dist and flow:
            self.n = dist.shape[0]
            self.dist = dist
            self.flow = flow
        else:
            raise AttributeError('Distance/flow matrices missing.')

        self.min_x = None
        if sln_file:
            _, self.min_v, self.min_x = parse_sln_file(sln_file=sln_file)

    def __call__(self, perm):
        ident = np.identity(self.n)
        permuted_flow = np.matmul(self.flow, ident[:, perm])
        permuted_dist = np.matmul(self.dist, np.transpose(ident[:, perm]))
        return np.trace(np.matmul(permuted_flow, permuted_dist))


class TSPObjectiveFunction(ObjectiveFunction):
    """
    This Class will use the distance matrices from the QAP dat files and return the TSP objective function value for a
    given permutation.
    """
    def __init__(self,
                 dat_file=None,
                 dist=None,
                 flow=None,
                 sln_file=None):
        super().__init__()
        if dat_file:
            self.n, self.dist, self.flow = parse_dat_file(dat_file=dat_file)
            self.dat_file = dat_file
        elif dist and flow:
            self.n = dist.shape[0]
            self.dist = dist
            self.flow = flow
        else:
            raise AttributeError('Distance/flow matrices missing.')

        self.min_x = None
        if sln_file:
            _, self.min_v, self.min_x = parse_sln_file(sln_file=sln_file)

    def __call__(self, perm):
        ident = np.identity(self.n)
        perm_matrix = ident[:, perm]
        cycle_perm = list(range(self.n))
        cycle_perm.remove(0)
        cycle_perm.append(0)
        cycle_perm_matrix = ident[:, cycle_perm]
        left_action = np.matmul(perm_matrix, cycle_perm_matrix)
        right_action = np.matmul(self.dist, perm_matrix)
        return np.trace(np.matmul(left_action, right_action))
