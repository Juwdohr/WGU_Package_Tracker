import csv
from dataclasses import dataclass, field
from typing import Dict, List

from . import Graph, Vertex


@dataclass
class Directed(Graph):
    """Represents a Directed Graph"""

    adjacency_list: Dict['Vertex', List['Vertex']] = field(init=False, default_factory=dict)
    edge_weights: Dict['tuple[Vertex, Vertex]', float] = field(init=False, default_factory=dict)

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

    def build_edges(self, data: csv.DictReader) -> None:
        """
        Creates all edges from the graph.
        Time Complexity: O(n)
        :param data: CSV Data from file
        :return:
        """
        for row in data:
            start_vertex = self.find_vertex(row.pop('').strip().split('\n')[0])
            for name, distance in row.items():
                if name != '':
                    end_vertex = self.find_vertex(name.strip().split('\n')[0])
                    self.add_directed_edge(start_vertex, end_vertex, float(distance))

    def extract_vertices(self, data: csv.DictReader) -> None:
        """
        Takes the data and extracts the Vertices
        Time Complexity: O(n)
        :param data: CSV Data from file
        :return: None
        """
        for name in data.fieldnames:
            if name != '':
                self.add_vertex(Vertex(name.strip().split('\n')[0]))

    def __repr__(self):
        return 'Directed()'

    def __str__(self):
        return self.adjacency_list
