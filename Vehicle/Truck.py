from dataclasses import dataclass, field
from datetime import datetime, timedelta, date, time

from Graph import Vertex


def load_truck(truck_id):
    switch = {
        1: [15, 16, 34, 14, 13, 30, 20],
        2: [29, 31, 40, 34, 18, 36, 3, 38],
        3: [6, 37, 25, 28, 9, 32, 2, 33]
    }

    return switch.get(truck_id, [])


def fastest_route(origin, destination):
    total_distance = 0

    current_location = destination
    while current_location is not origin:
        total_distance = current_location.distance + total_distance
        current_location = current_location.previous_vertex

    return total_distance


@dataclass
class Truck:
    id: int
    location: Vertex
    date_time: datetime = datetime.combine(date.today(), time(8, 0, 0))
    speed: int = 18
    trip_odometer: int = 0
    MAX_CAPACITY: int = 16
    load: list = field(default_factory=list)

    def load_package(self, package):
        if package not in self.load and len(self.load) < self.MAX_CAPACITY:
            self.load.append(package)
            return True
        return False

    def deliver_package(self, id: int):
        if id not in self.load:
            return False
        self.load.remove(id)
        return True

    def update_package(self, package_id, new_address):
        for package in self.load:
            if package_id == package:
                package.delivery_address = new_address

    def travel(self, next_location):
        distance_traveled = fastest_route(self.location, next_location)
        self.trip_odometer += distance_traveled
        self.location = next_location
        self.time += timedelta(hours=(distance_traveled / self.speed))
