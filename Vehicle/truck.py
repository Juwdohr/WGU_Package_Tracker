from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Optional

from Graph import Vertex, Graph, find_shortest_paths
from Package import Package, Status


def is_time_between(start_time, end_time, check_time):
    """
    Checks if a current_time is between two other times.
    Time Complexity: O(1)
    :param start_time: The start current_time.
    :param end_time: The end current_time.
    :param check_time: The current_time to check.
    :return: True if the current_time is between the start and end current_time.
    """
    if start_time < end_time:
        return start_time <= check_time <= end_time
    else:
        return start_time <= check_time or check_time <= end_time


def has_wrong_address(package: Package, current_time: time) -> bool:
    """
    Checks package address & updates if necessary at correct time.
    Time complexity: O(1)
    :param package: Package to check address and notes on.
    :param current_time: Trucks current time
    :return: True if the wrong address is present, otherwise false
    """
    if 'wrong address' in package.notes.lower() and current_time >= time(hour=10, minute=20):
        package.delivery_address = "410 S State St\nSalt Lake City, UT 84111"
        return False
    if 'wrong address' in package.notes.lower():
        return True


@dataclass
class Truck:
    id: int
    gps: Graph
    cargo: list[Package] = field(default_factory=list)
    time: time = time(8, 0)
    SPEED: int = field(init=False, repr=False, default=18)
    trip_odometer: int = field(init=False, repr=False, default=0)
    MAX_CAPACITY: int = field(init=False, repr=False, default=16)
    location: Vertex = field(init=False, repr=False)

    def __post_init__(self):
        """
        Sets default location, and parses correct data types
        Time Complexity: O(n)
        :return:
        """
        self.id = int(self.id)
        self.location = self.gps.find_vertex('HUB')  # O(n)

    def load(self, package: Package) -> None:
        """
        Function to represent loading truck with all_packages
        Time Complexity: 0(1)
        :param package: Package to be added to cargo
        :return: None
        """
        package.status = Status.ON_TRUCK
        package.departure_time = self.time
        self.cargo.append(package)

    def drive(self, next_location: Vertex) -> None:
        """
        Moves Truck to the next location and updates the Trip Odometer
        and the Trucks Clock
        Time Complexity: O(1)
        :param next_location: Vertex of next package delivery location
        :return: None
        """

        self.trip_odometer += next_location.distance
        self.location = next_location

        self.time = (datetime.combine(datetime.today(), self.time) + timedelta(hours=(
                next_location.distance / self.SPEED
        ))).time()

    def deliver_package(self, package: Package) -> bool:
        """
        Marks the package as delivered with a current_time stamp
        Time Complexity: O(1)
        :param package: Package to be delivered
        :return: bool
        """
        self.cargo.remove(package)
        return package.deliver(self.time)

    def set_departure(self, departure_time: time) -> None:
        """
        Marks packsages on the truck as EN_ROUTE, and sets the trucks current_time and package departure current_time
        Time Complexity: O(1)
        :param departure_time: Time of departure
        :return: None
        """
        self.time = departure_time

    def deliver_packages(self, end_time):
        """
        Delivers packages on the truck until specified current_time.
        Time Complexity: O(n^2)
        :param end_time: Specified current_time
        :return: None
        """
        while len(self.cargo) > 0 and self.time < end_time:
            # Check distances and times for all packages
            # Deliver package with same location, within 15 minutes, and/or the closest
            find_shortest_paths(self.gps, self.location)

            package = self.find_next_deliverable()
            next_location = self.gps.find_vertex(package.address)

            while next_location is not self.location:
                self.drive(next_location)
                if 'wrong address' in package.notes.lower() and self.time >= time(hour=10, minute=20):
                    package.delivery_address = "410 S State St\nSalt Lake City, UT 84111"
                    next_location = self.gps.find_vertex(package.address)

            self.deliver_package(package)
        self.drive(self.gps.find_vertex("HUB"))

    def find_next_deliverable(self) -> Package:
        """
        Finds the closest package to truck based on next_delivery_time
        Time Complexity: O(n)
        :return: Package to deliver
        """
        priority_queue = self.get_priority_queue()

        if len(priority_queue) == 1:
            return priority_queue.pop()
        elif len(priority_queue) > 1:
            return self.closest_package(priority_queue)
        else:
            return self.closest_package()

    def get_priority_queue(self) -> list:
        """
        Returns a list of packages that are ready to be delivered based on current_time
        Time Complexity: O(n)
        :return: list of packages
        """
        queue = []
        next_delivery_time = (datetime.combine(datetime.today(), self.time) + timedelta(minutes=30)).time()

        # Check for priorty
        for package in self.cargo:
            if has_wrong_address(package, self.time):
                continue

            # Check if package address is same as current truck location
            if package.address == self.location.label:
                return [package]

            if is_time_between(self.time, next_delivery_time, package.delivery_deadline):
                queue.append(package)
        return queue

    def closest_package(self, packages: list = None) -> Package:
        """
        Finds the closest package to truck based on distance
        Time Complexity: O(n)
        :return: Package to deliver
        """
        if packages is None:
            packages = self.cargo

        distance = float('inf')
        next_package = packages[0]
        for package in packages:
            if has_wrong_address(package, self.time):
                continue

            package_delivery_location: Optional[Vertex] = self.gps.find_vertex(package.address)

            if package_delivery_location == self.location.label:
                return package

            if package_delivery_location.distance < distance:
                distance = package_delivery_location.distance
                next_package = package

        return next_package
