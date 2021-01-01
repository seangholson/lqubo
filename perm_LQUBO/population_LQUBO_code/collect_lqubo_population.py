from perm_LQUBO.next_perm import NextPerm


class CollectLQUBOPopulation:

    def __init__(self,
                 current_perm=None,
                 objective_function=None,
                 response_record=None):
        self.objective_function = objective_function
        self.n_qubo = self.objective_function.n - 1
        self.response_rec = response_record
        self.current_perm = current_perm

    def collect_population(self):

        lqubo_population = []
        for response in self.response_rec:
            next_perm = NextPerm(lqubo_result=response[0], current_perm=self.current_perm).next_perm()
            lqubo_population.append(next_perm)

        return lqubo_population

