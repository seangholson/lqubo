import pandas as pd
import matplotlib.pyplot as plt

size_domain = {'tsp': ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']}

known_num_iterations = 100
iteration_domain = [(i+1)*5 for i in range(int(known_num_iterations/5))]

convergence_data = {'tsp': {
    'LQUBO': [],
    'LQUBO_WS': [],
    'HD_Slice_LQUBO': [],
    'HD_Slice_LQUBO_WS': [],
    'Rand_Slice_LQUBO': [],
    'Rand_Slice_LQUBO_WS': [],
}}


for instance in convergence_data:
    for solver in convergence_data[instance]:
        for iteration_number in range(int(known_num_iterations/5)):
            convergence_data[instance][solver].append(pd.read_csv("./convergence/" + instance + "_" + solver +
                                                                  "_20.csv")['convergence percent error vals'][
                                                          iteration_number]*100)


def plot_tsp_convergence():

    plt.plot(iteration_domain, convergence_data['tsp']['LQUBO'], 'o-', label='LQUBO')
    plt.plot(iteration_domain, convergence_data['tsp']['LQUBO_WS'], 's-.', label='LQUBO w/ Sorting')
    plt.plot(iteration_domain, convergence_data['tsp']['HD_Slice_LQUBO'], 'o--', label='HD Slice LQUBO')
    plt.plot(iteration_domain, convergence_data['tsp']['HD_Slice_LQUBO_WS'], 's--', label='HD Slice LQUBO w/ Sorting')
    plt.plot(iteration_domain, convergence_data['tsp']['Rand_Slice_LQUBO'], 'o-.', label='Rand Slice LQUBO')
    plt.plot(iteration_domain, convergence_data['tsp']['Rand_Slice_LQUBO_WS'], 's-.', label='Rand Slice LQUBO w/ Sorting')
    plt.xlabel('Iteration')
    plt.ylabel('Percent Error')
    plt.suptitle('Convergence of LQUBO Algorithm n = 20 Rand TSP')
    plt.legend(loc='upper right')
    plt.show()


plot_tsp_convergence()



