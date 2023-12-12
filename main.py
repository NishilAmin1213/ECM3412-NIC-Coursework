# pip install beautifulsoup4 lxml matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import ACO


def trial(path, no_ants, q, alpha, beta, evap_rate, max_eval, heuristic, n):
    # run an aco n times using the above parameters
    stats = []
    best_score = 9999999

    for i in range(0, n):
        trial = ACO.ACOGraph(path, no_ants, q, alpha, beta, evap_rate, max_eval, heuristic)
        output = trial.start_simulation()
        stats.append(output[0])
        if output[1] < best_score:
            best_score = output[1]

    print("Plotting Graph")
    for i in range(len(stats)):
        plt.plot(list(range(0, len(stats[i]))), stats[i], label='trial ' + str(i))
    plt.title("")
    plt.xlabel("Iterations")
    plt.ylabel("Global Best Fitness")
    plt.title("no. ants = " + str(no_ants) + ", q = " + str(q) + ", alpha = " + str(
        alpha) + ", beta = " + str(beta) + ", evap rate = " + str(
        evap_rate) + ",\nmax evals = " + str(
        max_eval) + ", heuristic = " + heuristic + ", best score = " + str(best_score))
    plt.legend()
    plt.savefig("ECM3412-NIC-Output")
    plt.show()


if __name__ == "__main__":
    # selectable options below
    paths = ['./data/burma14.xml', './data/brazil58.xml']
    heuristics = ['transition rule', '1/d', 'q/d']

    # Parameters should be passed in here:
    # (paths[x], no. ants, alpha, beta, evaporation rate, max no. of evaluations, heuristics[x], n)
    trial(paths[0], 50, 0.5, 1, 2, 0.51, 10000, heuristics[0], 5)
