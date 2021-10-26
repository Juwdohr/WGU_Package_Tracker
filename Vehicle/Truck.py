from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import Type

import HashTable
from Graph import Graph, Vertex, dijkstra_shortest_path


def fastest_route(origin: Vertex, destination: Vertex) -> int:
    total_distance = 0
    path = ''
    current_location = destination
    while current_location is not origin:
        path = '->' + current_location.label + path
        total_distance += current_location.distance
        current_location = current_location.previous_vertex
    path = origin.label + path
    return path, total_distance

@dataclass
class Truck:
    id: int
    location: Vertex
    load: list = field(default_factory=list)
    time: datetime = datetime.combine(date.today(), time(8, 0, 0))
    speed: int = 18
    trip_odometer: int = 0
    MAX_CAPACITY: int = 16

    def __post_init__(self):
        self.id = int(self.id)

    def load_package(self, id: int) -> bool:
        if id not in self.load and len(self.load) < self.MAX_CAPACITY:
            self.load.append(id)
            return True
        return False

    def deliver_package(self, id: int, _table: HashTable, _graph: Graph):
        package = _table.search(id)
        next_location = _graph.find_vertex(package.address)
        if next_location is not self.location:
            dijkstra_shortest_path(_graph, self.location)
            self.travel(next_location)
        print(self.time.time() > time(10, 20), f'Truck ID: {self.id}, Package ID: {id}, Time: {self.time.time()}')
        # if(self.time > time(10, 20) and 9 in self.load:
        #     package
        package.deliver(self.time.time())

    def travel(self, next_location: Vertex):
        distance_traveled = next_location.distance
        self.trip_odometer += distance_traveled
        self.location = next_location
        self.time += timedelta(hours=(distance_traveled / self.speed))
