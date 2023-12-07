import random
from bs4 import BeautifulSoup


class ACOGraph:
    def __init__(self, path, no_ants, q, evap_rate, max_eval):
        self.q = q
        self.evap_rate = evap_rate
        self.max_eval = max_eval

        self.vertices = []
        self.edges = []
        self.ants = []
        self.generate_graph(path, no_ants)

    def generate_graph(self, path, no_ants):
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
                    location = {vertex_num, int(edge.get_text())}

                    exists = False
                    for created_edge in self.edges:
                        if created_edge.location == location:
                            exists = True

                    if not exists:
                        self.edges.append(Edge(cost, location))

        # Instantiate Ants
        for i in range(no_ants):
            self.ants.append(Ant())


class Edge:
    def __init__(self, cost, location):
        self.cost = cost
        self.location = location
        self.pheromone = random.randint(0, 1)

    def __str__(self):
        return "Edge: " + str(self.location)


class Ant:
    def __init__(self):
        self.visited = []
        self.current_vertex = 0
        self.current_cost = 0

