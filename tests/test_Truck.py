import unittest
from Package import Package

from Graph import Vertex
from Vehicle import Truck


class test_Truck(unittest.TestCase):

    def setUp(self):
        self.truck_1 = Truck(1, Vertex('HUB'))
        self.truck_2 = Truck(2, Vertex('HUB'))
        self.package_list = [
            Package("6", "3060 Lester St", "West Valley City", "UT", "84119", "10:30 AM", "88", "Delayed on flight---will not arrive to depot until 9:05 am", ""),
            Package("7", "1330 2100 S", "Salt Lake City", "UT", "84106", "EOD", "8", ""),
            Package("8", "300 State St", "Salt Lake City", "UT", "84103", "EOD", "9", ""),
            Package("9", "300 State St", "Salt Lake City", "UT", "84103", "EOD", "2", "Wrong address listed"),
            Package("10", "600 E 900 S", "Salt Lake City", "UT", "84105", "EOD", "1", "")
        ]

    def tearDown(self):
        self.truck = None
        self.truck_2 = None
        self.truck_3 = None
        self.package_list = None

    def test_Truck_creation(self):
        self.assertIsNotNone(self.truck_1)
        self.assertEqual(self.truck_1.MAX_CAPACITY, 16)
        self.assertEqual(self.truck_1.speed, 18)
        self.assertEqual(len(self.truck_1.load), 0)
        self.assertEqual(self.truck_1.location.label, "HUB")
        self.assertEqual(self.truck_1.trip_odometer, 0)

        self.assertIsNotNone(self.truck_2)
        self.assertEqual(self.truck_2.MAX_CAPACITY, 16)
        self.assertEqual(self.truck_2.speed, 18)
        self.assertEqual(len(self.truck_2.load), 0)
        self.assertEqual(self.truck_2.location.label, "HUB")
        self.assertEqual(self.truck_2.trip_odometer, 0)

        truck_3 = Truck(3, Vertex('HUB'))
        for package in self.package_list:
            truck_3.load_package(package.id)

        self.assertIsNotNone(truck_3)
        self.assertEqual(truck_3.MAX_CAPACITY, 16)
        self.assertEqual(truck_3.speed, 18)
        self.assertEqual(len(truck_3.load), len(self.package_list))
        self.assertEqual(self.truck_2.location.label, "HUB")
        self.assertEqual(self.truck_2.trip_odometer, 0)

    def test_load_package(self):
        self.assertTrue(self.truck_1.load_package(1))

        self.truck_2.MAX_CAPACITY = 2
        self.assertEqual(self.truck_2.MAX_CAPACITY, 2)
        self.assertTrue(self.truck_2.load_package(2))
        self.assertTrue(self.truck_2.load_package(3))
        self.assertFalse(self.truck_2.load_package(4))

    def test_deliver_package(self):
        for package in self.package_list:
            self.truck_1.load_package(package.id)

        self.assertEqual(len(self.truck_1.load), 5)

        self.truck_1.deliver_package(self.package_list[3])
        self.assertTrue(len(self.truck_1.load), 4)


if __name__ == '__main__':
    unittest.main()
