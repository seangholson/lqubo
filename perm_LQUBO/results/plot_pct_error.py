import pandas as pd
import matplotlib.pyplot as plt
from utilities.objective_functions import QAPObjectiveFunction
import statistics as stat
import numpy as np
domain = {'had': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
          'nug': ['12', '14', '15', '16a', '16b', '17', '18', '20']}

data = {
    'had': {'percent_error': {
        'avg': {'LQUBO': [], 'New_LQUBO': []},
        'std_dev': {'LQUBO': [], 'New_LQUBO': []},
    },
            'timing_code': {
                'avg': {'LQUBO': [], 'New_LQUBO': []},
                'std_dev': {'LQUBO': [], 'New_LQUBO': []},
            }},
    'nug': {'percent_error': {
        'avg': {'LQUBO': [], 'New_LQUBO': []},
        'std_dev': {'LQUBO': [], 'New_LQUBO': []},
    },
            'timing_code': {
                'avg': {'LQUBO': [], 'New_LQUBO': []},
                'std_dev': {'LQUBO': [], 'New_LQUBO': []},
            }}
}


data1 = dict()
data1['data array'] = []
data1['avg'] = []
data1['sd'] = []
data1['optimal ans'] = []

had_domain = ['4', '6', '8', '10', '12', '14', '16', '18', '20']

QAP_of = []
for i in had_domain:
    QAP_of.append(QAPObjectiveFunction(dat_file='had' + i + '.dat',
                                       sln_file='had' + i + '.sln'))
    data1['data array'].append([])


for i in range(len(had_domain)):
    objective_function = QAP_of[i]
    n_obj = objective_function.n
    optimal_ans = objective_function.min_v
    had_ans = data1['data array'][i]
    for trial in range(100):
        obj_array = []
        for iteration in range(100):
            perm = np.random.permutation(n_obj)
            obj_array.append(objective_function(perm))

        obj_min = min(obj_array)
        had_ans.append((obj_min-optimal_ans)*100/optimal_ans)

    average_pct_err = stat.mean(had_ans)
    sd = stat.stdev(had_ans)
    data1['avg'].append(average_pct_err)
    data1['sd'].append(sd)

data2 = dict()
data2['data array'] = []
data2['avg'] = []
data2['sd'] = []
data2['optimal ans'] = []

nug_domain = ['12', '14', '15', '16a', '16b', '17', '18', '20']

QAP_of = []
for i in nug_domain:
    QAP_of.append(QAPObjectiveFunction(dat_file='nug' + i + '.dat',
                                       sln_file='nug' + i + '.sln'))
    data2['data array'].append([])
for i in range(len(nug_domain)):
    objective_function = QAP_of[i]
    n_obj = objective_function.n
    optimal_ans = objective_function.min_v
    nug_ans = data2['data array'][i]
    for trial in range(100):
        obj_array = []
        for iteration in range(100):
            perm = np.random.permutation(n_obj)
            obj_array.append(objective_function(perm))

        obj_min = min(obj_array)
        nug_ans.append((obj_min-optimal_ans)*100/optimal_ans)

    average = stat.mean(nug_ans)
    sd = stat.stdev(nug_ans)
    data2['avg'].append(average)
    data2['sd'].append(sd)

for instance in ['had', 'nug']:
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


def plot_had_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['had'], data['had']['percent_error']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['New_LQUBO'], 'o:', label='New LQUBO')
    a[0].plot(domain['had'], data1['avg'], 'o--', label='Random Perm Sampling')
    a[0].set_xlabel('QAP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['had'], data['had']['timing_code']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['New_LQUBO'], 'o:', label='New LQUBO')
    a[1].set_xlabel('QAP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Hadley-Rendl-Wolkowicz 100 Iterations')
    plt.show()


plot_had_data()


def plot_nug_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['New_LQUBO'], 'o:', label='New LQUBO')
    a[0].plot(domain['nug'], data2['avg'], 'o--', label='Random Perm Sampling')
    a[0].set_xlabel('QAP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['New_LQUBO'], 'o:', label='New LQUBO')
    a[1].set_xlabel('QAP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Nugent-Vollmann-Ruml 100 Iterations')
    plt.show()


plot_nug_data()
