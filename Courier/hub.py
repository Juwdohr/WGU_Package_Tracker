from dataclasses import dataclass, field
from datetime import time

import Graph
import HashTable
import Package
import Vehicle


def is_deliverable(package: Package.Package, current_time: time):
    """
    Updates status and checks if status of package is deliverable
    Time Complexity: O(1)
    :param package: Package to check
    :param current_time: Current current_time
    :return:
    """
    if package.status == Package.Status.DELAYED and current_time >= time(9, 5):
        package.status = Package.Status.AT_HUB
    return package.status not in [
        Package.Status.DELIVERED,
        Package.Status.ON_TRUCK,
        Package.Status.DELAYED,
        Package.Status.EN_ROUTE,
    ]


@dataclass
class Hub:
    packages: HashTable
    gps: Graph.Graph
    HUB: Graph.Vertex = field(init=False, repr=False, default=None)
    MAX_TRUCKS: int = field(init=False, repr=False, default=3)
    MAX_TRUCK_CAPACITY: int = field(init=False, repr=False, default=16)
    fleet: list = field(init=False, repr=False, default_factory=list)

    def __post_init__(self) -> None:
        """
        Creates all trucks for initial fleet.
        Time Complexity: O(n)
        :return: None
        """
        # create a fleet of trucks
        for i in range(1, self.MAX_TRUCKS):
            self.fleet.append(Vehicle.Truck(i, self.gps))
        self.HUB = self.gps.find_vertex("HUB")

    def get_packages_by_postal(self, truck: Vehicle.Truck) -> None:
        """
        Loads & sorts truck with all_packages
        Time Complexity: O(n)
        :rtype: list
        :return: list if Packages to load on to truck
        """

        # Cycle through all package ids
        for package_id in range(1, len(self.packages) + 1):
            package = self.packages.search(package_id)

            # Truck 1 needs to have packages from 84117, 84115, 84104, 84105, 84106, 84107
            # Truck 2 needs to have packages from 84102, 84119, 84111, 84103, 84121, 84118
            if (
                    truck.id == 1
                    and package.postal_code in ['84117', '84115', '84104', '84105', '84106', '84107']
                    and len(truck.cargo) < self.MAX_TRUCK_CAPACITY
                    and is_deliverable(package, truck.time)
            ):
                truck.load(package)

            if (
                truck.id == 2
                and package.postal_code
                in ['84102', '84119', '84111', '84123', '84103', '84121', '84118']
                and len(truck.cargo) < self.MAX_TRUCK_CAPACITY
                and is_deliverable(package, truck.time)
            ):
                truck.load(package)

    def release_trucks(self) -> None:
        """
        Releases each truck to run deliveries
        Time Complexity: O(n^2)
        :return: None
        """
        departure_time = time(hour=8, minute=0)
        for truck in self.fleet:
            self.load_truck(truck, departure_time)
            self.run_deliveries(truck)

    def run_deliveries(self, truck) -> None:
        """
        Runs all deliveries
        Time Complexity: O(n^2)
        :param truck:
        :return:
        """
        truck.deliver_packages(time(hour=9, minute=5))
        self.get_packages_by_postal(truck)
        truck.deliver_packages(time(hour=20, minute=0))

    def load_truck(self, truck, departure_time: time):
        """
        Sets the departure time and loads the truck
        Time Complexity: O(n)
        :param truck:
        :param departure_time:
        :return:
        """
        truck.set_departure(departure_time)
        self.get_packages_by_postal(truck)