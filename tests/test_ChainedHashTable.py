import unittest

from HashTable.Chained import ChainedHashTable


class ChainedHashTableTestCase(unittest.TestCase):

    def setUp(self):
        self.hash_table = ChainedHashTable()

    def tearDown(self):
        self.hash_table = None

    def test_init(self):
        self.assertIsInstance(self.hash_table, ChainedHashTable)
        self.assertEqual(len(self.hash_table.table), 10)
        for table in self.hash_table.table:
            self.assertEqual(len(table), 0)

    def test_insert(self):
        self.assertTrue(self.hash_table.insert(1, 'First'))
        self.assertTrue(self.hash_table.insert('two', 'Second'))

    def test_update(self):
        self.hash_table.insert(1, 'first')
        self.assertEqual(self.hash_table.table[1][0][1], 'first')
        self.assertTrue(self.hash_table.insert(1, 'First'))
        self.assertEqual(self.hash_table.table[1][0][1], 'First')

    def test_search(self):
        self.hash_table.insert(1, 'First')
        self.assertEqual(self.hash_table.search(1), 'First')

    def test_remove(self):
        self.hash_table.insert(1, 'First')
        self.assertTrue(self.hash_table.remove(1))
        self.assertFalse(self.hash_table.remove(2))


if __name__ == '__main__':
    unittest.main()
