# pip install beautifulsoup4 lxml matplotlib
import matplotlib.pyplot as plt

import ACO
from datetime import datetime


def trial(path, no_ants, q, alpha, beta, evap_rate, max_eval, heuristic):
    # run an aco 5 times using the above parameters
    stats = []
    n = 5

    for i in range(0,n):
        trial = ACO.ACOGraph(path, no_ants, q, alpha, beta, evap_rate, max_eval, heuristic)
        stats.append(trial.start_simulation('elitist'))

    print(stats)

    for i in range(len(stats)):
        plt.plot(list(range(0, len(stats[i]))), stats[i], label='trial ' + str(i))
    plt.title("")
    plt.xlabel("Iterations")
    plt.ylabel("Avg Fitness")
    plt.title("no. ants = " + str(no_ants) + ", q = " + str(q) + ", alpha = " + str(
        alpha) + ", beta = " + str(beta) + ", evap rate = " + str(
        evap_rate) + ",\nmax evals = " + str(
        max_eval) + ", heuristic = " + heuristic)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # specify the two paths here
    paths = ['./data/burma14.xml', './data/brazil58.xml']
    # specify heuristic options here
    heuristics = ['transition rule', '1/d', 'q/d']
    # specify ACO methods here
    methods = ['original', 'elitist']

    # Create an ACOGraph object - this is what will be used to run the Ant Colony Optimisation
    # Parameters should be passed in here:
    # (paths[x], no. ants, alpha, beta, evaporation rate, max no. of evaluations, heuristics[x])

    trial(paths[0], 100, 0.5, 1, 2, 0.5, 10000, heuristics[0])
    quit()
    my_aco = ACO.ACOGraph(paths[0], 100, 0.5, 1, 2, 0.5, 10000, heuristics[0])

    # call the 'start_simulation' method of the ACOGraph object to start the simulation
    my_aco.start_simulation(methods[1])

    # Output the best solutions path, fitness and plot the simulations statistics
    print("Simulation Complete - " + datetime.now().strftime("%H:%M:%S"))
    print("best path - " + str(my_aco.best_solution.visited))
    print("best fitness - " + str(my_aco.best_solution.fitness))
    my_aco.plot_stats()

