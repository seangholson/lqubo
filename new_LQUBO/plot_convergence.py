import pandas as pd
import matplotlib.pyplot as plt

size_domain = {'had': ['4', '6', '8', '10', '12', '14', '16', '18', '20'],
               'nug': ['12', '14', '15', '16a', '16b', '17', '18', '20']}

known_num_iterations = 100
iteration_domain = [(i + 1) * 5 for i in range(int(known_num_iterations / 5))]

convergence_data = {'had': {
    'LQUBO': [],
    'New_LQUBO': []

},
    'nug': {
        'LQUBO': [],
    'New_LQUBO': []
    }}

for instance in convergence_data:
    for solver in convergence_data[instance]:
        for iteration_number in range(int(known_num_iterations / 5)):
            convergence_data[instance][solver].append(pd.read_csv("../results/convergence/" + instance + "_" + solver +
                                                                  "_20.csv")['convergence percent error vals'][
                                                          iteration_number] * 100)


def plot_had_convergence():
    plt.plot(iteration_domain, convergence_data['had']['LQUBO'], 'o-', label='LQUBO')
    plt.plot(iteration_domain, convergence_data['had']['New_LQUBO'], 'o:', label='New LQUBO')
    plt.xlabel('Iteration')
    plt.ylabel('Percent Error')
    plt.suptitle('Convergence of LQUBO Algorithm n = 20 Hadley-Rendl-Wolkowicz')
    plt.legend(loc='upper right')
    plt.show()


plot_had_convergence()


def plot_nug_convergence():
    plt.plot(iteration_domain, convergence_data['nug']['LQUBO'], 'o-', label='LQUBO')
    plt.plot(iteration_domain, convergence_data['nug']['New_LQUBO'], 'o:', label='New LQUBO')
    plt.xlabel('Iteration')
    plt.ylabel('Percent Error')
    plt.suptitle('Convergence of LQUBO Algorithm n = 20 Nugent-Vollmann-Ruml')
    plt.legend(loc='upper right')
    plt.show()


plot_nug_convergence()


