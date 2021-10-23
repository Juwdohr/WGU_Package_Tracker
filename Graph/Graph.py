from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from .Vertex import Vertex


@dataclass
class Graph(ABC):
    vertices: list = field(default_factory=list)
    adjacency_list: dict = field(default_factory=dict)
    edge_weights: dict = field(default_factory=dict)

    @abstractmethod
    def add_vertex(self, new_vertex: Vertex):
        pass

    def find_vertex(self, label):
        for vertex in self.vertices:
            if vertex.label != label:
                continue
            return vertex
        return None