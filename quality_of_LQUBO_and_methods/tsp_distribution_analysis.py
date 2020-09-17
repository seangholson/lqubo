from utilities.objective_functions import TSPObjectiveFunction
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

tsp_domain = list(range(4, 21))
tsp_domain_str = []
tsp_of = []
for i in tsp_domain:
    tsp_of.append(TSPObjectiveFunction(num_points=i))
    tsp_domain_str.append(str(i))
    data['data array'].append([])

switch_networks = []
for obj in tsp_of:
    data['optimal ans'].append(obj.min_v)
    n_obj = obj.n
    s = SortingNetwork(n_obj)
    p = PermutationNetwork(n_obj)
    if s.depth <= p.depth:
        network = s
    else:
        network = p

    switch_networks.append(network)


for i in range(len(tsp_domain)):
    objective_function = tsp_of[i]
    switch_network = switch_networks[i]
    tsp_ans = data['data array'][i]
    for trial in range(100):
        obj_array = []
        for iteration in range(100):
            random_switch_setting = np.random.randint(0, 2, size=switch_network.depth)
            perm = switch_network.permute(random_switch_setting)
            obj_array.append(objective_function(perm))

        obj_min = min(obj_array)
        tsp_ans.append(obj_min)

    average = stat.mean(tsp_ans)
    sd = stat.stdev(tsp_ans)
    data['avg'].append(average)
    data['sd'].append(sd)


lqubo_data = []
lqubo_data_wp_ws = []
for elt in tsp_domain_str:
    lqubo_data.append(pd.read_csv("./results/experiment_data/tsp/iter_lim/LQUBO_" + elt + ".csv")['percent_error'][0])
    lqubo_data_wp_ws.append(pd.read_csv("./results/experiment_data/tsp/iter_lim/LQUBO_WP_and_WS_" + elt + ".csv")['percent_error'][0])

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

plt.scatter(x=tsp_domain_str, y=data['avg'], label="Random Sampling")
plt.scatter(x=tsp_domain_str, y=data['optimal ans'], label="Optimal TSP answer")
plt.scatter(x=tsp_domain_str, y=avg_lqubo_vals, label="LQUBO")
plt.scatter(x=tsp_domain_str, y=avg_lqubo_wp_ws_vals, label="LQUBO with Penalty and Sorting")
plt.ylabel("Total Distance")
plt.xlabel("TSP Size")
plt.suptitle("TSP Objective Function Distribution")
plt.legend()
plt.show()



