# Name: Joshua Dix
# Student ID: 001340233

import csv
from datetime import time, datetime

import Graph
import HashTable
from HashTable.chained import ChainedHashTable
from Package import Package, Status
from Vehicle import Truck


def load_file(file: str) -> csv.DictReader:
    """
    Loads file from CSV, and builds a data structure to hold the data
    Time complexity: O(1)
    :exception FileNoFoundError: Thrown if file cannot be found
    :exception IOError, OSError: Thrown if there is an issue reading from the file
    :param file: String of file location
    :return: None
    """
    try:
        data = csv.DictReader(open(file, 'r', -1, 'utf-8-sig'))
    except FileNotFoundError:
        print(f'{file} was not found.')
    except (IOError, OSError):
        print('Error occurred while opening the file.')

    else:
        return data


def load_distances() -> Graph.Undirected:
    """
    Builds a graph from a distances.csv file
    Time Complexity: O(n^2)
    :rtype: Graph
    :return: Returns a graph containing the distances from the CSV file
    """

    data = load_file("distances.csv")
    graph = Graph.Undirected()

    if data is not None:
        for name in data.fieldnames:
            if name != '':
                graph.add_vertex(Graph.Vertex(name.strip().split('\n')[0]))

        for row in data:
            start_vertex = graph.find_vertex(row.pop('').strip().split('\n')[0])
            for name, distance in row.items():
                if name != '':
                    end_vertex = graph.find_vertex(name.strip().split('\n')[0])
                    graph.add_undirected_edge(start_vertex, end_vertex, float(distance))

    return graph


def load_packages() -> ChainedHashTable:
    """
    Loads the packages from the file into a dictionary.
    Time Complexity: O(n)
    :rtype: ChainedHashTable
    :return: Returns a chained hash table containing packages
    """

    _data = load_file("packages.csv")
    table = HashTable.Chained()

    if _data is not None:

        for row in _data:
            package = Package(**row)
            table.insert(package.id, package)

    return table


def load_truck(truck_id: int) -> list:
    """
    Loads & sorts truck with packages
    Time Complexity: O(n log n)
    :rtype: list
    :return: list if Packages to load on to truck
    """

    load = []

    # Cycle through all package ids
    for package_id in range(1, len(packages) + 1):
        package = packages.search(package_id)

        # If package is delayed it cannot get onto a truck at this time.
        if package.status in [Status.DELIVERED, Status.ON_TRUCK, Status.DELAYED, Status.EN_ROUTE]:
            continue

        # Truck 1 needs to have packages from 84117, 84115, 84104
        if truck_id == 1 and package.postal_code in ['84117', '84115', '84104'] and len(load) < MAX_TRUCK_CAPACITY:
            load.append(package)

        # Truck 2 needs to have packages from 84102, 84119, 84111, 84103
        if truck_id == 2 and package.postal_code in ['84102', '84119', '84111', '84123', '84103'] and len(
                load) < MAX_TRUCK_CAPACITY:
            load.append(package)

        # Truck 3 needs packages from 84121, 84118, 84105, 84106, 84107
        if truck_id == 3 and package.postal_code in ['84121', '84118', '84105', '84106', '84107'] and len(
                load) < MAX_TRUCK_CAPACITY:
            load.append(package)

    # Sort load by delivery dead lines
    load.sort(key=lambda package: package.delivery_deadline, reverse=False)  # Time Complexity: O(n * log n)
    load.sort(key=lambda package: package.delivery_address, reverse=True)  # Time Complexity: O(n * log n)

    return load


def deliver_packages(truck: Truck) -> None:
    """
    Deliver all packages loaded onto truck
    Time Complexity: O(n)
    :param truck: Current truck
    :return: None
    """
    # Check for delayed packages at HUB before leaving
    load = pickup_delayed_packages(truck)
    if len(load) > 0:
        for package in load:
            truck.load(package)

    # Set departure time for all packages on truck
    for package in truck.cargo:
        package.status = Status.EN_ROUTE
        package.departure_time = truck.time

    for package in truck.cargo:
        if package.status is Status.DELIVERED:
            continue

        if 'wrong address' in package.notes.lower() and truck.time >= time(10, 20):
            package.delivery_address = "410 S State St\nSalt Lake City, UT 84111"

        next_location = truck.map.find_vertex(package.address)

        if next_location is not truck.location:
            Graph.find_shortest_paths(truck.map, truck.location)
            truck.drive(next_location)

        truck.deliver_package(package)

        if truck.time >= time(9, 5):
            break

    # Check again for delayed packages at HUB before continuing
    load = pickup_delayed_packages(truck)

    if len(load) > 0:
        for package in load:
            truck.drive(gps_map.find_vertex("HUB"))
            truck.load(package)

    for package in truck.cargo:
        if package.status in [Status.AT_HUB, Status.ON_TRUCK]:
            package.status = Status.EN_ROUTE
            package.departure_time = truck.time

    for package in truck.cargo:
        if 'wrong address' in package.notes.lower() and truck.time >= time(10, 20):
            package.delivery_address = "410 S State St\nSalt Lake City, UT 84111"

        next_location = truck.map.find_vertex(package.address)

        if next_location is not truck.location:
            Graph.find_shortest_paths(truck.map, truck.location)
            truck.drive(next_location)

        truck.deliver_package(package)


def pickup_delayed_packages(truck: Truck) -> list:
    """
    Sets delayed packages to At the Hub
    Sends truck to hub to get new packages
    Time Complexity: O(n)
    :param truck: Current truck looking for delayed packages
    :return:
    """
    for package_id in range(1, len(packages) + 1):
        package = packages.search(package_id)
        if package.status == Status.DELAYED and truck.time >= time(9, 5):
            package.status = Status.AT_HUB

    return load_truck(truck.id)


def lookup_single_package(package_id: int, lookup_time: time) -> None:
    """
    Looks up single package, and prints it status at a specified time.
    Time Complexity: O(n)
    :param package_id: ID of package to lookup
    :param lookup_time: Time to lookup
    :return:
    """
    package = packages.search(package_id)
    if package is None:
        return print('ID is not recognized')

    if lookup_time < package.departure_time or package.departure_time is None:
        status = Status.AT_HUB if 'delayed' not in package.notes.lower() else Status.DELAYED
        print(package, status.name)
    elif package.departure_time < lookup_time < package.delivery_time:
        status = Status.EN_ROUTE
        print(package, status.name)
    elif package.delivery_time < lookup_time:
        print(package, package.status.name, package.delivery_time)
    else:
        print('Time not recognized please try again')


def lookup_all_packages(lookup_time: time) -> None:
    """
    Loops through entire hashtable, printing all packages out based on time.
    Time Complexity: O(n)
    :param lookup_time:
    :return:
    """
    for package_id in range(1, len(packages) + 1):
        lookup_single_package(package_id, lookup_time)


def user_interface() -> None:
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
            lookup_time = datetime.strptime(input("Please enter a time in 24 hour format (HH:mm):  "), '%H:%M').time()
            print("ID, Delivery Address, Mass in KG, Delivery Deadline, Status")
            lookup_single_package(package_id, lookup_time)
            continue

        if user_input == 2:
            print('Getting all Package Data...')
            lookup_time = datetime.strptime(input("Please enter a time in 24 hour format (HH:mm):  "), '%H:%M').time()
            print("ID, Delivery Address, Mass in KG, Delivery Deadline, Status")
            lookup_all_packages(lookup_time)
            continue

    print("Goodbye")
    exit()


packages: ChainedHashTable = load_packages()
gps_map: Graph = load_distances()
MAX_TRUCKS: int = 3
MAX_TRUCK_CAPACITY: int = 16


def main() -> None:
    """
    Main function to run core algorithm
    Time complexity: O(n * log n)
    :return: None
    """
    # Create feet of trucks
    fleet = [Truck(i, gps_map, load_truck(i)) for i in range(1, MAX_TRUCKS + 1)]

    # Deliver Packages
    for truck in fleet:
        if truck.id == 1:
            truck.time = time(8, 30)
        if truck.id == 2:
            truck.time = time(9, 15)
        if truck.id == 3:
            truck.time = fleet[0].time

        deliver_packages(truck)

    print("Welcome to the WGUPS Package Delivery System")
    total_distance = 0
    for truck in fleet:
        print(f'Truck {truck.id}: {round(truck.trip_odometer, 1)} & finished at {format(truck.time, "%I:%M %p")}')
        total_distance += truck.trip_odometer
    print(f'Total: {round(total_distance, 1)}')


if __name__ == '__main__':
    """
    Starting point of program
    Time Complexity: O(n * log n)
    """
    # Run main portion of algorithm
    main()  # O(n * log n)

    # Display data to user after main program has run.
    user_interface()  # O(n)
