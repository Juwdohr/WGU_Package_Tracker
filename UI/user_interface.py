from dataclasses import dataclass
from datetime import time, datetime

import HashTable
from Package import Status


@dataclass
class UserInterface:
    packages: HashTable.Chained

    def print_header(self, fleet: list):
        """
        Prints the header for the program along with each truck's mileage, and total mileage.
        Time Complexity: O(n)
        :param fleet:
        :return:
        """

        print("Welcome to the Courier Package Delivery System")
        total_distance = 0
        for truck in fleet:
            print(f'Truck {truck.id}: {round(truck.trip_odometer, 1)} & finished at {format(truck.time, "%I:%M %p")}')
            total_distance += truck.trip_odometer
        print(f'Total: {round(total_distance, 1)}')

    def lookup_single_package(self, package_id: int, lookup_time: time) -> None:
        """
        Looks up single package, and prints it status at a specified end_time.
        Time Complexity: O(n)
        :param package_id: ID of package to lookup
        :param lookup_time: Time to lookup
        :return:
        """
        package = self.packages.search(package_id)  # O(n)

        if package is None:
            return print('ID is not recognized')

        if lookup_time < package.departure_time or package.departure_time is None:
            status = Status.AT_HUB if 'delayed' not in package.notes.lower() else Status.DELAYED
            print(package, f', {status.name}')

        elif package.departure_time < lookup_time < package.delivery_time:
            print(package, f', {Status.EN_ROUTE.name}')

        elif package.delivery_time < lookup_time:
            print(package, f', {package.status.name} @ {package.delivery_time}')

        else:
            print('Time not recognized please try again')

    def lookup_all_packages(self, lookup_time: time) -> None:
        """
        Loops through entire hashtable, printing all all_packages out based on end_time.
        Time Complexity: O(n)
        :param lookup_time:
        :return:
        """

        for package_id in range(1, len(self.packages) + 1):
            self.lookup_single_package(package_id, lookup_time)

    def run(self) -> None:
        """
        User interface to get data from user
        Time Complexity: O(n)
        :return:
        """
        user_input = ''

        while user_input != 3:
            print("Please choose one of the following options:")
            print("1. Get Specific Package Data")
            print("2. Get All Package Data")
            print("3. Exit")
            user_input = int(input("> "))

            if user_input == 1:
                package_id = int(input("Please enter the Package ID to lookup: "))
                lookup_time = datetime.strptime(input("Please enter a end_time in 24 hour format (HH:mm):  "),
                                                '%H:%M').time()
                print("ID, Delivery Address, Mass in KG, Delivery Deadline, Status")
                self.lookup_single_package(package_id, lookup_time)
                input("Press enter to continue.")
                continue

            if user_input == 2:
                print('Getting all Package Data...')
                lookup_time = datetime.strptime(input("Please enter a end_time in 24 hour format (HH:mm):  "),
                                                '%H:%M').time()
                print("ID, Delivery Address, Mass in KG, Delivery Deadline, Status")
                self.lookup_all_packages(lookup_time)
                input("Press enter to continue.")
                continue

        print("Goodbye")
        exit()






