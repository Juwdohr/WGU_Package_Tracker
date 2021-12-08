from dataclasses import dataclass, field
from datetime import time

from Graph import Graph, Vertex
import HashTable
from Package import Status
from Vehicle import Truck


@dataclass
class Hub:
    packages: HashTable
    gps: Graph
    HUB: Vertex = field(init=False, repr=False, default=None)
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
        for i in range(1, self.MAX_TRUCKS + 1):
            self.fleet.append(Truck(i, self.gps))
        self.HUB = self.gps.find_vertex("HUB")

    def get_packages_by_postal(self, truck_id: int) -> list:
        """
        Loads & sorts truck with all_packages
        Time Complexity: O(n)
        :rtype: list
        :return: list if Packages to load on to truck
        """

        load = []

        # Cycle through all package ids
        for package_id in range(1, len(self.packages) + 1):
            package = self.packages.search(package_id)

            # If package is delayed it cannot get onto a truck at this end_time.
            if package.status in [Status.DELIVERED, Status.ON_TRUCK, Status.DELAYED, Status.EN_ROUTE]:
                continue

            # Truck 1 needs to have all_packages from 84117, 84115, 84104
            if truck_id == 1 and package.postal_code in ['84117', '84115', '84104'] and len(
                    load) < self.MAX_TRUCK_CAPACITY:
                load.append(package)

            # Truck 2 needs to have all_packages from 84102, 84119, 84111, 84103
            if truck_id == 2 and package.postal_code in ['84102', '84119', '84111', '84123', '84103'] and len(
                    load) < self.MAX_TRUCK_CAPACITY:
                load.append(package)

            # Truck 3 needs all_packages from 84121, 84118, 84105, 84106, 84107
            if truck_id == 3 and package.postal_code in ['84121', '84118', '84105', '84106', '84107'] and len(
                    load) < self.MAX_TRUCK_CAPACITY:
                load.append(package)
        return load

    def release_trucks(self) -> None:
        self.fleet.reverse()
        for truck in self.fleet:
            if truck.id == 3:
                self.load_truck(truck, time(hour=8, minute=0))
                truck.deliver_packages(time(hour=20, minute=0))
                truck.drive(self.HUB)
            elif truck.id == 1:
                self.load_truck(truck, time(hour=8, minute=0))
                self.run_deliveries(truck)
            elif truck.id == 2:
                departure_time = self.fleet[0].time
                self.load_truck(truck, departure_time)
                self.run_deliveries(truck)

    # TODO Rename this here and in `release_trucks`
    def run_deliveries(self, truck):
        """
        Runs all deliveries
        Time Complexity: O(n^2)(
        :param truck:
        :return:
        """
        truck.deliver_packages(time(hour=9, minute=5))
        self.pickup_delayed_packages(truck)
        truck.deliver_packages(time(hour=20, minute=0))

    def load_truck(self, truck, departure_time: time):
        truck.set_departure(departure_time)
        truck.load(self.get_packages_by_postal(truck.id))

    def pickup_delayed_packages(self, truck: Truck) -> None:
        """
        Sets delayed packages to AT_HUB
        Sends truck to hub to get new all_packages
        Time Complexity: O(n^2)
        :param truck: Truck to load the packages
        :return: None
        """
        for package_id in range(1, len(self.packages) + 1):
            package = self.packages.search(package_id)
            if package.status == Status.DELAYED and truck.time >= time(9, 5):
                package.status = Status.AT_HUB

        load = self.get_packages_by_postal(truck.id)

        if len(load) > 0:
            if truck.location.label != "HUB":
                truck.drive(truck.map.find_vertex("HUB"))
            truck.load(load)
