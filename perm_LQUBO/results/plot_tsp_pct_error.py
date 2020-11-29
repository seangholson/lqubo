import pandas as pd
import matplotlib.pyplot as plt
from utilities.objective_functions import TSPObjectiveFunction
import statistics as stat
import numpy as np

data1 = dict()
data1['data array'] = []
data1['avg'] = []
data1['sd'] = []
data1['optimal ans'] = []

tsp_domain = list(range(4, 21))
tsp_domain_str = []
tsp_of = []
domain = {'tsp': ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']}


for i in tsp_domain:
    tsp_of.append(TSPObjectiveFunction(num_points=i))
    tsp_domain_str.append(str(i))
    data1['data array'].append([])


for i in range(len(tsp_domain)):
    objective_function = tsp_of[i]
    n_obj = objective_function.n
    optimal_ans = objective_function.min_v
    tsp_ans = data1['data array'][i]
    for trial in range(100):
        obj_array = []
        for iteration in range(100):
            perm = np.random.permutation(n_obj)
            obj_array.append(objective_function(perm))

        obj_min = min(obj_array)
        tsp_ans.append((obj_min-optimal_ans)*100/optimal_ans)

    average = stat.mean(tsp_ans)
    sd = stat.stdev(tsp_ans)
    data1['avg'].append(average)
    data1['sd'].append(sd)


data = {
    'tsp': {'percent_error': {
        'avg': {'LQUBO': [], 'New_LQUBO': []},
        'std_dev': {'LQUBO': [], 'New_LQUBO': []},
    },
            'timing_code': {
                'avg': {'LQUBO': [], 'New_LQUBO': []},
                'std_dev': {'LQUBO': [], 'New_LQUBO': []},
            }}
}

for instance in data:
    for metric in data[instance]:
        for stat in data[instance][metric]:
            for solver in data[instance][metric][stat]:
                for size in domain[instance]:
                    if stat == 'avg':
                        data[instance][metric][stat][solver].append(pd.read_csv("./results/experiment_data/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][0])
                    else:
                        data[instance][metric][stat][solver].append(pd.read_csv("./results/experiment_data/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][1])


def plot_tsp_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['New_LQUBO'], 'o:', label='New LQUBO')
    a[0].plot(domain['tsp'], data1['avg'], 'o--', label='Random Perm Sampling')
    a[0].set_xlabel('TSP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['New_LQUBO'], 'o:', label='New LQUBO')
    a[1].set_xlabel('TSP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Random TSP 100 Iterations')
    plt.show()


plot_tsp_data()


