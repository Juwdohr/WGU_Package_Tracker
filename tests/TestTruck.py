import unittest

from Graph import Vertex, Graph, Undirected
from Package import Package
from Vehicle import Truck


class TestTruck(unittest.TestCase):
    def setUp(self):
        HUB = Vertex("HUB")
        destination = Vertex(Vertex('3060 Lester St'))
        self.map: Graph = Undirected()
        self.map.add_vertex(HUB)
        self.map.add_vertex(destination)
        self.map.add_undirected_edge(HUB, destination, 1.4)

        self.truck = None

        self.truck = Truck(1, self.map)
        self.truck_2 = Truck(2, self.map)
        self.package_list = [
            Package("6", "3060 Lester St", "West Valley City", "UT", "84119", "10:30 AM", "88", "Delayed on flight---will not arrive to depot until 9:05 am"),
            Package("7", "1330 2100 S", "Salt Lake City", "UT", "84106", "EOD", "8", ""),
            Package("8", "300 State St", "Salt Lake City", "UT", "84103", "EOD", "9", ""),
            Package("9", "300 State St", "Salt Lake City", "UT", "84103", "EOD", "2", "Wrong address listed"),
            Package("10", "600 E 900 S", "Salt Lake City", "UT", "84105", "EOD", "1", "")
        ]

    def tearDown(self):
        self.map = None
        self.truck = None
        self.truck_2 = None
        self.truck_3 = None
        self.package_list = None

    def test_Truck_creation(self):
        self.assertIsNotNone(self.truck)
        self.assertEqual(self.truck.MAX_CAPACITY, 16)
        self.assertEqual(self.truck.SPEED, 18)
        self.assertEqual(len(self.truck.cargo), 0)
        self.assertEqual(self.truck.location.label, "HUB")
        self.assertEqual(self.truck.trip_odometer, 0)

        self.assertIsNotNone(self.truck_2)
        self.assertEqual(self.truck_2.MAX_CAPACITY, 16)
        self.assertEqual(self.truck_2.SPEED, 18)
        self.assertEqual(len(self.truck_2.cargo), 0)
        self.assertEqual(self.truck_2.location.label, "HUB")
        self.assertEqual(self.truck_2.trip_odometer, 0)

        truck_3 = Truck(3, self.map)
        for package in self.package_list:
            truck_3.load(package)

        self.assertIsNotNone(truck_3)
        self.assertEqual(truck_3.MAX_CAPACITY, 16)
        self.assertEqual(truck_3.SPEED, 18)
        self.assertEqual(len(truck_3.cargo), len(self.package_list))
        self.assertEqual(self.truck_2.location.label, "HUB")
        self.assertEqual(self.truck_2.trip_odometer, 0)

    def test_load_package(self):
        self.assertTrue(self.truck.load(self.package_list[0]))

        self.truck_2.MAX_CAPACITY = 2
        self.assertEqual(self.truck_2.MAX_CAPACITY, 2)
        self.assertTrue(self.truck_2.load(self.package_list[2]))
        self.assertTrue(self.truck_2.load(self.package_list[3]))
        self.assertFalse(self.truck_2.load(self.package_list[4]))

    def test_deliver_package(self):
        for package in self.package_list:
            self.truck.load(package)

        self.assertEqual(len(self.truck.cargo), 5)

        self.assertTrue(self.truck.deliver_package(self.package_list[0]), True)


if __name__ == '__main__':
    unittest.main()
