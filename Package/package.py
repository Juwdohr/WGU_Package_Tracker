from dataclasses import dataclass, field
from datetime import time, datetime
from enum import auto, Enum
from typing import Optional


class Status(Enum):
    DELAYED = auto()
    AT_HUB = auto()
    ON_TRUCK = auto()
    EN_ROUTE = auto()
    DELIVERED = auto()


@dataclass
class Package:
    """Represents a package to be delivered"""
    id: int
    address: str
    city: str
    state: str
    postal_code: str
    delivery_deadline: time
    mass: str
    notes: str
    status: Status = field(init=False, repr=False, default=Status.AT_HUB)
    departure_time: time = field(init=False, repr=False, default=None)
    delivery_time: Optional[time] = field(init=False, repr=False, default=None)

    def __post_init__(self) -> None:
        """
        Sets all items to default and parses need items to correct types
        Time Complexity: O(1)
        :return: None
        """
        self.id = int(self.id)
        self.mass = f'{self.mass} kg'

        if self.delivery_deadline == 'EOD':
            self.delivery_deadline = time(20, 00)
        else:
            self.delivery_deadline = datetime.strptime(self.delivery_deadline, "%I:%M %p").time()

        if 'delayed' in self.notes.lower():
            self.status = Status.DELAYED

    def __str__(self):
        """
        String representation of Package
        Time Complexity: O(1)
        :return: str = Representation of a package
        """
        return f'{self.id}, "{self.delivery_address}", {self.mass}, {self.delivery_deadline}'

    @property
    def delivery_address(self) -> str:
        """
        Represents the address, built from all known parts
        Time Complexity: O(1)
        :return: String representation of the address
        """
        return f'{self.address}, {self.city}, {self.state} {self.postal_code}'

    @delivery_address.setter
    def delivery_address(self, updated_delivery_address: str) -> None:
        """
        Updates the delivery address
        Time Complexity: O(1)
        :param updated_delivery_address: String representing the updated delivery address
        :return: None
        """
        self.address, rest = updated_delivery_address.split('\n')
        self.city, rest = rest.split(', ')
        self.state, self.postal_code = rest.split(' ')

    def deliver(self, timestamp: time) -> bool:
        """
        Marks the package as delivered and sets the current_time it was delivered
        Time Complexity: O(1)
        :param timestamp: Time that it was delivered
        :return:
        """
        self.delivery_time = timestamp
        self.status = Status.DELIVERED
        return True
