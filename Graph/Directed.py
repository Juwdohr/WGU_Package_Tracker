from dataclasses import dataclass
from .Graph import Graph
from .Vertex import Vertex


@dataclass
class Directed(Graph):

    def add_vertex(self, new_vertex: Vertex):
        self.vertices.append(new_vertex)
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def find_vertex(self, label):
        return super().find_vertex(label)
