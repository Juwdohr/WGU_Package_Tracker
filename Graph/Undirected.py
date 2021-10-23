from dataclasses import dataclass
from Graph.Directed import Directed
from Graph.Vertex import Vertex


@dataclass
class Undirected(Directed):

    def add_vertex(self, new_vertex: Vertex):
        super().add_vertex(new_vertex)

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0):
        super().add_directed_edge(from_vertex, to_vertex, weight)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def find_vertex(self, label):
        return super().find_vertex(label)
