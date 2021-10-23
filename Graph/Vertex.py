from dataclasses import dataclass, field
from typing import Any


@dataclass(unsafe_hash=True)
class Vertex:
    label: str
    distance: float = float('inf')
    previous_vertex: Any = None

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.distance = float('inf')
        self.previous_vertex = None
