from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Optional

from Graph import Vertex, Graph, find_shortest_paths
from Package import Package, Status


def is_time_between(start_time, end_time, check_time) -> bool:
    """
    Checks if a time is between two other times.
    :param start_time: The start time.
    :param end_time: The end time.
    :param check_time: The time to check.
    :return: True if the time is between the start and end time.
    """
    if start_time < end_time:
        return start_time <= check_time <= end_time
    else:
        return start_time <= check_time or check_time <= end_time


def update_needed(package_notes: str, current_time: time) -> bool:
    """
    Checks if package needs to be updated.
    Time Complexity: O(n)
    :param package_notes: Package notes to check
    :param current_time: time to check against
    :return:
    """
    return 'wrong address' in package_notes and current_time >= time(
        hour=10, minute=20
    )


def same_location(package_delivery_address, current_location):
    return package_delivery_address == current_location


def is_smaller_distance(distance, current_distance):
    return distance < current_distance


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

    def load(self, packages: list) -> None:
        """
        Function to represent loading truck with all_packages
        Time Complexity: 0(n)
        :param packages: List of all_packages to be added to truck
        :return: None
        """

        # clear out the delivered all_packages
        self.cargo += packages

        for package in packages:
            if package.status in [Status.DELIVERED]:
                packages.remove(package)
            else:
                package.status = Status.ON_TRUCK
                package.departure_time = self.time

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
        Marks the package as delivered with a time stamp
        Time Complexity: O(1)
        :param package: Package to be delivered
        :return: bool
        """
        self.cargo.remove(package)
        return package.deliver(self.time)

    def set_departure(self, departure_time: time) -> None:
        """
        Marks packsages on the truck as EN_ROUTE, and sets the trucks time and package departure time
        Time Complexity:(n)
        :param departure_time: Time of departure
        :return: None
        """
        self.time = departure_time

        for package in self.cargo:
            if package.status in [Status.AT_HUB, Status.ON_TRUCK]:
                package.status = Status.ON_TRUCK
                package.departure_time = self.time

    def deliver_packages(self, end_time):
        """
        Delivers packages on the truck until specified time
        Time Complexity: O(n^2)
        :param end_time: Specified time
        :return: None
        """
        while len(self.cargo) > 0 and self.time < end_time:
            # Check distances and times for all packages
            # Deliver package with same location, within 15 minuts, and/or the closest
            find_shortest_paths(self.map, self.location)

            next_deliverable = self.find_next_deliverable()

            next_location = self.map.find_vertex(next_deliverable.address)

            if next_location is not self.location:
                self.drive(next_location)

            self.deliver_package(next_deliverable)

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
            return self.get_next_package(priority_queue)
        else:
            return self.get_next_package()

    def get_priority_queue(self) -> list:
        """
        Returns a list of packages that are ready to be delivered based on time
        Time Complexity: O(n)
        :return: list of packages
        """

        # Check for priority

        queue = []

        for package in self.cargo:
            if update_needed(package.notes.lower(), self.time):
                package.delivery_address = "410 S State St\nSalt Lake City, UT 84111"
            elif 'wrong address' in package.notes.lower() or package.status is Status.DELIVERED:
                continue
            elif same_location(package.address, self.location.label):
                return [package]
            elif is_time_between(
                self.time,
                (datetime.combine(datetime.today(), self.time) + timedelta(minutes=30)).time(),
                package.delivery_deadline
            ):
                queue.append(package)
        return queue

    def get_next_package(self, packages: list = None) -> Package:
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
            if update_needed(package.notes.lower(), self.time):
                package.delivery_address = "410 S State St\nSalt Lake City, UT 84111"
            elif 'wrong address' in package.notes.lower() or package.status is Status.DELIVERED:
                continue

            package_delivery_location: Vertex = self.map.find_vertex(package.address)
            if same_location(package.address, self.location.label):
                return package
            elif is_smaller_distance(package_delivery_location.distance, distance):
                distance = package_delivery_location.distance
                next_package = package

        return next_package
