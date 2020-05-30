import pandas as pd
import matplotlib.pyplot as plt

domain = {'had': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
          'nug': ['12', '14', '15', '16a', '16b', '17', '18', '20']}

data = {
    'had': {'percent_error': {
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
            }},
    'nug': {'percent_error': {
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
                        data[instance][metric][stat][solver].append(pd.read_csv("./qap/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][0])
                    else:
                        data[instance][metric][stat][solver].append(pd.read_csv("./qap/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][1])


def plot_had_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['had'], data['had']['percent_error']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    a[0].set_xlabel('QAP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['had'], data['had']['timing_code']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    a[1].set_xlabel('QAP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Hadley-Rendl-Wolkowicz 100 Iterations')
    plt.show()


plot_had_data()


def plot_nug_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    a[0].set_xlabel('QAP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['LQUBO'], 'o-', label='LQUBO')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    a[1].set_xlabel('QAP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Nugent-Vollmann-Ruml 100 Iterations')
    plt.show()


plot_nug_data()
