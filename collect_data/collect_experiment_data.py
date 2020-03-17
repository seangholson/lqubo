from experiment_code.run_and_plot_QAP import RunExperimentsAndPlotStatsQAP
from experiment_code.run_and_plot_TSP import RunExperimentsAndPlotStatsTSP

# Run this file from QAP-Quantum-Computing directory

# number of trials of experiment
num_trials = 10
# type of sampler, choose between 'QPU', 'SA', or 'Tabu'
sampler = 'Tabu'

run_qap = RunExperimentsAndPlotStatsQAP(num_trials=num_trials, sampler=sampler)
# run_tsp = RunExperimentsAndPlotStatsTSP(num_trials=num_trials, sampler=sampler)

run_qap.run_experiments()
# run_tsp.run_experiments()

# plots for Hadley - Rendl iteration limit problems
run_qap.plot_iter_lim_had()
# run_tsp.plot_iter_lim_had()

# plots for Hadley - Rendl time limit problems
run_qap.plot_time_lim_had()
# run_tsp.plot_time_lim_had()

# plots for Nugent - Ruml iteration limit problems
run_qap.plot_iter_lim_nug()
# run_tsp.plot_iter_lim_nug()

# plots for Nugent - Ruml time limit problems
run_qap.plot_time_lim_nug()
# run_tsp.plot_time_lim_nug()


