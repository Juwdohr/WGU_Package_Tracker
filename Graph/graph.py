from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from typing import Optional, Dict, List, NewType, Tuple

from .vertex import Vertex

@dataclass
class Graph(ABC):
    """Abstract class defining a graph"""
    adjacency_list: Dict['Vertex', List['Vertex']] = field(init=False, default_factory=dict)
    edge_weights: Dict['tuple[Vertex, Vertex]', float] = field(init=False, default_factory=dict)

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def add_vertex(self, new_vertex) -> None:
        """
        Adds a Vertex to the graph
        Time Complexity: O(1)
        :param new_vertex: Vertex to add to graph
        :return: None
        """
        self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}

    def find_vertex(self, label: str) -> Optional[Vertex]:
        """
        Function to find a graph
        Time Complexity: O(n)
        :param label: Label of Vertex to find
        :return: Vertex with corresponding label
        """
        for key in self.adjacency_list:
            if key.label == label:
                return key
        return None
