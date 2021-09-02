import csv

import HashTable


def load_packages():
    hash_table = HashTable.Chained()
    try:
        packages = csv.DictReader(open('WGUPS Packages.csv', 'r'))
    except FileNotFoundError as e:
        print(e)
    else:
        for package in packages:
            package_id = package.pop("Package ID")
            hash_table.insert(package_id, package)
    finally:
        return hash_table

if __name__ == '__main__':
    package_table = load_packages()
