from utilities.objective_functions import QAPObjectiveFunction
from switch_networks.switch_networks import PermutationNetwork, SortingNetwork
import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = dict()
data['data array'] = []
data['avg'] = []
data['sd'] = []
data['optimal ans'] = []

nug_domain = ['12', '14', '15', '16a', '16b', '17', '18', '20']

QAP_of = []
for i in nug_domain:
    QAP_of.append(QAPObjectiveFunction(dat_file='nug' + i + '.dat',
                                       sln_file='nug' + i + '.sln'))
    data['data array'].append([])


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


for i in range(len(nug_domain)):
    objective_function = QAP_of[i]
    switch_network = switch_networks[i]
    nug_ans = data['data array'][i]
    for trial in range(100):
        obj_array = []
        for iteration in range(100):
            random_switch_setting = np.random.randint(0, 2, size=switch_network.depth)
            perm = switch_network.permute(random_switch_setting)
            obj_array.append(objective_function(perm))

        obj_min = min(obj_array)
        nug_ans.append(obj_min)

    average = stat.mean(nug_ans)
    sd = stat.stdev(nug_ans)
    data['avg'].append(average)
    data['sd'].append(sd)

lqubo_data = []
lqubo_data_wp_ws = []
for elt in nug_domain:
    lqubo_data.append(pd.read_csv("./results/experiment_data/nug/iter_lim/LQUBO_" + elt + ".csv")['percent_error'][0])
    lqubo_data_wp_ws.append(pd.read_csv("./results/experiment_data/nug/iter_lim/LQUBO_WP_and_WS_" + elt + ".csv")['percent_error'][0])

avg_lqubo_vals = []
for i in range(len(lqubo_data)):
    percent_error = (lqubo_data[i]/100)
    obj_val = percent_error * data['optimal ans'][i] + data['optimal ans'][i]
    avg_lqubo_vals.append(obj_val)

avg_lqubo_wp_ws_vals = []
for i in range(len(lqubo_data_wp_ws)):
    percent_error = (lqubo_data_wp_ws[i]/100)
    obj_val = percent_error * data['optimal ans'][i] + data['optimal ans'][i]
    avg_lqubo_wp_ws_vals.append(obj_val)

plt.scatter(x=nug_domain, y=data['avg'], label="Random Sampling")
plt.scatter(x=nug_domain, y=data['optimal ans'], label="Optimal QAP answer")
plt.scatter(x=nug_domain, y=avg_lqubo_vals, label="LQUBO")
plt.scatter(x=nug_domain, y=avg_lqubo_wp_ws_vals, label="LQUBO with Penalty and Sorting")
plt.ylabel("Total Distance")
plt.xlabel("QAP Size")
plt.suptitle("Nugent-Ruml Objective Function Distribution")
plt.legend()
plt.show()




