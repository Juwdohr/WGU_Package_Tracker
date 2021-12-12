from dataclasses import dataclass

from . import Directed, Vertex


@dataclass
class Undirected(Directed):
    """Represents an Undirected Graph"""

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
        """"
        Builds the graph from csv data
        Time complexity: O(n^2)
        :param data: CSV Data
        :return: None
        """
        for row in data:
            start_vertex: Vertex = self.find_vertex(row.pop('').strip().split('\n')[0])
            for name, distance in row.items():
                if name != '':
                    end_vertex: Vertex = self.find_vertex(name.strip().split('\n')[0])
                    self.add_undirected_edge(start_vertex, end_vertex, float(distance))

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
