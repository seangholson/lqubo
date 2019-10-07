from qap.qap_objective_function import QAPObjectiveFunction
from solvers.QAP_Solvers import LocalQUBOIterativeSolver, QAPEnumerator, NaturalEncodingSolver

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

# This shows how to instantiate the objective function with no known solution, but it's small so
# it's computed automatically:
obj = QAPObjectiveFunction(dat_file='had6.dat')

# Use cases:

enu = QAPEnumerator(objective_function=obj)
act_v, act_p = enu.minimize_objective()

# This instantiates the iterative dwave solver:

iterative_qpu = LocalQUBOIterativeSolver(objective_function=obj, dwave_sampler=EmbeddingComposite(DWaveSampler()))
apx_v, apx_p, data = iterative_qpu.minimize_objective()

iterative_SA = LocalQUBOIterativeSolver(objective_function=obj)
apx_v2, apx_p2, data2 = iterative_SA.minimize_objective()

# This instantiates the natural formulation of QAP as QUBO:

natural_qpu = NaturalEncodingSolver(objective_function=obj, dwave_sampler=EmbeddingComposite(DWaveSampler()))
apx_p3, apx_v3 = natural_qpu.minimize_objective()

natural_SA = NaturalEncodingSolver(objective_function=obj)
apx_p4, apx_v4 = natural_SA.minimize_objective()

