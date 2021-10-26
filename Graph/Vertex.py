from dataclasses import dataclass, field
from typing import Type


@dataclass(eq=False, unsafe_hash=False)
class Vertex:
    # Dataclass for a new Vertx object. All vertex objects
    # start with a distance of positive infinity.
    label: str
    distance: float = field(init=False)
    previous_vertex: Type['Vertex'] = field(init=False)

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.distance = float('inf')
        self.previous_vertex = None
