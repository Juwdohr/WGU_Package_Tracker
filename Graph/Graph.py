from abc import ABC, abstractmethod

from .Vertex import Vertex


class Graph(ABC):
    def __init__(self) -> None:
        self.adjacency_list = {}  # vertex dictionary {key:value}
        self.edge_weights = {}  # edge dictionary {key:value}

    def add_vertex(self, new_vertex) -> None:
        self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0) -> None:
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def find_vertex(self, label: str) -> Vertex:
        for key in self.adjacency_list:
            if key.label != label:
                continue
            return key
        return None

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
