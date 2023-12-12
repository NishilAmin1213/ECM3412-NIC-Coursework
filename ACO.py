import random
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

class ACOGraph:
    def __init__(self, path, no_ants, q, alpha, beta, evap_rate, max_eval, heuristic):
        """
        :param path: path to the XML file with data
        :param no_ants: number of ants to use in each iteration of the simulation
        :param q: the parameter 'q' which is used
        :param alpha: the parameter 'alpha' which is used
        :param beta: the parameter 'beta' which is used
        :param evap_rate: the numerical value to control the rate at which pheromone evaporation occurs
        :param max_eval: the maximum number of fitness evaluations to allow
        :param heuristic: the string representation of the desired heuristic
        """

        # store passed in variables
        self.max_eval = max_eval
        self.eval_counter = [0]
        self.stats = []
        self.best_solution = 0
        self.no_ants = no_ants

        self.vertices = []
        self.edges = []
        self.ants = []
        self.graph = []
        self.generate_graph(path)

        # store passed in variables as class variables for Edge and Ant
        Edge.heuristic = heuristic
        Edge.alpha = alpha
        Edge.beta = beta
        Edge.evap_rate = evap_rate
        self.q = Edge.q = q
        Edge.edges = self.edges

        Ant.graph = self.graph
        Ant.eval_counter = self.eval_counter

    def generate_graph(self, path):
        """
        method to define and fill a representation of the graph, in the form of a 2D array
        :param path: path to the XML file with the data
        :return: 2D array representation of the graph
        """
        print("Generating Graph")
        # Open the XML file
        with open(path, 'r') as xml_file:
            # Read the XML file using bs4
            data = xml_file.read()
            bs4_data = BeautifulSoup(data, 'xml')

            # find all vertex blocks in the XML filea and create a correctly sized 2D array with all values set to 0
            vertices = bs4_data.find_all('vertex')
            for i in range(len(vertices)):
                tmp = []
                for j in range(len(vertices)):
                    tmp.append(0)
                self.graph.append(tmp)

            # for each vertex in the XML file
            for vertex_num in range(len(vertices)):
                # store vertex number in self.vertices
                self.vertices.append(vertex_num)

                # iterate through each edge in the XML file for a specific vertex
                for edge in list(filter("\n".__ne__, list(vertices[vertex_num].children))):
                    # get the cost and location for the edge
                    cost = edge.get("cost")
                    location = {vertex_num, int(edge.get_text())}
                    # create an 'Edge' object
                    tmp_edge = Edge(int(float(cost)), location)

                    # if the edge has not been placed in the graph, place the edge in the graph
                    if self.graph[vertex_num][int(edge.get_text())] == 0:
                        # place the edge in the graph, in both permutations of [row][col
                        # the same instance of the edge object will be in both indexes
                        self.graph[vertex_num][int(edge.get_text())] = tmp_edge
                        self.graph[int(edge.get_text())][vertex_num] = tmp_edge

                        # append the edge to the array of edges
                        self.edges.append(tmp_edge)

    def generate_new_ants(self):
        """
        Method to generate the desired number of 'Ant' objects and clear all old ants
        """
        #print("Generating New Ants")
        # Empty the self.ants array
        self.ants = []
        # Fill the recently emptied array with new Ants, each placed at a random vertex
        for i in range(self.no_ants):
            self.ants.append(Ant(random.choice(self.vertices)))

    def start_simulation(self):
        """
        method to simulate the ACO
        """
        print("Starting Simulation - " + datetime.now().strftime("%H:%M:%S"))

        # while loop to keep running simulation iterations until the maximum number of fitness evaluations is reached
        while self.eval_counter[0] < self.max_eval:

            # generate new ants
            self.generate_new_ants()

            # move ants
            total_fitness = 0
            for ant in self.ants:
                ant.move()
                total_fitness += ant.fitness
                # update pheromone for all ants in the iteration (elitist ACO)
                ant.update_pheromone_trail()
            # at this point, all ants have completed traversal

            # find best ant of this iteration
            best_ant = Ant.get_best_ant(self.ants)

            # update best solution of all time
            if self.best_solution == 0:
                self.best_solution = best_ant
            if best_ant.fitness < self.best_solution.fitness:
                self.best_solution = best_ant

            # update pheromone for the global best ant (elitist ACO)
            self.best_solution.update_pheromone_trail()

            # evaporate pheromone in all edges
            for row in self.graph:
                for edge in row:
                    if edge != 0:
                        edge.evaporate_pheromone()
                        edge.set_score()

            # store global best fitness of this iteraation into stats array
            self.stats.append(self.best_solution.fitness)

        return [self.stats, self.best_solution.fitness]


class Edge:
    def __init__(self, cost, location):
        """
        :param cost: the cost associated to the edge
        :param location: the location of the edge - this is a set containing the two vertices that the edge connects
        """
        self.cost = cost
        self.pheromone = random.random()
        self.location = location
        self.score = 0

    def set_score(self):
        """
        this method uses the heuristic to return the score of an edge, this could be 1/d, q/d, or use the transition rule
        :return: numerical value of the score
        """

        if self.heuristic == '1/d':
            return 1/self.cost
            return 1/self.cost

        if self.heuristic == 'q/d':
            return self.q/self.cost

        if self.heuristic == 'transition rule':
            # apply the transition rule to return the score
            total_cost = 0
            total_pheromone = 0
            for edge in self.edges:
                total_cost += edge.cost
                total_pheromone += edge.pheromone

            self.score = (((self.pheromone ** self.alpha) * ((1 / self.cost) ** self.beta)) /
                    ((total_pheromone ** self.alpha) * ((1 / total_cost) ** self.beta)))

    def update_pheromone(self, ant_fitness):
        """
        Update the pheromone using the passed in fitness
        :param ant_fitness: the fitness of the best ant in an iteration
        """
        # adds q/fitness to the pheromone of an edge
        self.pheromone += self.q / ant_fitness

    def evaporate_pheromone(self):
        """
        Evaporate pheromone from an edge
        """
        # multiplied the edge's pheromone by 1-evap rate
        self.pheromone *= (1-self.evap_rate)


class Ant:
    def __init__(self, vertex):
        """
        :param vertex: the vertex to place the ant initially
        """
        # set the start fitness of an ant to 0
        self.fitness = 0
        # set the array of visited vertices to the initial vertex passed in
        self.visited = [vertex]
        # set the current vertex to the initial vertex passed in
        self.current_vertex = vertex

    @classmethod
    def get_best_ant(cls, ants):
        """
        Class method to return the best ant in a passed in array of ants
        :param ants: array of ant objects
        :return: the best ant that is found in the provided array
        """
        # set the best solution to the first element of the array
        best_ant = ants[0]
        best_fitness = ants[0].fitness

        # compare this to the rest of the ants in the array
        for ant in ants:
            if ant.fitness <= best_fitness:
                # if a ant with a better fitness is found, then make this ant the new best ant
                best_fitness = ant.fitness
                best_ant = ant

        # return the best ant
        return best_ant

    def update_pheromone_trail(self):
        """
        follow the ants path and update the pheromone for every edge that it has travelled through
        """
        for i in range(0, len(self.visited) - 1):
            # for each edge that the ant has travelled, update the pheromone using the ants fitness
            Ant.graph[self.visited[i]][self.visited[i + 1]].update_pheromone(self.fitness)
        # update the edge between the final node in the array and the first node
        Ant.graph[self.visited[-1]][self.visited[0]].update_pheromone(self.fitness)

    def get_possible_moves(self):
        """
        return an array of the possible edge objects that the ant can travel taking the visited nodes into account
        """
        possible_moves = []

        for row in range(0, len(Ant.graph)):
            for col in range(0, len(Ant.graph)):
                # for each row in the graph, make sure the edge starts or ends from the current vertex
                if (row == self.current_vertex) or (col == self.current_vertex):
                    # make sure that one end of the edge has not been visited
                    if (row not in self.visited) or (col not in self.visited):
                        # this is a valid edge, append it to the 'possible_moves' array
                        possible_moves.append(Ant.graph[row][col])

        # return the array of possible moves
        return possible_moves

    def get_best_move(self, possible_moves):
        """
        get the best move from the array of possible moves
        :param possible_moves: array of Edge objects, these are all the possible moves the ant can make
        :return: an the best Edge object in this array
        """

        # set the best move to the first element of the possible moves array
        best_move = possible_moves[0]
        best_score = possible_moves[0].score

        # for the rest of the moves, if there is a better edge, set this to the new best move
        for edge in possible_moves:
            if edge.score > best_score:
                best_score = edge.score
                best_move = edge

        # return the best move (an edge object)
        return best_move

    def set_fitness(self):
        """
        calculate the fitness of the ant and set the fitness attribute of the ant
        """
        # for each move made by the ant, get the cost and add it to the fitness
        for i in range(0, len(self.visited) - 1):
            edge = Ant.graph[self.visited[i]][self.visited[i + 1]]
            self.fitness += edge.cost
        # add the cost between the final node and first node to the fitness
        self.fitness += Ant.graph[self.visited[-1]][self.visited[0]].cost

        # increment the 'eval_counter'
        Ant.eval_counter[0] += 1

    def move(self):
        """
        move the ant through the graph
        """
        # set flag to break the code out of the loop later on
        finished = False

        # whilst the finished variable is not True
        while not finished:

            # get possible moves
            possible_moves = self.get_possible_moves()

            # check if the ant has completed its traversal
            if len(possible_moves) == 0:
                # Ant has finished, set its fitness
                self.set_fitness()
                # set the finished variable to True to prevent this ant from trying to make another move
                finished = True
                # skip the rest of this while loop
                continue

            # get the best move out of the possible moves
            move = self.get_best_move(possible_moves)

            # make the move using this edge
            move = move.location.copy()
            move.remove(self.current_vertex)
            new_vertex = move.pop()
            self.visited.append(new_vertex)
            self.current_vertex = new_vertex
