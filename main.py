import csv

import HashTable
import Graph
from Graph import Vertex, dijkstra_shortest_path
from Package import Package
from Vehicle import Truck

MAX_TRUCKS = 3


def load_file(file, structure):
    try:
        data = csv.DictReader(open(file, 'r', -1, 'utf-8-sig'))
    except FileNotFoundError:
        print(f'{file} was not found.')

    except (IOError, OSError):
        print('Error occurred while opening the file.')

    else:
        if file == 'WGUPSPackageFile.csv':
            for line_item in data:
                package = Package(**line_item)
                structure.insert(package.id, package)

        else:
            # This is the Distance Table to make a graph from
            vertices = []
            for name in data.fieldnames:
                if name == '':
                    continue
                name = name.strip().split('\n')[0]
                vertex = Vertex(name)
                vertices.append(vertex)
                structure.add_vertex(vertex)

            for line_item in data:
                start_vertex = structure.find_vertex(line_item[''].strip().split('\n')[0])
                del line_item['']
                for key in line_item:
                    structure.add_undirected_edge(start_vertex, structure.find_vertex(key.strip().split('\n')[0]), float(line_item[key]))

    finally:
        return structure


def load_truck(truck_id):
    switch = {
        1: [25, 26, 15, 16, 34, 14, 40, 4, 20, 21, 28, 13, 39, 1, 19],
        2: [5, 12, 31, 32, 17, 6, 8, 37, 38, 9, 30, 3, 36, 18],
        3: [27, 35, 7, 29, 2, 33, 11, 24, 23, 10, 22]
    }

    return switch.get(truck_id, [])


if __name__ == '__main__':
    packages = HashTable.Chained()
    distances = Graph.Undirected()

    load_file('WGUPSPackageFile.csv', packages)
    load_file('WGUPSDistanceTable.csv', distances)

    HUB = distances.find_vertex('HUB')

    dijkstra_shortest_path(distances, HUB)

    fleet = [Truck(i, HUB, load_truck(i)) for i in range(1, MAX_TRUCKS + 1)]
    # Deliver Packages
    for truck in fleet:
        for id in truck.load:
            package = packages.search(id)
            next_location = distances.find_vertex(package.address)
            if next_location is not truck.location:
                dijkstra_shortest_path(distances, truck.location)
                truck.travel(next_location)
            truck.deliver_package(package)
        if truck.id == 1:
            dijkstra_shortest_path(distances, truck.location)
            truck.travel(HUB)
            print(f"Truck 1 finished at {truck.time}")
            fleet[2].time = truck.time

    total_distance = 0
    # Check distances for testing
    for truck in fleet:
        print(f'Truck {truck.id}: {truck.trip_odometer}\nTruck {truck.id} finished at {format(truck.time.time(), "%I:%M %p")}')
        total_distance += truck.trip_odometer
    print(f'Total: {round(total_distance, 1)}')

    if total_distance < 140:
        for i in range(1, len(packages) + 1):
            package = packages.search(i)
            print(f'Package ID: {package.id}, Deadline: {package.delivery_deadline}, Delivered @ {package.delivery_time}')
            print()