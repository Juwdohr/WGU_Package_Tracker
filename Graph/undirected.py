from dataclasses import dataclass

from . import Directed, Vertex


@dataclass
class Undirected(Directed):
    """Represents an Undirected Graph"""

    def add_undirected_edge(self, vertex_a: Vertex, vertex_b: Vertex, weight: float = 1.0) -> None:
        """
        Adds an undirected edge to a Graph
        Time Complexity: 0(1)
        :param vertex_a: Starting Vertex
        :param vertex_b: Ending Vertex
        :param weight: Weight to get from A to B
        :return: None
        """

        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def __repr__(self):
        """
        Returns string representation of
        Time Complexity: O(1)
        :return:
        """

        return 'Undirected()'

    def __str__(self):
        """
        Returns string representation
        Time Complexity: O(n)
        :return: string representation of Adjacency List
        """

        return self.adjacency_list.__str__()
