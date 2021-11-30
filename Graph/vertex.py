from dataclasses import dataclass, field
from typing import Type, Optional


@dataclass(eq=False, unsafe_hash=False)
class Vertex:
    """This represents a point within a graph"""
    # Dataclass for a new Vertx object. All vertex objects
    # start with a distance of positive infinity.
    label: str
    distance: float = field(init=False)
    previous_vertex: Optional['Vertex'] = field(init=False)

    def __post_init__(self):
        """
        Sets the uninitialized variables to their defaults
        Time Complexity: O(1)
        :return: None
        """
        self.reset()

    def reset(self):
        """
        Resets the vertex to original values.
        Time Complexity: O(1)
        :return: None
        """
        self.distance = float('inf')
        self.previous_vertex = None
