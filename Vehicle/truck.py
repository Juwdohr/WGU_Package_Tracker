from dataclasses import dataclass, field
from datetime import datetime, time, timedelta

from Graph import Vertex, Graph
from Package import Package, Status


@dataclass
class Truck:
    id: int
    map: Graph
    cargo: list[Package] = field(default_factory=list)
    time: time = time(8, 0)
    SPEED: int = field(init=False, repr=False, default=18)
    trip_odometer: int = field(init=False, repr=False, default=0)
    MAX_CAPACITY: int = field(init=False, repr=False, default=16)
    location: Vertex = field(init=False, repr=False)

    def __post_init__(self):
        """
        Sets default location, and parses correct data types
        Time Complexity: O(1)
        :return:
        """
        self.id = int(self.id)
        self.location = self.map.find_vertex('HUB')

    def load(self, item: Package) -> bool:
        """
        Function to represent loading truck with packages
        Time Complexity: 0(n * log n)
        :param item: Package to be added onto truck
        :return: True if package is not already on the truck, and the truck
        has space to add package, otherwise False


        """
        # clear out the delivered packages
        undelivered_packages = [package for package in self.cargo if package.status != Status.DELIVERED]

        if item not in self.cargo and len(undelivered_packages) < self.MAX_CAPACITY:
            item.status = Status.ON_TRUCK
            undelivered_packages.append(item)
            undelivered_packages.sort(key=lambda package: package.delivery_deadline, reverse=False)
            undelivered_packages.sort(key=lambda package: package.delivery_address, reverse=True)

            self.cargo = undelivered_packages
            return True
        return False

    def drive(self, next_location: Vertex) -> None:
        """
        Moves Truck to the next location and updates the Trip Odometer
        and the Trucks Clock
        Time Complexity: O(1)
        :param next_location: Vertex of next package delivery location
        :return: None
        """
        distance_traveled = next_location.distance
        self.trip_odometer += distance_traveled
        self.location = next_location

        self.time = (datetime.combine(datetime.today(), self.time) + timedelta(hours=(distance_traveled / self.SPEED))).time()

    def deliver_package(self, package: Package) -> bool:
        """
        Marks the package as delivered with a time stamp
        Time Complexity: O(1)
        :param package: Package to be delivered
        :return: None
        """
        return package.deliver(self.time)
