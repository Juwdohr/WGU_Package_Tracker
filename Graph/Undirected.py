from .Directed import Directed


class Undirected(Directed):

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def __repr__(self):
        return 'Undirected()'

    def __str__(self):
        return self.adjacency_list.__str__()