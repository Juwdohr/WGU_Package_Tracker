from dataclasses import dataclass

from . import Graph, Vertex


@dataclass
class Directed(Graph):
    """Represents a Directed Graph"""

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0) -> None:
        """
        Function to a directed edge to a graph
        Time Complexity: O(1)
        :param from_vertex: Starting Vertex
        :param to_vertex: Ending Vertex
        :param weight: Weight to drive to Vertex
        :return: None
        """
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def __repr__(self):
        return 'Directed()'

    def __str__(self):
        return self.adjacency_list
