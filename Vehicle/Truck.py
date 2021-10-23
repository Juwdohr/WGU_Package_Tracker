from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta


def fastest_route(location, next_location) -> int:
    pass


@dataclass
class Truck:
    id: int
    location: str
    time: datetime = datetime.combine(date.today(), time(8, 0, 0))
    speed: int = 18
    trip_odometer: int = 0
    MAX_CAPACITY: int = 16
    load: list = field(default_factory=list)

    def load_package(self, id: int) -> bool:
        if id not in self.load and len(self.load) < self.MAX_CAPACITY:
            self.load.append(id)
            return True
        return False

    def deliver_package(self, id: int) -> bool:
        if id not in self.load:
            return False
        self.load.remove(id)
        return True

    def travel(self, next_location):
        distance_traveled = fastest_route(self.location, next_location)
        self.trip_odometer += distance_traveled
        self.location = next_location
        self.time += timedelta(hours=distance_traveled / self.speed)

