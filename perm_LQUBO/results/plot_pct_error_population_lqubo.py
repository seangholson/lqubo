import pandas as pd
import matplotlib.pyplot as plt

domain = {'had': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
          'nug': ['12', '14', '15', '16a', '16b', '17', '18', '20']}

data = {
    'had': {'percent_error': {
        'avg': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
        'std_dev': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
    },
            'timing_code': {
                'avg': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
                'std_dev': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
            }},

    'nug': {'percent_error': {
        'avg': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
        'std_dev': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
    },
            'timing_code': {
                'avg': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
                'std_dev': {'Population_Based_LQUBO_ps_1_nr_250': [], 'Population_Based_LQUBO_ps_50_nr_5': [], 'Population_Based_LQUBO_ps_125_nr_2': [], 'Population_Based_LQUBO_ps_250_nr_1': []},
            }}

}


for instance in data:
    for metric in data[instance]:
        for stat in data[instance][metric]:
            for solver in data[instance][metric][stat]:
                for size in domain[instance]:
                    if stat == 'avg':
                        data[instance][metric][stat][solver].append(pd.read_csv("../results/experiment_data/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][0])
                    else:
                        data[instance][metric][stat][solver].append(pd.read_csv("../results/experiment_data/" + instance + "/iter_lim/" +
                                                                                solver + "_" + size + ".csv")[
                                                                        metric][1])


def plot_had_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['had'], data['had']['percent_error']['avg']['Population_Based_LQUBO_ps_1_nr_250'], 'o-', label='ps=1; nr=250')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['Population_Based_LQUBO_ps_50_nr_5'], 'o:', label='ps=50; nr=5')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['Population_Based_LQUBO_ps_125_nr_2'], 'o-.', label='ps=125; nr=2')
    a[0].plot(domain['had'], data['had']['percent_error']['avg']['Population_Based_LQUBO_ps_250_nr_1'], 'o--',
              label='ps=250; nr=1')
    a[0].set_xlabel('QAP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['had'], data['had']['timing_code']['avg']['Population_Based_LQUBO_ps_1_nr_250'], 'o-', label='ps=1; nr=250')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['Population_Based_LQUBO_ps_50_nr_5'], 'o:', label='ps=50; nr=5')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['Population_Based_LQUBO_ps_125_nr_2'], 'o-.', label='ps=125; nr=2')
    a[1].plot(domain['had'], data['had']['timing_code']['avg']['Population_Based_LQUBO_ps_250_nr_1'], 'o--',
              label='ps=250; nr=1')
    a[1].set_xlabel('QAP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Hadley-Rendl-Wolkowicz 100 Iterations')
    plt.show()


plot_had_data()


def plot_nug_data():

    fig, a = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['Population_Based_LQUBO_ps_1_nr_250'], 'o-', label='ps=1; nr=250')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['Population_Based_LQUBO_ps_50_nr_5'], 'o:', label='ps=50; nr=5')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['Population_Based_LQUBO_ps_125_nr_2'], 'o-.', label='ps=125; nr=2')
    a[0].plot(domain['nug'], data['nug']['percent_error']['avg']['Population_Based_LQUBO_ps_250_nr_1'], 'o--',
              label='ps=250; nr=1')
    a[0].set_xlabel('QAP Size')
    a[0].set_ylabel('Percent Error')
    a[0].legend(loc='upper left')

    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['Population_Based_LQUBO_ps_1_nr_250'], 'o-', label='ps=1; nr=250')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['Population_Based_LQUBO_ps_50_nr_5'], 'o:', label='ps=50; nr=5')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['Population_Based_LQUBO_ps_125_nr_2'], 'o-.', label='ps=125; nr=2')
    a[1].plot(domain['nug'], data['nug']['timing_code']['avg']['Population_Based_LQUBO_ps_250_nr_1'], 'o--',
              label='ps=250; nr=1')
    a[1].set_xlabel('QAP Size')
    a[1].set_ylabel('Time of Code (sec)')
    a[1].legend(loc='upper left')
    plt.suptitle('Nugent-Vollmann-Ruml 100 Iterations')
    plt.show()


plot_nug_data()
