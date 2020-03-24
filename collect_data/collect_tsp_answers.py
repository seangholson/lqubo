from solvers.solvers import QAPEnumerator
from utilities.objective_functions import TSPObjectiveFunction

had_domain = ['4', '6', '8', '10', '12', '14', '16', '18', '20']
nug_domain = ['12', '14', '15', '16a', '16b', '17', '18', '20']

had_of = []
nug_of = []

# generate had objective functions
for size in had_domain:
    had_of.append(TSPObjectiveFunction(dat_file='had'+size+'.dat'))

# generate nug objective functions
for size in nug_domain:
    nug_of.append((TSPObjectiveFunction(dat_file='nug'+size+'.dat')))

for index in range(len(had_domain)):
    enu = QAPEnumerator(objective_function=had_of[index])
    min_v, min_perm = enu.minimize_objective()
    print('had {} min objective: {}'.format(had_domain[index], min_v))
    print('had {} min perm {}'.format(had_domain[index], min_perm))

for index in range(len(nug_domain)):
    enu = QAPEnumerator(objective_function=nug_of[index])
    min_v, min_perm = enu.minimize_objective()
    print('nug {} min objective: {}'.format(nug_domain[index], min_v))
    print('nug {} min perm {}'.format(nug_domain[index], min_perm))


