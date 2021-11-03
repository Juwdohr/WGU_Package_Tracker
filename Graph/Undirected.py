from dataclasses import dataclass

from . import Directed, Vertex


@dataclass
class Undirected(Directed):
    """Represents an Undirected Graph"""

    def add_undirected_edge(self, vertex_a: Vertex, vertex_b: Vertex, weight: float = 1.0) -> None:
        """
        Adds an undirected edge to a Graph
        :param vertex_a: Starting Vertex
        :param vertex_b: Ending Vertex
        :param weight: Weight to get from A to B
        :return: None
        """
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def __repr__(self):
        return 'Undirected()'

    def __str__(self):
        return self.adjacency_list.__str__()
