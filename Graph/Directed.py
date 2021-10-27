from .Graph import Graph


class Directed(Graph):

    def add_directed_edge(self, from_vertex, to_vertex, weight: float = 1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def __repr__(self):
        return 'Directed()'

    def __str__(self):
        return self.adjacency_list
