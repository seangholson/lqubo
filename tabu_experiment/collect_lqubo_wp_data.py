from tabu_experiment.run_qap_experiments_class import RunExperimentsAndPlotStatsQAP

# Run this file from QAP-Quantum-Computing directory

# number of trials of experiment
num_trials = 2

# type of sampler, choose between 'QPU', 'SA', or 'Tabu'
sampler = 'Tabu'

# toggle the ability to save the csv that comes out of a set of experiments
save_csv = True

run_qap = RunExperimentsAndPlotStatsQAP(num_trials=num_trials, sampler=sampler, save_csv=save_csv)

run_qap.run_lqubo_wp_experiments()
