from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta

from Graph import Vertex
from Package import Package


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

    def deliver_package(self, package: Package):
        package.deliver(self.time)

    def travel(self, next_location: Vertex):
        distance_traveled = next_location.distance
        self.trip_odometer += distance_traveled
        self.location = next_location
        self.time += timedelta(hours=(distance_traveled / self.speed))
