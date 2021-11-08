import unittest
from datetime import time

from Package import Package, Status


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.package_1 = Package(1, "195 W Oakland Ave", "Salt Lake City", "UT", "84115", "10:30 AM", "21", "")
        self.package_2 = Package(2, "2530 S 500 E", "Salt Lake City", "UT", "84106", "EOD", "44", "")
        self.package_6 = Package("6", "3060 Lester St", "West Valley City", "UT", "84119", "10:30 AM", "88", "Delayed on flight---will not arrive to depot until 9:05 am")
        self.package_9 = Package("9", "300 State St", "Salt Lake City", "UT", "84103", "EOD", "2", "Wrong address listed")

    def test_Package_creation(self):
        self.assertIsInstance(self.package_1, Package)
        self.assertIsInstance(self.package_1.id, int)
        self.assertIsInstance(self.package_2.id, int)
        self.assertIsInstance(self.package_6.id, int)
        self.assertIsInstance(self.package_9.id, int)
        self.assertIsInstance(self.package_1.delivery_deadline, time)
        self.assertIsInstance(self.package_2.delivery_deadline, time)
        self.assertIsInstance(self.package_6.delivery_deadline, time)
        self.assertIsInstance(self.package_9.delivery_deadline, time)
        self.assertEqual(self.package_6.status, Status.DELAYED)
        self.assertEqual(self.package_9.status, Status.AT_HUB)

    def test_update_address(self):
        self.package_9.delivery_address = "410 S State St\nSalt Lake City, UT 84111"
        self.assertEqual(self.package_9.delivery_address, "410 S State St, Salt Lake City, UT 84111")


if __name__ == '__main__':
    unittest.main()
