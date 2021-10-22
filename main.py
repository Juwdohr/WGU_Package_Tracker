import csv

import HashTable
from Package import Package

MAX_PACKAGES = 16
MAX_TRUCKS = 3


def load_file(file, structure):
    try:

        data = csv.DictReader(open(file, 'r', -1, 'utf-8-sig'))

    except FileNotFoundError:

        print(f'{file} was not found.')

    except (IOError, OSError):

        print('Error occurred while opening the file.')

    else:

        for line_item in data:
            package = Package(**line_item)
            structure.insert(package.id, package)

        return structure


if __name__ == '__main__':
    package_table = load_file('WGUPSPackageFile.csv', HashTable.Chained())
