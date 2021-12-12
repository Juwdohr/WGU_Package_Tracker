from dataclasses import dataclass
from typing import Optional

from . import Graph, Vertex


@dataclass
class Directed(Graph):
    """Represents a Directed Graph"""

    def extract_vertices(self, data_fieldnames) -> None:
        """
        Converts fieldnames from CSV File to vertices
        Time complexity: O(n)
        :param data_fieldnames: CSV data fieldnames
        :return: None
        """
        for name in data_fieldnames:
            if name != '':
                self.add_vertex(Vertex(name.strip().split('\n')[0]))

    def build_graph(self, data) -> None:
        """
        Builds the graph from csv data
        Time complexity: O(n)
        :param data: CSV Data
        :return: None
        """
        for row in data:
            start_vertex: Vertex = self.find_vertex(row.pop('').strip().split('\n')[0])
            for name, distance in row.items():
                if name != '':
                    end_vertex: Vertex = self.find_vertex(name.strip().split('\n')[0])
                    self.add_directed_edge(start_vertex, end_vertex, float(distance))

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
