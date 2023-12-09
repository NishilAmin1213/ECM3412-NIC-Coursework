import random
from bs4 import BeautifulSoup


class ACOGraph:
    def __init__(self, path, no_ants, q, evap_rate, max_eval):
        self.evap_rate = evap_rate
        self.max_eval = max_eval
        self.iterations = 0
        self.best_solution = 0
        self.no_ants = no_ants

        self.vertices = []
        self.edges = []
        self.ants = []
        self.generate_graph(path, q)

    def generate_graph(self, path, q):
        print("Generating Graph")
        with open(path, 'r') as xml_file:
            data = xml_file.read()
            bs4_data = BeautifulSoup(data, 'xml')

            vertices = bs4_data.find_all('vertex')
            for vertex_num in range(0, len(vertices)):
                # store vertex number in self.vertices
                self.vertices.append(vertex_num)

                edges = list(vertices[vertex_num].children)
                edges = list(filter("\n".__ne__, edges))

                for edge in edges:
                    cost = edge.get("cost")
                    location = {int(vertex_num), int(edge.get_text())}

                    exists = False
                    for created_edge in self.edges:
                        if created_edge.location == location:
                            exists = True

                    if not exists:
                        self.edges.append(Edge(int(float(cost)), location, q))

    def generate_new_ants(self):
        # Instantiate Ants
        print("Generating New Ants")
        self.ants = []
        for i in range(self.no_ants):
            self.ants.append(Ant(random.choice(self.vertices)))

    def get_edge(self, origin, dest):
        for edge in self.edges:
            if (origin in edge.location) and (dest in edge.location):
                return edge

    def calculate_ant_fitness(self, ant):
        total = 0
        for i in range(0, len(ant.visited)-1):
            edge = self.get_edge(ant.visited[i], ant.visited[i + 1])
            total += edge.cost
        return total

    def update_best_solution(self):
        if self.best_solution == 0:
            self.best_solution = self.ants[0]
        # check all ants until we find an ant with a better solution than the current best
        for ant in self.ants:
            if self.calculate_ant_fitness(ant) <= self.calculate_ant_fitness(self.best_solution):
                self.best_solution = ant

    def update_best_ant_pheromone(self):
        # check all ants until we find an ant with a better solution than the current best
        best_ant = self.ants[0]
        best_ant_fitness = self.calculate_ant_fitness(self.ants[0])

        for ant in self.ants:
            if self.calculate_ant_fitness(ant) <= best_ant_fitness:
                best_ant_fitness = self.calculate_ant_fitness(ant)
                best_ant = ant

        # update pheromone for the trail of this best ant
        for i in range(0, len(best_ant.visited)-1):
            edge = self.get_edge(best_ant.visited[i], best_ant.visited[i+1])
            edge.update_pheromone(best_ant_fitness)


    def start_simulation(self):
        print("Starting Simulation")

        while (self.iterations < self.max_eval):

            '''
            Generate initial ant population;
            Calculate the fitness values for each ant of the colony;
            Find optimal solution using selection methods;
            Update pheromone concentration;
            '''

            # generate new ants
            self.generate_new_ants()
            self.iterations += 1


            # move each ant from start to finish
            for ant in self.ants:
                ant.move(self.edges)
                print("Visited: " + str(ant.visited) + " Score = " + str(self.calculate_ant_fitness(ant)) + "\n")
            # at this point, all ants have completed traversing the graph

            # update pheromone for best ant
            self.update_best_ant_pheromone()

            # update best solution
            self.update_best_solution()

            # evaporate pheromone in all edges
            for edge in self.edges:
                edge.evaporate_pheromone(self.evap_rate)


class Edge:
    def __init__(self, cost, location, q):
        self.q = q
        self.cost = cost
        self.location = location
        self.pheromone = random.random()
    def __str__(self):
        return "Edge: " + str(self.location)

    def get_score(self):
        return self.pheromone

    def update_pheromone(self, ant_fitness):
        # After an ant completes its path, update the pheromone in the construction graph based on its fitness.
        self.pheromone += self.q/ant_fitness

    def evaporate_pheromone(self, e):
        self.pheromone *= e


class Ant:
    def __init__(self, vertex):
        self.visited = [vertex]

    def current_vertex(self):
        return self.visited[-1]

    def get_possible_moves(self, edges):
        possible_moves = []
        for edge in edges:
            if self.current_vertex() in edge.location:
                # the 'edge' must start or end at the current node
                move = edge.location.copy()
                move.remove(self.current_vertex()) # move now stores the destination vertex number
                dest = move.pop()
                if dest not in self.visited:
                    # the 'edge' is between the current node and an unvisited node
                    possible_moves.append(edge)

        return possible_moves

    def move(self, edges):
        finished = False

        while not finished:

            possible_moves = self.get_possible_moves(edges)
            # use the heuristic to choose a move out of the possible moves

            if len(possible_moves) == 0:
                # ant has traversed all nodes
                finished = True
                continue

            # Determine the best move
            best_move = possible_moves[0]
            best_score = possible_moves[0].get_score()

            for edge in possible_moves:
                if edge.get_score() > best_score:
                    best_score = edge.get_score()
                    best_move = edge

            # update the Ant
            move = best_move.location.copy()
            move.remove(self.current_vertex())
            new_node = move.pop()
            self.visited.append(new_node)


