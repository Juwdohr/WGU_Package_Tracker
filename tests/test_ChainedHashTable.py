import unittest
from HashTable import HashTable


class ChainedHashTableTestCase(unittest.TestCase):

    def test_init(self):
        hash_table = HashTable.Chained()
        self.assertEqual(len(hash_table.table), 10)
        for table in hash_table.table:
            self.assertEqual(len(table), 0)

    def test_insert(self):
        hash_table = HashTable.Chained()
        self.assertTrue(hash_table.insert(1, 'First'))
        self.assertTrue(hash_table.insert('two', 'Second'))

    def test_update(self):
        hash_table = HashTable.Chained()
        hash_table.insert(1, 'first')
        self.assertEqual(hash_table.table[1][0][1], 'first')
        self.assertTrue(hash_table.insert(1, 'First'))
        self.assertEqual(hash_table.table[1][0][1], 'First')

    def test_search(self):
        hash_table = HashTable.Chained()
        hash_table.insert(1, 'First')
        self.assertEqual(hash_table.search(1), 'First')

    def test_remove(self):
        hash_table = HashTable.Chained()
        hash_table.insert(1, 'First')
        self.assertTrue(hash_table.remove(1))
        self.assertFalse(hash_table.remove(2))


if __name__ == '__main__':
    unittest.main()
