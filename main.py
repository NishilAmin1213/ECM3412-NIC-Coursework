# pip install beautifulsoup4 lxml
from bs4 import BeautifulSoup
import ACO
import ACO1
from datetime import datetime


def get_metadata(path):
    """
    Retrieves metadata from the XML file
    :param path: path to the XML file
    :return: dictionary containing metadata of the XML File
    """
    res = {}
    headers = ['name', 'source', 'description', 'doublePrecision', 'ignoredDigits']

    # Open the XML file at the given path
    with open(path, 'r') as xml_file:
        # Read the XML file using bs4
        data = xml_file.read()
        bs4_data = BeautifulSoup(data, 'xml')

        # For each of the hard coded parameters, get the value from the XML and store it in the dictionary
        for header in headers:
            value = bs4_data.find(header).get_text()
            res[header] = value

    # return the dictionary
    return res


if __name__ == "__main__":
    # specify the two paths here
    brazil = './data/brazil58.xml'
    burma = './data/burma14.xml'
    # select the path to operate on
    path = burma

    # get the metadata for the XML file
    metadata = get_metadata(path)

    # define heuristics options
    heuristics = ['transition rule', '1/d', 'q/d']
    # select a heuristic from the above options
    heuristic = heuristics[0]

    # higher q rewards worse answers, lower q rewards good answers faster
    # Create an ACOGraph object - this is what will be used to run the Ant Colony Optimisation
    # Parameters should be passed in here:
    # (path, no. ants, alpha, beta, evaporation rate, max no. of evaluations, heuristic string)
    my_aco = ACO1.ACOGraph(path, 100, 0.5, 1, 2, 0.5, 10000, heuristic)

    # call the 'start_simulation' method of the ACOGraph object to start the simulation
    methods = ['original', 'elitist']
    my_aco.start_simulation(methods[1])

    # Output the best solutions path, fitness and plot the simulations statistics
    print("Simulation Complete - " + datetime.now().strftime("%H:%M:%S"))
    print("best path - " + str(my_aco.best_solution.visited))
    print("best fitness - " + str(my_aco.best_solution.fitness))
    my_aco.plot_stats()
