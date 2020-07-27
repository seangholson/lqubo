from utilities.objective_functions import QAPObjectiveFunction
from switch_networks.switch_networks import PermutationNetwork, SortingNetwork
import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = dict()
data['avg'] = []
data['sd'] = []
data['optimal ans'] = []

had_domain = ['4', '6', '8', '10', '12', '14', '16', '18', '20']

QAP_of = []
for i in had_domain:
    QAP_of.append(QAPObjectiveFunction(dat_file='had' + i + '.dat',
                                       sln_file='had' + i + '.sln'))


switch_networks = []
for obj in QAP_of:
    data['optimal ans'].append(obj.min_v)
    n_obj = obj.n
    s = SortingNetwork(n_obj)
    p = PermutationNetwork(n_obj)
    if s.depth <= p.depth:
        network = s
    else:
        network = p

    switch_networks.append(network)


for i in range(len(had_domain)):
    objective_function = QAP_of[i]
    switch_network = switch_networks[i]
    QAP_ans = []
    for trial in range(1000):
        random_switch_setting = np.random.randint(0, 2, size=switch_network.depth)
        perm = switch_network.permute(random_switch_setting)
        QAP_ans.append(objective_function(perm))

    average = stat.mean(QAP_ans)
    sd = stat.stdev(QAP_ans)
    data['avg'].append(average)
    data['sd'].append(sd)

lqubo_data = []
for elt in had_domain:
    lqubo_data.append(pd.read_csv("./results/experiment_data/had/iter_lim/LQUBO_" + elt + ".csv")['percent_error'][0])

avg_obj_vals = []
for i in range(len(lqubo_data)):
    percent_error = (lqubo_data[i]/100)
    obj_val = percent_error * data['optimal ans'][i] + data['optimal ans'][i]
    avg_obj_vals.append(obj_val)

plt.errorbar(x=had_domain, y=data['avg'], yerr=data['sd'])
plt.scatter(x=had_domain, y=data['avg'], label="Average QAP answer")
plt.scatter(x=had_domain, y=data['optimal ans'], label="Optimal QAP answer")
plt.scatter(x=had_domain, y=avg_obj_vals, label="LQUBO Avg Answer")
plt.ylabel("Total Distance")
plt.xlabel("QAP Size")
plt.suptitle("Hadley-Rendl Objective Function Distribution")
plt.legend()
plt.show()




