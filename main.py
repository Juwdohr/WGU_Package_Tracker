# Name: Joshua Dix
# Student ID: 001340233

import csv

import Courier
import Graph
import UI
from HashTable import Chained


def main(wgups: Courier) -> None:
    """
    Main function to run core algorithm
    Time complexity: O(n^2)
    :return: None
    """

    wgups.release_trucks()

    # Display data to user after main program has run.
    user_interface = UI.UserInterface(wgups.packages)
    user_interface.print_header(wgups.fleet)
    user_interface.run()


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

    _data = load_file("distances.csv")
    graph = Graph.Undirected()

    if _data is not None:
        graph.extract_vertices(_data.fieldnames)
        graph.build_graph(_data)

    return graph


def load_packages() -> Chained:
    """
    Loads the all_packages from the file into a dictionary.
    Time Complexity: O(n)
    :rtype: ChainedHashTable
    :return: Returns a chained hash table containing all_packages
    """

    _data = load_file("packages.csv")
    table = Chained()

    if _data is not None:
        table.build_table(_data)

    return table


if __name__ == '__main__':
    """
    Starting point of program
    Time Complexity: O(n^2)
    """
    main(Courier.Hub(load_packages(), load_distances()))  # O(n^2)
