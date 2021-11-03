from .Chained_HashTable import ChainedHashTable as Chained
from Package import Package

def build(data, hash_table):
    for line_item in data:
        package = Package(**line_item)
        hash_table.insert(package.id, package)