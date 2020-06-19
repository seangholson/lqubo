import pandas as pd
import matplotlib.pyplot as plt

domain = {'tsp': ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']}

data = {
    'tsp': {'percent_error': {
        'avg': {'LQUBO': [],
                'LQUBO_WS': [],
                'HD_Slice_LQUBO': [],
                'HD_Slice_LQUBO_WS': [],
                'Rand_Slice_LQUBO': [],
                'Rand_Slice_LQUBO_WS': []},
        'std_dev': {'LQUBO': [],
                    'LQUBO_WS': [],
                    'HD_Slice_LQUBO': [],
                    'HD_Slice_LQUBO_WS': [],
                    'Rand_Slice_LQUBO': [],
                    'Rand_Slice_LQUBO_WS': []},
    },
            'timing_code': {
                'avg': {'LQUBO': [],
                        'LQUBO_WS': [],
                        'HD_Slice_LQUBO': [],
                        'HD_Slice_LQUBO_WS': [],
                        'Rand_Slice_LQUBO': [],
                        'Rand_Slice_LQUBO_WS': []},
                'std_dev': {'LQUBO': [],
                            'LQUBO_WS': [],
                            'HD_Slice_LQUBO': [],
                            'HD_Slice_LQUBO_WS': [],
                            'Rand_Slice_LQUBO': [],
                            'Rand_Slice_LQUBO_WS': []},
            }}
}

for instance in data:
    for metric in data[instance]:
        for stat in data[instance][metric]:
            for solver in data[instance][metric][stat]:
                for size in domain[instance]:
                    if stat == 'avg':
                        data[instance][metric][stat][solver].append(pd.read_csv("./experiment_data/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][0])
                    else:
                        data[instance][metric][stat][solver].append(pd.read_csv("./experiment_data/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][1])


def plot_tsp_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    a[0].plot(domain['tsp'], data['tsp']['percent_error']['avg']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    a[0].set_xlabel('TSP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    a[1].plot(domain['tsp'], data['tsp']['timing_code']['avg']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    a[1].set_xlabel('TSP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Random TSP 100 Iterations')
    plt.show()


plot_tsp_data()



