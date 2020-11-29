import pandas as pd
import matplotlib.pyplot as plt

size_domain = {'tsp': ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']}

known_num_iterations = 100
iteration_domain = [(i+1)*5 for i in range(int(known_num_iterations/5))]

convergence_data = {'tsp': {
    'LQUBO': [],
    'New_LQUBO': []
}}


for instance in convergence_data:
    for solver in convergence_data[instance]:
        for iteration_number in range(int(known_num_iterations/5)):
            convergence_data[instance][solver].append(pd.read_csv("../results/convergence/" + instance + "_" + solver +
                                                                  "_20.csv")['convergence percent error vals'][
                                                          iteration_number]*100)


def plot_tsp_convergence():

    plt.plot(iteration_domain, convergence_data['tsp']['LQUBO'], 'o-', label='LQUBO')
    plt.plot(iteration_domain, convergence_data['tsp']['New_LQUBO'], 'o:', label='New LQUBO')
    plt.xlabel('Iteration')
    plt.ylabel('Percent Error')
    plt.suptitle('Convergence of LQUBO Algorithm n = 20 Random TSP')
    plt.legend(loc='upper right')
    plt.show()


plot_tsp_convergence()


