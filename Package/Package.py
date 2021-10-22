from dataclasses import dataclass
from datetime import time


@dataclass
class Package:
    id: int
    address: str
    city: str
    state: str
    postal_code: str
    delivery_deadline: time
    mass: int
    notes: str
    location: str = "HUB"
    status: str = "En route"
    delivery_time: time = None

    def __post_init__(self):
        self.id = int(self.id)

    @property
    def delivery_address(self):
        return f"{self.address}\n{self.city}, {self.state} {self.postal_code}"

    @delivery_address.setter
    def delivery_address(self, updated_delivery_address):
        self.address, rest = updated_delivery_address.split('\n')
        self.city, rest = rest.split(', ')
        self.city, self.postal_code = rest.split

    def deliver(self, timestamp):
        self.delivery_time = timestamp
        self.status = "Delivered"
