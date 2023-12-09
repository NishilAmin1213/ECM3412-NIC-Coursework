import random
from bs4 import BeautifulSoup


class ACOGraph():
    def __init__(self, path, no_ants, q, evap_rate, max_eval):
        self.evap_rate = evap_rate
        self.max_eval = max_eval
        self.eval_counter = [0]
        self.best_solution = 0
        self.no_ants = no_ants

        self.vertices = []
        self.ants = []
        self.graph = []
        self.generate_graph(path, q)
        Edge.q = q
        Ant.graph = self.graph
        Ant.eval_counter = self.eval_counter

    def generate_graph(self, path, q):
        print("Generating Graph")
        with open(path, 'r') as xml_file:
            data = xml_file.read()
            bs4_data = BeautifulSoup(data, 'xml')

            vertices = bs4_data.find_all('vertex')
            self.graph = [[0 for i in range(len(vertices))] for j in range(len(vertices))]

            for vertex_num in range(0, len(vertices)):
                # store vertex numbers in self.vertices
                self.vertices.append(vertex_num)

                for edge in list(filter("\n".__ne__, list(vertices[vertex_num].children))):
                    cost = edge.get("cost")
                    location = {vertex_num, int(edge.get_text())}
                    tmp_edge = Edge(int(float(cost)), q, location)

                    if self.graph[vertex_num][int(edge.get_text())] == 0:
                        self.graph[vertex_num][int(edge.get_text())] = tmp_edge
                        self.graph[int(edge.get_text())][vertex_num] = tmp_edge

    def generate_new_ants(self):
        print("Generating New Ants")
        self.ants = []
        for i in range(self.no_ants):
            self.ants.append(Ant(random.choice(self.vertices)))

    def start_simulation(self):
        print("Starting Simulation")

        while self.eval_counter[0] < self.max_eval:
            x = self.eval_counter[0]
            x1 = Ant.eval_counter[0]
            y = self.max_eval
            '''
            Generate initial ant population;
            Calculate the fitness values for each ant of the colony;
            Find optimal solution using selection methods;
            Update pheromone concentration;
            '''

            # generate new ants
            self.generate_new_ants()

            # move ants
            for ant in self.ants:
                ant.move()

            # at this point, all ants have completed traversal

            # find best ant of this iteration
            best_ant = Ant.get_best_ant(self.ants)

            # update pheromone for the best ant
            best_ant.update_pheromone_trail()

            # update best solution of all time
            if self.best_solution == 0:
                self.best_solution = best_ant

            if best_ant.fitness < self.best_solution.fitness:
                self.best_solution = best_ant

            # evaporate pheromone in all edges
            for row in self.graph:
                for edge in row:
                    if edge != 0:
                        edge.evaporate_pheromone()


class Edge:
    q = 0

    def __init__(self, cost, q, location):
        self.cost = cost
        self.pheromone = random.random()
        self.location = location

    def get_score(self):
        return self.pheromone

    def get_cost(self):
        return self.cost

    def update_pheromone(self, ant_fitness):
        self.pheromone += self.q/ant_fitness

    def evaporate_pheromone(self):
        self.pheromone *= self.q


class Ant:

    def __init__(self, vertex):
        self.fitness = 0
        self.visited = [vertex]
        self.current_vertex = vertex

    @classmethod
    def get_best_ant(cls, ants):
        # check all ants until we find an ant with a better solution than the current best
        best_ant = ants[0]
        best_fitness = ants[0].fitness

        for ant in ants:
            if ant.fitness <= best_fitness:
                best_fitness = ant.fitness
                best_ant = ant

        return best_ant


    def update_pheromone_trail(self):
        for i in range(0, len(self.visited) - 1):
            edge = Ant.graph[self.visited[i]][self.visited[i + 1]]
            edge.update_pheromone(self.fitness)

    def get_possible_moves(self):
        possible_moves = []

        for row in range(0, len(Ant.graph)):
            for col in range(0, len(Ant.graph)):

                # make sure the edge starts or ends from the current vertex
                if (row == self.current_vertex) or (col == self.current_vertex):
                    # make sure that one end of the edge has not been visited
                    if (row not in self.visited) or (col not in self.visited):
                        # this is a valid edge
                        possible_moves.append(Ant.graph[row][col])

        return possible_moves

    def get_best_move(self, possible_moves):
        # Determine the best move out of the array of possible moves passed in
        best_move = possible_moves[0]
        best_score = possible_moves[0].get_score()

        for edge in possible_moves:
            if edge.get_score() > best_score:
                best_score = edge.get_score()
                best_move = edge

        return best_move

    def set_fitness(self):
        for i in range(0, len(self.visited) - 1):
            edge = Ant.graph[self.visited[i]][self.visited[i + 1]]
            self.fitness += edge.get_cost()
        Ant.eval_counter[0] += 1

    def move(self):
        finished = False

        while not finished:

            # get possible moves
            possible_moves = self.get_possible_moves()

            # check if the ant has completed its traversal
            if len(possible_moves) == 0:
                # Ant has finished, set its fitness
                self.set_fitness()
                x = Ant.eval_counter[0]
                finished = True
                print("ANT: " + str(self.visited) + " Score: " + str(self.fitness) + " Eval = " + str(Ant.eval_counter[0]))
                continue

            # get the best move out of the possible moves
            move = self.get_best_move(possible_moves)

            # make the move using this edge
            move = move.location.copy()
            move.remove(self.current_vertex)
            new_vertex = move.pop()
            self.visited.append(new_vertex)
            self.current_vertex = new_vertex
