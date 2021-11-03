from dataclasses import dataclass, field
from typing import Optional

from Package import Package


@dataclass
class ChainedHashTable:
    """Represents a hashtable using chaining"""

    table: list = field(init=False, default_factory=list)
    capacity: int = 10

    def __post_init__(self) -> None:
        """
        Constructor with optional initial capacity parameter.
        Assigns all buckets with an empty list.
        Initialize the hash table with empty bucket list entries.
        :return: None
        """
        for _ in range(self.capacity):
            self.table.append([])

    def __len__(self):
        """return the length of all rows of the hashtable"""
        return sum(len(self.table[i]) for i in range(len(self.table)))

    def __iter__(self):
        for i in range(1, len(self) + 1):
            return i

    def insert(self, key, item):
        """
        Inserts a new item tp or updates an existing item in the hash table.
        :param key: Key to retrieve the item from hash table
        :param item: Item to store in the hash table
        :return: True either if the item is found and updated, or if the item is inserted into.
        """
        # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key: int) -> Optional[Package]:
        """
        Searches for an item with matching key in the hash table.
        :param key: Key to find the hashtable
        :return: Returns the item if found, or None if not found.
        """
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    def remove(self, key: int) -> bool:
        """
        Removes an item with matching key from the hash table.
        :param key: Key to Item to remove
        :return: True it item is found, false if item is not found.
        """
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
                return True

        return False
