from dataclasses import dataclass, field
from datetime import time, datetime


@dataclass
class Package:
    id: int
    address: str
    city: str
    state: str
    postal_code: str
    delivery_deadline: time
    mass: str
    notes: str
    status: str = 'En Route'
    delivery_time: time = field(init=False)

    def __post_init__(self):
        self.id = int(self.id)
        self.mass = f'{self.mass} kg'

        if self.delivery_deadline == 'EOD':
            self.delivery_deadline = time(20, 00)
        else:
            self.delivery_deadline = datetime.strptime(self.delivery_deadline, "%I:%M %p").time()

        if 'delayed' in self.notes.lower() or 'wrong address' in self.notes.lower():
            self.status = 'Delayed'

    def __str__(self):
        return f'ID: {self.id}\nDeadline: {self.delivery_deadline}\nStatus: {self.status} @ {self.delivery_time}'

    @property
    def delivery_address(self):
        return f'{self.address}\n{self.city}, {self.state} {self.postal_code}'

    @delivery_address.setter
    def delivery_address(self, updated_delivery_address):
        self.address, self.city, rest = updated_delivery_address.split(', ')
        self.state, self.postal_code = rest.split(' ')

    def deliver(self, timestamp:time):
        self.delivery_time = timestamp
        self.status = 'Delivered'
